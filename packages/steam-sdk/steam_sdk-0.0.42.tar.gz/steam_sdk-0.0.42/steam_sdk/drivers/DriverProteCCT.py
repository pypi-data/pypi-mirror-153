import os
import subprocess
from pathlib import Path


class DriverProteCCT:
    '''
        Class to drive ProteCCT models
    '''

    def __init__(self, path_exe=None, path_folder_ProteCCT=None, verbose=False):
        # Unpack arguments
        self.path_exe          = path_exe
        self.path_folder_ProteCCT = path_folder_ProteCCT
        self.verbose           = verbose
        if verbose:
            print('path_exe =          {}'.format(path_exe))
            print('path_folder_ProteCCT = {}'.format(path_folder_ProteCCT))

    def run_ProteCCT(self, simFileName: str, inputDirectory: str = 'input', outputDirectory: str = 'output'):
        '''
        ** Run ProteCCT model **
        :param simFileName: Name of the simulation file to run
        :param outputDirectory: Relative path of the input directory with respect to path_folder_ProteCCT
        :param outputDirectory: Relative path of the output directory with respect to path_folder_ProteCCT
        :return:
        '''
        # Unpack arguments
        path_exe = self.path_exe
        path_folder_ProteCCT = self.path_folder_ProteCCT
        verbose = self.verbose

        full_path_input  = os.path.join(path_folder_ProteCCT, inputDirectory, simFileName + '.xlsx')
        full_path_output = os.path.join(path_folder_ProteCCT, outputDirectory)

        if not os.path.isdir(full_path_output):
            print("Output folder {} does not exist. Making it now".format(full_path_output))
            Path(full_path_output).mkdir(parents=True)

        if verbose:
            print('path_exe =             {}'.format(path_exe))
            print('path_folder_ProteCCT = {}'.format(path_folder_ProteCCT))
            print('simFileName =          {}'.format(simFileName))
            print('inputDirectory =       {}'.format(inputDirectory))
            print('outputDirectory =      {}'.format(outputDirectory))
            print('full_path_input =      {}'.format(full_path_input))
            print('full_path_output =     {}'.format(full_path_output))
        # Run model
        return subprocess.call([path_exe, full_path_input, full_path_output])
