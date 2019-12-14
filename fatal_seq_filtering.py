import json
import os, fnmatch

LOG_DIRECTORY = "./simple_filtered_localized/"
FILTERED_DIRECTORY = "./final_filtered_localized/"

def main():
    midplane_list = []
    directory_list = os.scandir(LOG_DIRECTORY)
    for entry in directory_list:
        if(entry.is_file()):
            midplane_list.append(entry.name)

    for midplane in midplane_list:
        if(midplane == ".DS_Store"):
            continue
        print("Analyzing FATAL sequences in {}".format(midplane))
        with open("{}{}".format(LOG_DIRECTORY, midplane), "r") as log:
            data = json.load(log)

            in_sequence = False
            comp_code = None
            new_data = []
            for entry in data:
                if(entry["SEVERITY"] == "FATAL"):
                    print(entry["RECID"])
                    if(not in_sequence):
                        in_sequence = True
                        comp_code = "{}_{}_{}".format(entry["COMPONENT"], entry["SUBCOMPONENT"], entry["ERRCODE"])
                        new_data.append(entry)
                    elif(in_sequence):
                        if(comp_code == "{}_{}_{}".format(entry["COMPONENT"], entry["SUBCOMPONENT"], entry["ERRCODE"])):
                            print("Removing entry with {}".format(comp_code))
                        else:
                            in_sequence = True
                            comp_code = "{}_{}_{}".format(entry["COMPONENT"], entry["SUBCOMPONENT"], entry["ERRCODE"])
                            new_data.append(entry)
                else:
                    new_data.append(entry)



            new_file = open("{}{}".format(FILTERED_DIRECTORY, midplane), "w")
            new_file.write(json.dumps(new_data, indent=4))
            new_file.close()

if __name__ == "__main__":
    main()
