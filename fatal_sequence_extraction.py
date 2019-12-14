import json
import os, fnmatch

LOG_DIRECTORY = "./final_filtered_localized/"

def main():
    midplane_list = []
    directory_list = os.scandir(LOG_DIRECTORY)
    for entry in directory_list:
        if(entry.is_file()):
            midplane_list.append(entry.name)

    print("Number of midplane files: {}".format(len(midplane_list)))

    fatal_sequences = []
    for midplane in midplane_list:
        print(midplane)
        with open("{}{}".format(LOG_DIRECTORY, midplane), "r") as log:
            data = json.load(log)

            sequence_list = []
            last_fatal_time = None
            prev_last_fatal = None
            for entry in data:
                # Hit Fatal event
                if(entry["SEVERITY"] == "FATAL"):
                    if(last_fatal_time == None
                        or entry["EVENT_TIME"] - last_fatal_time >= 7200):
                        prev_last_fatal = last_fatal_time
                        last_fatal_time = entry["EVENT_TIME"]
                        # Start the back up extract sequence
                        new_sequence = []
                        found_start = False
                        sequence_list.reverse()
                        for seq_item in sequence_list:
                            # Find the start
                            if(not found_start):
                                # If the event is within 1 minute before the fatal event
                                if(entry["EVENT_TIME"] - seq_item["EVENT_TIME"] >= 60):
                                # If the event is within 45 minutes before the fatal event
                                #if(entry["EVENT_TIME"] - seq_item["EVENT_TIME"] >= 2700):
                                # If the event is within 15 minutes before the fatal event
                                #if(entry["EVENT_TIME"] - seq_item["EVENT_TIME"] >= 900):
                                # If the event is within 75 minutes before the fatal event
                                #if(entry["EVENT_TIME"] - seq_item["EVENT_TIME"] >= 4500):
                                # If the event is within 120 minutes before the fatal event
                                #if(entry["EVENT_TIME"] - seq_item["EVENT_TIME"] >= 7200):
                                    new_sequence.append(seq_item)
                                    found_start = True
                            else:
                                new_sequence.append(seq_item)
                                if(len(new_sequence) == 6):
                                    break

                        print("New sequnce: {}".format(len(new_sequence)))
                        if(len(new_sequence) >= 2 and
                            prev_last_fatal != None and
                            new_sequence[len(new_sequence) - 1]["EVENT_TIME"] - prev_last_fatal >= 14400):
                            print(len(new_sequence))
                            new_sequence.reverse()
                            fatal_sequences.append(new_sequence)
                        else:
                            print("Threw out sequence, because precceded by close FATAL event")
                        sequence_list = []
                    else:
                        prev_last_fatal = last_fatal_time
                        last_fatal_time = entry["EVENT_TIME"]
                        sequence_list = []
                        continue

                else:
                    sequence_list.append(entry)

    print(len(fatal_sequences))

    fatal_seq_file = open("fatal_sequences", "w")
    fatal_seq_file.write(json.dumps(fatal_sequences, indent=4))
    fatal_seq_file.close()

if __name__ == "__main__":
    main()
