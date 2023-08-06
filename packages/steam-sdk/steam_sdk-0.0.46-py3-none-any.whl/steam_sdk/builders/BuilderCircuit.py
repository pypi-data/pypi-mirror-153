from pathlib import Path

from steam_sdk.data import DataModelCircuit


class BuilderCircuit:
    """
        Class to generate circuit netlist models
    """

    def __init__(self,
                 path_parent: Path = None,
                 circuit_data: DataModelCircuit = None,
                 flag_build: bool = True,
                 verbose: bool = False):
        """
            # TODO: documentation
        """
        
        # Unpack arguments
        self.path_parent: Path = path_parent  # This variable might be useful in the future to access other input files located in the parent folder
        self.circuit_data: DataModelCircuit = circuit_data
        self.flag_build: bool = flag_build
        self.verbose: bool = verbose

        if (not self.circuit_data) and flag_build:
            raise Exception('Cannot build model instantly without providing circuit_data input file.')

        if flag_build:
            # Assemble netlist
            self.print_netlist_entries()


    def print_netlist_entries(self):
        for component in self.circuit_data.Netlist:
            if self.verbose:
                print(component)
        pass