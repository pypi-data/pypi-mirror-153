from pydantic import BaseModel
from typing import (List)


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
    circuit_name: str = None
    model: Model = Model()


############################
# Auxiliary files
class Auxiliary_Files(BaseModel):
    """
        Level 1: Class for general information on the case study
    """
    files_to_include: List[str] = []

############################
# Stimuli
class Stimuli(BaseModel):
    """
        Level 1: Stimulus files
    """
    stimulus_files: List[str] = []


############################
# Libraries
class Libraries(BaseModel):
    """
        Level 1: Component libraries
    """
    component_libraries: List[str] = []


############################
# Global parameters
class Global_Parameters(BaseModel):
    """
        Level 1: Global circuit parameters
    """
    global_parameters: dict = None


############################
# Netlist, defined as a list of Component objects
class Component(BaseModel):
    """
        Level 1: Circuit component
    """
    type: str = None
    name: str = None
    nodes: List[str] = []
    value: str = None
    parameters: dict = None


############################
# Simulation options
class Options(BaseModel):
    """
        Level 1: Simulation options
    """
    options_simulation: dict = None
    options_autoconverge: dict = None
    flag_inCOSIM: bool = None


############################
# Analysis settings
class SimulationTime(BaseModel):
    """
        Level 2: Simulation time settings
    """
    time_start: float = None
    time_end:   float = None
    min_time_step: float = None
    time_schedule: dict = None

class Analysis(BaseModel):
    """
        Level 1: Analysis settings
    """
    analysis_type: str = None
    simulation_time: SimulationTime = SimulationTime()


############################
# Post-processing settings
class Settings_Probe(BaseModel):
    """
        Level 2: Probe settings
    """
    probe_type: str = None
    variables: List[str] = []

class PostProcess(BaseModel):
    """
        Level 1: Post-processing settings
    """
    probe: Settings_Probe = Settings_Probe()


############################
# Highest level
class DataCircuit(BaseModel):
    '''
        **Class for the circuit netlist inputs**

        This class contains the data structure of circuit netlist model inputs.

        :param N: test 1
        :type N: int
        :param n: test 2
        :type n: int

        :return: DataCircuit object
    '''

    GeneralParameters: General = General()
    AuxiliaryFiles: Auxiliary_Files = Auxiliary_Files()
    Stimuli: Stimuli = Stimuli()
    Libraries: Libraries = Libraries()
    GlobalParameters: Global_Parameters = Global_Parameters()
    Netlist: List[Component] = [Component()]
    Options: Options = Options()
    Analysis: Analysis = Analysis()
    PostProcess: PostProcess = PostProcess()
