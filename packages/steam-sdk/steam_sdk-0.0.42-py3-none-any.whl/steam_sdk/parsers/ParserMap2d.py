import numpy as np
import math
from pathlib import Path


def parseRoxieMap2d(map2dFile: Path, headerLines: int = 1, verbose: bool = True):
    '''

        **Generates array-stream of values of map2dFile**
        :param map2dFile: path of map2dFile containing the content to parse
        :param headerLines: which index the header line is at - will start to read after that
        :param verbose: optional parameter, default True - if print information to user along parsing

    '''

    # Open map2dfile
    fileContent = open(map2dFile, "r").read()
    # Split content of file in rows
    fileContentByRow = fileContent.split("\n")
    # Create array-matrix to fill in with the values of the file
    output_matrix = np.array([[None for x in range(10)] for y in range(headerLines+1, len(fileContentByRow)-1)], dtype=float)

    # Assign values to the matrix row by row
    for index, rowContent in enumerate(fileContentByRow):
        if index > headerLines and rowContent:  #without header
            row = rowContent.split()
            output_array = np.array([])  # create temp. array
            output_array = np.append(output_array, int(row[0]))  # strands to groups
            output_array = np.append(output_array, int(row[1]))  # strands to halfturn
            output_array = np.append(output_array, float(row[2]))  # idx
            output_array = np.append(output_array, float(row[3])/1000)  # x_strands in [m]
            output_array = np.append(output_array, float(row[4])/1000)  # y_strands in [m]
            output_array = np.append(output_array, float(row[5]))  # Bx
            output_array = np.append(output_array, float(row[6]))  # By
            output_array = np.append(output_array, float(row[7])/1000000)  # Area in [m^2]
            output_array = np.append(output_array, float(row[8]))  # I_strands
            output_array = np.append(output_array, float(row[9]))  # fill factor
            output_matrix[index-headerLines-1] = output_array  # assign into matrix

    return output_matrix

def getParametersFromMap2d(map2dFile: Path, headerLines: int = 1, verbose: bool = True):
    """
        Load auxiliary parameters to self.Auxiliary parameters using magnetic field from ROXIE
        :param map2dFile: path of map2dFile containing the content to parse
        :param headerLines: which index the header line is at - will start to read after that
        :param verbose: optional parameter, default True - if print information to user along parsing
        :return param_dict: return dictionary with parameter names as keys and content as values
    """

    strandToGroup = np.array([])
    strandToHalfTurn = np.array([])
    idx, x_strands, y_strands, Bx, By, Area, I_strands, fillFactor = ([],) * 8

    fileContent = open(map2dFile, "r").read()
    fileContentByRow = fileContent.split("\n")
    for index, rowContent in enumerate(fileContentByRow):
        if index > headerLines and rowContent:
            row = rowContent.split()
            strandToGroup = np.hstack([strandToGroup, int(row[0])])
            strandToHalfTurn = np.hstack([strandToHalfTurn, int(row[1])])
            # idx = np.hstack([idx, float(row[2])])
            x_strands = np.hstack([x_strands, float(row[3]) / 1000])  # in [m]
            y_strands = np.hstack([y_strands, float(row[4]) / 1000])  # in [m]
            # Bx = np.hstack([Bx, float(row[5])])
            # By = np.hstack([By, float(row[6])])
            # Area = np.hstack([Area, float(row[7])])
            I_strands = np.hstack([I_strands, float(row[8])])
            # fillFactor = np.hstack([fillFactor, float(row[9])])

    strandToHalfTurn = np.int_(strandToHalfTurn)
    strandToGroup = np.int_(strandToGroup)

    # nT (has as many elements as groups. Each element defines the number of half-turns in that group)
    counter_nT = 1
    nT = []

    for i in range(1, len(strandToGroup)):
        if strandToHalfTurn[i] != strandToHalfTurn[i-1] and strandToGroup[i] == strandToGroup[i-1]: #counts the number of half-turns in the group by counting non-equal strandsToHalfTurn
            counter_nT += 1
        if strandToGroup[i] != strandToGroup[i-1] or i == len(strandToGroup) - 1: #the counted number is stored in the array and the counter restarts
            nT.append(counter_nT)
            counter_nT = 1

    # nStrands_inGroup (has as many elements as groups. Each element defines the number of strands in the conductor of that group)
    counter_nStrands_inGroup = 1
    nStrands_inGroup = []

    for i in range(1, len(strandToGroup)):
        if strandToGroup[i] == strandToGroup[i-1] and strandToHalfTurn[i] != strandToHalfTurn[i-1]:  #the number of equal strandsToHalfTurn are only counted once per group and otherwise resetted
            counter_nStrands_inGroup = 1
        elif strandToHalfTurn[i] == strandToHalfTurn[i - 1]:  #counts the number of strands in the group by counting equal strandsToHalfTurn
            counter_nStrands_inGroup += 1
        if strandToGroup[i] != strandToGroup[i - 1] or i == len(strandToGroup) - 1:  #the counted number is stored in the array and the counter restarts
            nStrands_inGroup.append(counter_nStrands_inGroup)
            counter_nStrands_inGroup = 1

    # I_strands (has as many elements as groups. Each element defines the polarity of the current in the conductor)
    sign = lambda x: math.copysign(1, x)
    polarities_inGroup = []

    for i in range(1, len(strandToGroup)):
        if strandToGroup[i] != strandToGroup[i-1] or i == len(strandToGroup) - 1:  #for each group the polarities is stored in the array
            polarities_inGroup.append(sign(I_strands[i-1]))


     # TODO: Check that the number of strands is the same as defined in the  model input .yaml file

    # print('nT:', nT)
    # print('nStrands_inGroup:', nStrands_inGroup)
    # print('polarities_inGroup:', polarities_inGroup)
    # print('strandToHalfTurn:', strandToHalfTurn)
    # print('strandToGroup:', strandToGroup)
    # print('x_strands:', x_strands)
    # print('y_strands:', y_strands)
    # print('I_strands:', I_strands)

    return nT, nStrands_inGroup, polarities_inGroup, strandToHalfTurn, strandToGroup, x_strands, y_strands, I_strands

    # typeWindings = DictionaryLEDET.lookupWindings(self.DataModelMagnet.Options_LEDET.input_generation_options.flag_typeWindings)
    # # Average half-turn positions
    # nHalfTurns = int(np.max(strandToHalfTurn))
    # x_ave, y_ave = [], []
    # for ht in range(1, nHalfTurns + 1):
    #     x_ave = np.hstack([x_ave, np.mean(x[np.where(strandToHalfTurn == ht)])])
    #     y_ave = np.hstack([y_ave, np.mean(y[np.where(strandToHalfTurn == ht)])])
    #
    # # Average group positions
    # x_ave_group, y_ave_group = [], []
    # nGroups = int(np.max(strandToGroup))
    # for g in range(1, nGroups + 1):
    #     x_ave_group = np.hstack([x_ave_group, np.mean(x[np.where(strandToGroup == g)])])
    #     y_ave_group = np.hstack([y_ave_group, np.mean(y[np.where(strandToGroup == g)])])

    # if typeWindings == 'multipole':
    #     # Define the magnetic coil
    #     definedMagneticCoil = MagneticCoil.MagneticCoil()
    #     xPos, yPos, iPos, xBarePos, yBarePos, xS, yS, iS = \
    #         MagneticCoil.MagneticCoil()(fileNameData, fileNameCadata, verbose=verbose)
    #     MagnetGeo = MagnetGeometry(xPos, yPos, iPos, xBarePos, yBarePos, xS, yS, iS, x, y, x_ave, y_ave,
    #                                x_ave_group, y_ave_group)

    # Reference current taken as the current in the first conductor appearing in the ROXIE .data file
    # if self.DataModelMagnet.Conductor.type.conductor_type == 'ribbon':
    #     print('Ribbon-cable conductor with {} strands selected.'.format(
    #         self.yaml_conductor_dict_leaves['n_strands_in_ribbon']))
    #     self.Magnet.Options.Iref = definedMagneticCoil.blockParametersList[0].current / \
    #                                self.yaml_conductor_dict_leaves['n_strands_in_ribbon']
    # else:
    #     self.Magnet.Options.Iref = definedMagneticCoil.blockParametersList[0].current


def modify_map2d_ribbon_cable(map2dFile: Path, geometry_ribbon_cable: list, list_flag_ribbon: list, verbose: bool = False):
    """
        **Edit (put values at their correct position) the current ROXIE field map due to its ribbon-cable properties**

        :param map2dFile: path of map2dFile containing the content to modify
        :param geometry_ribbon_cable: defines the distribution (Number of Layers) in the conductors (half turns) of each group
         of a ribbon-type conductor -> [No. of Layers, Conductor per Group]
        :param verbose: optional parameter, default True - if print information to user along parsing
        :return NewMap2d: return modified array-matrix with values now at the correct position like the ribbon-characteristcs
    """

    # Read file and get array-matrix-stream
    output_array_old = parseRoxieMap2d(map2dFile)

    # Create new array(matrix) with same properties as input array to assign values to its correct position
    NewMap2d = np.array([[None for x in range(10)]for y in range(len(output_array_old))], dtype=float)

    # Reorder values according to Arr_Ribbon_Dist
    # initialize counters
    counter_strands = 0
    counter_halfTurns = 0
    SumLayers = 0

    for k in range(len(geometry_ribbon_cable)):  # goes through each group of Arr_Ribbon_Dist, that defines each group--> [No. of Layers, Conductor per Group]
        for j in range(geometry_ribbon_cable[k][0]):  # goes through number of layers of each conductor
            if list_flag_ribbon[SumLayers]:  # groups
                for i in range(geometry_ribbon_cable[k][1]):  # goes through each conductor (half turn) of group
                    fc = output_array_old[j + i * geometry_ribbon_cable[k][0] + counter_strands]
                    NewMap2d[i + j * geometry_ribbon_cable[k][1] + counter_strands, :] = fc
                    NewMap2d[i + j * geometry_ribbon_cable[k][1] + counter_strands, 0] = j + SumLayers + 1  # groups
                    NewMap2d[i + j * geometry_ribbon_cable[k][1] + counter_strands, 1] = 1 + counter_halfTurns  # half-turns
                    NewMap2d[i + j * geometry_ribbon_cable[k][1] + counter_strands, 2] = 1 + i + j * geometry_ribbon_cable[k][1] + counter_strands  # strands
                    counter_halfTurns = counter_halfTurns+1
            else:  # special case when the cable is not a ribbon cable
                fc = output_array_old[j+counter_strands]
                NewMap2d[counter_strands+j, :] = fc
                NewMap2d[counter_strands+j, 0] = SumLayers + 1  # groups
                NewMap2d[counter_strands+j, 1] = counter_halfTurns + 1  # half-turns
                # no need to correct the strands
        if list_flag_ribbon[SumLayers]:  # groups
            counter_strands = counter_strands + geometry_ribbon_cable[k][0] * geometry_ribbon_cable[k][1]
            SumLayers = SumLayers + geometry_ribbon_cable[k][0]
        else:  # special case when the cable is not a ribbon cable
            counter_strands = counter_strands + geometry_ribbon_cable[k][0]
            counter_halfTurns = counter_halfTurns+1
            SumLayers = SumLayers + 1

    return NewMap2d

def create_map2d_file(matrix_map2d, header_line, output_file_location: Path, new_file_name: str, verbose: bool = False):

    NewMap2d = matrix_map2d

    # Write new .map2d File
    mat = np.matrix(NewMap2d)
    head = np.array(header_line.split()).transpose()
    head_merge = np.array([None for x in range(10)])
    for i in range(len(head_merge) - 1):
        head_merge[i] = head[i]
    head_merge[9] = head[9] + " " + head[10]
    mat = mat.astype(float)

    with open(output_file_location, 'wb') as f:
        np.savetxt(f, np.array([head_merge]), fmt="%s")
        np.savetxt(f, [""], fmt="%s")
        for row in mat:
            np.savetxt(f, row, fmt=["%i", "%i", "%i", "%.4f", "%.4f", "%.4f", "%.4f", "%.4f", "%.4f", "%.4f"])

    if verbose:
        print('File {} saved.'.format(new_file_name))


def multiply_column_by_value(matrix, column_number: int, multiplication_factor: float):
    matrix[:, column_number] = multiplication_factor * matrix[:, column_number]