from pydantic import BaseModel
from typing import (List, Union, Literal)


class ConstantJc(BaseModel):
    """
        Level 3: Class for setting constant Jc
    """
    type: Literal['Constant Jc']
    Jc_constant: float = None  # [A/m^2]


class Bottura(BaseModel):
    """
        Level 3: Class for setting Bottura fit
    """
    type: Literal['Bottura']
    Tc0_Bottura: float = None  # [K]
    Bc20_Bottura: float = None  # [T]
    Jc_ref_Bottura: float = None  # [A/m^2]
    C0_Bottura: float = None  # [-]
    alpha_Bottura: float = None  # [-]
    beta_Bottura: float = None  # [-]
    gamma_Bottura: float = None  # [-]


class CUDI1(BaseModel):
    """
        Level 3: Class for Nb-Ti fit based on "Fit 1" in CUDI manual
    """
    type: Literal['CUDI1']
    Tc0_CUDI1: float = None  # [K]
    Bc20_CUDI1: float = None  # [T]
    C1_CUDI1: float = None  # [A]
    C2_CUDI1: float = None  # [A/T]


class CUDI3(BaseModel):
    """
        Level 3: Class for Nb-Ti fit based on "Fit 3" in CUDI manual
    """
    type: Literal['CUDI3']
    Tc0_CUDI3: float = None  # [K]
    Bc20_CUDI3: float = None  # [T]
    c1_CUDI3: float = None  # [-]
    c2_CUDI3: float = None  # [-]
    c3_CUDI3: float = None  # [-]
    c4_CUDI3: float = None  # [-]
    c5_CUDI3: float = None  # [-]
    c6_CUDI3: float = None  # [-]


class Summers(BaseModel):
    """
        Level 3: Class for cable Summer's Nb3Sn fit
    """
    type: Literal['Summers']
    Tc0_Summers: float = None  # [K]
    Bc20_Summers: float = None  # [T]
    Jc0_Summers: float = None  # [A*T^0.5/m^2]


class Bordini(BaseModel):
    """
        Level 3: Class for cable Bordini's Nb3Sn fit
    """
    type: Literal['Bordini']
    Tc0_Bordini: float = None  # [K]
    Bc20_Bordini: float = None  # [T]
    C0_Bordini: float = None  # [A*T/m^2]
    alpha_Bordini: float = None  # [-]


class BSCCO_2212_LBNL(BaseModel):
    """
        Level 3: Class for cable Bi-2212 fit developed in LBNL
    """
    # only ad-hoc fit [T. Shen, D. Davis, E. Ravaioli with LBNL, Berkeley, CA]
    type: Literal['BSCCO_2212_LBNL']
    f_scaling_Jc_BSCCO2212: float = None  # [-] used for the ad-hoc fit


# ------------------- Cable types ---------------------------#
class Mono(BaseModel):
    """
        Mono cable type: This is basically type of cable consisting of one strand - not really a cable
    """
    type: Literal['Mono']
    bare_cable_width: float = None
    bare_cable_height_low: float = None
    bare_cable_height_high: float = None
    bare_cable_height_mean: float = None
    th_insulation_along_width: float = None
    th_insulation_along_height: float = None
    # Fractions given with respect to the insulated conductor
    f_superconductor: float = None
    f_stabilizer: float = None  # (related to CuFraction in ProteCCT)
    f_insulation: float = None
    f_inner_voids: float = None
    f_outer_voids: float = None
    f_core: float = None
    # Available materials depend on the component and on the selected program
    material_insulation: str = None
    material_inner_voids: str = None
    material_outer_voids: str = None
    material_core: str = None


class Rutherford(BaseModel):
    """
        Rutherford cable type: for example LHC MB magnet cable
    """
    type: Literal['Rutherford']
    n_strands: int = None
    n_strand_layers: int = None
    n_strands_per_layers: int = None
    bare_cable_width: float = None
    bare_cable_height_low: float = None
    bare_cable_height_high: float = None
    bare_cable_height_mean: float = None
    th_insulation_along_width: float = None
    th_insulation_along_height: float = None
    width_core: float = None
    height_core: float = None
    strand_twist_pitch: float = None
    strand_twist_pitch_angle: float = None
    Rc: float = None
    Ra: float = None
    # Fractions given with respect to the insulated conductor
    f_superconductor: float = None
    f_stabilizer: float = None  # (related to CuFraction in ProteCCT)
    f_insulation: float = None
    f_inner_voids: float = None
    f_outer_voids: float = None
    f_core: float = None
    # Available materials depend on the component and on the selected program
    material_insulation: str = None
    material_inner_voids: str = None
    material_outer_voids: str = None
    material_core: str = None


class Ribbon(BaseModel):
    """
        Mono cable type: This is basically type of cable consisting of one strand - not really a cable
    """
    type: Literal['Ribbon']
    n_strands: int = None  # This defines the number of "strands" in the ribbon cable, which are physically glued but electrically in series
    bare_cable_width: float = None
    bare_cable_height_low: float = None
    bare_cable_height_high: float = None
    bare_cable_height_mean: float = None
    th_insulation_along_width: float = None  # This defines the thickness of the insulation around each strand (DIFFERENT FROM ROXIE CADATA FILE)
    th_insulation_along_height: float = None  # This defines the thickness of the insulation around each strand (DIFFERENT FROM ROXIE CADATA FILE)
    # Fractions given with respect to the insulated conductor
    f_superconductor: float = None
    f_stabilizer: float = None  # (related to CuFraction in ProteCCT)
    f_insulation: float = None
    f_inner_voids: float = None
    f_outer_voids: float = None
    f_core: float = None
    # Available materials depend on the component and on the selected program
    material_insulation: str = None
    material_inner_voids: str = None
    material_outer_voids: str = None
    material_core: str = None


# ------------------- Conductors ---------------------------#

class Round(BaseModel):
    """
        Level 2: Class for strand parameters
    """
    type: Literal['Round']
    diameter: float = None  # ds_inGroup (LEDET), DConductor (BBQ), DStrand (ProteCCT)
    Cu_noCu_in_strand: float = None
    RRR: float = None  # RRR_Cu_inGroup (LEDET), RRRStrand (ProteCCT)
    T_ref_RRR_high: float = None  # TupRRR (SIGMA), Reference temperature for RRR measurements
    T_ref_RRR_low: float = None  # CURRENTLY NOT USED
    fil_twist_pitch: float = None
    f_Rho_effective: float = None
    material_superconductor: str = None
    material_stabilizer: str = None
    filament_diameter: float = None  # df_inGroup (LEDET)

class Rectangular(BaseModel):
    """
        Level 2: Class for strand parameters
    """
    type: Literal['Rectangular']
    bare_width: float = None
    bare_height: float = None
    Cu_noCu_in_strand: float = None
    RRR: float = None  # RRR_Cu_inGroup (LEDET), RRRStrand (ProteCCT)
    T_ref_RRR_high: float = None  # TupRRR (SIGMA), Reference temperature for RRR measurements
    T_ref_RRR_low: float = None  # CURRENTLY NOT USED
    fil_twist_pitch: float = None
    f_Rho_effective: float = None
    bare_corner_radius: float = None
    material_superconductor: str = None
    material_stabilizer: str = None
    filament_diameter: float = None  # df_inGroup (LEDET)

# ------------------- Conductors ---------------------------#

class Conductor(BaseModel):
    """
        Level 1: Class for conductor parameters
    """
    name: str = None  # conductor name
    version: str = None
    case: str = None
    state: str = None
    # For the below 3 parts see: https://gitlab.cern.ch/steam/steam_sdk/-/blob/master/docs/STEAM_SDK_Conductor_structure.svg
    cable: Union[Rutherford, Mono, Ribbon] = {'type': 'Rutherford'}     # TODO: Busbar, Rope, Roebel, CORC, TSTC, CICC
    strand: Union[Round, Rectangular] = {'type': 'Round'}       # TODO: Tape, WIC
    Jc_fit: Union[ConstantJc, Bottura, CUDI1, CUDI3, Summers, Bordini, BSCCO_2212_LBNL] = {'type': 'CUDI1'}   # TODO: CUDI other numbers? , Roxie?
