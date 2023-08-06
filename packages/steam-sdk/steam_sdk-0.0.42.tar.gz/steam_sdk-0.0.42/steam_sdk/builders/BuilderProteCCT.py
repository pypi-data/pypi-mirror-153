import os
from pathlib import Path
import pandas as pd

from steam_sdk.data import DataModelMagnet, DictionaryProteCCT
from steam_sdk.data.DataProteCCT import ProteCCTInputs
from steam_sdk.parsers.ParserExcel import write2Excel
from steam_sdk.data.TemplateProteCCT import get_template_ProteCCT_input_sheet


class BuilderProteCCT:
    """
        Class to generate ProteCCT models
    """

    def __init__(self,
                 input_model_data: DataModelMagnet = None,
                 flag_build: bool = True,
                 verbose: bool = True):
        """
            Object is initialized by defining ProteCCT variable structure and file template.
            Optionally, the argument model_data can be passed to read the variables of a BuilderModel object.
            If flagInstantBuild is set to True, the ProteCCT input file is generated.
            If verbose is set to True, additional information will be displayed
        """
        # Unpack arguments
        self.verbose: bool = verbose
        self.model_data: DataModelMagnet = input_model_data

        # Data structure
        self.Inputs = ProteCCTInputs()

        if not self.model_data and flag_build:
            raise Exception('Cannot build model instantly without providing DataModelMagnet')

        if flag_build:
            # Add method to translate all ProteCCT parameters from model_data to ProteCCT dataclasses
            self.translateModelDataToProteCCT()

            # Load conductor data from DataModelMagnet keys, and calculate+set relevant parameters
            self.loadConductorData()

            # Edit the entry magnet_name (required for ProteCCT)
            self.Inputs.magnetIdentifier = '\"' + self.Inputs.magnetIdentifier


    def setAttribute(self, ProteCCTclass, attribute: str, value):
        try:
            setattr(ProteCCTclass, attribute, value)
        except:
            setattr(getattr(self, ProteCCTclass), attribute, value)


    def getAttribute(self, ProteCCTclass, attribute):
        try:
            return getattr(ProteCCTclass, attribute)
        except:
            return getattr(getattr(self, ProteCCTclass), attribute)


    def translateModelDataToProteCCT(self):
        """"
            Translates and sets parameters in self.DataModelMagnet to DataProteCCT if parameter exists in ProteCCT
        """
        # Transform DataModelMagnet structure to dictionary with dot-separated branches
        df = pd.json_normalize(self.model_data.dict(), sep='.')
        dotSepModelData = df.to_dict(orient='records')[0]

        for keyModelData, value in dotSepModelData.items():
            keyProteCCT = DictionaryProteCCT.lookupModelDataToProteCCT(keyModelData)
            if keyProteCCT:
                if keyProteCCT in self.Inputs.__annotations__:
                    self.setAttribute(self.Inputs, keyProteCCT, value)
                else:
                    print('Can find {} in lookup table but not in DataProteCCT'.format(keyProteCCT))


    def loadConductorData(self):
        '''
            Load selected conductor data from DataModelMagnet keys, check inputs, calculate and set missing variables
        '''

        # Check inputs and unpack variables
        if len(self.model_data.Conductors) > 1:
            raise Exception('For ProteCCT models, the key Conductors cannot contain more than one entry.')
        conductor_type = self.model_data.Conductors[0].cable.type
        if conductor_type != 'Mono':
            raise Exception('For ProteCCT models, the only supported cable type is Mono.')

        # Load variables
        DStrand   = self.model_data.Conductors[0].strand.diameter
        Cu_noCu   = self.model_data.Conductors[0].strand.Cu_noCu_in_strand
        RRRStrand = self.model_data.Conductors[0].strand.RRR

        # Calculate Cu fraction
        CuFraction = Cu_noCu / (1 + Cu_noCu)

        # Set calculated variables
        self.setAttribute(self.Inputs, 'DStrand',    DStrand)
        self.setAttribute(self.Inputs, 'CuFraction', CuFraction)
        self.setAttribute(self.Inputs, 'RRRStrand',  RRRStrand)
