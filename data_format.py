import csv
import json

def main():
    component_map = {}
    sub_component_map = {}
    err_code_map = {}
    severity_map = {}

    # Open the sequence files and create maps of possible
    fatal_seq_log = open("fatal_sequences", "r")
    non_fatal_seq_log = open("non_fatal_sequences", "r")

    fatal_seq_log = json.load(fatal_seq_log)
    non_fatal_seq_log = json.load(non_fatal_seq_log)

    for seq in fatal_seq_log:
        for entry in seq:
            # Add component
            if(entry["COMPONENT"] not in component_map):
                next_number = len(component_map.keys()) + 1
                component_map[entry["COMPONENT"]] = next_number

            # Add sub component
            if(entry["SUBCOMPONENT"] not in sub_component_map):
                next_number = len(sub_component_map.keys()) + 1
                sub_component_map[entry["SUBCOMPONENT"]] = next_number

            # Add error code
            if(entry["ERRCODE"] not in err_code_map):
                next_number = len(err_code_map.keys()) + 1
                err_code_map[entry["ERRCODE"]] = next_number

            # Add severity
            if(entry["SEVERITY"] not in severity_map):
                next_number = len(severity_map.keys()) + 1
                severity_map[entry["SEVERITY"]] = next_number

    for seq in non_fatal_seq_log:
        for entry in seq:
            if(entry["COMPONENT"] not in component_map):
                next_number = len(component_map.keys()) + 1
                component_map[entry["COMPONENT"]] = next_number

            # Add sub component
            if(entry["SUBCOMPONENT"] not in sub_component_map):
                next_number = len(sub_component_map.keys()) + 1
                sub_component_map[entry["SUBCOMPONENT"]] = next_number

            # Add error code
            if(entry["ERRCODE"] not in err_code_map):
                next_number = len(err_code_map.keys()) + 1
                err_code_map[entry["ERRCODE"]] = next_number

            # Add severity
            if(entry["SEVERITY"] not in severity_map):
                next_number = len(severity_map.keys()) + 1
                severity_map[entry["SEVERITY"]] = next_number

    num_comp = len(component_map.keys())
    num_sub_comp = len(sub_component_map.keys())
    num_err_codes = len(err_code_map.keys())
    num_severity = len(severity_map.keys())

    # Normalize mappings to 0 to 1
    for comp in component_map.keys():
        component_map[comp] = component_map[comp]/num_comp
    for sub_comp in sub_component_map.keys():
        sub_component_map[sub_comp] = sub_component_map[sub_comp]/num_sub_comp
    for code in err_code_map.keys():
        err_code_map[code] = err_code_map[code]/num_err_codes
    for severity in severity_map.keys():
        severity_map[severity] = severity_map[severity]/num_severity

    print(component_map)
    print(sub_component_map)
    print(err_code_map)
    print(severity_map)

    with open('sequence_data.csv', mode='w') as seq_csv:
        seq_writer = csv.writer(seq_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
        header = ["C1", "SC1", "EC1", "SEV1",
                    "C2", "SC2", "EC2", "SEV2",
                        "C3", "SC3", "EC3", "SEV3",
                            "C4", "SC4", "EC4", "SEV4",
                                "C5", "SC5", "EC5", "SEV5",
                                    "C6", "SC6", "EC6", "SEV6", "CLASS"]

        seq_writer.writerow(header)

        for seq in fatal_seq_log:
            new_seq = [0]*24
            i = 0
            for entry in seq:
                new_seq[i] = (component_map[entry["COMPONENT"]])
                i += 1
                new_seq[i] = (sub_component_map[entry["SUBCOMPONENT"]])
                i += 1
                new_seq[i] = (err_code_map[entry["ERRCODE"]])
                i += 1
                new_seq[i] = (severity_map[entry["SEVERITY"]])
                i += 1

            new_seq.append(0)
            seq_writer.writerow(new_seq)

        j = 0
        for seq in non_fatal_seq_log:
            if(len(seq) < 2):
                print("Throwing out small vector")
                continue

            new_seq = [0]*24
            i = 0
            for entry in seq:
                new_seq[i] = (component_map[entry["COMPONENT"]])
                i += 1
                new_seq[i] = (sub_component_map[entry["SUBCOMPONENT"]])
                i += 1
                new_seq[i] = (err_code_map[entry["ERRCODE"]])
                i += 1
                new_seq[i] = (severity_map[entry["SEVERITY"]])
                i += 1

            new_seq.append(1)
            if(j % 54 == 0):
                seq_writer.writerow(new_seq)
            j += 1
    print(component_map)
    print(sub_component_map)
    print(err_code_map)
    print(severity_map)

    print("Component map len: {}".format(len(component_map.values())))
    print("Subcomponent map len: {}".format(len(sub_component_map.values())))
    print("Error code map len: {}".format(len(err_code_map.values())))
    print("Severity map len:".format(len(severity_map.values())))
    """
    with open('non_fatal_seq_data.csv', mode='w') as non_fatal_seq_csv:
        non_fatal_seq_writer = csv.writer(non_fatal_seq_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)

        for seq in non_fatal_seq_log:
            if(len(seq) < 2):
                print("Throwing out small vector")
                continue
            new_seq = [0]*24
            i = 0
            for entry in seq:
                new_seq[i] = (component_map[entry["COMPONENT"]])
                i += 1
                new_seq[i] = (sub_component_map[entry["SUBCOMPONENT"]])
                i += 1
                new_seq[i] = (err_code_map[entry["ERRCODE"]])
                i += 1
                new_seq[i] = (severity_map[entry["SEVERITY"]])
                i += 1

            new_seq.append(0)
            non_fatal_seq_writer.writerow(new_seq)
    """

if __name__ == "__main__":
    main()
