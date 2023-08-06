import os
import shutil
from pathlib import Path
import yaml

from steam_sdk.builders.BuilderPyBBQ import BuilderPyBBQ
from steam_sdk.data.DataModelConductor import DataModelConductor
from steam_sdk.data.DataModelMagnet import *
from steam_sdk.data.DataModelCircuit import DataModelCircuit
from steam_sdk.data.DataRoxieParser import APIdata
from steam_sdk.builders.BuilderLEDET import BuilderLEDET
from steam_sdk.builders.BuilderSIGMA import BuilderSIGMA
from steam_sdk.builders.BuilderProteCCT import BuilderProteCCT
from steam_sdk.parsers.ParserLEDET import ParserLEDET, copy_modified_map2d_ribbon_cable, copy_map2d
from steam_sdk.parsers.ParserPSPICE import ParserPSPICE
from steam_sdk.parsers.ParserProteCCT import ParserProteCCT
from steam_sdk.parsers.ParserProtePyBBQ import ParserPyBBQ
from steam_sdk.parsers.ParserRoxie import ParserRoxie
from steam_sdk.parsers.ParserMap2d import getParametersFromMap2d
from steam_sdk.parsers.dict_to_yaml import dict_to_yaml
from steam_sdk.plotters import PlotterRoxie
from steam_sdk.plotters.PlotterModel import PlotterModel


class BuilderModel:
    """
        Class to generate STEAM models, which can be later on written to input files of supported programs
    """

    def __init__(self,
                 file_model_data: str = None, software: List[str] = None, case_model: str = 'magnet',
                 relative_path_settings: str = '',
                 flag_build: bool = True, flag_dump_all: bool = False, flag_json: bool = False,
                 dump_all_path: str = '', output_path: str = '',
                 verbose: bool = False, flag_plot_all: bool = False):
        """
            Builder object to generate models from STEAM simulation tools specified by user

            output_path: path to the output models
            dump_all_path: path to the final yaml file
        """

        # Unpack arguments
        self.software: List[str] = software
        if not self.software: self.software = []  # This avoids error when None is passed to software # TODO: Verify this is sound coding
        valid_cases = ['magnet', 'circuit', 'conductor']
        if case_model in valid_cases:
            self.case_model = case_model
        else:
            raise ValueError('results: case_model must be one of {}.'.format(valid_cases))
        self.relative_path_settings: str = relative_path_settings
        self.file_model_data: str = file_model_data
        self.flag_build = flag_build
        self.flag_dump_all: bool = flag_dump_all
        self.flag_plot_all: bool = flag_plot_all
        self.flag_json: bool = flag_json
        self.dump_all_path: str = dump_all_path  # TODO Merge dump_all_path and output_path ?
        self.output_path: str = output_path
        self.verbose: bool = verbose

        if self.verbose:
            print('case_model: {}'.format(case_model))

        # If a model needs to be built, the output folder is not an empty string, and the folder does not exist, make it
        if flag_build and self.output_path != '' and not os.path.isdir(self.output_path):
            print("Output folder {} does not exist. Making it now".format(self.output_path))
            Path(self.output_path).mkdir(parents=True)

        ### Case of a magnet model
        if case_model == 'magnet':
            # Initialize
            self.model_data: DataModelMagnet = DataModelMagnet()
            self.roxie_data: APIdata = APIdata()
            self.path_magnet = None
            self.path_data = None
            self.path_cadata = None
            self.path_iron = None
            self.path_map2d = None
            self.path_settings = None

            # If flag_build set true, the model will be generated during the initialization
            if flag_build:
                if self.verbose:
                    print('output_path: {}'.format(self.output_path))

                # Load model data from the input .yaml file
                self.loadModelData(self.case_model)

                # Set paths of input files and settings
                self.set_input_paths(self.case_model)

                # Load model data from the input ROXIE files
                self.loadRoxieData()

                # Build model
                for s in self.software:
                    if s == 'LEDET':    self.buildLEDET(case_model=self.case_model)
                    if s == 'SIGMA':    self.buildSIGMA()
                    if s == 'ProteCCT': self.buildProteCCT()

                if flag_dump_all:
                    self.dumpAll()

                if flag_plot_all:
                    PlotterRoxie.plot_all(self.roxie_data)
                    PM = PlotterModel(self.roxie_data)
                    PM.plot_all(self.model_data)

        ### Case of a circuit model
        elif case_model == 'circuit':
            # Initialize
            self.circuit_data: DataModelCircuit = DataModelCircuit()
            self.path_settings = None

            # If flag_build set true, the model will be generated during the initialization
            if flag_build:
                if self.verbose:
                    print('output_path: {}'.format(self.output_path))

                # Load model data from the input .yaml file
                self.loadModelData(self.case_model)

                # Set paths of input files and settings
                self.set_input_paths(self.case_model)

                # Build circuit model
                for s in self.software:
                    if s == 'PSPICE': self.buildPSPICE()

        ### Case of a conductor model
        elif case_model == 'conductor':
            # Initialize
            self.conductor_data: DataModelConductor = DataModelConductor()
            self.path_settings = None

            # If flag_build set true, the model will be generated during the initialization
            if flag_build:
                if self.verbose:
                    print('output_path: {}'.format(self.output_path))

                # Load model data from the input .yaml file
                self.loadModelData(self.case_model)

                # Set paths of input files and settings
                self.set_input_paths(self.case_model)

                # Build model
                for s in self.software:
                    if s == 'LEDET':    self.buildLEDET(case_model=self.case_model)
                    if s == 'PyBBQ':    self.buildPyBBQ()


    def set_input_paths(self, case_model: str):
        """
            Sets input paths and displays related information
        """
        # TODO: Add test for this method

        # Find folder where the input file is located, which will be used as the "anchor" for all input files
        self.path_magnet = Path(self.file_model_data).parent

        if case_model == 'magnet':
            # Set a few paths relative to the "anchor" path
            # If input paths are not defined, their value remains to their default None
            # The construct Path(x / y).resolve() allows defining relative paths in the .yaml input file
            if self.model_data.Sources.coil_fromROXIE:
                self.path_data = Path(self.path_magnet / self.model_data.Sources.coil_fromROXIE).resolve()
            if self.model_data.Sources.magnetic_field_fromROXIE:
                self.path_map2d = Path(self.path_magnet / self.model_data.Sources.magnetic_field_fromROXIE).resolve()
            if self.model_data.Sources.conductor_fromROXIE:
                self.path_cadata = Path(self.path_magnet / self.model_data.Sources.conductor_fromROXIE).resolve()
            if self.model_data.Sources.iron_fromROXIE:
                self.path_iron = Path(self.path_magnet / self.model_data.Sources.iron_fromROXIE).resolve()
        elif case_model in ['circuit', 'conductor']:
            self.path_data   = None
            self.path_map2d  = None
            self.path_cadata = None
            self.path_iron   = None
        else:
            raise Exception ('case_model ({}) no supported'.format(case_model))

        # Set settings path
        # Find user name
        user_name = 'user'  # till GitLab path problem is solved
        for environ_var in ['HOMEPATH', 'SWAN_HOME']:
            if environ_var in os.environ:
                user_name = os.path.basename(os.path.normpath(os.environ[environ_var]))
        if self.verbose:
            print('user_name:   {}'.format(user_name))

        # TODO: Change this logic with a tree structure depending on the current location, not the file location
        if self.relative_path_settings == '':
            self.path_settings = Path(os.getcwd())
        else:
            self.path_settings = Path(os.getcwd() / self.relative_path_settings).resolve()

        if Path.exists(Path.joinpath(self.path_settings, f"settings.{user_name}.yaml")):
            with open(Path.joinpath(self.path_settings, f"settings.{user_name}.yaml"), 'r') as stream:
                self.settings_dict = yaml.safe_load(stream)
        else:
            with open(Path.joinpath(Path(os.getcwd()).parent, "settings.SYSTEM.yaml"), 'r') as stream:
                self.settings_dict = yaml.safe_load(stream)
            # raise Exception('Cannot find paths without settings file')

        # Display defined paths
        if self.verbose:
            print('These paths were set:')
            print('path_magnet:   {}'.format(self.path_magnet))
            print('path_cadata:   {}'.format(self.path_cadata))
            print('path_iron:     {}'.format(self.path_iron))
            print('path_map2d:    {}'.format(self.path_map2d))
            print('path_settings: {}'.format(self.path_settings))


    def loadModelData(self, case_model: str):
        """
            Loads model data from yaml file to model data object
        """
        if self.verbose:
            print('Loading .yaml file to model data object.')

        if not self.file_model_data:
            raise Exception('No .yaml path provided.')

        if case_model == 'magnet':
            # Load yaml keys into DataModelMagnet dataclass
            with open(self.file_model_data, "r") as stream:
                dictionary_yaml = yaml.safe_load(stream)
                self.model_data = DataModelMagnet(**dictionary_yaml)
        elif case_model == 'circuit':
            # Load yaml keys into DataModelCircuit dataclass
            with open(self.file_model_data, "r") as stream:
                dictionary_yaml = yaml.safe_load(stream)
                self.circuit_data = DataModelCircuit(**dictionary_yaml)
        elif case_model == 'conductor':
            # Load yaml keys into DataModelConductor dataclass
            with open(self.file_model_data, "r") as stream:
                dictionary_yaml = yaml.safe_load(stream)
                self.conductor_data = DataModelConductor(**dictionary_yaml)


    def loadRoxieData(self):
        """
            Apply roxie parser to fetch magnet information for the given magnet and stores in member variable
        """
        if not self.model_data:
            raise Exception('Model data not loaded to object.')

        # TODO: add option to set a default path if no path is provided
        #######################################
        # Alternative if provided path is wrong
        if self.path_iron is not None and not os.path.isfile(self.path_iron):
            print('Cannot find {}, will attempt to proceed without file'.format(self.path_iron))
            self.path_iron = None
        if self.path_data is not None and not os.path.isfile(self.path_data):
            print('Cannot find {}, will attempt to proceed without file'.format(self.path_data))
            self.path_data = None
        if self.path_cadata is not None and not os.path.isfile(self.path_cadata):
            print('Cannot find {}, will attempt to proceed without file'.format(self.path_cadata))
            self.path_cadata = None

        ############################################################
        # Load information from ROXIE input files using ROXIE parser
        roxie_parser = ParserRoxie()
        self.roxie_data = roxie_parser.getData(dir_data=self.path_data, dir_cadata=self.path_cadata, dir_iron=self.path_iron)

    def buildLEDET(self, case_model: str = 'magnet'):
        """
            Building a LEDET model
            case_model is a string defining the type of model to build (magnet or conductor)
        """

        if case_model == 'magnet':
            magnet_name = self.model_data.GeneralParameters.magnet_name
            nameFileSMIC = os.path.join(self.output_path, magnet_name + '_selfMutualInductanceMatrix.csv')  # full path of the .csv file with self-mutual inductances to write

            # Copy/edit the ROXIE map2d file
            suffix = "_All"
            if self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == 1:
                #     # [[...half_turn_length, Ribbon...n_strands],.....]
                # TODO: geometry when conductor has a combination of ribbon and non-ribbon cables

                # List of flags that are True is the cable type is "Ribbon"
                list_flag_ribbon = []
                for i, cond in enumerate(self.model_data.CoilWindings.conductor_to_group):
                    list_flag_ribbon.append(self.model_data.Conductors[cond-1].cable.type == 'Ribbon')

                nT_from_original_map2d, nStrands_inGroup_original_map2d, _, _, _, _, _, _ = getParametersFromMap2d(
                    map2dFile=self.path_map2d, headerLines=self.model_data.Options_LEDET.field_map_files.headerLines,
                    verbose=self.verbose)

                n_groups_original_file = len(nT_from_original_map2d)
                geometry_ribbon_cable = []

                for i in range(n_groups_original_file):
                    list = [None, None]
                    list[0] = int(nStrands_inGroup_original_map2d[i])  # layers
                    list[1] = nT_from_original_map2d[i]  # number of half-turns; in case it is not a ribbon cable, it is going to be ignored in the modify-ribbon-cable function
                    geometry_ribbon_cable.append(list)

                if self.verbose:
                    print('geometry_ribbon_cable: {}'.format(geometry_ribbon_cable))

                file_name_output = copy_modified_map2d_ribbon_cable(magnet_name,
                                                                    self.path_map2d,
                                                                    self.output_path, geometry_ribbon_cable,
                                                                    self.model_data.Options_LEDET.field_map_files.flagIron,
                                                                    self.model_data.Options_LEDET.field_map_files.flagSelfField,
                                                                    list_flag_ribbon,
                                                                    suffix=suffix, verbose=self.verbose)

            elif self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == 0 or self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == None:
                file_name_output = copy_map2d(magnet_name, self.path_map2d,
                                              self.output_path, self.model_data.Options_LEDET.field_map_files.flagIron,
                                              self.model_data.Options_LEDET.field_map_files.flagSelfField, suffix=suffix,
                                              verbose=self.verbose)

            self.map2d_file_modified = os.path.join(self.output_path, file_name_output)

            # Copy the additional geometry and magnetic field csv file, if defined in the input file
            if self.model_data.Options_LEDET.simulation_3D.sim3D_flag_Import3DGeometry == 1:
                name_geometry_csv_file = magnet_name + '_' + str(self.conductor_data.Options_LEDET.simulation_3D.sim3D_import3DGeometry_modelNumber) + '.csv'
                input_path_full  = os.path.join(self.path_magnet, name_geometry_csv_file)
                output_path_full = os.path.join(self.output_path, name_geometry_csv_file)
                shutil.copy2(input_path_full, output_path_full)
                if self.verbose:
                    print('File {} copied to {}.'.format(input_path_full, output_path_full))

            builder_ledet = BuilderLEDET(path_magnet=self.path_magnet, input_model_data=self.model_data,
                                         input_roxie_data=self.roxie_data, input_map2d=self.map2d_file_modified,
                                         smic_write_path=nameFileSMIC, flag_build=self.flag_build, flag_plot_all=self.flag_plot_all,
                                         verbose=self.verbose,
                                         case_model=case_model)

            # Copy or modify+copy magnet-name_E....map2d files
            number_input_files = len([entry for entry in os.listdir(self.path_magnet) if os.path.isfile(os.path.join(self.path_magnet, entry))])
            for file in range(number_input_files+1):
                suffix = '_E{}'.format(file)
                path_map2d_E = os.path.join(self.path_magnet, magnet_name + suffix + '.map2d')
                if os.path.isfile(path_map2d_E):
                    if self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == 1:
                        copy_modified_map2d_ribbon_cable(magnet_name,
                                                         path_map2d_E,
                                                         self.output_path, geometry_ribbon_cable,
                                                         self.model_data.Options_LEDET.field_map_files.flagIron,
                                                         self.model_data.Options_LEDET.field_map_files.flagSelfField,
                                                         list_flag_ribbon,
                                                         suffix=suffix, verbose=self.verbose)
                    elif self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == 0 or self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == None:
                        copy_map2d(magnet_name, path_map2d_E, self.output_path, self.model_data.Options_LEDET.field_map_files.flagIron,
                                              self.model_data.Options_LEDET.field_map_files.flagSelfField, suffix=suffix,
                                              verbose=self.verbose)

            # Write output excel file
            parser_ledet = ParserLEDET(builder_ledet)
            nameFileLEDET = os.path.join(self.output_path, magnet_name + '.xlsx')  # full path of the LEDET input file to write
            parser_ledet.writeLedet2Excel(full_path_file_name=nameFileLEDET, verbose=self.verbose, SkipConsistencyCheck=True)

            # Write output yaml file
            nameFileLedetYaml = os.path.join(self.output_path, magnet_name + '.yaml')  # full path of the LEDET input file to write
            parser_ledet.write2yaml(full_path_file_name=nameFileLedetYaml, verbose=self.verbose, SkipConsistencyCheck=True)

            # Write output json file
            if self.flag_json:
                nameFileLedetJson = os.path.join(self.output_path, magnet_name + '.json')  # full path of the LEDET input file to write
                parser_ledet.write2json(full_path_file_name=nameFileLedetJson, verbose=self.verbose, SkipConsistencyCheck=True)

        elif case_model == 'conductor':
            conductor_name = self.conductor_data.GeneralParameters.conductor_name

            # Copy the ROXIE map2d file, if defined in the input file
            if self.path_map2d:
                suffix = "_All"
                file_name_output = copy_map2d(conductor_name,
                                              self.path_map2d,
                                              self.output_path,
                                              self.conductor_data.Options_LEDET.field_map_files.flagIron,
                                              self.conductor_data.Options_LEDET.field_map_files.flagSelfField,
                                              suffix=suffix,
                                              verbose=self.verbose)
                self.map2d_file_modified = os.path.join(self.output_path, file_name_output)
            else:
                self.map2d_file_modified = None
                if self.verbose:
                    print('Map2d file {} not present, hence it will not be copied.'.format(self.path_map2d))

            # Copy the additional geometry and magnetic field csv file, if defined in the input file
            if self.conductor_data.Options_LEDET.simulation_3D.sim3D_flag_Import3DGeometry == 1:
                name_geometry_csv_file = conductor_name + '_' + str(self.conductor_data.Options_LEDET.simulation_3D.sim3D_import3DGeometry_modelNumber) + '.csv'
                input_path_full  = os.path.join(self.path_magnet, name_geometry_csv_file)
                output_path_full = os.path.join(self.output_path, name_geometry_csv_file)
                shutil.copy2(input_path_full, output_path_full)
                if self.verbose:
                    print('File {} copied to {}.'.format(input_path_full, output_path_full))

            builder_ledet = BuilderLEDET(path_magnet=self.path_magnet, input_model_data=self.conductor_data,
                                         input_map2d=self.map2d_file_modified,
                                         flag_build=self.flag_build, flag_plot_all=self.flag_plot_all,
                                         verbose=self.verbose,
                                         case_model=case_model)

            # Write output excel file
            parser_ledet = ParserLEDET(builder_ledet)
            nameFileLEDET = os.path.join(self.output_path, conductor_name + '.xlsx')  # full path of the LEDET input file to write
            parser_ledet.writeLedet2Excel(full_path_file_name=nameFileLEDET, verbose=self.verbose, SkipConsistencyCheck=True)

            # Write output yaml file
            nameFileLedetYaml = os.path.join(self.output_path, conductor_name + '.yaml')  # full path of the LEDET input file to write
            parser_ledet.write2yaml(full_path_file_name=nameFileLedetYaml, verbose=self.verbose, SkipConsistencyCheck=True)

            # Write output json file
            if self.flag_json:
                nameFileLedetJson = os.path.join(self.output_path, conductor_name + '.json')  # full path of the LEDET input file to write
                parser_ledet.write2json(full_path_file_name=nameFileLedetJson, verbose=self.verbose, SkipConsistencyCheck=True)

        else:
            raise Exception('Case model {} is not supported when building a LEDET model.'.format(case_model))

    def buildProteCCT(self):
        """
            Building a ProteCCT model
        """
        magnet_name = self.model_data.GeneralParameters.magnet_name
        builder_protecct = BuilderProteCCT(input_model_data=self.model_data, flag_build=self.flag_build, verbose=self.verbose)

        # Write output excel file
        parser_protecct = ParserProteCCT(builder_protecct)
        nameFileProteCCT = os.path.join(self.output_path, magnet_name + '.xlsx')  # full path of the ProteCCT input file to write
        parser_protecct.writeProtecct2Excel(full_path_file_name=nameFileProteCCT, verbose=self.verbose, SkipConsistencyCheck=True)


    def buildSIGMA(self):
        """
            Building a SIGMA model
        """
        BuilderSIGMA(input_model_data=self.model_data, input_roxie_data=self.roxie_data,
                     settings_dict=self.settings_dict, output_path=self.output_path,
                     flag_build=self.flag_build, verbose=self.verbose)

    def buildPSPICE(self):
        """
            Build a PSPICE circuit netlist model
        """
        circuit_data = self.circuit_data
        circuit_name = self.circuit_data.GeneralParameters.circuit_name

        # Write output .cir file
        parser_pspice = ParserPSPICE(circuit_data=circuit_data, path_input=self.path_magnet, output_path=self.output_path)
        nameFilePSPICE = os.path.join(self.output_path, circuit_name + '.cir')  # full path of the PSPICE netlist to write
        parser_pspice.write2pspice(full_path_file_name=nameFilePSPICE, verbose=self.verbose)

        # Copy additional files
        parser_pspice.copy_additional_files()

    def buildPyBBQ(self):
        """
            Building a PyBBQ model
        """
        conductor_name = self.conductor_data.GeneralParameters.conductor_name
        builder_PyBBQ = BuilderPyBBQ(input_model_data=self.conductor_data, flag_build=self.flag_build, verbose=self.verbose)

        # Write output yaml file
        parser_PyBBQ = ParserPyBBQ(builder_PyBBQ)
        nameFilePyBBQ = os.path.join(self.output_path, conductor_name + '.yaml')  # full path of the PyBBQ input file to write
        parser_PyBBQ.writePyBBQ2yaml(full_path_file_name=nameFilePyBBQ, verbose=self.verbose)

    def dumpAll(self):
        """
            Writes model data and data from Roxie parser in a combined .yaml file
        """
        # TODO add one more layer for model_data and roxie_data
        if self.verbose:
            print('Writing model data and data from Roxie parser in a combined .yaml file')
        # TODO: add also data from BuilderLEDET, BulderSIGMA, etc

        all_data_dict = {**self.model_data.dict(), **self.roxie_data.dict()}

        # Define output folder
        if self.dump_all_path != '':
            dump_all_path = self.dump_all_path
        elif self.output_path != '':
            dump_all_path = self.output_path
        else:
            dump_all_path = ''

        # If the output folder is not an empty string, and it does not exist, make it
        if self.dump_all_path != '' and not os.path.isdir(self.dump_all_path):
            print("Output folder {} does not exist. Making it now".format(self.dump_all_path))
            Path(self.dump_all_path).mkdir(parents=True)

        # Write output .yaml file
        dump_all_full_path = os.path.join(dump_all_path, self.model_data.GeneralParameters.magnet_name + '_all_data.yaml')
        # with open(dump_all_full_path, 'w') as outfile:
        #     yaml.dump(all_data_dict, outfile, default_flow_style=False, sort_keys=False)
        dict_to_yaml(all_data_dict, dump_all_full_path, list_exceptions=['Conductors'])


