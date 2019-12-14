import json
import os, fnmatch

LOG_DIRECTORY = "./final_filtered_localized/"

def filtered_time_check():
    midplane_list = []
    directory_list = os.scandir(LOG_DIRECTORY)
    for entry in directory_list:
        if(entry.is_file()):
            midplane_list.append(entry.name)

    print("Number of midplane files: {}".format(len(midplane_list)))

    fatal_sequences = []
    for midplane in midplane_list:
        if(midplane == ".DS_Store"):
            continue
        with open("{}{}".format(LOG_DIRECTORY, midplane), "r") as log:
            data = json.load(log)

            last_time = 0
            for entry in data:
                if(entry["EVENT_TIME"] < last_time):
                    print("Events out of time")
                    print(entry["EVENT_TIME"], last_time)

                last_time = entry["EVENT_TIME"]

def fatal_sequence_check():
    print("Checking fatal sequences")
    with open("fatal_sequences", "r") as log:
        data = json.load(log)

        print("Checking {} fatal sequences".format(len(data)))
        for seq in data:
            last_time = 0
            location = None
            for entry in seq:
                if(entry["SEVERITY"] == "FATAL"):
                    print("FATAL severity has gotten into fatal sequence")
                    exit()

                if(location == None):
                    location = entry["LOCATION"][0:7]
                elif(entry["LOCATION"][0:7] != location):
                    print("Location not equivalent across sequence")
                    exit()

                if(last_time > entry["EVENT_TIME"]):
                    print("Out of time...")
                    exit()

                last_time = entry["EVENT_TIME"]

def non_fatal_sequence_check():
    print("Checking non fatal sequences")
    with open("non_fatal_sequences", "r") as log:
        data = json.load(log)

        print("Checking {} non fatal sequences".format(len(data)))
        for seq in data:
            last_time = 0
            location = None
            for entry in seq:
                if(entry["SEVERITY"] == "FATAL"):
                    print("FATAL severity has gotten into non fatal sequence")
                    exit()

                if(location == None):
                    location = entry["LOCATION"][0:7]
                elif(entry["LOCATION"][0:7] != location):
                    print("Location not equivalent across sequence")
                    exit()

                if(last_time > entry["EVENT_TIME"]):
                    print("Out of time...")
                    exit()

                last_time = entry["EVENT_TIME"]


if __name__ == "__main__":
    filtered_time_check()
    fatal_sequence_check()
    non_fatal_sequence_check()
