from pydantic import BaseModel
from typing import (List)

"""
    These classes define the four PyBBQ dataclasses, which contain the variables to write in the PyBBQ 
    input file.
"""

class DataPyBBQ(BaseModel):
    # Cable geometry and operating values:
    width: float = None
    height: float = None
    CuSC: float = None
    non_void: float = None
    shape: str = None
    strands: int = None # New
    strand_dmt: float = None # New
    layers: int = None
    insulation_thickness: float = None
    busbar_length: float = None
    T1: float = None

    # Magnetic Field
    Calc_b_from_geometry: bool = None
    Background_Bx: float = None
    Background_By: float = None
    Background_Bz: float = None
    Self_Field: float = None
    B0_dump: bool = None

    # Materials:
    material: str = None            # New
    tapetype: str = None            # New
    RRR: float = None               # New
    Jc_4K_5T_NbTi: float = None     # New

    # Load
    Current: float = None
    Inductance: float = None
    DumpR: float = None

    # Cooling
    c5: float = None                # New
    c6: float = None                # New
    p: float = None                 # New
    Pmax: float = None              # New
    Helium_cooling: bool = None
    Helium_cooling_internal: bool = None    # New
    Wetted_p: float = None          # New

    # Protection and Detection
    Detection_Voltage: float = None
    Protection_Delay: float = None

    # Analysis
    Tref: float = None              # New
    Posref: List[float] = None      # New

    # Solver setting:
    output: bool = None
    dt: float = None
    t0: List[float] = []
    sections: int = None # Moved
    print_every: int = None     # New
    store_every: int = None     # New
    plot_every: int = None      # New
    sim_name: str = None        # New


