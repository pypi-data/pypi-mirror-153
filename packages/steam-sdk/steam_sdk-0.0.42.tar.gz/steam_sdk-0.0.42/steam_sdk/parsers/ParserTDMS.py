import os
import numpy as np
import pandas as pd

from pathlib import Path
from nptdms import TdmsFile


class ParserTDMS:
    """
        Class with methods to read TDMS files
    """

    def __init__(self, path_tdms: Path):
        """
            Initialization using the path to the TDMS file that should be read
        """
        # Reads TDMS file
        self.TDMSFile = TdmsFile.read(path_tdms)
        self.signal_data = np.array([[]])

    def getSpecificSignal(self, group_name: str, signal_name: str):
        """
            This function gets a specific signal (channel) from a group of a TDMS file.

            - groups: A group is an instance of the TdmsGroup class, and can contain multiple channels of data
            - channel: Channels are instances of the TdmsChannel class and act like arrays - in this case: signals of the measurement
        """

        # get signal data
        signal_output = self.TDMSFile[group_name][signal_name][:]
        return signal_output

    def appendColumnToSignalData(self, dictionary: {}):
        """
            Appending the values of the specified signals in ascending order to signal_data without the name of the group or the signal
             -> row by row: so each array represents each row with one value of each desired signal
            Input: dictionary: {group_name_1: [signal_name1, signal_name2,...], group_name_2: [signal_name3, signal_name4,...],...}
        """
        for group in dictionary.keys():
            for channel in dictionary[group]:
                if self.signal_data.size == 0:
                    self.signal_data = np.atleast_2d(self.TDMSFile[group][channel][:]).T
                else:
                    self.signal_data = np.column_stack((self.signal_data, self.TDMSFile[group][channel][:]))

    def printTDMSproperties(self):
        """
            This function prints the general properties of a TDMS file.
        """

        # Iterate over all items in the file properties and print them
        print("#### GENERAL PROPERTIES ####")
        for name, value in self.TDMSFile.properties.items():
            print("{0}: {1}".format(name, value))

    def printTDMSgroups(self, flag_channel_prop: int = 0):
        """
            This function prints the general properties of a TDMS file, like    the general properties
                                                                                group names and their properties
                                                                                channel names and if wished their properties
        """

        count = 1
        print("#### GROUP PROPERTIES ####")
        print(self.TDMSFile.properties)
        for g in self.TDMSFile.groups():
            print("@@@GROUP", count)
            print("{}".format(g))
            for name, value in g.properties.items():
                print("{0}: {1}".format(name, value))
                print("# CHANNELS OF GROUP {}#".format(count))
                for c in g.channels():
                    print("# CHANNEL #")
                    print("{}".format(c))
                    print(c.name)
                    if flag_channel_prop == 1:
                        print("# CHANNEL PROPERTIES #")
                        for name, value in c.properties.items():
                            print("{0}: {1}".format(name, value))
            count = count + 1

    def writeTDMSToCsv(self, path_output: Path, dictionary: {}):
        """
            This function writes the signals of the signal_data dictionary of this class of a TDMS file to a specific csv file.
            dictionary for header with names of the groups and signal that are used in the TDMS file
            header: Groupname_signalname, ....
        """
        # Get signal
        # signal_output = getspecificSignal(path_tdms, group_name, signal_name)
        # np.savetxt(path_output, signal_output, delimiter=",")
        # headers, units,...

        header = []
        for group in dictionary.keys():
            for channel in dictionary[group]:
                header.append(group + '_' + channel)

        tdms_df = pd.DataFrame(self.signal_data)
        tdms_df.to_csv(path_output, header=header, index=False)

    def get_timeVector(self, signal_name: str, group_name: str):
        """
            This function gets the time_vector of a specific signal of a TDMS file to a specific csv file, which provides the following properties:
                wf_increment, wf_samples, wf_samples
        """
        #self.printTDMSgroups(flag_channel_prop=1)
        inc = self.TDMSFile[group_name][signal_name].properties['wf_increment']
        samples = self.TDMSFile[group_name][signal_name].properties['wf_samples']
        off = self.TDMSFile[group_name][signal_name].properties['wf_start_offset']

        time_vec = np.arange(off, off + inc*samples, inc)

        return time_vec


#### HELPER functions ####

def getAllTDMSfiles(path_folder):
    """
        Gets all TDMS files in a specific folder and returns a list of the names of the TDMS files
    """
    # TODO: Not tested
    list_all_files = os.listdir(path_folder)
    list_tdms_files = []
    for file in list_all_files:
        if file.endswith(".tdms"):
            list_tdms_files.append(file)

    return list_tdms_files