# coding=utf-8
import codecs
import os
import random
import shutil
import sys
import tempfile
import unittest

from openmodule.utils.matching import PlateYamlSelector

plates = ["G ARIVO 1", "BÖ SE-11", "GÜ-NTH ER 123", "OQ:123 AB",
          "SLDFKJWPEOÄÜSDGIEFH .:S.F: WE:. OWEKRQÖ.Ö: .WEIJFA.DF", "ASDFÖÜĆẐ"]
legacy_results = ["GARIV01", "B0SE11", "GUNTHER123", "00123AB", "SLDFKJWPE0AUSDGIEFHSFWE0WEKR000WEIJFADF", "ASDF0UCZ"]
a10_results = ["G:ARIVO1", "BO:SE11", "GU:NTHER123", "OO:123AB",
               "SLDFKJWPEOAUSDGIEFH:SFWEOWEKROOOWEIJFADF", "ASDFOUCZ"]
a20_results = ["G ARIVO1", "BO SE11", "GU-NTHER123", "OO:123AB",
               "SLDFKJWPEOAUSDGIEFH SFWEOWEKROOOWEIJFADF", "ASDFOUCZ"]
d10_results = ["GARIVO1", "BÖSE11", "GÜNTHER123", "OQ123AB", "SLDFKJWPEOÄÜSDGIEFHSFWEOWEKRQÖÖWEIJFADF", "ASDFÖÜCZ"]
d20_results = ["G:ARIVO:1", "BÖ:SE:11", "GÜ:NTH:ER:123", "OQ:123:AB",
               "SLDFKJWPEOÄÜSDGIEFH:::S:F::WE:::OWEKRQÖ:Ö:::WEIJFA:DF", "ASDFÖÜCZ"]
d30_results = ["G ARIVO 1", "BÖ SE-11", "GÜ-NTH ER 123", "OQ:123 AB",
               "SLDFKJWPEOÄÜSDGIEFH .:S.F: WE:. OWEKRQÖ.Ö: .WEIJFA.DF", "ASDFÖÜCZ"]
t10_results = ["GARIVO1", "BÖSE11", "GÜNTHER123", "OQ123AB",
               "SLDFKJWPEOÄÜSDGIEFHSFWEOWEKRQÖÖWEIJFADF", "ASDFÖÜCZ"]
t20_results = ["G ARIVO1", "BÖ SE11", "GÜ-NTHER123", "OQ:123AB",
               "SLDFKJWPEOÄÜSDGIEFH SFWEOWEKRQÖÖWEIJFADF", "ASDFÖÜCZ"]
t30_results = ["GARIVO 1", "BÖSE-11", "GÜNTHER 123", "OQ123 AB",
               "SLDFKJWPEOÄÜSDGIEFHSFWEOWEKRQÖÖWEIJFA.DF", "ASDFÖÜCZ"]
t40_results = ["G ARIVO 1", "BÖ SE-11", "GÜ-NTH ER 123", "OQ:123 AB",
               "SLDFKJWPEOÄÜSDGIEFH .:S.F: WE:. OWEKRQÖ.Ö: .WEIJFA.DF", "ASDFÖÜCZ"]
all_results = [[["A", 10], a10_results], [["A", 20], a20_results], [["DEFAULT", 10], d10_results],
               [["DEFAULT", 20], d20_results], [["DEFAULT", 30], d30_results], [["TEST", 10], t10_results],
               [["TEST", 20], t20_results], [["TEST", 30], t30_results], [["TEST", 40], t40_results]]


def gen_plate(plates, countries):
    co = []
    for c in countries:
        co.append({"code": c, "confidence": 0.5})
    pl = []
    for p in plates:
        pl.append({"plate": p, "confidence": 0.1})

    return {
        "plate": {"plate": plates[0], "confidence": 0.1},
        "country": co,
        "alternatives": pl
    }


def prepare_db(plates, default_country_order=[], dco_w_legacy=False, caps=[]):
    pys = PlateYamlSelector(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/utils_matching"), "",
                            default_country_order, dco_w_legacy)
    db = {}
    for i, p in enumerate(plates):
        pys.insert_into_db_and_create_record(db, p[0], "SRB" if p[1] == "TEST" else p[1], p[1], p[2], i)

    return db, default_country_order, dco_w_legacy


plates_mo = [gen_plate(["G ÄRIVQ-0"], ["F", "A", "SRB", "OTHER"]),
             gen_plate(["G ÄRIVQ-0"], ["A", "F", "SRB", "OTHER"]),
             gen_plate(["G ÄRIVQ-0"], ["SRB", "A", "F", "OTHER"]),
             gen_plate(["G ÄRIVQ-0"], ["D", "OTHER"]),
             gen_plate(["G ÄRIVQ-0"], ["OTHER"]),
             gen_plate(["GARIV00"], ["F", "A", "SRB", "OTHER"]),
             gen_plate(["GARIV00"], ["A", "F", "SRB", "OTHER"]),
             gen_plate(["GARIV00"], ["SRB", "A", "F", "OTHER"]),
             gen_plate(["GARIV00"], ["D", "OTHER"]),
             gen_plate(["GARIV00"], ["OTHER"]),
             gen_plate(["G ARIVO0"], ["F", "A", "SRB", "OTHER"]),
             gen_plate(["G ARIVO0"], ["A", "F", "SRB", "OTHER"]),
             gen_plate(["G ARIVO0"], ["SRB", "A", "F", "OTHER"]),
             gen_plate(["G ARIVO0"], ["D", "OTHER"]),
             gen_plate(["G ARIVO0"], ["OTHER"]),
             gen_plate(["G:ARIV00"], ["F", "A", "SRB", "OTHER"]),
             gen_plate(["G:ARIV00"], ["A", "F", "SRB", "OTHER"]),
             gen_plate(["G:ARIV00"], ["SRB", "A", "F", "OTHER"]),
             gen_plate(["G:ARIV00"], ["D", "OTHER"]),
             gen_plate(["G:ARIV00"], ["OTHER"]),
             gen_plate(["X-YZ"], ["F", "A", "SRB", "OTHER"]),
             gen_plate(["X-YZ"], ["A", "F", "SRB", "OTHER"]),
             gen_plate(["X-YZ"], ["SRB", "A", "F", "OTHER"]),
             gen_plate(["X-YZ"], ["D", "OTHER"]),
             gen_plate(["X-YZ"], ["OTHER"]),
             gen_plate(["G-ÄRIVQ-0"], ["SRB"]),
             gen_plate(["G-ÄRIVQ-0"], ["CH"])
             ]

results_mo = [[3, 0, 2, 1, 2, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 4, 5, 5, 6, 4, -1, -1],
              [3, 0, 2, 1, 0, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 4, 5, 5, 6, 5, -1, -1],
              [3, 0, 2, 1, 1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 4, 5, 5, 6, 4, -1, -1],
              [3, 0, 2, 1, 1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 4, 5, 5, 6, 6, -1, -1],
              [3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 4, 5, 5, 6, 4, 2, -1],
              [3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 4, 5, 5, 6, 5, 2, -1],
              [3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 4, 5, 5, 6, 4, 2, -1],
              [3, 0, 2, 1, 2, 3, 0, 2, 1, 2, 3, 0, 2, 1, 2, 3, 0, 2, 1, 2, 4, 5, 5, 6, 6, 2, -1],
              [3, 0, 2, 1, 1, 3, 0, 2, 1, 1, 3, 0, 2, 1, 1, 3, 0, 2, 1, 1, 4, 5, 5, 6, 6, 2, -1],
              [3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 3, 0, 2, 1, 0, 4, 5, 5, 6, 4, 2, -1]]

dbs = [
    prepare_db([("G ÄRIVQ-0", "A", 100), ("G ÄRIVQ-0", "D", 100), ("G ÄRIVQ-0", "TEST", 100), ("G ÄRIVQ-0", "F", 100),
                ("X-YZ", "F", 100), ("X-YZ", "A", 10), ("X-YZ", "D", 0)],
               []),
    prepare_db([("G ÄRIVQ-0", "A", 100), ("G ÄRIVQ-0", "D", 100), ("G ÄRIVQ-0", "TEST", 100), ("G ÄRIVQ-0", "F", 100),
                ("X-YZ", "F", 100), ("X-YZ", "A", 10), ("X-YZ", "D", 0)],
               ['A']),
    prepare_db([("G ÄRIVQ-0", "A", 100), ("G ÄRIVQ-0", "D", 100), ("G ÄRIVQ-0", "TEST", 100), ("G ÄRIVQ-0", "F", 100),
                ("X-YZ", "F", 100), ("X-YZ", "A", 10), ("X-YZ", "D", 0)],
               ['D']),
    prepare_db([("G ÄRIVQ-0", "A", 100), ("G ÄRIVQ-0", "D", 100), ("G ÄRIVQ-0", "TEST", 100), ("G ÄRIVQ-0", "F", 100),
                ("X-YZ", "F", 100), ("X-YZ", "A", 10), ("X-YZ", "D", 0)],
               ['D'], dco_w_legacy=True),
    prepare_db(
        [("GARIV00", "A", 0), ("GARIV00", "D", 0), ("GARIV00", "TEST", 0), ("GARIV00", "F", 0), ("X-YZ", "F", 100),
         ("X-YZ", "A", 10), ("X-YZ", "D", 0)],
        []),
    prepare_db(
        [("GARIV00", "A", 0), ("GARIV00", "D", 0), ("GARIV00", "TEST", 0), ("GARIV00", "F", 0), ("X-YZ", "F", 100),
         ("X-YZ", "A", 10), ("X-YZ", "D", 0)],
        ['A']),
    prepare_db(
        [("GARIV00", "A", 0), ("GARIV00", "D", 0), ("GARIV00", "TEST", 0), ("GARIV00", "F", 0), ("X-YZ", "F", 100),
         ("X-YZ", "A", 10), ("X-YZ", "D", 0)],
        ['SRB', "D"]),
    prepare_db(
        [("GARIV00", "A", 0), ("GARIV00", "D", 0), ("GARIV00", "TEST", 0), ("GARIV00", "F", 0), ("X-YZ", "F", 100),
         ("X-YZ", "A", 10), ("X-YZ", "D", 0)],
        ['SRB', "D"], dco_w_legacy=True),
    prepare_db(
        [("GARIV00", "A", 0), ("GARIV00", "D", 0), ("GARIV00", "TEST", 0), ("GARIV00", "F", 0), ("X-YZ", "F", 100),
         ("X-YZ", "A", 10), ("X-YZ", "D", 0)],
        ['D'], dco_w_legacy=True),
    prepare_db(
        [("GARIV00", "A", 0), ("GARIV00", "D", 0), ("GARIV00", "TEST", 0), ("GARIV00", "F", 0), ("X-YZ", "F", 100),
         ("X-YZ", "A", 10), ("X-YZ", "D", 0)],
        ['X'], dco_w_legacy=True)
]

plates_alt = [gen_plate(["X-YZ", "X YZ"], ["F", "OTHER"]),
              gen_plate(["X-YZ", "X YZ"], ["OTHER"]),
              gen_plate(["X-YZ", "XYZ", "X YZ"], ["OTHER"]),
              gen_plate(["XYZA", "XYZ:"], ["D"]),
              gen_plate(["XYZA", "XYZ:"], ["CH"])]
results_alt = [[0, 0, 0, 2, -1], [2, 2, 2, 2, -1], [3, 1, 2, -1, -1]]
dbs_alt = [
    prepare_db([("X:YZ", "A", 10), ("X YZ", "TEST", 40), ("XYZ", "D", 0), ("X YZ", "F", 30)], []),
    prepare_db([("X YZ", "A", 20), ("X YZ", "TEST", 40), ("XYZ", "D", 0), ("X YZ", "F", 30)], []),
    prepare_db([("X YZ", "A", 20), ("X YZ", "TEST", 40), ("XYZ", "D", 30), ("X YZ", "F", 30)], [])
]


class MatchingTest(unittest.TestCase):
    def do_stuff(self, results, scheme, version):
        pys = PlateYamlSelector(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/utils_matching"),
                                "")
        for p, r in zip(plates, results):
            converted = pys.convert(p, scheme, version)
            success = r == converted
            if not success:  # pragma: no cover
                print(scheme, version)
                print(p, "->", converted)
            self.assertTrue(success)

    def test_legacy_convert(self):
        self.do_stuff(legacy_results, "LEGACY", 0)

    def test_selection(self):
        pys = PlateYamlSelector(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/utils_matching"),
                                "")
        inputs = [["LEGACY", 0], ["LEGACY", 1], ["DEFAULT", 0], ["DEFAULT", 1], ["DEFAULT", 10], ["DEFAULT", 11],
                  ["DEFAULT", 20], ["DEFAULT", 25], ["DEFAULT", 35], ["A", 5], ["A", 10], ["A", 15], ["A", 20],
                  ["A", 25], ["TEST", 5], ["TEST", 55], ["ASD", 0], ["aeg", 1], ["whbns", 10],
                  ["sh", 11], ["af", 20], ["hs", 25], ["jsd", 35]]
        results = [["LEGACY", 0], ["LEGACY", 0], ["LEGACY", 0], ["LEGACY", 0], ["DEFAULT", 10], ["DEFAULT", 10],
                   ["DEFAULT", 20], ["DEFAULT", 20], ["DEFAULT", 30], ["LEGACY", 0], ["A", 10], ["A", 10], ["A", 20],
                   ["A", 20], ["LEGACY", 0], ["TEST", 40], ["LEGACY", 0], ["LEGACY", 0], ["DEFAULT", 10],
                   ["DEFAULT", 10], ["DEFAULT", 20], ["DEFAULT", 20], ["DEFAULT", 30]]
        for i, r in zip(inputs, results):
            yaml = pys.get_best_yaml(*i)
            self.assertEqual(r, [yaml.scheme, yaml.version])

    def test_various_conversions(self):
        for res in all_results:
            self.do_stuff(res[1], res[0][0], res[0][1])

    def test_matching_order_no_alternatives(self):
        for i, db1 in enumerate(dbs):
            db = db1[0]
            pys = PlateYamlSelector(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/utils_matching"), "", db1[1],
                db1[2])
            for j, plate in enumerate(plates_mo):
                res = pys.match_plate(plate, db)
                res = None if len(res[0]) == 0 else res[0][0]
                sys.stdout.flush()
                success = results_mo[i][j] == (-1 if res is None else res["id"])
                if not success:  # pragma: no cover
                    print("database", i)
                    print("plate", j, ":", plate["plate"], "|", plate["country"][0]["code"], "|", results_mo[i][j],
                          "->")
                    if res is not None:
                        print(res["plate"], "|", res["plate_scheme"], "|", res["plate_scheme_version"], "|",
                              res["id"], "|", res["used_scheme"], "|", res["used_version"], "|", res["exactitude"])
                    else:
                        print()
                self.assertTrue(success)

    def test_matching_order_with_alternatives(self):
        for i, db1 in enumerate(dbs_alt):
            db = db1[0]
            pys = PlateYamlSelector(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/utils_matching"), "", db1[1],
                db1[2])
            for j, plate in enumerate(plates_alt):
                res = pys.match_plate(plate, db, return_only_best=False)
                res = None if len(res[0]) == 0 else res[0][0]
                sys.stdout.flush()
                success = results_alt[i][j] == (-1 if res is None else res["id"])
                if not success:  # pragma: no cover
                    print("database", i)
                    print("plate", j, ":", plate["plate"], "|", plate["country"][0]["code"], "|", results_alt[i][j],
                          "->")
                    if res is not None:
                        print(res["plate"], "|", res["plate_scheme"], "|", res["plate_scheme_version"], "|",
                              res["id"], "|", res["used_scheme"], "|", res["used_version"], "|", res["exactitude"])
                    else:
                        print()
                self.assertTrue(success)

    def test_matching_order_ed1(self):
        plates_ed1 = [gen_plate(["X-YZ"], ["F", "OTHER"]), gen_plate(["X-YZ"], ["OTHER"]), gen_plate(["XYZA"], ["D"]),
                      gen_plate(["XYZA"], ["CH"])]
        results_ed1 = [[0, 0, 2, -1], [2, 2, 2, -1], [2, 1, -1, -1], [2, 0, -1, -1]]
        dbs_ed1 = [
            prepare_db([("X:YZ", "A", 10), ("X YZ", "TEST", 40), ("XYZ", "D", 0), ("X YZ", "F", 30)], []),
            prepare_db([("X YZ", "A", 20), ("X YZ", "TEST", 40), ("XYZ", "D", 0), ("X YZ", "F", 30)], []),
            prepare_db([("X YZ", "A", 20), ("X YZ", "TEST", 40), ("X YZ", "F", 30)], []),
            prepare_db([("X YZ", "A", 20), ("X YZ", "TEST", 40), ("X YZ", "F", 30)], ["A"])
        ]

        for i, db1 in enumerate(dbs_ed1):
            db = db1[0]
            pys = PlateYamlSelector(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/utils_matching"), "", db1[1],
                db1[2])
            for j, plate in enumerate(plates_ed1):
                res = pys.match_plate(plate, db, False, 1)
                res = None if len(res[0]) == 0 else res[0][0]
                sys.stdout.flush()
                success = results_ed1[i][j] == (-1 if res is None else res["id"])
                if not success:  # pragma: no cover
                    print("database", i)
                    print("plate", j, ":", plate["plate"], "|", plate["country"][0]["code"], "|", results_ed1[i][j],
                          "->")
                    if res is not None:
                        print(res["plate"], "|", res["plate_scheme"], "|", res["plate_scheme_version"], "|",
                              res["id"], "|", res["used_scheme"], "|", res["used_version"], "|", res["exactitude"])
                    else:
                        print()
                self.assertTrue(success)

    def test_random(self):
        dbs = []
        for i in range(200):
            pdbs = []
            for i in range(100):
                pdbs.append((''.join(
                    random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ:-. ") for _ in range(random.randint(5, 10))),
                             ''.join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ") for _ in
                                     range(random.randint(1, 5))), random.randint(0, 10) * 10))
            dbs.append(prepare_db(pdbs, [
                ''.join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ") for _ in range(random.randint(1, 2))),
                ''.join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ") for _ in range(random.randint(1, 2))),
                ''.join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ") for _ in range(random.randint(1, 2)))],
                                  random.randint(0, 1)))
        ps = []
        for i in range(1000):
            ps.append(gen_plate([''.join(
                random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ:-. ") for _ in range(random.randint(5, 10))),
                ''.join(
                    random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ:-. ") for _ in range(random.randint(5, 10))),
                ''.join(
                    random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ:-. ") for _ in range(random.randint(5, 10))),
                ''.join(
                    random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ:-. ") for _ in
                    range(random.randint(5, 10)))],
                [''.join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ") for _ in range(random.randint(1, 2))),
                 ''.join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ") for _ in range(random.randint(1, 2))),
                 ''.join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ") for _ in range(random.randint(1, 2))),
                 ]))
        for db in dbs:
            pys = PlateYamlSelector(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/utils_matching"), "", db[1], db[2])
            for p in ps:
                pys.match_plate(p, db[0], random.randint(0, 1), random.randint(0, 1), return_only_best=False)

    def test_no_yamls(self):
        pys = PlateYamlSelector("/")
        self.assertEqual("GARIV01", pys.convert("G ARIVO 1", "A", 10))

    def test_reload(self):
        tempdir = tempfile.mktemp()
        os.makedirs(tempdir, exist_ok=True)
        try:
            revision_path = os.path.join(tempdir, "revision")
            default_10_path = os.path.join(tempdir, "DEFAULT-10.yml")

            with open(revision_path, 'w') as f:
                f.write("1")
            pys = PlateYamlSelector(tempdir, revision_path)
            self.assertEqual("GARIV01", pys.convert("G ARIVO 1", "A", 10))
            with open(default_10_path, "w") as f:
                f.write("""
    allowed: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ:-. "
    kept_separators: ALL
    exactitude: 1.3
    """)

            # revision did not change, no reload is happening
            pys.reload_yamls()
            self.assertEqual("GARIV01", pys.convert("G ARIVO 1", "A", 10))

            # change revision to trigger reload
            with open(revision_path, 'w') as f:
                f.write("2")
            pys.reload_yamls()
            self.assertEqual("G ARIVO 1", pys.convert("G ARIVO 1", "A", 10))
        finally:
            shutil.rmtree(tempdir)

    def test_performance(self):
        def print_time(name):
            diff = time.time() - start
            print(name, f"{diff:.02f} for {count} = {(count / diff):.02f} per second")

        import time
        ps = []
        count = 100000
        start = time.time()
        initial_start = start
        for i in range(count):
            ps.append((''.join(
                random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWX-YZÄÖÜ:-. ") for _ in range(random.randint(5, 10))),
                       random.choice(["A", "D", "TEST", "F"]), 100))
        print_time("Random Plates")

        start = time.time()
        db = prepare_db(ps, ['A', 'D'], False)
        print_time("Prepare DB")

        pys = PlateYamlSelector(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/utils_matching"),
                                "", db[1], db[2])

        start = time.time()
        pys.match_plate(plates_mo[3], db[0])
        print_time("Match plate")

        start = initial_start
        print_time("Total time")
