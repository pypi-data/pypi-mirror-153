from pydantic import BaseModel, PrivateAttr
from typing import (Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union, Type)

from ..data.DataConductor import Conductor


############################
# Source files
class SourceFiles(BaseModel):
    """
        Level 1: Class for the source files
    """
    coil_fromROXIE: str = None    # ROXIE .data file
    conductor_fromROXIE: str = None  # ROXIE .cadata file
    iron_fromROXIE: str = None    # ROXIE .iron file
    BH_fromROXIE: str = None      # ROXIE .bhdata file (BH-curves)
    magnetic_field_fromROXIE: str = None # ROXIE .map2d file
    sm_inductance: str = None


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


class MagnetInductance(BaseModel):
    """
        Level 2: Class for magnet inductance assignment
    """
    fL_I: List[float] = []
    fL_L: List[float] = []


class General(BaseModel):
    """
        Level 1: Class for general information on the case study
    """
    magnet_name: str = None
    circuit_name: str = None
    model: Model = Model()
    T_initial: float = None               # T00 (LEDET), Top (SIGMA)
    magnetic_length: float = None   # l_magnet (LEDET), magLength (SIGMA), magneticLength (ProteCCT)
    magnet_inductance: MagnetInductance = MagnetInductance()


############################
# Coil Windings
class ElectricalOrder(BaseModel):
    """
        Level 2: Class for the order of the electrical pairs
    """
    group_together: List[List[int]] = []   # elPairs_GroupTogether
    reversed: List[int] = []         # elPairs_RevElOrder


class HeatExchange(BaseModel):
    """
        Level 2: Class for heat exchange information
    """
    heat_exchange_max_distance: float = None  # heat exchange max_distance
    iContactAlongWidth_pairs_to_add: List[List[int]] = [[]]
    iContactAlongWidth_pairs_to_remove: List[List[int]] = [[]]
    iContactAlongHeight_pairs_to_add: List[List[int]] = [[]]
    iContactAlongHeight_pairs_to_remove: List[List[int]] = [[]]
    th_insulationBetweenLayers: float = None


class Multipole(BaseModel):
    """
        Level 2: Class for multi-pole coil data
    """
    alphaDEG_ht: List[float] = []  # Inclination angle of each half-turn, alphaDEG (LEDET)
    rotation_ht: List[float] = []  # Rotation of each half-turn, rotation_block (LEDET)
    mirror_ht: List[float]   = []  # Mirror around quadrant bisector line for half-turn, mirror_block (LEDET)
    mirrorY_ht: List[float]  = []  # Mirror around Y axis for half-turn, mirrorY_block (LEDET)


class Solenoid(BaseModel):
    """
        Level 2: Class for Solenoid windings
    """
    tbc: str = None


class Pancake(BaseModel):
    """
        Level 2: Class for Pancake windings
    """
    tbc: str = None


class CCT_straight(BaseModel):
    """
        Level 2: Class for straight CCT windings
    """
    # TODO These variables could be renamed. Current names are as they appear in ProteCCT
    inner_radius_formers: List[float] = []  # innerRadiusFormers (ProteCCT)
    former_thickness_underneath_coil: float = None # formerThicknessUnderneathCoil. Thickness of the former underneath the slot holding the strands in [m] (ProteCCT)
    inner_radius_outer_cylinder: float = None  # innerRadiusOuterCylinder (ProteCCT)
    thickness_outer_cylinder: float = None # thicknessOuterCylinder (ProteCCT)


class CCT_curved(BaseModel):
    """
        Level 2: Class for curved CCT windings
    """
    tbc: str = None


class CoilWindings(BaseModel):
    """
        Level 1: Class for winding information
    """
    conductor_to_group: List[int] = []  # This key assigns to each group a conductor of one of the types defined with Conductor.name
    group_to_coil_section: List[int] = []  # This key assigns groups of half-turns to coil sections
    polarities_in_group: List[int] = []  # This key assigns the polarity of the current in each group # TODO: Consider if it is convenient to remove this
    n_half_turn_in_group: List[int] = []
    half_turn_length: List[float] = []
    electrical_pairs: ElectricalOrder = ElectricalOrder()  # Variables used to calculate half-turn electrical order
    heat_exchange: HeatExchange = HeatExchange()  # Variables used to calculate heat exchange
    multipole: Multipole = Multipole()
    pancake: Pancake = Pancake()
    solenoid: Solenoid = Solenoid()
    CCT_straight: CCT_straight = CCT_straight()
    CCT_curved: CCT_curved = CCT_curved()


############################
# Conductor keys are defined in data\DataConductor()

############################
# Circuit
class Circuit(BaseModel):
    """
        Level 1: Class for the circuit parameters
    """
    R_circuit: float = None             # R_circuit
    L_circuit: float = None             # Lcir (SIGMA)
    R_parallel: float = None


############################
# Power Supply (aka Power Converter)
class PowerSupply(BaseModel):
    """
        Level 1: Class for the power supply (aka power converter)
    """
    I_initial: float = None          # I00 (LEDET), I_0 (SIGMA), I0 (BBQ)
    t_off: float = None            # t_PC
    t_control_LUT: List[float] = []    # t_PC_LUT
    I_control_LUT: List[float] = []    # I_PC_LUT
    R_crowbar: float = None     # Rcrow (SIGMA), RCrowbar (ProteCCT)
    Ud_crowbar: float = None


############################
# Quench Protection
class EnergyExtraction(BaseModel):
    """
        Level 2: Class for the energy extraction parameters
    """
    t_trigger: float = None                 # tEE (LEDET), tSwitchDelay (ProteCCT)
    R_EE: float = None       # R_EE_triggered (LEDET)
    power_R_EE: float = None # RDumpPower (ProteCCT), variable used to simulate varistors used in an EE system
    L: float = None
    C: float = None


class QuenchHeater(BaseModel):
    """
        Level 2: Class for the quench heater parameters
    """
    N_strips: int = None                              # nHeaterStrips
    t_trigger: List[float] = []                        # tQH
    U0: List[float] = []
    C: List[float] = []
    R_warm: List[float] = []
    w: List[float] = []
    h: List[float] = []
    s_ins: List[float] = []
    type_ins: List[float] = []
    s_ins_He: List[float] = []
    type_ins_He: List[float] = []
    l: List[float] = []
    l_copper: List[float] = []
    l_stainless_steel: List[float] = []
    f_cover: List[float] = []
    iQH_toHalfTurn_From: List[float] = []
    iQH_toHalfTurn_To: List[float] = []


class CLIQ(BaseModel):
    """
        Level 2: Class for the CLIQ parameters
    """
    t_trigger: float = None                        # tCLIQ
    current_direction: List[int] = []    # directionCurrentCLIQ
    sym_factor: float = None               # symFactor
    N_units: int = None                          # nCLIQ
    U0: float = None                       # V_cliq_0 (SIGMA)
    C: float = None                        # C_cliq (SIGMA)
    R: float = None                        # Rcapa (LEDET), R_cliq (SIGMA)
    L: float = None                        # L_cliq
    I0: float = None                       # I_cliq_0


class QuenchProtection(BaseModel):
    """
        Level 1: Class for quench protection
    """
    Energy_Extraction: EnergyExtraction = EnergyExtraction()
    Quench_Heaters: QuenchHeater = QuenchHeater()
    CLIQ: CLIQ = CLIQ()


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
# getDP options
class GETDP(BaseModel):
    """
        Level 1: Class for getDP options
    """
    placeholder_parameter: int = None


############################
# LEDET options
class TimeVectorLEDET(BaseModel):
    """
        Level 2: Class for simulation time vector in LEDET
    """
    time_vector_params: List[float] = []


class FieldMapFilesLEDET(BaseModel):
    """
        Level 2: Class for field map file parameters in LEDET
    """
    Iref: float = None
    flagIron: int = None
    flagSelfField: int = None
    headerLines: int = None
    columnsXY: List[int] = []
    columnsBxBy: List[int] = []
    flagPlotMTF: int = None
    flag_modify_map2d_ribbon_cable: int = None


class InputGenerationOptionsLEDET(BaseModel):
    """
        Level 2: Class for input generation options in LEDET
    """
    flag_typeWindings: int = None
    flag_calculateInductanceMatrix: int = None
    flag_useExternalInitialization: int = None
    flag_initializeVar: int = None


class SimulationLEDET(BaseModel):
    """
        Level 2: Class for simulation options in LEDET
    """
    flag_fastMode: float = None
    flag_controlCurrent: float = None
    flag_automaticRefinedTimeStepping: float = None


class PhysicsLEDET(BaseModel):
    """
        Level 2: Class for physics options in LEDET
    """
    flag_IronSaturation: int = None
    flag_InvertCurrentsAndFields: int = None
    flag_ScaleDownSuperposedMagneticField: int = None
    flag_HeCooling: int = None
    fScaling_Pex: float = None
    fScaling_Pex_AlongHeight: float = None
    fScaling_MR: float = None
    flag_scaleCoilResistance_StrandTwistPitch: int = None
    flag_separateInsulationHeatCapacity: int = None
    flag_persistentCurrents: int = None
    flag_ISCL: int = None
    fScaling_Mif: float = None
    fScaling_Mis: float = None
    flag_StopIFCCsAfterQuench: int = None
    flag_StopISCCsAfterQuench: int = None
    tau_increaseRif: float = None
    tau_increaseRis: float = None
    fScaling_RhoSS: float = None
    maxVoltagePC: float = None
    minCurrentDiode: float = None
    flag_symmetricGroundingEE: int = None
    flag_removeUc: int = None
    BtX_background: float = None
    BtY_background: float = None


class QuenchInitializationLEDET(BaseModel):
    """
        Level 2: Class for quench initialization parameters in LEDET
    """
    iStartQuench: List[int] = []
    tStartQuench: List[float] = []
    lengthHotSpot_iStartQuench: List[float] = []
    fScaling_vQ_iStartQuench: List[float] = []


class PostProcessingLEDET(BaseModel):
    """
        Level 2: Class for post processing options in LEDET
    """
    flag_showFigures: int = None
    flag_saveFigures: int = None
    flag_saveMatFile: int = None
    flag_saveTxtFiles: int = None
    flag_generateReport: int = None
    tQuench: List[float] = []
    initialQuenchTemp: List[float] = []
    flag_hotSpotTemperatureInEachGroup: int = None


class Simulation3DLEDET(BaseModel):
    """
        Level 2: Class for 3D simulation parameters and options in lEDET
    """
    # Variables in the "Options" sheet
    flag_3D: int = None
    flag_adaptiveTimeStepping: int = None
    sim3D_flag_Import3DGeometry: int = None
    sim3D_import3DGeometry_modelNumber: int = None

    # Variables in the "Inputs" sheet
    sim3D_uThreshold: float = None
    sim3D_f_cooling_down: float = None
    sim3D_f_cooling_up: float = None
    sim3D_f_cooling_left: float = None
    sim3D_f_cooling_right: float = None
    sim3D_fExToIns: float = None
    sim3D_fExUD: float = None
    sim3D_fExLR: float = None
    sim3D_min_ds_coarse: float = None
    sim3D_min_ds_fine: float = None
    sim3D_min_nodesPerStraightPart: float = None
    sim3D_min_nodesPerEndsPart: float = None
    sim3D_idxFinerMeshHalfTurn: List[int] = []
    sim3D_Tpulse_sPosition: float = None
    sim3D_Tpulse_peakT: float = None
    sim3D_Tpulse_width: float = None
    sim3D_tShortCircuit: float = None
    sim3D_coilSectionsShortCircuit: List[int] = []
    sim3D_R_shortCircuit: float = None
    sim3D_shortCircuitPosition: float = None
    sim3D_durationGIF: float = None
    sim3D_flag_saveFigures: int = None
    sim3D_flag_saveGIF: int = None
    sim3D_flag_VisualizeGeometry3D: int = None
    sim3D_flag_SaveGeometry3D: int = None


class PlotsLEDET(BaseModel):
    """
        Level 2: Class for plotting parameters in lEDET
    """
    suffixPlot: List[str] = []
    typePlot: List[int] = []
    outputPlotSubfolderPlot: List[str] = []
    variableToPlotPlot: List[str] = []
    selectedStrandsPlot: List[str] = []
    selectedTimesPlot: List[str] = []
    labelColorBarPlot: List[str] = []
    minColorBarPlot: List[str] = []
    maxColorBarPlot: List[str] = []
    MinMaxXYPlot: List[int] = []
    flagSavePlot: List[int] = []
    flagColorPlot: List[int] = []
    flagInvisiblePlot: List[int] = []


class VariablesToSaveLEDET(BaseModel):
    """
        Level 2: Class for variables to save in lEDET
    """
    variableToSaveTxt: List[str] = []
    typeVariableToSaveTxt: List[int] = []
    variableToInitialize: List[str] = []


class LEDET(BaseModel):
    """
        Level 1: Class for LEDET options
    """
    time_vector: TimeVectorLEDET = TimeVectorLEDET()
    field_map_files: FieldMapFilesLEDET = FieldMapFilesLEDET()
    input_generation_options: InputGenerationOptionsLEDET = InputGenerationOptionsLEDET()
    simulation: SimulationLEDET = SimulationLEDET()
    physics: PhysicsLEDET = PhysicsLEDET()
    quench_initiation: QuenchInitializationLEDET = QuenchInitializationLEDET()
    post_processing: PostProcessingLEDET = PostProcessingLEDET()
    simulation_3D: Simulation3DLEDET = Simulation3DLEDET()
    plots: PlotsLEDET = PlotsLEDET()
    variables_to_save: VariablesToSaveLEDET = VariablesToSaveLEDET()


############################
# ProteCCT options
class TimeVectorProteCCT(BaseModel):
    """"
        Level 2: Class for ProteCCT time vector options
    """
    tMaxStopCondition: float = None
    minTimeStep: float = None


class GeometryGenerationOptionsProteCCT(BaseModel):
    """"
        Level 2: Class for ProteCCT geometry generation options
    """
    totalConductorLength: float = None
    numTurnsPerStrandTotal: int = None
    thFormerInsul: float = None
    wStrandSlot: float = None
    numRowStrands: int = None
    numColumnStrands: int = None
    IcFactor: float = None
    polyimideToEpoxyRatio: float = None
    windingOrder: str = None  # Note: it will be written in a single cell in the ProteCCT file


class PhysicsProteCCT(BaseModel):
    """"
        Level 2: Class for ProteCCT physics options
    """
    M: List[List[float]] = [[]]
    BMaxAtNominal: float = None
    BMinAtNominal: float = None
    INominal: float = None
    fieldPeriodicity: float = None
    RRRFormer: float = None
    RRROuterCylinder: float = None
    coolingToHeliumBath: int = None
    fLoopLength: float = None
    addedHeCpFrac: float = None
    addedHeCoolingFrac: float = None


class SimulationProteCCT(BaseModel):
    """"
        Level 2: Class for ProteCCT physics options
    """
    tempMaxStopCondition: float = None
    IOpFractionStopCondition: float = None
    fracCurrentChangeMax: float = None
    resultsAtTimeStep: float = None
    deltaTMaxAllowed: float = None
    turnLengthElements: int = None
    externalWaveform: int = None
    saveStateAtEnd: int = None
    restoreStateAtStart: int = None
    silentRun: int = None


class PlotsProteCCT(BaseModel):
    """"
        Level 2: Class for ProteCCT plots options
    """
    withPlots: int = None
    plotPauseTime: float = None


class PostProcessingProteCCT(BaseModel):
    """"
        Level 2: Class for ProteCCT post-processing options
    """
    withVoltageEvaluation: int = None
    voltageToGroundOutputSelection: str = None  # Note: it will be written in a single cell in the ProteCCT file


class PROTECCT(BaseModel):
    """"
        Level 1: Class for ProteCCT options
    """
    time_vector: TimeVectorProteCCT = TimeVectorProteCCT()
    geometry_generation_options: GeometryGenerationOptionsProteCCT = GeometryGenerationOptionsProteCCT()
    simulation: SimulationProteCCT = SimulationProteCCT()
    physics: PhysicsProteCCT = PhysicsProteCCT()
    post_processing: PostProcessingProteCCT = PostProcessingProteCCT()
    plots: PlotsProteCCT = PlotsProteCCT()


############################
# SIGMA options
class TimeVectorSIGMA(BaseModel):
    """
        Level 2: Class for simulation time vector in SIGMA
    """
    time_step: float = None


class SimulationSIGMA(BaseModel):
    """
        Level 2: Class for simulation parameters in SIGMA
    """
    max_mesh_size: float = None


class PhysicsSIGMA(BaseModel):
    """
        Level 2: Class for physics parameters in SIGMA
    """
    FLAG_M_pers: float = None
    FLAG_ifcc: int = None
    FLAG_iscc_crossover: int = None
    FLAG_iscc_adjw: int = None
    FLAG_iscc_adjn: int = None
    tauCC_PE: float = None


class QuenchInitializationSIGMA(BaseModel):
    """
        Level 2: Class for quench initialization parameters in SIGMA
    """
    PARAM_time_quench: float = None
    FLAG_quench_all: int = None
    FLAG_quench_off: int = None


class SIGMA(BaseModel):
    """
        Level 1: Class for SIGMA options
    """
    time_vector: TimeVectorSIGMA = TimeVectorSIGMA()
    simulation: SimulationSIGMA = SimulationSIGMA()
    physics: PhysicsSIGMA = PhysicsSIGMA()
    quench_initialization: QuenchInitializationSIGMA = QuenchInitializationSIGMA()


############################
# Highest level
class DataModel(BaseModel):
    '''
        **Class for the STEAM inputs**

        This class contains the data structure of STEAM model inputs.

        :param N: test 1
        :type N: int
        :param n: test 2
        :type n: int

        :return: DataModel object
    '''

    Sources: SourceFiles = SourceFiles()
    GeneralParameters: General = General()
    CoilWindings: CoilWindings = CoilWindings()
    Conductors: List[Conductor] = [Conductor(cable={'type': 'Rutherford'}, strand={'type': 'Round'}, Jc_fit={'type': 'CUDI1'})]
    Circuit: Circuit = Circuit()
    Power_Supply: PowerSupply = PowerSupply()
    Quench_Protection: QuenchProtection = QuenchProtection()
    Options_BBQ: BBQ = BBQ()
    Options_getDP: GETDP = GETDP()
    Options_LEDET: LEDET = LEDET()
    Options_ProteCCT: PROTECCT = PROTECCT()
    Options_SIGMA: SIGMA = SIGMA()
