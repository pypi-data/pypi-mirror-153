from datetime import datetime
import re

SYS_POS = slice(5, 6)
SYS_EXT_POS = slice(5, 7)
RUN_POS = slice(7, 9)
DEV_START_POS = 9  # slice(9, 12)
VSN_POS = slice(1, 3)


class psense_exp_title:
    def __init__(self):
        # process experiment Information
        self.typeof_study = dict(
            {
                "H": "Clinical",
                "F": "Flow System",
                "B": "Beaker",
                "A": "Heat Block",
                "P": "Prototype",
                "R": "Pre-Clinical",
                "C": "Flow Cell",
            }
        )

        self.typeof_sensor = dict(
            {
                "G": "Glucose",
                "O": "Oxygen",
                "L": "Lactate",
                "K": "Ketone",
                "T": "Temperature",
                "X": "Multi (legacy)",
                "A": "Acetylcholine",
                "C": "Choline",
                "N": "Other",
            }
        )
        self.typeof_electrode = dict(
            {"C": "Circular", "R": "Rectangular", "D": "Distributed", "X": "Other"}
        )
        self.typeof_stack = dict(
            {
                "R": "Ring",
                "P": "Planar",
                "X": "Other",
            }
        )
        self.typeof_process = dict(
            {
                "S": "Standard",
                "V": "Volcano",
                "B": "Blanket",
                "W": "Sandwich",
                "0": "No Silicone",
            }
        )
        self.typeof_extras = dict(
            {
                "M": "Mediator",
                "C": "Catalase",
                "P": "Peroxidase",
                "N": "NAD+",
                "O": "Other",
                "X": "X",
            }
        )

    def decode(self, expid):
        """translate a percusense experiment identifier string into a human-
        readble dictionary"""

        res = []
        try:
            regions = expid.upper().split("-")

            # should have 5 "regions" in an experiment code -- attempt to handle partial codes
            regions.extend([""] * (5 - len(regions)))

            if len(regions[0]) > 4:
                study = {
                    "start": datetime.strptime(
                        "{}-{}-{}".format(
                            regions[0][:2],
                            max(ord(regions[0][2:3]) - 64, 1),
                            max(1, int(regions[0][3:5])),
                        ),
                        "%y-%m-%d",
                    )
                    .date()
                    .isoformat(),
                    "type": self.typeof_study.get(regions[0][SYS_POS]),
                    "run": regions[0][RUN_POS],
                    "device": regions[0][DEV_START_POS:],
                }

                # special cases -- 2-digit study type
                if regions[0][SYS_EXT_POS] == "AN":
                    study["type"] = "Pre-Clinical"
                elif regions[0][SYS_EXT_POS] == "HU":
                    study["type"] = "Clinical"

            else:
                study = []

            if len(regions[2]) > 0:
                sensor = dict()
                sensor["code"] = "{}-{}-{}".format(regions[1], regions[2], regions[3])
                sensor["count"] = regions[4][0]
                sensor["vsn"] = regions[4][VSN_POS]

                electrodes = []
                if sensor["count"].isalpha():
                    # legacy, or single-analyte
                    text = regions[4]
                    electrodes = [
                        dict(
                            type=self.typeof_sensor.get(text[0]),
                            electrode=self.typeof_electrode.get(text[3]),
                            stack=self.typeof_stack.get(text[4]),
                            process=self.typeof_process.get(text[5]),
                            extras=self.typeof_extras.get(text[6]),
                        )
                    ]
                else:
                    # multi-analyte
                    for elec in range(int(regions[4][:1])):
                        offset = 3 + (elec * 3)
                        text = regions[4][slice(offset, offset + 3)]
                        res = dict(
                            type=self.typeof_sensor.get(text[0]),
                            electrode=self.typeof_electrode.get(text[1]),
                            process=self.typeof_process.get(text[2]),
                        )
                        electrodes.append(res)

                sensor["electrodes"] = electrodes
            else:
                sensor = []

            res = dict(study=study, sensor=sensor)
        except BaseException:
            pass

        return res


"Simple IO Functions"


def yn_input(message, default="y"):
    "i/o: collect a yes/no answer from input"
    choices = "Y/n" if default.lower() in ("y", "yes") else "y/N"
    choice = input("{} ({}) ".format(message, choices))
    values = ("y", "yes", "") if choices == "Y/n" else ("y", "yes")
    return choice.strip().lower() in values


def answer_input(message, choices, default="0", is_required=True):
    "i/o: collect a typed answer from input (regex response validation)"
    is_valid = False

    if isinstance(choices, list):
        while not is_valid:
            choice_str = ", ".join(choices)
            choice = input("{} ({})".format(message, choice_str)).strip().upper()
            if len(choice) == 0 and not is_required:
                return default
            elif len(choice) > 0 and choice in choices:
                return choice

            print("Invalid Input ({})".format(choice))

    elif isinstance(choices, str):
        while not is_valid:
            choice = input(message).strip().upper()
            if len(choice) == 0 and not is_required:
                return default
            elif len(choice) > 0 and choice in str(
                re.search(r"{}".format(choices.upper()), choice)
            ):

                return choice

            print("Invalid Input ({})".format(choice))

    assert False


def timestamp_input(message, use_seconds=False):
    is_valid = False
    while not is_valid:
        entry = (
            input(
                "{} (yyyy-mm-dd HH:MM{}): ".format(
                    message, ":SS" if use_seconds else ""
                )
            )
            .strip()
            .upper()
        )
        try:
            entry = datetime.strptime(
                entry, "%Y-%m-%d %H:%M{}".format(":%S" if use_seconds else "")
            )
            is_valid = True
        except ValueError:
            print(
                " > invalid entry (expected format: yyyy-mm-dd HH:MM{})".format(
                    ":SS" if use_seconds else ""
                )
            )
            pass

    return entry


def exptype_input():
    "i/o: selection of starting a new experiment or resuming an existing one"
    message = "\nSelect experiment type and press enter\n\t[1] Start a new sensor (default)\n\t[2] Resume an existing sensor\n > "
    isvalid = False
    while not isvalid:
        choice = input(message).strip()
        if choice == "":
            return True
        elif choice.isnumeric():
            choice = int(choice)
            if choice == 2:
                return False
            else:
                return True
        else:
            print("Invalid input.")


def setup_new_experiment(device):
    "i/o: user input to generate a new percusense experiment id (new format as of 07/23/2020)"
    assert isinstance(device, str), "device must be of type string"

    exp_beaker = answer_input(
        "Specify the test system:\n\tA#: Heat Block\n\tB#: Beaker\n\tF#: Flow System\n\tH#: Clinical (also, HU)\n\tR#: Pre-Clinical (also, AN)\n",
        "([ABCFPHR][0-9]|AN|HU){1}",
        "ZZ",
        True,
    )
    exp_run = int(
        answer_input("Specify the run number [1]: ", "[0-9]{1,2}", "1", False)
    )
    exp_lot_we = answer_input(
        "Mfg Identifier 1 (Lot, required): ", "[0-9]{1,3}[A-Z0-9]{0,1}", "1", True
    )
    exp_lot_re = int(answer_input("Mfg Identifier 2 [000]: ", "[0-9]{0,3}", "0", False))
    exp_lot_sn = answer_input("Sensor ID [00]: ", "[A-Z0-9]{0,2}", "00", False)

    exp_vsn = int(answer_input("VSN Substrate Design [15]: ", "[0-9]{1,2}", "15", True))

    exp_we_count = int(
        answer_input("How many WE are connected? [2]: ", "[0-9]{1}", "2", False)
    )

    electrodes = []
    for electrode in range(exp_we_count):
        print("> Enter Information about WE #{}".format(electrode + 1))
        exp_type = answer_input(
            "Sensor Type ([G]lucose, (O)xygen, (L)actate, (K)etone, (T)emp, (A)cetylcholine, (C)holine, (N) Other): ",
            "[GOLKACNT]",
            "G",
            False,
        )
        exp_discs = (
            answer_input(
                "Electrode Shape ([C]ircular, (R)ectangular, (D)istributed, (X)): ",
                "[A-Z]{1}",
                "C",
                False,
            )
            .strip()
            .upper()
        )
        exp_volcano = (
            answer_input(
                "Process Label ([V]olcano, (S)tandard, (B)lanket, Sand(W)ich, (X)): ",
                "[A-Z]{1}",
                "V",
                True,
            )
            .strip()
            .upper()
        )
        electrodes.append(dict(type=exp_type, electrode=exp_discs, process=exp_volcano))

    region1 = "{}{}{}{}{:02d}{:0>3.3}".format(
        datetime.now().strftime("%y"),
        chr(int(datetime.now().strftime("%m")) + 64),
        datetime.now().strftime("%d"),
        exp_beaker,
        exp_run,
        device,
    )
    region2 = "{:0>4.4}-{:03d}-{:.2}".format(
        exp_lot_we,
        exp_lot_re,
        exp_lot_sn.zfill(2),
    )
    region3 = "{}{:02d}{}".format(
        exp_we_count,
        exp_vsn,
        "".join(
            [
                "{}{}{}".format(elec["type"], elec["electrode"], elec["process"])
                for elec in electrodes
            ]
        ),
    )
    expid = "{}-{}-{}".format(region1, region2, region3).strip().upper()

    print("> done with data input. ")
    print("Experiment ID: {}".format(expid))

    return expid
