import json
import random
import tempfile

from contextlib import contextmanager

# TODO: make these real country codes.  Not necessary, but nicer.
# eventually get from reddit-service-admin/admin/lib/geolocations.py
LOCALES = ["us", "gb", "es"]
APP_NAMES = [
    "app_1",
    "app_2",
    "app_3",
    "app_4",
    "app_5",
]  # TODO: figure out if this is enough.


@contextmanager
def create_temp_config_file(contents):
    with tempfile.NamedTemporaryFile() as f:
        f.write(json.dumps(contents).encode())
        f.seek(0)
        yield f


def make_request_context_map(h={}):
    return {
        "user_id": str(h.get("user_id", random.choice(range(1000)))),
        "locale": h.get("locale", random.choice(LOCALES + [None])),
        "device_id": str(h.get("device_id", 10000 + random.choice(range(1000)))),
        "country_code": h.get("locale", random.choice(LOCALES + [None])),
        "origin_service": h.get("origin_service"),  # do I care about this one?
        "user_is_employee": h.get(
            "user_is_employee", random.choice([True, False, None])
        ),
        "logged_in": h.get("logged_in", random.choice([True, False, None])),
        "app_name": h.get("app_name", random.choice(APP_NAMES + [None])),
        "build_number": int(h.get("build_number", 1000 + random.choice(range(1000)))),
    }


def make_experiment(n, h={}):
    version = int(h.get("version", random.choice(range(10000))))
    variants = h.get(
        "variants", h.get("experiment", {}).get("variants", make_variants())
    )
    shuffle_version = h.get(
        "shuffle_version",
        h.get("experiment", {}).get("shuffle_version", random.choice(range(100))),
    )
    return {
        "id": int(h.get("id", random.choice(range(10000)))),
        "name": str(h.get("name", "genexp_" + str(n))),
        "enabled": True,  # TODO: make this false sometimes?  lowpri
        "owner": "test",
        "version": str(version),
        "type": "range_variant",
        "start_ts": 0,  # we'Re not interested in testing start/stop
        "stop_ts": 2147483648,
        "experiment": {
            "variants": variants,
            "experiment_version": int(version),
            "shuffle_version": int(shuffle_version),
            "bucket_val": "user_id",  # TODO: make this handle device_id, etc.
            "log_bucketing": False,
            # "overrides": {}, # TODO: build this.
            # "targeting": targeting_tree(),
        },
    }


def make_overrides(variants):
    names = [v["name"] for v in variants]
    return {n: targeting_tree() for n in names}


def targeting_tree():
    """Generate a random targeting tree."""
    return {"EQ": {"field": "user_id", "values": ["3", "5", "7"]}}


def make_variants(h={}):
    return h or [  # TODO: actually generate variantsets.  Lowpri?
        {"range_start": 0.0, "range_end": 0.2, "name": "control_1"},
        {"range_start": 0.2, "range_end": 0.4, "name": "variant_2"},
        {"range_start": 0.4, "range_end": 0.6, "name": "variant_3"},
        {"range_start": 0.6, "range_end": 0.8, "name": "variant_4"},
    ]
