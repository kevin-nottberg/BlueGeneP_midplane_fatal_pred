import json
import os, fnmatch

FILTERED_DIRECTORY = "./final_filtered_localized/"

def main():
    midplane_list = []
    directory_list = os.scandir(FILTERED_DIRECTORY)
    for entry in directory_list:
        if(entry.is_file()):
            midplane_list.append(entry.name)

    sev_terminations = 0
    err_terminations = 0
    for midplane in midplane_list:
        if( midplane == ".DS_Store"):
            continue
        print("Analyzing FATAL sequences in {}".format(midplane))
        with open("{}{}".format(FILTERED_DIRECTORY, midplane), "r") as log:
            data = json.load(log)

            fatal_count = 0
            start_recid = 0
            start_time = 0
            comp_code = None
            for entry in data:
                if(entry["SEVERITY"] == "FATAL"):
                    if(fatal_count == 0):
                        start_recid = entry["RECID"]
                        start_time = entry["EVENT_TIME"]
                        comp_code = "{}_{}_{}".format(entry["COMPONENT"], entry["SUBCOMPONENT"], entry["ERRCODE"])

                    if(comp_code == "{}_{}_{}".format(entry["COMPONENT"], entry["SUBCOMPONENT"], entry["ERRCODE"])):
                        fatal_count += 1
                    else:
                        print("Different ERR: Found {} long FATAL sequence starting at {}".format(fatal_count, start_recid))
                        err_terminations += 1
                        if(fatal_count > 1):
                            span = (entry["EVENT_TIME"] - start_time)
                            print("Sequence occurs across {} secs and {} mins".format(span, span/60))
                        fatal_count = 0
                        comp_code = None
                elif(fatal_count != 0):
                    print("Different SEV: Fount {} long FATAL sequence starting at {}".format(fatal_count, start_recid))
                    sev_terminations += 1
                    if(fatal_count > 1):
                        span = (entry["EVENT_TIME"] - start_time)
                        print("Sequence occurs across {} secs and {} mins".format(span, span/60))
                    fatal_count = 0

        input("Press Entry to continue...")

    print("SEV Terminations: {}, ERR Terminations: {}".format(sev_terminations, err_terminations))
if __name__ == "__main__":
    main()
