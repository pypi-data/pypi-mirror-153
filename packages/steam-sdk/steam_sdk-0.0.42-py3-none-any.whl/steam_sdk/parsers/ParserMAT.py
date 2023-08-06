import os
import numpy as np
import pandas as pd
import h5py
from pathlib import Path


def getSpecificSignalMAT(path_sim, model_name, simNumber, list_Signals):

    simulationSignalsToPlot = pd.DataFrame()

    for i in range(len(simNumber)):
        path_simulationSignals = os.path.join(path_sim + str(simNumber[i]) + '.mat')
        with h5py.File(path_simulationSignals, 'r') as simulationSignals:
            for n in range(len(list_Signals)):
                simulationSignal = np.array(simulationSignals[list_Signals[n]])
                simulationSignal = simulationSignal.flatten().tolist()
                simulationSignal.insert(0, list_Signals[n]+'_'+str(simNumber[i]))
                simulationSignal = [simulationSignal]
                temp_frame = pd.DataFrame(simulationSignal)
                temp_frame.set_index(0, inplace=True)
                simulationSignalsToPlot = simulationSignalsToPlot.append(temp_frame)
    return simulationSignalsToPlot

# def gettime_vectorMAT(path_sim, simNumber):
#
#     path_simulationSignals = os.path.join(path_sim + str(simNumber[0]) + '.mat')
#
#     with h5py.File(path_simulationSignals, 'r') as simulationSignals:
#         simulationSignal = np.array(simulationSignals['time_vector'])
#         simulationSignal = simulationSignal.flatten().T.tolist()
#         simulationSignal.insert(0, 'time_vector')
#         simulationSignal = [simulationSignal]
#         simulationSignalsToPlot = pd.DataFrame(simulationSignal)
#         simulationSignalsToPlot.set_index(0, inplace=True)
#     return simulationSignalsToPlot

# def writeTDMSToCsv(self, path_output: Path, dictionary: {}):
#     """
#         This function writes the signals of the signal_data dictionary of this class of a TDMS file to a specific csv file.
#         dictionary for header with names of the groups and signal that are used in the TDMS file
#         header: Groupname_signalname, ....
#     """
#     # Get signal
#     # signal_output = getspecificSignal(path_tdms, group_name, signal_name)
#     # np.savetxt(path_output, signal_output, delimiter=",")
#     # headers, units,...
#
#     header = []
#     for group in dictionary.keys():
#         for channel in dictionary[group]:
#             header.append(group + '_' + channel)
#
#     tdms_df = pd.DataFrame(self.signal_data)
#     tdms_df.to_csv(path_output, header=header, index=False)
