import os
import re
import shutil
from copy import deepcopy
from pathlib import Path
import yaml

from steam_sdk.data.DataSettings import DataSettingsSTEAM
from steam_sdk.builders.BuilderModel import BuilderModel
from steam_sdk.data.DataAnalysis import DataAnalysis, AnalysisStep
from steam_sdk.drivers.DriverLEDET import DriverLEDET
from steam_sdk.drivers.DriverPSPICE import DriverPSPICE
from steam_sdk.drivers.DriverPyBBQ import DriverPyBBQ
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing
from steam_sdk.utils.rgetattr import rgetattr
from steam_sdk.utils.sgetattr import rsetattr


class AnalysisSTEAM:
    """
        Class to run analysis based on STEAM_SDK
    """

    def __init__(self, file_name_analysis: str = None,
                 relative_path_settings: str = '',
                 verbose: bool = False):
        """
            Analysis based on STEAM_SDK
        """

        # Initialize
        self.file_name_analysis = file_name_analysis
        self.relative_path_settings = Path(relative_path_settings).resolve()
        self.verbose = verbose
        self.data_analysis = None  # object containing the information read from the analysis input file
        self.settings      = DataSettingsSTEAM()  # object containing the settings acquired during initialization
        self.library_path  = None
        self.output_path   = None
        self.temp_path     = None
        self.list_models   = {}  # this dictionary will be populated with BuilderModel objects and their names
        self.list_sims     = []  # this list will be populated with integers indicating simulations to run

        # Check that input file is provided
        if not self.file_name_analysis:
            raise Exception('No .yaml input file provided.')

        # Load yaml keys into DataAnalysis dataclass
        with open(self.file_name_analysis, "r") as stream:
            dictionary_yaml = yaml.safe_load(stream)
            self.data_analysis = DataAnalysis(**dictionary_yaml)

        # Read working folders and set them up
        self.set_up_working_folders()

        # Read analysis settings
        self.read_settings()


    def setAttribute(self, dataclassSTEAM, attribute: str, value):
        try:
            setattr(dataclassSTEAM, attribute, value)
        except:
            setattr(getattr(self, dataclassSTEAM), attribute, value)


    def getAttribute(self, dataclassSTEAM, attribute):
        try:
            return getattr(dataclassSTEAM, attribute)
        except:
            return getattr(getattr(self, dataclassSTEAM), attribute)

    def set_up_working_folders(self):
        """
            ** Read working folders and set them up **
            This method performs the following tasks:
             - Check all folder paths are defined. If not, raise an exception.
             - Check if model library folder is present. If not, raise an exception.
             - Check if output folder is present. If not, make it.
             - Check if temporary folder is present. If so, delete it.

        """

        # Unpack inputs
        verbose = self.verbose
        library_path = self.data_analysis.WorkingFolders.library_path
        output_path = self.data_analysis.WorkingFolders.output_path
        temp_path = self.data_analysis.WorkingFolders.temp_path

        # Raise exceptions if folders are not defined.
        if not library_path:
            raise Exception('Model library path must be defined. Key to provide: WorkingFolders.library_path')
        if not output_path:
            raise Exception('Output folder path must be defined. Key to provide: WorkingFolders.output_path')
        if not temp_path:
            raise Exception('Temporary folder path must be defined. Key to provide: WorkingFolders.temp_path')

        # Resolve all paths and re-assign them to the self variables
        self.library_path = Path(self.data_analysis.WorkingFolders.library_path).resolve()
        self.output_path = Path(self.data_analysis.WorkingFolders.output_path).resolve()
        self.temp_path = Path(self.data_analysis.WorkingFolders.temp_path).resolve()
        library_path = self.library_path
        output_path = self.output_path
        temp_path = self.temp_path

        if verbose:
            print('Model library path:    {}'.format(library_path))
            print('Output folder path:    {}'.format(output_path))
            print('Temporary folder path: {}'.format(temp_path))

        # Check if model library folder is present. If not, raise an exception.
        if not os.path.isdir(library_path):
            raise Exception(
                'Model library path refers to a not-existing folder: {}. Key to change: WorkingFolders.library_path'.format(
                    library_path))

        # Check if output folder is present. If not, make it.
        if not os.path.isdir(output_path):
            Path(output_path).mkdir(parents=True, exist_ok=True)
            print('Folder {} did not exist. It was made now.'.format(output_path))

        # Check if temporary folder is present. If so, delete it.
        if os.path.isdir(temp_path):
            shutil.rmtree(temp_path)
            print('Folder {} already existed. It was removed.'.format(temp_path))


    def read_settings(self):
        """
            ** Read analysis settings **

            They will be read either form a local settings file (if flag_permanent_settings=False)
            or from the keys in the input analysis file (if flag_permanent_settings=True)
        """

        verbose = self.verbose

        if self.data_analysis.GeneralParameters.flag_permanent_settings:
            # Read settings from analysis input file (yaml file)
            if verbose:
                print('flag_permanent_settings is set to True')
            dictonary_settings = self.data_analysis.PermanentSettings.__dict__
        else:
            # Read settings from local settings file (yaml file)
            user_name = os.getlogin()
            full_path_file_settings = os.path.join(self.relative_path_settings, f"settings.{user_name}.yaml")
            if verbose:
                print('flag_permanent_settings is set to False')
                print('user_name:               {}'.format(user_name))
                print('relative_path_settings:  {}'.format(self.relative_path_settings))
                print('full_path_file_settings: {}'.format(full_path_file_settings))
            if not os.path.isfile(full_path_file_settings):
                raise Exception('Local setting file {} not found. This file must be provided when flag_permanent_settings is set to False.'.format(full_path_file_settings))
            with open(full_path_file_settings, 'r') as stream:
                dictonary_settings = yaml.safe_load(stream)

        # Assign the keys read either from permanent-settings or local-settings
        for name, _ in self.settings.__dict__.items():
            if name in dictonary_settings:
                value = dictonary_settings[name]
                self.setAttribute(self.settings, name, value)
                if verbose: print('{} : {}. Added.'.format(name, value))
            else:
                if verbose: print('{}: not found in the settings. Skipped.'.format(name))

        # Dump read keys to temporary settings file locally
        user_name = os.getlogin()
        name_file_settings = f"settings.{user_name}.yaml"
        path_temp_file_settings = Path(os.path.join('', name_file_settings)).resolve()
        with open(path_temp_file_settings, 'w') as yaml_file:
            yaml.dump(dictonary_settings, yaml_file, default_flow_style=False, sort_keys=False)
        if verbose: print('File {} was saved locally.'.format(path_temp_file_settings))


    def run_analysis(self, verbose: bool = None):
        """
            ** Run the analysis **
        """

        # Unpack and assign default values
        step_definitions = self.data_analysis.AnalysisStepDefinition
        if not verbose:
            verbose = self.verbose

        # Print the selected analysis steps
        if verbose:
            print('Defined analysis steps (not in sequential order):')
            for def_step in step_definitions:
                step = def_step.step
                print('{}'.format(step.step_name))

        # Print analysis sequence
        if verbose: print('Defined sequence of analysis steps:')
        for s, seq_step in enumerate(self.data_analysis.AnalysisStepSequence):
            if verbose: print('Step {}/{}: {}'.format(s+1, len(self.data_analysis.AnalysisStepSequence), seq_step))

        # Run analysis (and re-print analysis steps)
        if verbose: print('Analysis started.')
        for s, seq_step in enumerate(self.data_analysis.AnalysisStepSequence):
            if verbose: print('Step {}/{}: {}'.format(s + 1, len(self.data_analysis.AnalysisStepSequence), seq_step))
            current_step = (i for i, v in enumerate(step_definitions) if step_definitions[i].step.step_name == seq_step)
            current_step = next(current_step, None)
            # if verbose: print('Index of current step: {}'.format(current_step))

            step = step_definitions[current_step].step  # this is the object containing the information about the current step
            if step.type == 'MakeModel':
                self.step_make_model(step, verbose=verbose)
            elif step.type == 'ModifyModel':
                self.step_modify_model(step, verbose=verbose)
            elif step.type == 'ModifyModelMultipleVariables':
                self.step_modify_model_multiple_variables(step, verbose=verbose)
            elif step.type == 'RunSimulation':
                self.step_run_simulation(step, verbose=verbose)
            elif step.type == 'PostProcess':
                self.step_postprocess(step, verbose=verbose)
            elif step.type == 'SetUpFolder':
                self.step_setup_folder(step, verbose=verbose)
            else:
                raise Exception('Unknown type of analysis step: {}'.format(step.type))


    def step_make_model(self, step, verbose: bool = False):
        if verbose:
            print('Making model object named {}'.format(str(step.model_name)))

        file_model_data = os.path.join(self.library_path, step.case_model + 's', step.file_model_data, 'input', 'modelData_' + step.file_model_data + '.yaml')
        case_model      = step.case_model
        software        = step.software  # remember this is a list, not a string
        verbose_of_step = step.verbose
        flag_build      = step.flag_build
        flag_dump_all   = step.flag_dump_all
        flag_plot_all   = step.flag_plot_all
        flag_json       = step.flag_json
        output_folder   = self.output_path
        relative_path_settings = ''

        # Build the model
        BM = BuilderModel(file_model_data=file_model_data, case_model=case_model, software=software,
                          verbose=verbose_of_step, flag_build=flag_build,
                          flag_dump_all=flag_dump_all, flag_plot_all=flag_plot_all, flag_json=flag_json,
                          output_path=output_folder, relative_path_settings=relative_path_settings)

        # Build simulation file
        if step.simulation_number:
            if 'LEDET' in step.software:
                flag_yaml = True  # Hard-coded for the moment
                self.setup_sim_LEDET(simulation_name=step.simulation_name, sim_number=step.simulation_number, flag_yaml=flag_yaml, flag_json=flag_json)
            if 'PyBBQ' in step.software:
                self.setup_sim_PyBBQ(simulation_name=step.simulation_name, sim_number=step.simulation_number)
            if 'PSPICE' in step.software:
                self.setup_sim_PSPICE(simulation_name=step.simulation_name, sim_number=step.simulation_number)

        # Add the reference to the model in the dictionary
        self.list_models[step.model_name] = BM


    def step_modify_model(self, step, verbose: bool = False):
        if verbose:
            print('Modifying model object named {}'.format(str(step.model_name)))

        # Check inputs
        if step.model_name not in self.list_models:
            raise Exception('Name of the model to modify ({}) does not correspond to any of the defined models.'.format(step.model_name))
        len_variable_value = len(step.variable_value)
        len_simulation_numbers  = len(step.simulation_numbers)
        len_new_model_name = len(step.new_model_name)
        if len_new_model_name > 0 and not len_new_model_name == len_variable_value:
            raise Exception('The length of new_model_name and variable_value must be the same, but they are {} and {} instead.'.format(len_new_model_name, len_variable_value))
        if len_simulation_numbers > 0 and not len_simulation_numbers == len_variable_value:
            raise Exception('The length of simulation_numbers and variable_value must be the same, but they are {} and {} instead.'.format(len_simulation_numbers, len_variable_value))

        # Change the value of the selected variable
        for v, value in enumerate(step.variable_value):
            BM = self.list_models[step.model_name]  # original BuilderModel object
            case_model = BM.case_model  # model case (magnet, conductor, circuit)

            if 'Conductors[' in step.variable_to_change:  # Special case when the variable to change is the Conductors key
                if verbose:
                    idx_conductor = int(step.variable_to_change.split('Conductors[')[1].split(']')[0])
                    conductor_variable_to_change = step.variable_to_change.split('].')[1]
                    print('Variable {} is treated as a Conductors key. Conductor index: #{}. Conductor variable to change: {}.'.format(step.variable_to_change, idx_conductor, conductor_variable_to_change))

                    old_value = self.get_attribute_model(case_model, BM, conductor_variable_to_change, idx_conductor)
                    print('Variable {} changed from {} to {}.'.format(conductor_variable_to_change, old_value, value))

                if len_new_model_name > 0:  # Make a new copy of the BuilderModel object, and change it
                    self.list_models[step.new_model_name[v]] = deepcopy(BM)
                    BM = self.list_models[step.new_model_name[v]]
                    rsetattr(BM.model_data.Conductors[idx_conductor], conductor_variable_to_change, value)
                    if verbose:
                        print('Model {} copied to model {}.'.format(step.model_name, step.new_model_name[v]))

                else:  # Change the original BuilderModel object
                    rsetattr(BM.model_data.Conductors[idx_conductor], conductor_variable_to_change, value)

            else:  # Standard case when the variable to change is not the Conductors key
                if verbose:
                    old_value = self.get_attribute_model(case_model, BM, step.variable_to_change)
                    print('Variable {} changed from {} to {}.'.format(step.variable_to_change, old_value, value))

                if len_new_model_name > 0:  # Make a new copy of the BuilderModel object, and change it
                    self.list_models[step.new_model_name[v]] = deepcopy(BM)
                    BM = self.list_models[step.new_model_name[v]]
                    self.set_attribute_model(case_model, BM, step.variable_to_change, value)
                    if verbose:
                        print('Model {} copied to model {}.'.format(step.model_name, step.new_model_name[v]))

                else:  # Change the original BuilderModel object
                    self.set_attribute_model(case_model, BM, step.variable_to_change, value)

            # Build simulation file
            if len_simulation_numbers > 0:
                simulation_number = step.simulation_numbers[v]
                if 'LEDET' in step.software:
                    flag_json = BM.flag_json
                    BM.buildLEDET(case_model=case_model)
                    self.setup_sim_LEDET(simulation_name=step.simulation_name, sim_number=simulation_number, flag_json=flag_json)
                if 'PyBBQ' in step.software:
                    BM.buildPyBBQ()
                    self.setup_sim_PyBBQ(simulation_name=step.simulation_name, sim_number=simulation_number)
                if 'PSPICE' in step.software:
                    BM.buildPSPICE()
                    self.setup_sim_PSPICE(simulation_name=step.simulation_name, sim_number=simulation_number)

    def get_attribute_model(self, case_model: str, builder_model: BuilderModel, name_variable: str, idx_conductor: int = None):
        '''
        Helper function used to get an attribute from a key of the model data.
        Depending on the model type (circuit, magnet, conductor), the data structure to access is different.
        Also, there is a special case when the variable to read is a sub-key of the Conductors key. In such a case, an additional parameter idx_conductor must be defined (see below).
        :param case_model: Model type
        :param builder_model: BuilderModel object to access
        :param name_variable: Name of the variable to read
        :param idx_conductor: When defined, a sub-key form the Conductors key is read. The index of the conductor to read is defined by idx_conductor
        :return: Value of the variable to get
        '''

        if case_model == 'magnet':
            if idx_conductor is None:  # Standard case when the variable to change is not the Conductors key
                value = rgetattr(builder_model.model_data, name_variable)
            else:
                value = rgetattr(builder_model.model_data.Conductors[idx_conductor], name_variable)
        elif case_model == 'conductor':
            if idx_conductor is None:  # Standard case when the variable to change is not the Conductors key
                value = rgetattr(builder_model.conductor_data, name_variable)
            else:
                value = rgetattr(builder_model.conductor_data.Conductors[idx_conductor], name_variable)
        elif case_model == 'circuit':
            value = rgetattr(builder_model.circuit_data, name_variable)
        else:
            raise Exception(f'Model type not supported: case_model={case_model}')
        return value

    def set_attribute_model(self, case_model: str, builder_model: BuilderModel, name_variable: str, value_variable: float, idx_conductor: int = None):
        '''
        Helper function used to set a key of the model data to a certaub value.
        Depending on the model type (circuit, magnet, conductor), the data structure to access is different.
        Also, there is a special case when the variable to change is a sub-key of the Conductors key. In such a case, an additional parameter idx_conductor must be defined (see below).
        :param case_model: Model type
        :param builder_model: BuilderModel object to access
        :param name_variable: Name of the variable to change
        :param value_variable: New value of the variable of the variable
        :param idx_conductor: When defined, a sub-key form the Conductors key is read. The index of the conductor to read is defined by idx_conductor
        :return: Value of the variable to get
        '''

        if case_model == 'magnet':
            if idx_conductor is None:  # Standard case when the variable to change is not the Conductors key
                rsetattr(builder_model.model_data, name_variable, value_variable)
            else:
                rsetattr(builder_model.model_data.Conductors[idx_conductor], name_variable, value_variable)
        elif case_model == 'conductor':
            if idx_conductor is None:  # Standard case when the variable to change is not the Conductors key
                rsetattr(builder_model.conductor_data, name_variable, value_variable)
            else:
                rsetattr(builder_model.conductor_data.Conductors[idx_conductor], name_variable, value_variable)
        elif case_model == 'circuit':
            rsetattr(builder_model.circuit_data, name_variable, value_variable)
        else:
            raise Exception(f'Model type not supported: case_model={case_model}')


    def step_modify_model_multiple_variables(self, step, verbose: bool = False):
        if verbose:
            print('Modifying model object named {}'.format(str(step.model_name)))

        # Check inputs
        if step.model_name not in self.list_models:
            raise Exception('Name of the model to modify ({}) does not correspond to any of the defined models.'.format(step.model_name))
        len_variables_to_change = len(step.variables_to_change)
        len_variables_value     = len(step.variables_value)
        if not len_variables_to_change == len_variables_value:
            raise Exception('The length of variables_to_change and variables_value must be the same, but they are {} and {} instead.'.format(len_variables_to_change, len_variables_value))

        # Loop through the list of variables to change
        for v, variable_to_change in enumerate(step.variables_to_change):
            # For each variable to change, make an instance of AnalysisStep and call the step_modify_model() method
            next_step = AnalysisStep(step={'type': 'ModifyModel'}).step
            next_step.model_name = step.model_name
            next_step.variable_to_change = variable_to_change
            next_step.variable_value = step.variables_value[v]
            if v+1 == len_variables_to_change:  # If this is the last variable to change, import new_model_name and simulation_numbers from the step
                next_step.new_model_name = step.new_model_name
                next_step.simulation_numbers = step.simulation_numbers
            else:  # else, set new_model_name and simulation_numbers to empty lists to avoid making models/simulations for intermediate changes
                next_step.new_model_name = []
                next_step.simulation_numbers = []
            next_step.simulation_name = step.simulation_name
            next_step.software = step.software
            self.step_modify_model(next_step, verbose=verbose)
        if verbose:
            print('All variables of step {} were changed.'.format(step.step_name))


    def step_run_simulation(self, step, verbose: bool = False):
        software = step.software
        simulation_name = step.simulation_name
        simFileType = step.simFileType
        for sim_number in step.simulation_numbers:
            if verbose:
                print('Running simulation of model {} #{} using {}.'.format(simulation_name, sim_number, software))
            # Run simulation
            self.run_sim(software, simulation_name, sim_number, simFileType, verbose)


    def step_postprocess(self, step, verbose: bool = False):
        if verbose: print('postprocessing')
        pass


    def step_setup_folder(self, step, verbose: bool = False):
        '''
        Set up simulation working folder.
        The function applies a different logic for each simulation software.
        '''
        list_software = step.software
        simulation_name = step.simulation_name

        for software in list_software:
            if verbose:
                print('Set up folder of model {} for {}.'.format(simulation_name, software))

            if 'LEDET' in software:
                local_LEDET_folder = Path(self.settings.local_LEDET_folder)
                # Make magnet input folder and its subfolders
                make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input').resolve(), verbose=verbose)
                make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input' / 'Control current input').resolve(), verbose=verbose)
                make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input' / 'Initialize variables').resolve(), verbose=verbose)
                make_folder_if_not_existing(Path(local_LEDET_folder / simulation_name / 'Input' / 'InitializationFiles').resolve(), verbose=verbose)

                # Copy csv files from the output folder
                list_csv_files = [entry for entry in os.listdir(self.output_path) if (simulation_name in entry) and ('.csv' in entry)]
                for csv_file in list_csv_files:
                    file_to_copy = os.path.join(self.output_path,                                               csv_file)
                    file_copied  = os.path.join(Path(local_LEDET_folder / simulation_name / 'Input').resolve(), csv_file)
                    shutil.copyfile(file_to_copy, file_copied)
                    print('Csv file {} copied to {}.'.format(file_to_copy, file_copied))

                # Make magnet field-map folder
                field_maps_folder = Path(local_LEDET_folder / '..' / 'Field maps' / simulation_name).resolve()
                make_folder_if_not_existing(field_maps_folder, verbose=verbose)

                # Copy field-map files from the output folder
                list_field_maps = [entry for entry in os.listdir(self.output_path) if (simulation_name in entry) and ('.map2d' in entry)]
                for field_map in list_field_maps:
                    file_to_copy = os.path.join(self.output_path,  field_map)
                    file_copied  = os.path.join(field_maps_folder, field_map)
                    shutil.copyfile(file_to_copy, file_copied)
                    print('Field map file {} copied to {}.'.format(file_to_copy, file_copied))

            elif 'PSPICE' in software:
                local_PSPICE_folder = Path(self.settings.local_PSPICE_folder)
                local_model_folder = Path(local_PSPICE_folder / simulation_name).resolve()
                # Make magnet input folder
                make_folder_if_not_existing(local_model_folder, verbose=verbose)

                # Copy lib files from the output folder
                list_lib_files = [entry for entry in os.listdir(self.output_path) if (simulation_name in entry) and ('.lib' in entry)]
                for lib_file in list_lib_files:
                    file_to_copy = os.path.join(self.output_path, lib_file)
                    file_copied = os.path.join(local_model_folder, lib_file)
                    shutil.copyfile(file_to_copy, file_copied)
                    print('Lib file {} copied to {}.'.format(file_to_copy, file_copied))

                # Copy stl files from the output folder
                list_stl_files = [entry for entry in os.listdir(self.output_path) if (simulation_name in entry) and ('.stl' in entry)]
                for stl_file in list_stl_files:
                    file_to_copy = os.path.join(self.output_path,   stl_file)
                    file_copied  = os.path.join(local_model_folder, stl_file)
                    shutil.copyfile(file_to_copy, file_copied)
                    print('Stl file {} copied to {}.'.format(file_to_copy, file_copied))

            else:
                raise Exception(f'Software {software} not supported for automated folder setup.')


    def setup_sim_LEDET(self, simulation_name, sim_number, flag_yaml=True, flag_json=False):
        '''
        Set up a LEDET simulation by copying the last file generated by BuilderModel to the output folder and to the
        local LEDET working folder. The original file is then deleted.
        If flag_yaml=True, the model is set up to be run using a yaml input file.
        If flag_json=True, the model is set up to be run using a json input file.
        '''

        # Unpack
        output_folder      = self.output_path
        local_LEDET_folder = self.settings.local_LEDET_folder

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        # Copy simulation file
        list_suffix = ['.xlsx']
        if flag_yaml == True:
            list_suffix.append('.yaml')
        if flag_json == True:
            list_suffix.append('.json')

        for suffix in list_suffix:
            file_name_temp   = os.path.join(output_folder, simulation_name + suffix)
            file_name_output = os.path.join(output_folder, simulation_name + '_' + str(sim_number) + suffix)
            file_name_local  = os.path.join(local_LEDET_folder, simulation_name, 'Input', simulation_name + '_' + str(sim_number) + suffix)

            shutil.copyfile(file_name_temp, file_name_output)
            print('Simulation file {} generated.'.format(file_name_output))

            shutil.copyfile(file_name_temp, file_name_local)
            print('Simulation file {} copied.'.format(file_name_local))

            os.remove(file_name_temp)
            print('Temporary file {} deleted.'.format(file_name_temp))


    def setup_sim_PSPICE(self, simulation_name, sim_number):
        '''
        Set up a PSPICE simulation by copying the last file generated by BuilderModel to the output folder and to the
        local PSPICE working folder.
        The simulation netlist and auxiliary files are copied in a new numbered subfoldered.
        The original file is then deleted.
        '''

        # Unpack
        output_folder = self.output_path
        local_PSPICE_folder = Path(self.settings.local_PSPICE_folder)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        # Make simulation folder
        local_model_folder = os.path.join(local_PSPICE_folder, simulation_name, str(sim_number))
        make_folder_if_not_existing(local_model_folder)

        # Copy simulation file
        file_name_temp = os.path.join(output_folder, simulation_name + '.cir')
        file_name_local = os.path.join(local_model_folder, simulation_name + '.cir')
        print('Simulation file {} generated.'.format(file_name_temp))

        shutil.copyfile(file_name_temp, file_name_local)
        print('Simulation file {} copied.'.format(file_name_local))

        os.remove(file_name_temp)
        print('Temporary file {} deleted.'.format(file_name_temp))

        # Copy lib files from the output folder
        list_lib_files = [entry for entry in os.listdir(output_folder) if (simulation_name in entry) and ('.lib' in entry)]
        for lib_file in list_lib_files:
            file_to_copy = os.path.join(output_folder, lib_file)
            file_copied = os.path.join(local_model_folder, lib_file)
            shutil.copyfile(file_to_copy, file_copied)
            print('Lib file {} copied to {}.'.format(file_to_copy, file_copied))

        # Copy stl files from the output folder
        list_stl_files = [entry for entry in os.listdir(output_folder) if (simulation_name in entry) and ('.stl' in entry)]
        for stl_file in list_stl_files:
            file_to_copy = os.path.join(output_folder,   stl_file)
            file_copied  = os.path.join(local_model_folder, stl_file)
            shutil.copyfile(file_to_copy, file_copied)
            print('Stl file {} copied to {}.'.format(file_to_copy, file_copied))


    def setup_sim_PyBBQ(self, simulation_name, sim_number):
        '''
        Set up a PyBBQ simulation by copying the last file generated by BuilderModel to the output folder and to the
        local PyBBQ working folder.
        The original file is then deleted.
        '''

        # Unpack
        output_folder = self.output_path
        local_PyBBQ_folder = Path(self.settings.local_PyBBQ_folder)

        # Add simulation number to the list
        self.list_sims.append(sim_number)

        # Make simulation folder
        local_model_folder = os.path.join(local_PyBBQ_folder, simulation_name, str(sim_number))
        make_folder_if_not_existing(local_model_folder)

        # Copy simulation file
        file_name_temp = os.path.join(output_folder, simulation_name + '.yaml')
        file_name_local = os.path.join(local_model_folder, simulation_name + '.yaml')
        print('Simulation file {} generated.'.format(file_name_temp))

        shutil.copyfile(file_name_temp, file_name_local)
        print('Simulation file {} copied.'.format(file_name_local))

        os.remove(file_name_temp)
        print('Temporary file {} deleted.'.format(file_name_temp))


    def run_sim(self, software: str, simulation_name: str, sim_number: int, simFileType: str = None, verbose: bool = False):
        '''
        Run selected simulation.
        The function applies a different logic for each simulation software.
        '''
        if software == 'LEDET':
            dLEDET = DriverLEDET(path_exe=self.settings.LEDET_path, path_folder_LEDET=self.settings.local_LEDET_folder, verbose=verbose)
            dLEDET.run_LEDET(simulation_name, str(sim_number), simFileType=simFileType)
        elif software == 'PyBBQ':
            local_model_folder_input  = os.path.join(self.settings.local_PyBBQ_folder, simulation_name, str(sim_number))
            relative_folder_output = os.path.join(simulation_name, str(sim_number))
            dPyBBQ = DriverPyBBQ(path_exe=self.settings.PyBBQ_path, path_folder_PyBBQ=self.settings.local_PyBBQ_folder, path_folder_PyBBQ_input=local_model_folder_input, verbose=verbose)
            dPyBBQ.run_PyBBQ(simulation_name, outputDirectory=relative_folder_output)
        elif software == 'PSPICE':
            local_model_folder = Path(Path(self.settings.local_PSPICE_folder) / simulation_name / str(sim_number)).resolve()
            dPSPICE = DriverPSPICE(path_exe=self.settings.PSPICE_path, path_folder_PSPICE=local_model_folder, verbose=verbose)
            dPSPICE.run_PSPICE(simulation_name, suffix='')
        else:
            raise Exception(f'Software {software} not supported for automated running.')
