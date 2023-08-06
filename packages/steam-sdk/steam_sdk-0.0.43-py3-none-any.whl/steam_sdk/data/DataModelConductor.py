from pydantic import BaseModel, PrivateAttr
from typing import (Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union, Type)


from steam_sdk.data.DataConductor import Conductor
from steam_sdk.data.DataModelMagnet import Circuit, PowerSupply, QuenchProtection, LEDET


############################
# General parameters
class Model(BaseModel):
    """
        Level 2: Class for information on the model
    """
    name: str = None  # magnetIdentifier (ProteCCT)
    version: str = None
    case: str = None
    state: str = None


class General(BaseModel):
    """
        Level 1: Class for general information on the case study
    """
    conductor_name: str = None
    model: Model = Model()
    material_database_path: str = None
    T_initial: float = None
    length_busbar: float = None

############################
# Conductor geometry


############################
# BBQ options
class GeometryBBQ(BaseModel):
    """
        Level 2: Class for geometry options in BBQ
    """
    thInsul: float = None
    lenBusbar: float = None


class SimulationBBQ(BaseModel):
    """
        Level 2: Class for simulation options in BBQ
    """
    meshSize: float = None


class PhysicsBBQ(BaseModel):
    """
        Level 2: Class for physics options in BBQ
    """
    adiabaticZoneLength: float = None
    aFilmBoilingHeliumII: float = None
    aKap: float = None
    BBackground: float = None
    BPerI: float = None
    IDesign: float = None
    jointLength: float = None
    jointResistancePerMeter: float = None
    muTInit: float = None
    nKap: float = None
    QKapLimit: float = None
    Rjoint: float = None
    symmetryFactor: float = None
    tauDecay: float = None
    TInitMax: float = None
    TInitOp: float = None
    TLimit: float = None
    tValidation: float = None
    TVQRef: float = None
    VThreshold: float = None
    withCoolingToBath: float = None


class QuenchInitializationBBQ(BaseModel):
    """
        Level 2: Class for quench initialization parameters in BBQ
    """
    sigmaTInit: float = None


class BBQ(BaseModel):
    """
        Level 1: Class for BBQ options
    """
    geometry: GeometryBBQ = GeometryBBQ()
    simulation: SimulationBBQ = SimulationBBQ()
    physics: PhysicsBBQ = PhysicsBBQ()
    quench_initialization: QuenchInitializationBBQ = QuenchInitializationBBQ()


############################
# PyBBQ options
class GeometryPyBBQ(BaseModel):
    """
        Level 2: Class for geometry options in PyBBQ
    """
    thInsul: float = None
    lenBusbar: float = None
    tapetype: str = None


class MagneticFieldPyBBQ(BaseModel):
    """
        Level 1: Class for magnetic-field options in PyBBQ
    """
    Calc_b_from_geometry: bool =  None
    Background_Bx: float =  None
    Background_By: float =  None
    Background_Bz: float =  None
    Self_Field: float =  None
    B0_dump: bool =  None


class SimulationPyBBQ(BaseModel):
    """
        Level 2: Class for simulation options in PyBBQ
    """
    meshSize: float = None
    layers: int = None
    output: bool = None
    dt: float = None
    t0: List[float] = []
    posref: List[float] = []
    print_every: int = None
    store_every: int = None
    plot_every: int = None

class PhysicsPyBBQ(BaseModel):
    """
        Level 2: Class for physics options in PyBBQ
    """
    adiabaticZoneLength: float = None
    aFilmBoilingHeliumII: float = None
    aKap: float = None
    BBackground: float = None
    BPerI: float = None
    IDesign: float = None
    jointLength: float = None
    jointResistancePerMeter: float = None
    muTInit: float = None
    nKap: float = None
    QKapLimit: float = None
    Rjoint: float = None
    symmetryFactor: float = None
    tauDecay: float = None
    TInitMax: float = None
    TLimit: float = None
    tValidation: float = None
    TVQRef: float = None
    VThreshold: float = None
    withCoolingToBath: bool = None
    withCoolingInternal: bool = None
    Jc_4K_5T_NbTi: float = None


class QuenchInitializationPyBBQ(BaseModel):
    """
        Level 2: Class for quench initialization parameters in PyBBQ
    """
    sigmaTInit: float = None

class PyBBQ(BaseModel):
    """
        Level 1: Class for PyBBQ options
    """
    geometry: GeometryBBQ = GeometryBBQ()
    magnetic_field: MagneticFieldPyBBQ = MagneticFieldPyBBQ()
    simulation: SimulationPyBBQ = SimulationPyBBQ()
    physics: PhysicsPyBBQ = PhysicsPyBBQ()
    quench_initialization: QuenchInitializationPyBBQ = QuenchInitializationPyBBQ()



############################
# Highest level
class DataModelConductor(BaseModel):
    '''
        **Class for the STEAM inputs**

        This class contains the data structure of STEAM model inputs.

        :param N: test 1
        :type N: int
        :param n: test 2
        :type n: int

        :return: DataModelMagnet object
    '''

    GeneralParameters: General = General()
    Conductors: List[Conductor] = [Conductor(cable={'type': 'Rutherford'}, strand={'type': 'Round'}, Jc_fit={'type': 'CUDI1'})]
    Circuit: Circuit = Circuit()
    Power_Supply: PowerSupply = PowerSupply()
    Quench_Protection: QuenchProtection = QuenchProtection()
    Options_BBQ: BBQ = BBQ()
    Options_LEDET: LEDET = LEDET()
    Options_PyBBQ: PyBBQ = PyBBQ()
