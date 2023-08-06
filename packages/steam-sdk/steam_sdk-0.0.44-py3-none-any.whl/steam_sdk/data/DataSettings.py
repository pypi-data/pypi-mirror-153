from dataclasses import dataclass


@dataclass
class DataSettingsSTEAM:
    """
        Dataclass of settings for STEAM analyses
        This will be populated either form a local settings file (if flag_permanent_settings=False)
        or from the keys in the input analysis file (if flag_permanent_settings=True)
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