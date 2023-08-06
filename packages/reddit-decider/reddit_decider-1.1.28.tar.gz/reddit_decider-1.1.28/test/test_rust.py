import os

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    import rust_decider

    decider = rust_decider.init(
        "darkmode overrides targeting holdout mutex_group fractional_availability value",
        f"{TEST_DIR}/../../cfg.json",
    )

    if decider:
        ctx_dict = {
            "user_id": "795244",
            "locale": None,
            "canonical_url": "www.reddit.com",
            "user_is_employee": True,
            "logged_in": False,
            "app_name": "ios",
            "build_number": 1234,
            "country_code": "UA",
            "cookie_created_timestamp": 1648859753.233,
            "other_fields": {
                "knoxness": "max",
                "romans": 7,
                "yiqi_is_badass": True,
                "romansFlaws": None,
            },
        }
        ctx = rust_decider.make_ctx(ctx_dict)
        print("context:")
        print(ctx.inspect())

        # choose
        a = decider.choose("genexp_0", ctx)
        print(a.inspect())
        print(f"'genexp_0' choose() error (should be None): {a.err()}")
        print(f"choose() decision(): {a.decision()}")
        print(f"choose() events(): {a.events()}")

        # choose bucket_val: "device_id", without device_id in ctx
        b = decider.choose("genexp_device_id", ctx)
        print(
            f"'genexp_device_id' choose() error (should be 'Missing device_id in context'): {b.err()}"
        )

        ca = decider.choose_all(ctx)
        print(f"results from choose_all: {ca}")

        # choose bucket_val: "device_id"
        ctx_dict = {"user_id": "blah", "device_id": "795244"}
        ctx = rust_decider.make_ctx(ctx_dict)
        c = decider.choose("genexp_device_id", ctx)
        print(f"'genexp_device_id' choose() error (shuold be None): {c.err()}")
        print(f"choose() decision(): {c.decision()}")

        # get_bool
        d = decider.get_bool("dc_bool", ctx)
        print(f"get_bool(): {d.val()}")

        # get_int
        e = decider.get_int("dc_int", ctx)
        print(f"get_int(): {e.val()}")

        # get_float
        f = decider.get_float("dc_float", ctx)
        print(f"get_float(): {f.val()}")

        # get_string
        g = decider.get_string("dc_string", ctx)
        print(f"get_string(): {g.val()}")

        # get_string missing feature error
        h = decider.get_string("missing", ctx)
        print(f"get_string() err: {h.err()}")

        # get_map
        i = decider.get_map("dc_map", ctx).val()
        print(f"get_map(): {i}")
        print(f"get_map() nested_map: {i['v']['nested_map']}")
        print(f"get_map() nested_map val: {i['v']['nested_map']['x']}")

        # get_experiment
        g = decider.get_experiment("genexp_0")
        print(f"get_experiment(): {g.err()}")
        print(f"get_experiment() {g.val()}")
    else:
        print("Failed to init decider")
