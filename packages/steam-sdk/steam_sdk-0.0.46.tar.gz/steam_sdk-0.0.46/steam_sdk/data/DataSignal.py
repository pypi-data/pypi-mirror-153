from pydantic import BaseModel, PrivateAttr
from typing import (Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union, Type)


############################
# Signals
class Signal(BaseModel):
    """
        Level 2: Class for Configuration options
        - Each Signal is either measured, simulated, or measured+simulated comparison.
        - Each signal is obtained by summing together existing original signals (for example: summing voltage taps to obtain voltages across coil sections)
        - Multipliers can be defined to modify the original signal (for example: changing polarity, applying a gain)
        - The Signal is obtained with the cross product of original signals and multipliers
          (for example: If meas_signals_to_add=[V1, V2] and  meas_multipliers: [+2, -0.001] the defined signal will be V1*2-0.001*V2)

        Note: Meas = Measurement and Sim = simulation

        unit: Physical units of the signal (the same for meas and sim)
        meas_label: Label of the measured signal
        meas_signals_to_add: List of original signals to sum together to define a signal
        meas_multipliers: List of multipliers for the measured signals
        sim_label: Label of the simulated signal
        sim_signals_to_add: List of original signals to sum together to define a signal
        sim_multipliers: List of multipliers for the simulated signals
    """
    unit: str = None
    meas_label: str = None
    meas_signals_to_add: List[str] = []
    meas_multipliers: List[float] = []
    sim_label: str = None
    sim_signals_to_add: List[str] = []
    sim_multipliers: List[float] = []


############################
# Configuration
class Configuration(BaseModel):
    """
        Level 1: Class for Configuration options

        configuration_name: Name of the defined configuration (it will be called by the software)
        SignalList: List of defined signals (they could be measured, simulated, or measured+simulated comparison)

    """
    configuration_name: str = None
    SignalList: List[Signal] = [Signal(), Signal()]


############################
# Highest level
class DataSignal(BaseModel):
    '''
        **Class for the defining configuration of measured and simulated signals**

        This class contains the data structure of signals.

        :return: DataSignal object
    '''

    ConfigurationList: List[Configuration] = [Configuration()]
