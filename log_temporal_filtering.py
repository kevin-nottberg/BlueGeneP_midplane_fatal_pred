import json, csv
import os, fnmatch
from log_coupling import Log_Coupling

LOG_DIRECTORY="./new_time_localized/"
FILTERED_DIRECTORY = "./simple_filtered_localized/"

def main():
    # Load in a log file
    midplane_list = []
    directory_list = os.scandir(LOG_DIRECTORY)
    for entry in directory_list:
        # print all files
        if(entry.is_file()):
            midplane_list.append(entry.name)

    print("Number of midplane logs: {}".format(len(midplane_list)))

    sum_original = 0
    sum_final = 0

    removal_csv_file = open('filteration_removal_metrics.csv', mode='w')
    data_writer = csv.writer(removal_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
    header = ["Midplane", "% Record Removal"]
    data_writer.writerow(header)

    for midplane in midplane_list:
        with open("{}{}".format(LOG_DIRECTORY, midplane), "r") as log:
            print("Midplane: {}".format(midplane))
            data = json.load(log)

            event_catalog = {}
            final_log_list = []

            length_orig = 0
            # Check to make sure that the events are already sorted by time
            start_time = None
            try:
                for entry in data:
                    length_orig += 1
                    if(start_time == None):
                        start_time = entry["EVENT_TIME"]
                    elif( start_time > entry["EVENT_TIME"] ):
                        print("\tThe log needs to be sorted on time")
                        exit()
                    else:
                        start_time = entry["EVENT_TIME"]
            except KeyError as error:
                print(entry)
                exit()

            length_final = 0
            # Start grouping all entries in logs
            start_time = None
            for entry in data:
                if(start_time == None):
                    #print("New start time")
                    start_time = entry["EVENT_TIME"]
                elif( entry["EVENT_TIME"] - start_time >= 3600 ):
                    #print(entry["EVENT_TIME"] - start_time)
                    #print("Reached the end of an hour bucket. Simplifying data")
                    #print("Dumping")
                    for coupling in event_catalog.values():
                        simplified_entries = coupling.event_times.keys()
                        for final_entry in sorted(simplified_entries):
                            length_final += 1
                            final_log_list.append(coupling.event_times[final_entry])

                    start_time = entry["EVENT_TIME"]
                    event_catalog = {}

                elif( entry["SEVERITY"] == "FATAL" ):
                    #print("Hit a FATAL event. End of bucket. Simplifying data")
                    #print("Dumping")
                    for coupling in event_catalog.values():
                        simplified_entries = coupling.event_times.keys()
                        for final_entry in sorted(simplified_entries):
                            length_final += 1
                            final_log_list.append(coupling.event_times[final_entry])

                    length_final += 1
                    final_log_list.append(entry)
                    event_catalog = {}
                    continue

                key = "{}_{}_{}_{}".format(entry["COMPONENT"], entry["SUBCOMPONENT"], entry["ERRCODE"], entry["SEVERITY"])
                if( event_catalog.get(key) != None ):
                    # Get the log coupling and add the entry to it
                    #print("Adding entry to previous bucket")
                    event_catalog[key].add_entry(entry)
                else:
                    # Make new log coupling and add it to the event log
                    #print("Creating new entry")
                    new_coupling = Log_Coupling(entry)
                    new_coupling.add_entry(entry)
                    event_catalog[key] = new_coupling

            print("Original length: {}\n Final Length: {}\n % Removal: {}"
                    .format(length_orig, length_final, ((length_orig-length_final)/length_orig)*100))
            percent_removal = ((length_orig-length_final)/length_orig) * 100
            data_writer.writerow([midplane, percent_removal])
            filtered_file = open("{}{}".format(FILTERED_DIRECTORY, midplane), "w")

            sorted_final_log_list = []
            ent_dict = {}
            for ent in final_log_list:
                ent_dict[ent["EVENT_TIME"]] = ent

            for key in sorted(ent_dict.keys()):
                sorted_final_log_list.append(ent_dict.get(key))

            filtered_file.write(json.dumps(sorted_final_log_list, indent=4))
            filtered_file.close()

    sum_original += length_orig
    sum_final += length_final

    print("Full compression: {}".format(((sum_original-sum_final)/sum_original)*100))
if __name__ == "__main__":
    main()
