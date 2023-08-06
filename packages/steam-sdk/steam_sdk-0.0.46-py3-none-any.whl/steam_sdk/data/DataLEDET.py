import numpy as np
from dataclasses import dataclass


"""
    These classes define the four LEDET dataclasses, which contain the variables to write in the four sheets of a LEDET 
    input file: Inputs, Options, Plots and Variables.
"""
@dataclass
class LEDETInputs:
    T00: float = None
    l_magnet: float = None
    I00: float = None
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
    t_PC: float = None
    t_PC_LUT: np.ndarray = np.array([])
    I_PC_LUT: np.ndarray = np.array([])
    R_circuit: float = None
    R_crowbar: float = None
    Ud_crowbar: float = None
    tEE: float = None
    R_EE_triggered: float = None
    tCLIQ: np.ndarray = None
    directionCurrentCLIQ: np.ndarray = np.array([])
    nCLIQ: np.ndarray = np.array([])
    U0: np.ndarray = np.array([])
    C: np.ndarray = np.array([])
    Rcapa: np.ndarray = np.array([])
    tQH: np.ndarray = np.array([])
    U0_QH: np.ndarray = np.array([])
    C_QH: np.ndarray = np.array([])
    R_warm_QH: np.ndarray = np.array([])
    w_QH: np.ndarray = np.array([])
    h_QH: np.ndarray = np.array([])
    s_ins_QH: np.ndarray = np.array([])
    type_ins_QH: np.ndarray = np.array([])
    s_ins_QH_He: np.ndarray = np.array([])
    type_ins_QH_He: np.ndarray = np.array([])
    l_QH: np.ndarray = np.array([])
    f_QH: np.ndarray = np.array([])
    iQH_toHalfTurn_From: np.ndarray = np.array([])
    iQH_toHalfTurn_To: np.ndarray = np.array([])
    tQuench: np.ndarray = np.array([])
    initialQuenchTemp: np.ndarray = np.array([])
    iStartQuench: np.ndarray = np.array([1])
    tStartQuench: np.ndarray = np.array([])
    lengthHotSpot_iStartQuench: np.ndarray = np.array([])
    fScaling_vQ_iStartQuench: np.ndarray = np.array([])
    sim3D_uThreshold: float = None
    sim3D_f_cooling_down: np.ndarray = np.array([])
    sim3D_f_cooling_up: np.ndarray = np.array([])
    sim3D_f_cooling_left: np.ndarray = np.array([])
    sim3D_f_cooling_right: np.ndarray = np.array([])
    sim3D_fExToIns: float = None
    sim3D_fExUD: float = None
    sim3D_fExLR: float = None
    sim3D_min_ds_coarse: float = None
    sim3D_min_ds_fine: float = None
    sim3D_min_nodesPerStraightPart: int = None
    sim3D_min_nodesPerEndsPart: int = None
    sim3D_idxFinerMeshHalfTurn: np.ndarray = np.array([])
    sim3D_Tpulse_sPosition: float = None
    sim3D_Tpulse_peakT: float = None
    sim3D_Tpulse_width: float = None
    sim3D_tShortCircuit: float = None
    sim3D_coilSectionsShortCircuit: np.ndarray = np.array([])
    sim3D_R_shortCircuit: float = None
    sim3D_shortCircuitPosition: np.ndarray = np.array([])
    sim3D_durationGIF: float = None
    sim3D_flag_saveFigures: int = None
    sim3D_flag_saveGIF: int = None
    sim3D_flag_VisualizeGeometry3D: int = None
    sim3D_flag_SaveGeometry3D: int = None
    M_m: np.ndarray = np.array([])
    fL_I: np.ndarray = np.array([])
    fL_L: np.ndarray = np.array([])
    HalfTurnToInductanceBlock: np.ndarray = np.array([])
    M_InductanceBlock_m: np.ndarray = np.array([])

    f_RRR1_Cu_inGroup: np.ndarray = np.array([])
    f_RRR2_Cu_inGroup: np.ndarray = np.array([])
    f_RRR3_Cu_inGroup: np.ndarray = np.array([])
    RRR1_Cu_inGroup: np.ndarray = np.array([])
    RRR2_Cu_inGroup: np.ndarray = np.array([])
    RRR3_Cu_inGroup: np.ndarray = np.array([])

@dataclass
class LEDETOptions:
    time_vector_params: np.ndarray = np.array([])
    Iref: float = None
    flagIron: int = None
    flagSelfField: int = None
    headerLines: int = None
    columnsXY: np.ndarray = np.array([])
    columnsBxBy: np.ndarray = np.array([])
    flagPlotMTF: int = None
    fieldMapNumber: int = None
    flag_typeWindings: int = None
    flag_calculateInductanceMatrix: int = None
    flag_useExternalInitialization: int = None
    flag_initializeVar: int = None
    flag_fastMode: int = None
    flag_controlCurrent: int = None
    flag_automaticRefinedTimeStepping: int = None
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
    flag_showFigures: int = None
    flag_saveFigures: int = None
    flag_saveMatFile: int = None
    flag_saveTxtFiles: int = None
    flag_generateReport: int = None
    flag_hotSpotTemperatureInEachGroup: int = None
    flag_3D: int = None
    flag_adaptiveTimeStepping: int = None
    sim3D_flag_Import3DGeometry: int = None
    sim3D_import3DGeometry_modelNumber: int = None

@dataclass
class LEDETPlots:
    suffixPlot: str = ''
    typePlot: int = None
    outputPlotSubfolderPlot: str = ''
    variableToPlotPlot: np.ndarray = np.array([])
    selectedStrandsPlot: np.ndarray = np.array([])
    selectedTimesPlot: np.ndarray = np.array([])
    labelColorBarPlot: np.ndarray = np.array([])
    minColorBarPlot: float = None
    maxColorBarPlot: float = None
    MinMaxXYPlot: np.ndarray = np.array([])
    flagSavePlot: int = None
    flagColorPlot: int = None
    flagInvisiblePlot: int = None

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
    heat_exchange_max_distance: float = None
    iContactAlongWidth_pairs_to_add: np.ndarray = np.array([])
    iContactAlongWidth_pairs_to_remove: np.ndarray = np.array([])
    iContactAlongHeight_pairs_to_add: np.ndarray = np.array([])
    iContactAlongHeight_pairs_to_remove: np.ndarray = np.array([])
    th_insulationBetweenLayers: np.ndarray = np.array([])
    # The following parameters are needed for self-mutual inductance calculation
    nStrands_inGroup_ROXIE: np.ndarray = np.array([])
    x_strands: np.ndarray = np.array([])  # TODO: add correct keys based on the ParserROXIE() parameters
    y_strands: np.ndarray = np.array([])  # TODO: add correct keys based on the ParserROXIE() parameters
    I_strands: np.ndarray = np.array([])  # TODO: add correct keys based on the ParserROXIE() parameters
