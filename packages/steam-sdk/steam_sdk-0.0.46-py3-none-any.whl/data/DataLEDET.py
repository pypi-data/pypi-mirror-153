import numpy as np
from dataclasses import dataclass
"""
    These classes define the four LEDET dataclasses, which contain the variables to write in the four sheets of a LEDET 
    input file: Inputs, Options, Plots and Variables.
"""
@dataclass
class LEDETInputs:
    T00: float = 0.0
    l_magnet: float = 0.0
    I00: float = 0.0
    GroupToCoilSection: np.ndarray = np.array([])
    polarities_inGroup: np.ndarray = np.array([])
    nT: np.ndarray = np.array([])
    nStrands_inGroup: np.ndarray = np.array([])
    l_mag_inGroup: np.ndarray = np.array([])
    ds_inGroup: np.ndarray = np.array([])
    f_SC_strand_inGroup: np.ndarray = np.array([])
    f_ro_eff_inGroup: np.ndarray = np.array([])
    Lp_f_inGroup: np.ndarray = np.array([])
    RRR_Cu_inGroup: np.ndarray = np.array([])
    SCtype_inGroup: np.ndarray = np.array([])
    STtype_inGroup: np.ndarray = np.array([])
    insulationType_inGroup: np.ndarray = np.array([])
    internalVoidsType_inGroup: np.ndarray = np.array([])
    externalVoidsType_inGroup: np.ndarray = np.array([])
    wBare_inGroup: np.ndarray = np.array([])
    hBare_inGroup: np.ndarray = np.array([])
    wIns_inGroup: np.ndarray = np.array([])
    hIns_inGroup: np.ndarray = np.array([])
    Lp_s_inGroup: np.ndarray = np.array([])
    R_c_inGroup: np.ndarray = np.array([])
    Tc0_NbTi_ht_inGroup: np.ndarray = np.array([])
    Bc2_NbTi_ht_inGroup: np.ndarray = np.array([])
    c1_Ic_NbTi_inGroup: np.ndarray = np.array([])
    c2_Ic_NbTi_inGroup: np.ndarray = np.array([])
    Tc0_Nb3Sn_inGroup: np.ndarray = np.array([])
    Bc2_Nb3Sn_inGroup: np.ndarray = np.array([])
    Jc_Nb3Sn0_inGroup: np.ndarray = np.array([])
    alpha_Nb3Sn0_inGroup: np.ndarray = np.array([])
    f_scaling_Jc_BSCCO2212_inGroup: np.ndarray = np.array([])
    df_inGroup: np.ndarray = np.array([])
    selectedFit_inGroup: np.ndarray = np.array([])
    fitParameters_inGroup: np.ndarray = np.array([])
    overwrite_f_internalVoids_inGroup: np.ndarray = np.array([])
    overwrite_f_externalVoids_inGroup: np.ndarray = np.array([])
    alphasDEG: np.ndarray = np.array([])
    rotation_block: np.ndarray = np.array([])
    mirror_block: np.ndarray = np.array([])
    mirrorY_block: np.ndarray = np.array([])
    el_order_half_turns: np.ndarray = np.array([])
    iContactAlongWidth_From: np.ndarray = np.array([])
    iContactAlongWidth_To: np.ndarray = np.array([])
    iContactAlongHeight_From: np.ndarray = np.array([])
    iContactAlongHeight_To: np.ndarray = np.array([])
    t_PC: float = 0.0
    t_PC_LUT: np.ndarray = np.array([])
    I_PC_LUT: np.ndarray = np.array([])
    R_circuit: float = 0.0
    R_crowbar: float = 0.0
    Ud_crowbar: float = 0.0
    tEE: float = 9999
    R_EE_triggered: float = 0.0
    tCLIQ: np.ndarray = 9999
    directionCurrentCLIQ: np.ndarray = np.array([0])
    nCLIQ: np.ndarray = np.array([0])
    U0: np.ndarray = np.array([0])
    C: np.ndarray = np.array([0])
    Rcapa: np.ndarray = np.array([0])
    tQH: np.ndarray = np.array([9999])
    U0_QH: np.ndarray = np.array([0])
    C_QH: np.ndarray = np.array([0])
    R_warm_QH: np.ndarray = np.array([0])
    w_QH: np.ndarray = np.array([0])
    h_QH: np.ndarray = np.array([0])
    s_ins_QH: np.ndarray = np.array([0])
    type_ins_QH: np.ndarray = np.array([0])
    s_ins_QH_He: np.ndarray = np.array([0])
    type_ins_QH_He: np.ndarray = np.array([0])
    l_QH: np.ndarray = np.array([0])
    f_QH: np.ndarray = np.array([0])
    iQH_toHalfTurn_From: np.ndarray = np.array([0])
    iQH_toHalfTurn_To: np.ndarray = np.array([0])
    tQuench: np.ndarray = np.array([])
    initialQuenchTemp: np.ndarray = np.array([])
    iStartQuench: np.ndarray = np.array([1])
    tStartQuench: np.ndarray = np.array([9999])
    lengthHotSpot_iStartQuench: np.ndarray = np.array([0.01])
    fScaling_vQ_iStartQuench: np.ndarray = np.array([1.0])
    sim3D_uThreshold: float = 1e6
    sim3D_f_cooling_down: np.ndarray = np.array([0.0])
    sim3D_f_cooling_up: np.ndarray = np.array([0.0])
    sim3D_f_cooling_left: np.ndarray = np.array([0.0])
    sim3D_f_cooling_right: np.ndarray = np.array([0.0])
    sim3D_fExToIns: float = 1
    sim3D_fExUD: float = 1
    sim3D_fExLR: float = 1
    sim3D_min_ds_coarse: float = 0.1
    sim3D_min_ds_fine: float = 0.001
    sim3D_min_nodesPerStraightPart: int = 4
    sim3D_min_nodesPerEndsPart: int = 4
    sim3D_idxFinerMeshHalfTurn: np.ndarray = np.array([])
    sim3D_Tpulse_sPosition: float = 0.0
    sim3D_Tpulse_peakT: float = 20
    sim3D_Tpulse_width: float = 0.01
    sim3D_tShortCircuit: float = 1e9
    sim3D_coilSectionsShortCircuit: np.ndarray = np.array([0])
    sim3D_R_shortCircuit: float = 1e9
    sim3D_shortCircuitPosition: np.ndarray = np.array([0])
    sim3D_durationGIF: float = 20
    sim3D_flag_saveFigures: int = 1
    sim3D_flag_saveGIF: int = 1
    sim3D_flag_VisualizeGeometry3D: int = 1
    sim3D_flag_SaveGeometry3D: int = 1
    M_m: np.ndarray = np.array([])
    fL_I: np.ndarray = np.array([])
    fL_L: np.ndarray = np.array([])
    HalfTurnToInductanceBlock: np.ndarray = np.array([])
    M_InductanceBlock_m: np.ndarray = np.array([])

    f_RRR1_Cu_inGroup: np.ndarray = np.array([0])
    f_RRR2_Cu_inGroup: np.ndarray = np.array([0])
    f_RRR3_Cu_inGroup: np.ndarray = np.array([0])

    RRR1_Cu_inGroup: np.ndarray = np.array([0])
    RRR2_Cu_inGroup: np.ndarray = np.array([0])
    RRR3_Cu_inGroup: np.ndarray = np.array([0])

@dataclass
class LEDETOptions:
    time_vector_params: np.ndarray = np.array([])
    Iref: float = 0.0
    flagIron: float = 0.0
    flagSelfField: float = 0.0
    headerLines: float = 0.0
    columnsXY: np.ndarray = np.array([])
    columnsBxBy: np.ndarray = np.array([])
    flagPlotMTF: float = 0.0
    flag_typeWindings: float = 0.0
    flag_calculateInductanceMatrix: float = 0.0
    flag_useExternalInitialization: float = 0.0
    flag_initializeVar: float = 0.0
    flag_fastMode: float = 0.0
    flag_controlCurrent: float = 0.0
    flag_automaticRefinedTimeStepping: float = 0.0
    flag_IronSaturation: float = 0.0
    flag_InvertCurrentsAndFields: float = 0.0
    flag_ScaleDownSuperposedMagneticField: float = 0.0
    flag_HeCooling: float = 0.0
    fScaling_Pex: float = 0.0
    fScaling_Pex_AlongHeight: float = 0.0
    fScaling_MR: float = 0.0
    flag_scaleCoilResistance_StrandTwistPitch: float = 0.0
    flag_separateInsulationHeatCapacity: float = 0.0
    flag_persistentCurrents: float = 0.0
    flag_ISCL: float = 0.0
    fScaling_Mif: float = 0.0
    fScaling_Mis: float = 0.0
    flag_StopIFCCsAfterQuench: float = 0.0
    flag_StopISCCsAfterQuench: float = 0.0
    tau_increaseRif: float = 0.0
    tau_increaseRis: float = 0.0
    fScaling_RhoSS: float = 0.0
    maxVoltagePC: float = 0.0
    minCurrentDiode: float = 10
    flag_symmetricGroundingEE: float = 0.0
    flag_removeUc: float = 0.0
    BtX_background: float = 0.0
    BtY_background: float = 0.0
    flag_showFigures: float = 0.0
    flag_saveFigures: float = 0.0
    flag_saveMatFile: float = 0.0
    flag_saveTxtFiles: float = 0.0
    flag_generateReport: float = 0.0
    flag_hotSpotTemperatureInEachGroup: float = 0.0
    flag_3D: int = 0
    flag_adaptiveTimeStepping: int = 0
    sim3D_flag_Import3DGeometry: int = 0
    sim3D_import3DGeometry_modelNumber: int = 0

@dataclass
class LEDETPlots:
    suffixPlot: str = ''
    typePlot: int = 0
    outputPlotSubfolderPlot: str = ''
    variableToPlotPlot: np.ndarray = np.array([])
    selectedStrandsPlot: np.ndarray = np.array([])
    selectedTimesPlot: np.ndarray = np.array([])
    labelColorBarPlot: np.ndarray = np.array([])
    minColorBarPlot: float = 0.0
    maxColorBarPlot: float = 0.0
    MinMaxXYPlot: np.ndarray = np.array([])
    flagSavePlot: int = 0
    flagColorPlot: int = 0
    flagInvisiblePlot: int = 0

@dataclass
class LEDETVariables:
    variableToSaveTxt: np.ndarray = np.array([])
    typeVariableToSaveTxt: np.ndarray = np.array([])
    variableToInitialize: np.ndarray = np.array([])

@dataclass
class LEDETAuxiliary:
    # The following parameters are needed for conductor ordering
    strandToHalfTurn: np.ndarray = np.array([])
    strandToGroup: np.ndarray = np.array([])
    indexTstart: np.ndarray = np.array([])
    indexTstop: np.ndarray = np.array([])
    # The following parameters are needed for conductor definition
    type_to_group: np.ndarray = np.array([])  # TODO: change name, or make it obsolete
    f_SC_strand_inGroup: np.ndarray = np.array([])  # TODO: decide whether to implement calculation in BuilderLEDET()
    f_ST_strand_inGroup: np.ndarray = np.array([])  # TODO: decide whether to implement calculation in BuilderLEDET()
    # The following parameters are needed for thermal links calculation and options
    elPairs_GroupTogether: np.ndarray = np.array([])
    elPairs_RevElOrder: np.ndarray = np.array([])
    heat_exchange_max_distance: float = 0.0
    iContactAlongWidth_pairs_to_add: np.ndarray = np.array([])
    iContactAlongWidth_pairs_to_remove: np.ndarray = np.array([])
    iContactAlongHeight_pairs_to_add: np.ndarray = np.array([])
    iContactAlongHeight_pairs_to_remove: np.ndarray = np.array([])
    th_insulationBetweenLayers: np.ndarray = np.array([])
    # The following parameters are needed for self-mutual inductance calculation
    x_strands: np.ndarray = np.array([])  # TODO: add correct keys based on the ParserROXIE() parameters
    y_strands: np.ndarray = np.array([])  # TODO: add correct keys based on the ParserROXIE() parameters
    I_strands: np.ndarray = np.array([])  # TODO: add correct keys based on the ParserROXIE() parameters
