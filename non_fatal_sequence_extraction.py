import json
import os, fnmatch, math

LOG_DIRECTORY = "./final_filtered_localized/"

LENGTH_SEQUENCE = 6

def main():
    midplane_list = []
    directory_list = os.scandir(LOG_DIRECTORY)
    for entry in directory_list:
        if(entry.is_file()):
            midplane_list.append(entry.name)

    non_fatal_sequences = []
    for midplane in midplane_list:
        with open("{}{}".format(LOG_DIRECTORY, midplane), "r") as log:
            data = json.load(log)

            last_fatal_time = 0
            sequence_start = False
            sequence = []
            for entry in data:
                if(entry["SEVERITY"] == "FATAL"):
                    last_fatal_time = entry["EVENT_TIME"]
                    """
                    Start to pop the last events and see if they
                    are far enough from this event
                    """
                    for i in range(len(sequence) - 1, 0 -1):
                        if((last_fatal_time - sequnce[i]) < 7200):
                            # Remove the item
                            sequence.pop(i)
                        else:
                            break

                    num_sequences = math.ceil(len(sequence)/LENGTH_SEQUENCE)
                    print(num_sequences)
                    for i in range(num_sequences):
                        print("Start {} : End {}".format(i*LENGTH_SEQUENCE, (i+1)*LENGTH_SEQUENCE))
                        new_sequence = sequence[i*LENGTH_SEQUENCE : ((i+1)*LENGTH_SEQUENCE)]
                        if(len(new_sequence) < 6 or len(new_sequence) > 6):
                            print("New sequence length: {}".format(len(new_sequence)))
                        non_fatal_sequences.append(new_sequence)

                    new_sequence = sequence[i*LENGTH_SEQUENCE: len(sequence)]
                    if(len(new_sequence) < 6 or len(new_sequence) > 6):
                        print("New sequence length: {}".format(len(new_sequence)))
                    non_fatal_sequences.append(new_sequence)

                    sequence_start = False
                    sequence = []
                elif(sequence_start == False and
                        (entry["EVENT_TIME"] - last_fatal_time) >= 7200):
                    sequence.append(entry)
                    sequence_start = True
                else:
                    sequence.append(entry)

            num_sequences = math.ceil(len(sequence)/LENGTH_SEQUENCE)
            for i in range(num_sequences):
                new_sequence = sequence[i*LENGTH_SEQUENCE : ((i+1)*LENGTH_SEQUENCE)]
                if(len(new_sequence) < 6 or len(new_sequence) > 6):
                    print("New sequence length: {}".format(len(new_sequence)))
                non_fatal_sequences.append(new_sequence)

            new_sequence = sequence[i*LENGTH_SEQUENCE: len(sequence)]
            if(len(new_sequence) < 6 or len(new_sequence) > 6):
                print("New sequence length: {}".format(len(new_sequence)))
            non_fatal_sequences.append(new_sequence)

    print(len(non_fatal_sequences))
    fatal_seq_file = open("non_fatal_sequences", "w")
    fatal_seq_file.write(json.dumps(non_fatal_sequences, indent=4))
    fatal_seq_file.close()

if __name__ == "__main__":
    main()
