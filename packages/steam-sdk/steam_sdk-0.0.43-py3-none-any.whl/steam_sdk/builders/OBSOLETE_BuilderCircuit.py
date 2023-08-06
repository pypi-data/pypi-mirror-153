# CLASS DECLARED OBSOLETE - WILL BE DELETED FROM STEAM_SDK SOON
#
# import os
# from pathlib import Path
# import ntpath
# import shutil
#
# from steam_sdk.data import DataModelCircuit
#
#
# class BuilderCircuit:
#     """
#         Class to generate circuit netlist models
#     """
#
#     def __init__(self,
#                  # path_parent: Path = None,
#                  circuit_data: DataModelCircuit = None,
#                  output_path: str = '',
#                  flag_build: bool = True,
#                  verbose: bool = False):
#         """
#             # TODO: documentation
#         """
#
#         # Unpack arguments
#         # self.path_parent: Path = path_parent  # This variable might be useful in the future to access other input files located in the parent folder
#         self.circuit_data: DataModelCircuit = circuit_data
#         self.output_path: str = output_path
#         self.flag_build: bool = flag_build
#         self.verbose: bool = verbose
#
#         if (not self.circuit_data) and flag_build:
#             raise Exception('Cannot build model instantly without providing circuit_data input file.')
#
#         if flag_build:
#             # Print netlist
#             if self.verbose:
#                 self.print_netlist_entries()
#
#             # Copy additional files
#             self.copy_additional_files()
#
#
#
#     def print_netlist_entries(self):
#         '''
#             Print the netlist entries defined in the input file
#         '''
#         print('Netlist entries defined in the input file:')
#         for component in self.circuit_data.Netlist:
#             print(component)
#
#     def copy_additional_files(self):
#         for file_to_copy in self.circuit_data.GeneralParameters.additional_files:
#             file_name = ntpath.basename(file_to_copy)
#             file_to_write = os.path.join(self.output_path, file_name)
#             shutil.copyfile(file_to_copy, file_to_write)
#             if self.verbose:
#                 print('Additional file copied from {} to {}.'.format(file_to_copy, file_to_write))