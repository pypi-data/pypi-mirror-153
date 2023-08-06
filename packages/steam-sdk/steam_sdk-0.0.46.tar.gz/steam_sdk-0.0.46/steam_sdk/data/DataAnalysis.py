from pydantic import BaseModel
from typing import (List, Union, Literal)


############################
# General parameters
class Model(BaseModel):
    """
        Level 2: Class for information on the model
    """
    name: str = None
    version: str = None
    case: str = None
    state: str = None

class General(BaseModel):
    """
        Level 1: Class for general information on the case study
    """
    analysis_name: str = None
    flag_permanent_settings: bool = None
    model: Model = Model()

############################
# Permanent settings
class PermanentSettings(BaseModel):
    """
        Level 1: Class for information on the permanent settings
        These settings should point to paths that will not change in time
    """
    comsolexe_path:      str = None  # full path to comsol.exe, only COMSOL53a is supported
    JAVA_jdk_path:       str = None  # full path to folder with java jdk
    CFunLibPath:         str = None  # path to dll files with material properties
    LEDET_path:          str = None  #
    PyBBQ_path:          str = None  #
    ProteCCT_path:       str = None  #
    PSPICE_path:         str = None  #
    COSIM_path:          str = None  #
    FiQuS_path:          str = None  #
    PSPICE_library_path: str = None  #
    local_LEDET_folder:  str = None  # full path to local LEDET folder
    local_PyBBQ_folder:  str = None  # full path to local PyBBQ folder
    local_PSPICE_folder: str = None  # full path to local PSPICE folder

############################
# Working folders
class WorkingFolders(BaseModel):
    """
        Level 1: Class for information on the working folders
    """
    library_path: str = None  #
    output_path:  str = None  # it would be nice if model_name and software could be read as parameters from other keys (anchors)
    temp_path:    str = None

############################
# Analysis step definition
class MakeModel(BaseModel):
    """
        Level 2: Analysis step to generate a model using BuilderModel
    """
    step_name:         str = None  # this key will be called by AnalysisStepSequence
    type:              Literal['MakeModel']
    model_name:        str = None
    file_model_data:   str = None  # it would be nice if it could be read as parameters from other keys (anchors)
    case_model:        str = None
    software:          List[str] = []
    simulation_name:   str = None
    simulation_number: int = None
    flag_build:        bool = None
    flag_dump_all:     bool = None
    verbose:           bool = None
    flag_plot_all:     bool = None
    flag_json:         bool = None

class ModifyModel(BaseModel):
    """
        Level 2: Analysis step to modify an existing BuilderModel object by changing one variable
    """
    step_name:              str = None  # this key will be called by AnalysisStepSequence
    type:                   Literal['ModifyModel']
    model_name:             str = None
    variable_to_change:     str = None
    variable_value:         list = []
    new_model_name:         List[str] = []  # if not empty, new copies of the model object will be built
    simulation_numbers:     List[int] = []  # if not empty, simulation files will be built
    simulation_name:        str = None
    software:               List[str] = []

class ModifyModelMultipleVariables(BaseModel):
    """
        Level 2: Analysis step to modify an existing BuilderModel object by changing a list of variables
    """
    step_name:              str = None  # this key will be called by AnalysisStepSequence
    type:                   Literal['ModifyModelMultipleVariables']
    model_name:             str = None
    variables_to_change:    List[str] = []
    variables_value:        List[list] = [[]]
    new_model_name:         List[str] = []  # if not empty, new copies of the model object will be built
    simulation_numbers:     List[int] = []  # if not empty, simulation files will be built
    simulation_name:        str = None
    software:               List[str] = []

class SetUpFolder(BaseModel):
    step_name:  str = None  # this key will be called by AnalysisStepSequence
    type:       Literal['SetUpFolder']
    simulation_name: str = None
    software: List[str] = []

class RunSimulation(BaseModel):
    """
        Level 2: Analysis step to run a simulation file
    """
    step_name:          str = None  # this key will be called by AnalysisStepSequence
    type:               Literal['RunSimulation']
    software:           str = None
    simulation_name:    str = None
    simulation_numbers: List[int] = []
    simFileType:        str = None

class PostProcess(BaseModel):
    """
        Level 2: Analysis step to run a simulation file
    """
    step_name:          str = None  # this key will be called by AnalysisStepSequence
    type:               Literal['PostProcess']

class AnalysisStep(BaseModel):
    """
        Level 1: Class for information on the analysis step
        Objects of this class will be defined in AnalysisStepDefinition
    """
    step: Union[MakeModel, ModifyModel, ModifyModelMultipleVariables, SetUpFolder, RunSimulation, PostProcess] = {}

############################
# Highest level
class DataAnalysis(BaseModel):
    '''
        **Class for the circuit netlist inputs**

        This class contains the data structure of an analysis performed with STEAM_SDK.

        :param N: test 1
        :type N: int
        :param n: test 2
        :type n: int

        :return: DataModelCircuit object
    '''

    GeneralParameters: General = General()
    PermanentSettings: PermanentSettings = PermanentSettings()
    WorkingFolders:    WorkingFolders = WorkingFolders()
    AnalysisStepDefinition: List[AnalysisStep] = [
        AnalysisStep(step={'type': 'MakeModel'}),
        AnalysisStep(step={'type': 'ModifyModel'}),
        AnalysisStep(step={'type': 'ModifyModelMultipleVariables'}),
        AnalysisStep(step={'type': 'SetUpFolder'}),
        AnalysisStep(step={'type': 'RunSimulation'}),
        AnalysisStep(step={'type': 'PostProcess'}),
    ]
    AnalysisStepSequence: List[str] = []  # Here the analysis steps are defined, in execution order. Names must be defined in AnalysisStepDefinition. Repetitions ARE allowed.
