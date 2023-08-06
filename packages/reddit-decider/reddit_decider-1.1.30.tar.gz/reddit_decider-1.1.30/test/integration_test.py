#!/usr/bin/env python
import json
import os
import random
import time

from unittest import TestCase

import rust_decider

from hypothesis import strategies as st
from reddit_experiments import Experiments
from utils import APP_NAMES
from utils import LOCALES
from utils import make_experiment
from utils import make_request_context_map


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def setup_baseplate_experiments(cfg_path):
    h = json.load(open(cfg_path))
    # we really only want to populate the raw string cache of _cfg_data,
    # so that when we go looking for keys, we find them.
    el = Experiments(
        cfg_data=h, config_watcher=None, server_span=None, context_name=None
    )
    return el


def setup_decider(cfg_path):
    return rust_decider.init(
        "darkmode overrides targeting holdout mutex_group fractional_availability",
        cfg_path,
    )


@st.composite
def make_ctx_map(draw):
    return {  # TODO: make the nullable fields sometimes be None
        "user_id": str(draw(st.integers(min_value=1, max_value=1000))),
        "locale": draw(st.sampled_from(LOCALES + [None])),
        "device_id": str(draw(st.integers(min_value=10000, max_value=11000))),
        "country_code": draw(st.sampled_from(LOCALES + [None])),
        "origin_service": "shreddit",  # do I care about this one?
        "user_is_employee": draw(st.booleans()),
        "logged_in": draw(st.booleans()),
        "app_name": draw(st.sampled_from(APP_NAMES + [None])),
        "build_number": str(draw(st.integers(min_value=1, max_value=1000))),
    }


class Exp:
    def __init__(
        self,
        eid,
        name,
        enabled,
        version,
        shuffle_version,
        bucket_val,
        targeting=None,
        overrides=None,
    ):
        self.id = eid
        self.name = name
        self.enabled = enabled
        self.version = str(version)
        self.type = "range_variant"
        self.start_ts = 0
        self.stop_ts = 2147483648
        self.experiment = {
            "variants": make_variants(),
            "experiment_version": int(version),
            "shuffle_version": int(shuffle_version),
            "bucket_val": bucket_val,
            "log_bucketing": False,
            "overrides": overrides,
            "targeting": targeting,
        }

    @classmethod
    def strategy(cls):
        return st.builds(
            cls,
            st.integers(min_value=1),
            st.from_regex(r"^\A[a-z_0-9]{5,40}\Z"),
            st.booleans(),
            st.integers(min_value=0, max_value=10000),
            st.integers(min_value=0),
            st.sampled_from(["user_id", "device_id"]),
            targeting_tree(),
        )

    @classmethod
    def from_strategy(cls, s):
        return cls(
            s.id,
            s.name,
            s.enabled,
            s.version,
            s.shuffle_version,
            s.bucket_val,
            s.targeting,
            s.overrides,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
            "version": self.version,
            "owner": "test",
            "type": "range_variant",
            "start_ts": 0,  # we'Re not interested in testing start/stop
            "stop_ts": 2147483648,
            "experiment": {
                "variants": self.experiment["variants"],
                "experiment_version": self.experiment["experiment_version"],
                "shuffle_version": self.experiment["shuffle_version"],
                "bucket_val": self.experiment["bucket_val"],
                "log_bucketing": False,
                # "overrides": {}, # TODO: build this.
                "targeting": self.experiment["targeting"],
            },
        }


@st.composite
def make_exp(draw):
    version = draw(st.integers(min_value=0, max_value=10000))
    variants = make_variants()
    return {
        "id": draw(st.integers(min_value=1)),
        "name": draw(st.from_regex(r"^\A[a-z_0-9]{5,40}\Z")),
        "enabled": True,  # TODO: make this false sometimes?  lowpri
        "owner": "test",
        "version": str(version),
        "type": "range_variant",
        "start_ts": 0,  # we'Re not interested in testing start/stop
        "stop_ts": 2147483648,
        "experiment": {
            "variants": variants,
            "experiment_version": int(version),
            "shuffle_version": draw(st.integers(min_value=0)),
            "bucket_val": "user_id",
            "log_bucketing": False,
            # "overrides": {}, # TODO: build this.
            "targeting": targeting_tree(),
        },
    }


def make_op_node(op, field, val):
    """Generate a targeting tree op node."""
    if isinstance(val, list):
        val_field = "values"
    else:
        val_field = "value"

    val = str(val) if isinstance(val, bool) else val

    return {op: {"field": field, val_field: val}}


@st.composite
def targeting_tree(draw):
    return draw(
        st.recursive(
            bool_eq() | str_eq(),
            lambda cl: not_n(cl) | any_n(cl) | all_n(cl),
            max_leaves=20,
        )
    )


@st.composite
def user_ids(draw, elements=st.integers(min_value=1, max_value=1000)):
    return draw(st.lists(elements, min_size=1))


@st.composite
def bool_eq(draw):
    field = draw(st.sampled_from(["user_is_employee", "logged_in"]))
    val = draw(st.booleans())
    return make_op_node("EQ", field, val)


@st.composite
def str_eq(draw):
    field = draw(st.sampled_from(["user_id", "device_id"]))
    val = draw(user_ids())
    return make_op_node("EQ", field, val)


@st.composite
def not_n(draw, children):
    cl = draw(children)
    return {"NOT": cl}


@st.composite
def all_n(draw, children):
    cl = draw(st.lists(children))
    return {"ALL": cl}  # maybe have to set min_size?


@st.composite
def any_n(draw, children):
    cl = draw(st.lists(children))
    return {"ANY": cl}  # maybe have to set min_size?


def make_variants(h={}):
    return h or [  # TODO: actually generate variantsets.  Lowpri?
        {"range_start": 0.0, "range_end": 0.2, "name": "control_1"},
        {"range_start": 0.2, "range_end": 0.4, "name": "variant_2"},
        {"range_start": 0.4, "range_end": 0.6, "name": "variant_3"},
        {"range_start": 0.6, "range_end": 0.8, "name": "variant_4"},
    ]


def compare_implementations_against_cfg(
    cfg_path, user_ids, exp_names=None, ctx=make_request_context_map()
):
    if exp_names is None:
        h = json.load(open(cfg_path))

        # filter out DCs from the  default cfg- BP can't handle them
        exp_names = [k for k in h.keys() if k[0] in ["e", "g"]]

    dc = setup_decider(cfg_path)
    bp = setup_baseplate_experiments(cfg_path)
    successes = []
    failures = []
    for exp_name in exp_names:
        for uid in user_ids:
            ctx["user_id"] = str(uid)
            res, bpv = compare_single_call(dc, bp, exp_name, uid, ctx)
            if res.err() or not (bpv == res.decision()):
                failures.append(
                    {
                        "uid": uid,
                        "exp_name": exp_name,
                        "dc": res.decision(),
                        "bpv": bpv,
                        "ctx": ctx,
                        "res": res,
                    }
                )
                print(
                    f"failure:{exp_name} {uid} bp:{bpv} != dc:{res.decision()} ctx={ctx}"
                )
            else:
                successes.append(uid)
    return successes, failures


def compare_single_call(dc, bp, exp_name, uid, ctx_map=None):
    ctx_map = ctx_map or make_request_context_map({"user_id": str(uid)})
    ctx = rust_decider.make_ctx(ctx_map)
    res = dc.choose(exp_name, ctx)
    bpv = bp.variant(exp_name, **ctx_map)
    return [res, bpv]


class TestRustWithSdk(TestCase):
    def test_impls_against_cfg(self):
        cfg_path = f"{TEST_DIR}/../../cfg.json"
        h = json.load(open(cfg_path))
        exp_names = [k for k in h.keys() if k[0] in ["e", "g"]]
        uids = range(3000)
        good, bad = compare_implementations_against_cfg(cfg_path, uids, exp_names)
        if bad:
            print("mismatches found!\n\n", bad)
        else:
            print("all_good!")

        self.assertEqual(bad, [])
        self.assertEqual(len(good), len(uids) * len(exp_names))

    def test_impls_against_x0(self):
        cfg_path = f"{TEST_DIR}/../../cfg.json"
        exp_names = ["x0"]
        uids = range(100)
        ctx = make_request_context_map({"user_id": str(1), "user_is_employee": True})
        good, bad = compare_implementations_against_cfg(cfg_path, uids, exp_names, ctx)
        self.assertEqual(bad, [])
        self.assertEqual(len(good), len(uids) * len(exp_names))

    def test_impls_against_generated(self):
        # we want to be able to reproduce failures, so seed the RNG with the current timestamp,
        # and then log it on failures.  This will assist in debugging test fails.
        seed = int(time.time())
        random.seed(seed)
        msg = f"random seed={seed}"

        exp_cfg = {e["name"]: e for e in [make_experiment(n) for n in range(20)]}
        fn = "/tmp/genexp"  # TODO: generate the filename
        f = open(fn, "w")
        f.write(json.dumps(exp_cfg, indent=2))
        f.close()
        good, bad = compare_implementations_against_cfg(fn, range(3000))
        self.assertEqual(len(bad), 0, msg)
        self.assertEqual(len(good), 3000 * 20, msg)

    # @given(Exp.strategy())
    # def test_impls_against_hypothesis(self, exp):
    #     seed = int(time.time())
    #     random.seed(seed)
    #     msg = f"random seed={seed}"
    #     print(exp.to_dict())
    #     exp_cfg = {e["name"]:e for e in [exp.to_dict()]}
    #     fn = "/tmp/hypexp" # TODO: generate the filename
    #     f = open(fn, "w")
    #     f.write(json.dumps(exp_cfg, indent=2))
    #     f.close()
    #     good, bad = compare_implementations_against_cfg(fn, range(3000))
    #     self.assertEqual(len(bad), 0, msg)
    #     self.assertEqual(len(good), 3000, msg)
