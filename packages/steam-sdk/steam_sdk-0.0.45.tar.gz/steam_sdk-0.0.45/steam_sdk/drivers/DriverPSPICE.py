import os
import subprocess
from pathlib import Path


class DriverPSPICE:
    '''
        Class to drive PSPICE netlist models
    '''

    def __init__(self, path_exe=None, path_folder_PSPICE=None, verbose=False):
        # Unpack arguments
        self.path_exe          = path_exe
        self.path_folder_PSPICE = path_folder_PSPICE
        self.verbose           = verbose
        if verbose:
            print('path_exe:            {}'.format(path_exe))
            print('path_folder_PSPICE:  {}'.format(path_folder_PSPICE))

    def run_PSPICE(self, nameCircuit: str, suffix: str = ''):
        '''
        ** Run PSPICE model **
        :param nameCircuit: Name of the magnet model to run
        :param suffix: Number of the simulation to run
        :return:
        '''
        # Unpack arguments
        path_exe = self.path_exe
        path_folder_PSPICE = self.path_folder_PSPICE
        verbose = self.verbose

        full_name_file = os.path.join(path_folder_PSPICE, nameCircuit + suffix + '.cir')

        if verbose:
            print('path_exe:            {}'.format(path_exe))
            print('path_folder_PSPICE:  {}'.format(path_folder_PSPICE))
            print('nameCircuit:         {}'.format(nameCircuit))
            print('suffix:              {}'.format(suffix))
            print('full_name_file:      {}'.format(full_name_file))
            print('Absolute full_name_file: {}'.format(Path(full_name_file).resolve()))



        # Run model
        self.output = subprocess.call([path_exe, full_name_file])
        if verbose:
            print('Subprocess finished returning: \n{}'.format(self.output))



