import json, re, datetime

class Log_Entry:

    def __init__( self ):
        self.rec_id = ""
        self.rec_id_len = 11
        self.msg_id = ""
        self.msg_id_len = 10
        self.component = ""
        self.component_length = 16
        self.subcomponent = ""
        self.subcomponent_length = 20
        self.err_code = ""
        self.err_code_length = 40
        self.severity = ""
        self.severity_length = 8
        self.event_time = ""
        self.event_time_len = 26
        self.flags = ""
        self.flags_len = 10
        self.processor = ""
        self.processor_len = 11
        self.node = ""
        self.node_len = 11
        self.block = ""
        self.block_len = 32
        self.location = ""
        self.location_length = 64
        self.serial_number = ""
        self.serial_number_len = 19
        self.ecid = ""
        self.ecid_len = 31
        self.message = ""
        self.message_length = 1025

        self.lengths_list = [ 12, 11, 17, 21, 41, 9, 27, 11, 12, 12, 33, 65, 20, 32, 1026 ]
        self.json_data = {}

    def update_indexes( self, beg_ind, end_ind, next_length ):
        beg_ind = end_ind
        end_ind = beg_ind + self.lengths_list[next_length]

        return beg_ind, end_ind

    def create( self, log_entry ):
        beg_ind, end_ind = self.update_indexes(0, 0, 0)
        self.rec_id = log_entry[beg_ind : end_ind]
        self.rec_id = self.rec_id.decode('utf-8').strip()
        self.json_data["RECID"] = self.rec_id

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 1)
        self.msg_id = log_entry[beg_ind : end_ind]
        self.msg_id = self.msg_id.decode('utf-8').strip()
        self.json_data["MSG_ID"] = self.msg_id

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 2)
        self.component = log_entry[beg_ind : end_ind]
        self.component = self.component.decode('utf-8').strip()
        self.json_data["COMPONENT"] = self.component

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 3)
        self.subcomponent = log_entry[beg_ind : end_ind]
        self.subcomponent = self.subcomponent.decode('utf-8').strip()
        self.json_data["SUBCOMPONENT"] = self.subcomponent

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 4)
        self.err_code = log_entry[beg_ind : end_ind]
        self.err_code = self.err_code.decode('utf-8').strip()
        self.json_data["ERRCODE"] = self.err_code

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 5)
        self.severity = log_entry[beg_ind : end_ind]
        self.severity = self.severity.decode('utf-8').strip()
        self.json_data["SEVERITY"] = self.severity

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 6)
        # Convert the time to epoch time signiture
        raw_event_time = log_entry[beg_ind : end_ind]
        event_time_str = raw_event_time.decode('utf-8').strip()
        event_time_array = event_time_str.replace('-', '.').split('.')
        self.event_time = datetime.datetime(int(event_time_array[0]),
                                                int(event_time_array[1]),
                                                    int(event_time_array[2]),
                                                        int(event_time_array[3]),
                                                            int(event_time_array[4]),
                                                                int(event_time_array[5]),
                                                                    int(event_time_array[6])).timestamp()
        self.json_data["EVENT_TIME"] = self.event_time

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 7)
        self.flags = log_entry[beg_ind : end_ind]
        self.flags = self.flags.decode('utf-8').strip()
        self.json_data["FLAGS"] = self.flags

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 8)
        self.processor = log_entry[beg_ind : end_ind]
        self.processor = self.processor.decode('utf-8').strip()
        self.json_data["PROCESSOR"] = self.processor

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 9)
        self.node = log_entry[beg_ind : end_ind]
        self.node = self.node.decode('utf-8').strip()
        self.json_data["NODE"] = self.node

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 10)
        self.block = log_entry[beg_ind : end_ind]
        self.block = self.block.decode('utf-8').strip()
        self.json_data["BLOCK"] = self.block

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 11)
        self.location = log_entry[beg_ind : end_ind]
        self.location = self.location.decode('utf-8').strip()
        self.json_data["LOCATION"] = self.location

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 12)
        self.serial_number = log_entry[beg_ind : end_ind]
        self.serial_number = self.serial_number.decode('utf-8').strip()
        self.json_data["SERIALNUMBER"] = self.serial_number

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 13)
        self.ecid = log_entry[beg_ind : end_ind]
        self.ecid = self.ecid.decode('utf-8').strip()
        self.json_data["ECID"] = self.ecid

        beg_ind, end_ind = self.update_indexes(beg_ind, end_ind, 14)
        self.message = log_entry[beg_ind : end_ind]
        self.message = self.message.decode('utf-8').strip()
        self.json_data["MESSAGE"] = self.message


def main():
    with open( "Intrepid_RAS_0901_0908", "rb" ) as main_log:
        # Hash the location of the log entries mapped to their open file pointer
        log_location_list = {}

        # Move through introductory lines of the file
        for i in range(0, 6):
            print("Empty line: " + str(main_log.readline()))

        # Create regex expression for location to filter
        local_regex = re.compile("^(R[0-9]{2})-(M[0-9])-(N[0-9]{2})-([J,P][0-9]{1,2})+$")
        recid_regex = re.compile("^([0-9]{8})+$")

        new_line = main_log.readline()
        count = 0
        while( new_line != None and new_line != ""):
            if( new_line != b'\n' ):
                if(local_regex.match(new_line[206:271].decode('utf-8').strip()) != None):
                    print("Normal log entry format")
                    print("Create a new log entry")
                    new_log_entry = Log_Entry()
                    new_log_entry.create( new_line )

                else:
                    fixed_line = ""
                    start, block_count = 0, -1
                    str_block = False
                    new_log_entry = Log_Entry()

                    for i in range(0, len(new_line)):
                        if(chr(new_line[i]) != " "):
                            if(str_block == False):
                                start = i
                                str_block = True
                                block_count += 1
                            fixed_line += chr(new_line[i])
                        elif(chr(new_line[i]) == " "):
                            if(str_block):
                                str_block = False
                                if(block_count == 0):
                                    new_log_entry.rec_id = fixed_line
                                    new_log_entry.json_data["RECID"] = fixed_line
                                elif(block_count == 1):
                                    new_log_entry.msg_id = fixed_line
                                    new_log_entry.json_data["MSG_ID"] = fixed_line
                                elif(block_count == 2):
                                    new_log_entry.component = fixed_line
                                    new_log_entry.json_data["COMPONENT"] = fixed_line
                                elif(block_count == 3):
                                    new_log_entry.subcomponent = fixed_line
                                    new_log_entry.json_data["SUBCOMPONENT"] = fixed_line
                                elif(block_count == 4):
                                    new_log_entry.errcode = fixed_line
                                    new_log_entry.json_data["ERRCODE"] = fixed_line
                                elif(block_count == 5):
                                    new_log_entry.severity = fixed_line
                                    new_log_entry.json_data["SEVERITY"] = fixed_line
                                elif(block_count == 6):
                                    event_time_str = fixed_line
                                    event_time_array = event_time_str.replace('-', '.').split('.')
                                    try:
                                        new_log_entry.event_time = datetime.datetime(int(event_time_array[0]),
                                                                                    int(event_time_array[1]),
                                                                                    int(event_time_array[2]),
                                                                                    int(event_time_array[3]),
                                                                                    int(event_time_array[4]),
                                                                                    int(event_time_array[5]),
                                                                                    int(event_time_array[6])).timestamp()
                                        new_log_entry.json_data["EVENT_TIME"] = new_log_entry.event_time
                                    except ValueError:
                                        print("ValueError for time in nonstandard format")
                                    except IndexError:
                                        print("IndexError for time in nonstandard format")

                                elif(block_count == 7):
                                    new_log_entry.processor = fixed_line
                                    new_log_entry.json_data["PROCESSOR"] = fixed_line
                                    new_log_entry.flag = "-"
                                    new_log_entry.json_data["FLAGS"] = fixed_line
                                    new_log_entry.node = "-"
                                    new_log_entry.json_data["NODE"] = fixed_line
                                elif(block_count == 8):
                                    new_log_entry.block = fixed_line
                                    new_log_entry.json_data["BLOCK"] = fixed_line
                                elif(block_count == 9):
                                    new_log_entry.location = fixed_line
                                    new_log_entry.json_data["LOCATION"] = fixed_line
                                elif(block_count == 10):
                                    new_log_entry.serial_number = fixed_line
                                    new_log_entry.json_data["SERIALNUMBER"] = fixed_line
                                elif(block_count >= 11):
                                    new_log_entry.ecid = "N/A"
                                    new_log_entry.json_data["ECID"] = "N/A"
                                    new_log_entry.message = "N/A"
                                    new_log_entry.json_data["MESSAGE"] = "N/A"
                                    print("New style")
                                    print(new_log_entry.json_data)
                                    break
                                fixed_line = ""

                if(local_regex.match(new_log_entry.location)
                    and new_log_entry.message != ""
                    and new_log_entry.ecid != ""
                    and recid_regex.match(new_log_entry.rec_id)):
                    location = new_log_entry.json_data["LOCATION"][0:6]
                    print("Location: " + location)
                    if( location not in log_location_list ):
                        # Open a new file
                        new_file = open("./new_time_localized/" + location, "w")
                        log_location_list[location] = [new_file, []]

                    log_location_list[location][1].append(new_log_entry.json_data)
                    #write_file = log_location_list[location]
                    #write_file.write(json.dumps(new_log_entry.json_data, indent=4))
                else:
                    if(not local_regex.match(new_log_entry.location)):
                        print("Throwing out because it doesn't fit location regex")
                    elif(not recid_regex.match(new_log_entry.rec_id)):
                        print("Throwing out because it doesn't fit recid regex")
                    print("Throwing out data")

            new_line = main_log.readline()
            try:
                if(new_line.decode('utf-8') == ""):
                    break
            except UnicodeDecodeError as error:
                print("Sorry")

        for loc_data in log_location_list.values():
            write_file = loc_data[0]
            write_file.write(json.dumps(loc_data[1], indent=4))

if __name__ == "__main__":
    main()
