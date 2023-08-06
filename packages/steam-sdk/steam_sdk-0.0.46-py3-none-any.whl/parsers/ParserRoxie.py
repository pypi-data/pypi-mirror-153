import os
from pathlib import Path
import math
from math import *
import numpy as np
import yaml
from pydantic import BaseModel, PrivateAttr
from typing import (Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union, Type)

from builders import geometricFunctions
from data import DataRoxieParser as pd


def arcCenter(C, iL, oL, iR, oR, diff_radius=None):
    inner_radius = (np.sqrt(np.square(iL.x - C.x) + np.square(iL.y - C.y)) +
                    np.sqrt(np.square(iR.x - C.x) + np.square(iR.y - C.y))) / 2
    if diff_radius:
        outer_radius = inner_radius + diff_radius
    else:
        outer_radius = (np.sqrt(np.square(oL.x - C.x) + np.square(oL.y - C.y)) +
                        np.sqrt(np.square(oR.x - C.x) + np.square(oR.y - C.y))) / 2
    d_inner = [0.5 * abs((iR.x - iL.x)), 0.5 * abs((iL.y - iR.y))]
    d_outer = [0.5 * abs((oR.x - oL.x)), 0.5 * abs((oL.y - oR.y))]
    aa = [np.sqrt(np.square(d_inner[0]) + np.square(d_inner[1])),
          np.sqrt(np.square(d_outer[0]) + np.square(d_outer[1]))]
    bb = [np.sqrt(np.square(inner_radius) - np.square(aa[0])), np.sqrt(np.square(outer_radius) - np.square(aa[1]))]
    if iR.y < iL.y:
        M_inner = [iL.x + d_inner[0], iR.y + d_inner[1]]
        M_outer = [oL.x + d_outer[0], oR.y + d_outer[1]]
        if iR.y >= 0.:
            sign = [-1, -1]
        else:
            sign = [1, 1]
    else:
        M_inner = [iL.x + d_inner[0], iL.y + d_inner[1]]
        M_outer = [oL.x + d_outer[0], oL.y + d_outer[1]]
        if iR.y >= 0.:
            sign = [1, -1]
        else:
            sign = [-1, 1]
    inner = [M_inner[0] + sign[0] * bb[0] * d_inner[1] / aa[0], M_inner[1] + sign[1] * bb[0] * d_inner[0] / aa[0]]
    outer = [M_outer[0] + sign[0] * bb[1] * d_outer[1] / aa[1], M_outer[1] + sign[1] * bb[1] * d_outer[0] / aa[1]]
    return inner, outer


def sigDig(n):
    return np.format_float_positional(n, precision=8)


def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def evalContent(s, g):
    if isFloat(s):
        value = float(s)
    else:
        if any(item in s for item in '+-*/.(^'):
            if '^' in s:
                s = s.replace('^', '**')
            value = eval(s, g)
        else:
            value = g[s]
    return value


class ParserRoxie:
    """
        Class for the roxie parser
    """

    data: pd.APIdata = pd.APIdata()
    roxieData: pd.RoxieData = pd.RoxieData()
    rawData: pd.RoxieData = pd.RoxieData()

    dir_iron: Path = None
    dir_data: Path = None
    dir_cadata: Path = None

    no: int = None
    block: pd.Block = pd.Block()
    group: pd.Group = pd.Group()
    trans: pd.Trans = pd.Trans()
    condName: str = None
    cond_parameter: pd.CondPar = pd.CondPar()
    layer_radius = []

    def getIronYokeDataFromIronFile(self, iron_content: str = None, verbose: bool = False):
        """
            **Parse the content of the entire .iron file and store it in a IronDatabase object**

            Function returns a IronDatabase object that contains information about the iron yoke

            :param iron_content: .iron file content
            :type iron_content: str
            :param verbose: flag that determines whether the outputs are printed
            :type verbose: bool

            :return: IronDatabase
        """
        if verbose:
            print('File with iron database: {}'.format(self.dir_iron))

        functions = {'Cos': cos, 'Sin': sin, 'Tan': tan, 'Acos': acos, 'Asin': asin, 'Atan': atan, 'Sqrt': sqrt}

        data = self.data.iron

        designVariables = {}
        scalarVariables = {}
        corners = []
        bars = []

        if iron_content:
            fileNames = [1]
        else:
            fileNames = [self.dir_iron]
            path_iron = self.dir_iron.parent
            with open(fileNames[0]) as file:  # include .mod files
                fileContent = file.read()
                if 'include' in fileContent:
                    for i in fileContent.split('\n'):  # content by row
                        if i.strip()[:7] == 'include':
                            fileNames.append(Path.joinpath(path_iron, i.strip()[8:].strip(' )')))

        for f in fileNames:
            if isinstance(f, Path):
                file = open(f, "r")
                fileContent = file.read()
            else:
                fileContent = iron_content

            for i in fileContent.split('\n'):  # content by row
                fc = i.strip().strip(';')
                if (fc.strip()[:2] != '--') and (fc != '') and (fc.strip() != 'HyperMesh') and (
                        fc.strip()[:6] != 'Mirror') \
                        and (fc.strip()[:5] != 'Lmesh') and (fc.strip()[:7] != 'include') and (fc.strip()[0] != '#'):
                    if '--' in fc:  # is there a comment?
                        fc = fc[:fc.find('--')].strip().strip(';')

                    for j in fc.strip().split(';'):  # row content
                        statement = j.strip().split('=')

                        if j[:3] == 'dv ':  # design variable
                            designVariables[statement[0][3:].strip()] = \
                                evalContent(statement[1].strip(),
                                            {**designVariables, **scalarVariables, **data.key_points, **functions})

                        elif j[:2] == 'kp':  # key point
                            allGlobal = {**designVariables, **scalarVariables, **data.key_points, **functions}

                            if '@' in statement[1]:  # then the angle is specified
                                arg = statement[1].strip(' []').split('@')
                                A = [evalContent(arg[0].strip(), allGlobal), evalContent(arg[1].strip(), allGlobal)]
                                A = [A[0] * cos(A[1]), A[0] * sin(A[1])]
                            else:  # otherwise coordinates
                                arg = statement[1].strip(' []').split(',')
                                A = [evalContent(arg[0].strip(), allGlobal), evalContent(arg[1].strip(), allGlobal)]

                            data.key_points[statement[0].strip()] = pd.Coord(x=sigDig(A[0]), y=sigDig(A[1]))

                        elif j[:2] == 'ln':  # hyper line
                            statement[1] = statement[1].strip()
                            if statement[1][:5] == 'Hyper':
                                arguments = statement[1][10:-1].split(',')
                                lineType = arguments[2].strip(' "')

                                if lineType == 'Line':
                                    data.hyper_lines[statement[0].strip()] = pd.HyperLine(
                                        type='line', kp1=arguments[0].strip(), kp2=arguments[1].strip())

                                elif lineType[:6] == 'Corner':
                                    if lineType[6:] == 'Out':
                                        arg = arguments[0].strip() + arguments[1].strip() + 'Out'  # intersection point
                                        data.key_points[arg] = pd.Coord(
                                            x=data.key_points[arguments[1].strip()].x,
                                            y=data.key_points[arguments[0].strip()].y)
                                    else:
                                        arg = arguments[0].strip() + arguments[1].strip() + 'In'
                                        data.key_points[arg] = pd.Coord(x=data.key_points[arguments[0].strip()].x,
                                                                        y=data.key_points[arguments[1].strip()].y)

                                    corners.append(statement[0].strip())
                                    data.hyper_lines[statement[0].strip() + 'a'] = pd.HyperLine(
                                        type='line', kp1=arguments[0].strip(), kp2=arg)
                                    data.hyper_lines[statement[0].strip() + 'b'] = pd.HyperLine(
                                        type='line', kp1=arg, kp2=arguments[1].strip())

                                elif lineType == 'Bar':
                                    arg = [arguments[0].strip() + arguments[1].strip() + 'a',
                                           arguments[0].strip() + arguments[1].strip() + 'b']  # rectangle corner points
                                    A = [data.key_points[arguments[1].strip()].x,
                                         data.key_points[arguments[1].strip()].y]
                                    B = [data.key_points[arguments[0].strip()].x,
                                         data.key_points[arguments[0].strip()].y]
                                    if A[0] - B[0] != 0.0:
                                        alpha = math.atan((A[1] - B[1]) / (B[0] - A[0]))
                                    else:  # is the bar horizontal?
                                        alpha = math.pi / 2

                                    if len(arguments) == 3:  # is the height of the bar not specified?
                                        if alpha == math.pi / 2:
                                            h = (A[1] - B[1]) / 2
                                        else:
                                            h = (B[0] - A[0]) / 2 / math.cos(alpha)
                                    else:
                                        h = evalContent(arguments[3].strip(), {**designVariables, **scalarVariables,
                                                                               **data.key_points, **functions})

                                    data.key_points[arg[1]] = pd.Coord(x=sigDig(B[0] - h * math.sin(alpha)),
                                                                       y=sigDig(B[1] - h * math.cos(alpha)))
                                    data.key_points[arg[0]] = pd.Coord(
                                        x=sigDig(data.key_points[arg[1]].x + A[0] - B[0]),
                                        y=sigDig(data.key_points[arg[1]].y + A[1] - B[1]))

                                    bars.append(statement[0].strip())
                                    data.hyper_lines[statement[0].strip() + 'a'] = pd.HyperLine(
                                        type='line', kp1=arguments[0].strip(), kp2=arg[1])
                                    data.hyper_lines[statement[0].strip() + 'b'] = pd.HyperLine(
                                        type='line', kp1=arg[1], kp2=arg[0])
                                    data.hyper_lines[statement[0].strip() + 'c'] = pd.HyperLine(
                                        type='line', kp1=arg[0], kp2=arguments[1].strip())

                                elif lineType == 'Arc':
                                    arg = [arguments[0].strip(), arguments[1].strip()]
                                    if arguments[3].strip()[:2] == 'kp':
                                        arg.append(arguments[3].strip())

                                    else:  # is the radius of the arc provided?
                                        arg.append(arg[0] + arg[1][2:] + 'P3')
                                        D = 2 * evalContent(arguments[3].strip(),
                                                            {**designVariables, **scalarVariables,
                                                             **data.key_points, **functions})  # diameter

                                        A = [data.key_points[arg[1]].x, data.key_points[arg[1]].y]
                                        B = [data.key_points[arg[0]].x, data.key_points[arg[0]].y]
                                        M = [(B[0] + A[0]) / 2, (B[1] + A[1]) / 2]  # mid point
                                        dd = np.square(A[0] - B[0]) + np.square(A[1] - B[1])  # squared distance
                                        Dd = D * D - dd

                                        if Dd > 0.0:
                                            ss = (abs(D) - np.sqrt(Dd)) / 2  # compute sagitta
                                        else:
                                            ss = D / 2

                                        if M[1] - B[1] != 0.0:
                                            alpha = math.atan((B[0] - M[0]) / (M[1] - B[1]))
                                        else:
                                            alpha = math.pi / 2

                                        if A[0] == B[0]:
                                            # if B[0] == 0.0:
                                            #     sign = np.sign(ss)
                                            # else:
                                            sign = np.sign(B[1] - A[1])
                                        elif A[1] == B[1]:
                                            sign = np.sign(A[0] - B[0])
                                        else:
                                            if A[0] > B[0]:
                                                sign = np.sign((A[0] - B[0]) / (B[1] - A[1]))
                                            else:
                                                sign = np.sign((A[0] - B[0]) / (A[1] - B[1]))

                                        data.key_points[arg[2]] = pd.Coord(x=sigDig(M[0] + sign * ss * math.cos(alpha)),
                                                                           y=sigDig(M[1] + sign * ss * math.sin(alpha)))

                                    data.hyper_lines[statement[0].strip()] = pd.HyperLine(type='arc', kp1=arg[0],
                                                                                          kp2=arg[1], kp3=arg[2])

                                elif lineType == 'Circle':
                                    data.hyper_lines[statement[0].strip()] = pd.HyperLine(type='circle',
                                                                                          kp1=arguments[0].strip(),
                                                                                          kp2=arguments[1].strip())

                                elif lineType == 'EllipticArc':
                                    allGlobal = {**designVariables, **scalarVariables, **data.key_points, **functions}
                                    arg = [evalContent(arguments[3].strip(), allGlobal),
                                           evalContent(arguments[4].strip(), allGlobal)]  # axes of the ellipse
                                    data.hyper_lines[statement[0].strip()] = pd.HyperLine(type='ellipticArc',
                                                                                          kp1=arguments[0].strip(),
                                                                                          kp2=arguments[1].strip(),
                                                                                          arg1=arg[0], arg2=arg[1])

                                else:
                                    print(arguments[2].strip() + ' needs to be implemented')

                            elif statement[1][:4] == 'Line':
                                arguments = statement[1][5:-1].split(',')
                                data.hyper_lines[statement[0].strip()] = pd.HyperLine(type='line',
                                                                                      kp1=arguments[0].strip(),
                                                                                      kp2=arguments[1].strip())

                            else:
                                print(statement[1][:statement[1].find('(')] + ' needs to be implemented')

                        elif j[:2] == 'ar':  # area enclosed by hyper lines
                            statement[1] = statement[1].strip()
                            arguments = statement[1][10:-1].split(',')
                            arg = []
                            for k in range(len(arguments) - 1):
                                name = arguments[k].strip()
                                if name in corners:  # 2 lines are introduced for corners
                                    arg.extend([name + 'a', name + 'b'])
                                elif name in bars:  # 3 lines are introduced for bars
                                    arg.extend([name + 'a', name + 'b', name + 'c'])
                                else:
                                    arg.append(name)

                            data.hyper_areas[statement[0].strip()] = pd.HyperArea(material=arguments[-1].strip(),
                                                                                  lines=arg)

                        elif j[:2] == 'BH':
                            print('BH')

                        elif j[:11] == 'HyperHoleOf':
                            arguments = statement[0].strip()[12:-1].split(',')
                            data.hyper_holes[len(data.hyper_holes) + 1] = pd.HyperHole(areas=[arguments[0].strip(),
                                                                                              arguments[1].strip()])

                        else:  # scalar variables
                            scalarVariables[statement[0].strip()] = \
                                evalContent(statement[1].strip(),
                                            {**designVariables, **scalarVariables, **data.key_points, **functions})
            if isinstance(f, Path):
                file.close()

        return data

    def getConductorDataFromCadataFile(self, cadata_content: str = None, verbose: bool = False):
        """
            **Parse the content of the entire .cadata file and store it in a CableDatabase object**

            Function returns a CableDatabase object that contains information about all conductors

            :param cadata_content: .cadata file content
            :type cadata_content: str
            :param verbose: flag that determines whether the outputs are printed
            :type verbose: bool

            :return: CableDatabase
        """
        if verbose:
            print('File with cable database: {}'.format(self.dir_cadata))

        data = self.rawData.cadata  # self.data.cadata

        if cadata_content:
            fileContent = cadata_content
        else:
            file = open(self.dir_cadata, "r")
            fileContent = file.read()

        # separate rows
        fileContentByRow = fileContent.split("\n")

        for index in range(len(fileContentByRow)):
            fc = fileContentByRow[index]

            if fc[0:5] == "CABLE":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.cable[arg[1]] = pd.Cable(height=float(arg[2]), width_i=float(arg[3]), width_o=float(arg[4]),
                                                  ns=float(arg[5]), transp=float(arg[6]), degrd=float(arg[7]),
                                                  comment=" ".join(arg[8:]))

            elif fc[0:9] == "CONDUCTOR":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.conductor[arg[1]] = pd.Conductor(type=int(arg[2]), cableGeom=arg[3], strand=arg[4],
                                                          filament=arg[5], insul=arg[6], trans=arg[7], quenchMat=arg[8],
                                                          T_0=float(arg[9]), comment=" ".join(arg[10:]))
            elif fc[0:8] == "FILAMENT":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.filament[arg[1]] = pd.Filament(fildiao=float(arg[2]), fildiai=float(arg[3]), Jc_fit=arg[4],
                                                        fit=arg[5], comment=" ".join(arg[6:]))

            elif fc[0:5] == "INSUL":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.insul[arg[1]] = pd.Insulation(radial=float(arg[2]), azimut=float(arg[3]),
                                                       comment=" ".join(arg[4:]))

            elif fc[0:6] == "QUENCH":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.quench[arg[1]] = pd.Quench(SCHeatCapa=float(arg[2]), CuHeatCapa=float(arg[3]),
                                                    CuThermCond=float(arg[4]), CuElecRes=float(arg[5]),
                                                    InsHeatCapa=float(arg[6]), InsThermCond=float(arg[7]),
                                                    FillHeatCapa=float(arg[8]), He=float(arg[9]),
                                                    comment=" ".join(arg[10:]))
                # Add entry "NONE"
                data.quench["NONE"] = pd.Quench(SCHeatCapa=None, CuHeatCapa=None, CuThermCond=None, CuElecRes=None,
                                                InsHeatCapa=None, InsThermCond=None, FillHeatCapa=None,
                                                He=None, comment="")

            elif fc[0:6] == "STRAND":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.strand[arg[1]] = pd.Strand(diam=float(arg[2]), cu_sc=float(arg[3]), RRR=float(arg[4]),
                                                    Tref=float(arg[5]), Bref=float(arg[6]),
                                                    dJc_dB=float(arg[8]), comment=" ".join(arg[9:]))

            elif fc[0:9] == "TRANSIENT":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.transient[arg[1]] = pd.Transient(Rc=float(arg[2]), Ra=float(arg[3]), filTwistp=float(arg[4]),
                                                          filR0=float(arg[5]), fil_dRdB=float(arg[6]),
                                                          strandfillFac=float(arg[7]), comment=" ".join(arg[8:]))
                # Add entry "NONE"
                data.transient["NONE"] = pd.Transient(Rc=None, Ra=None, filTwistp=None, filR0=None,
                                                      fil_dRdB=None, strandfillFac=None, comment="")

            else:
                pass

        return data

    def getCoilDataFromDataFile(self, coil_content: str = None, verbose: bool = False):
        """
            **Parse the content of the entire .data file and store it in a Database object**

            Function returns a Database object that contains information about all conductors

            :param coil_content: .data file content
            :type coil_content: str
            :param verbose: flag that determines whether the outputs are printed
            :type verbose: bool

            :return: Database
        """
        if verbose:
            print('File with coil database: {}'.format(self.dir_data))

        data = self.rawData.coil

        # Define keywords
        keywords = {'group': {'key': 'LAYER ', 'index': 0},
                    'trans': {'key': 'EULER ', 'index': 0},
                    'block': {'key': 'BLOCK ', 'index': 0}}

        if coil_content:
            fileContent = coil_content
        else:
            file = open(self.dir_data, "r")
            fileContent = file.read()

        # Separate rows
        fileContentByRow = fileContent.split("\n")

        # Find group definition
        for i, row in enumerate(fileContentByRow):
            if keywords['group']['key'] in row:
                keywords['group']['index'] = i
            elif keywords['trans']['key'] in row:
                keywords['trans']['index'] = i
            elif keywords['block']['key'] in row:
                keywords['block']['index'] = i
            else:
                pass

        for key in keywords:
            firstRow = fileContentByRow[keywords[key]['index']]
            nRowsParameters = int(firstRow[5:])
            if verbose:
                print('{} definition parameters have {} row(s)'.format(key, nRowsParameters))

            # Separate part of the data with group definition information
            parameters = fileContentByRow[keywords[key]['index'] + 1:keywords[key]['index'] + 1 + nRowsParameters]

            # Assign parameters to a list of parameters objects
            for row in parameters:
                rowSplitStr = row.split()

                if key == 'group':
                    data.groups[rowSplitStr[0]] = pd.Group(symm=int(rowSplitStr[1]), typexy=int(rowSplitStr[2]),
                                                           blocks=list(map(int, rowSplitStr[3:-1])))
                elif key == 'trans':
                    data.transs[rowSplitStr[0]] = pd.Trans(x=float(rowSplitStr[1]), y=float(rowSplitStr[2]),
                                                           alph=float(rowSplitStr[3]), bet=float(rowSplitStr[4]),
                                                           string=str(rowSplitStr[5]), act=int(rowSplitStr[6]),
                                                           bcs=list(map(int, rowSplitStr[7:-1])))
                else:  # block
                    block_nr = int(rowSplitStr[0])
                    blocks_list = []
                    for group in data.groups:
                        blocks_list += data.groups[group].blocks
                        if block_nr in data.groups[group].blocks:
                            group_nr = int(group)
                            symm = data.groups[group].symm
                            if not data.transs:
                                coil = 1
                            else:
                                groups_list = []
                                trans_blocks_list = []
                                for trans in data.transs:
                                    if data.transs[trans].act == 1:
                                        groups_list += data.transs[trans].bcs
                                        if int(group) in data.transs[trans].bcs and data.transs[trans].string == \
                                                'SHIFT2':
                                            coil = int(trans)
                                    elif data.transs[trans].act == 3:
                                        trans_blocks_list += data.transs[trans].bcs
                                        if data.transs[trans].string == 'SHIFT2':
                                            coil = int(trans)
                                    else:
                                        raise Exception('Type of transformation not supported: check "ACT" under '
                                                        '"EULER" in the .data file.')
                    if 'coil' not in locals():
                        if block_nr not in blocks_list:
                            raise Exception('The current block does not belong to any group: check "LAYER" in the '
                                            '.data file.')
                        else:
                            if group_nr not in groups_list and block_nr not in trans_blocks_list:
                                raise Exception('The current block is not transformed or belongs to a group that is not'
                                                'transformed: check "BCS" under "EULER" in the .data file.')

                    radius = float(rowSplitStr[3])
                    if radius not in self.layer_radius:
                        self.layer_radius = self.layer_radius + [radius]
                        layer = len(self.layer_radius)
                    else:
                        layer = self.layer_radius.index(radius) + 1

                    turn = float(rowSplitStr[11])
                    if turn == 0:
                        pole = 1
                    else:
                        pole = turn * symm / 360 + 1

                    data.blocks[rowSplitStr[0]] = pd.Block(type=int(rowSplitStr[1]), nco=int(rowSplitStr[2]),
                                                           radius=radius, phi=float(rowSplitStr[4]),
                                                           alpha=float(rowSplitStr[5]), current=float(rowSplitStr[6]),
                                                           condname=rowSplitStr[7], n1=int(rowSplitStr[8]),
                                                           n2=int(rowSplitStr[9]), imag=int(rowSplitStr[10]),
                                                           turn=turn, coil=coil, pole=pole, layer=layer,
                                                           winding=block_nr, shift2=pd.Coord(x=0., y=0.),
                                                           roll2=pd.Roll(coor=pd.Coord(x=0., y=0.), alph=0.))

        # Print each parameters object in the list
        if verbose:
            for no in data.groups:
                arg = data.groups[no]  # group
                print('Parameters of group {}: (symmetry type: {}, group type: {}, block list: {}).'
                      .format(int(no), arg.symm, arg.typexy, arg.blocks))
            for no in data.transs:
                arg = data.transs[no]  # transformation
                print('Parameters of transformation {}:'
                      '(x: {}, y: {}, alpha: {}, bet: {}, string: {}, act: {}, bcs: {}).'
                      .format(int(no), arg.x, arg.y, arg.alph, arg.bet, arg.string, arg.act, arg.bcs))
            for no in data.blocks:
                arg = data.blocks[no]  # block
                print('Parameters of block {}:'
                      '(type: {}, nco: {}, radius: {}, phi: {}, alpha: {}, current: {}, condname: {},'
                      'n1: {}, n2: {}, imag: {}, turn: {}).'
                      .format(int(no), arg.type, arg.nco, arg.radius, arg.phi, arg.alpha,
                              arg.current, arg.condname, arg.n1, arg.n2, arg.imag, arg.turn))

        return data

    def applyMultipoleSymmetry(self, blocks: Dict[str, pd.Block] = None, group: pd.Group = None, verbose: bool = False):
        """
            **Apply N-order multipole symmetry to a list of blocks**

            Function returns the input list of blocks with new block appended

            :param blocks: list of blocks
            :type blocks: Dict
            :param group: group of blocks
            :type group: Group
            :param verbose: flag that determines whether the outputs are printed
            :type verbose: bool

            :return: list
        """
        if group:
            data = blocks
            self.group = group
            self.no = 1
        else:
            data = self.roxieData.coil.blocks

        # This index will increase with each added block
        nb = len(data)

        # Blocks to add to the attribute group.blocks
        blockToAddToGroup = []

        # Apply multipole geometry
        if self.group.typexy == 0:
            if verbose:
                print('typexy = {}: No symmetry action.'.format(self.group.typexy))

        elif self.group.typexy == 1:
            if verbose:
                print('typexy = {}: All.'.format(self.group.typexy))

            for additionalBlock in self.group.blocks:
                nOriginalBlocks = nb
                # idxBlock = additionalBlock - 1
                if verbose:
                    print('additionalBlock = {}'.format(additionalBlock))
                    print('pole={} of {}'.format(1, self.group.symm))

                block = data[str(additionalBlock)]  # self.blockParametersList[idxBlock]
                # Add return block to the original block
                nb += 1

                data[str(nb)] = pd.Block(type=block.type, nco=block.nco, radius=block.radius, phi=block.phi,
                                         alpha=block.alpha, current=-block.current, condname=block.condname,
                                         n1=block.n1, n2=block.n2, imag=1 - block.imag,
                                         turn=block.turn + 360 / self.group.symm, coil=self.no,
                                         pole=int((nb - nOriginalBlocks + 1) / 2), layer=block.layer,
                                         winding=additionalBlock, shift2=pd.Coord(x=0., y=0.),
                                         roll2=pd.Roll(coor=pd.Coord(x=0., y=0.), alph=0.))

                # Add return-line block index to group parameter list
                blockToAddToGroup = blockToAddToGroup + [nb]

                # This variable will switch between +1 and -1 for each pole
                signCurrent = +1

                # Add symmetric blocks
                for p in range(1, self.group.symm):
                    if verbose:
                        print('pole={} of {}'.format(p + 1, self.group.symm))

                    # Update current sign for this pole
                    signCurrent = signCurrent - 2 * np.sign(signCurrent)

                    # Add go-line block
                    nb += 1

                    data[str(nb)] = pd.Block(type=block.type, nco=block.nco, radius=block.radius, phi=block.phi,
                                             alpha=block.alpha, current=float(block.current * signCurrent),
                                             condname=block.condname, n1=block.n1, n2=block.n2, imag=block.imag,
                                             turn=block.turn + 360 / self.group.symm * p, coil=self.no, pole=int(p + 1),
                                             layer=block.layer, winding=additionalBlock, shift2=pd.Coord(x=0., y=0.),
                                             roll2=pd.Roll(coor=pd.Coord(x=0., y=0.), alph=0.))

                    tempBlock = data[str(nb)]

                    # Add return-line block index to group parameter list
                    blockToAddToGroup = blockToAddToGroup + [nb]

                    # Add return-line block to block parameter list
                    nb += 1

                    data[str(nb)] = pd.Block(type=tempBlock.type, nco=tempBlock.nco, radius=tempBlock.radius,
                                             phi=tempBlock.phi, alpha=tempBlock.alpha, current=-tempBlock.current,
                                             condname=tempBlock.condname, n1=tempBlock.n1, n2=tempBlock.n2,
                                             imag=1 - tempBlock.imag, turn=tempBlock.turn + 360 / self.group.symm,
                                             coil=self.no, pole=int((nb - nOriginalBlocks + 1) / 2),
                                             layer=tempBlock.layer, winding=additionalBlock,
                                             shift2=pd.Coord(x=0., y=0.),
                                             roll2=pd.Roll(coor=pd.Coord(x=0., y=0.), alph=0.))

                    # Add return-line block index to group parameter list
                    blockToAddToGroup = blockToAddToGroup + [nb]

        elif self.group.typexy == 2:
            if verbose:
                print('typexy = {}: One coil.'.format(self.group.typexy))

            for additionalBlock in self.group.blocks:
                nOriginalBlocks = nb
                if verbose:
                    print('additionalBlock = {}'.format(additionalBlock))

                block = data[str(additionalBlock)]
                nb += 1
                data[str(nb)] = pd.Block(type=block.type, nco=block.nco, radius=block.radius, phi=block.phi,
                                         alpha=block.alpha, current=-block.current, condname=block.condname,
                                         n1=block.n1, n2=block.n2, imag=1 - block.imag,
                                         turn=block.turn + 360 / self.group.symm, coil=self.no,
                                         pole=block.pole, layer=block.layer,
                                         winding=additionalBlock, shift2=pd.Coord(x=0., y=0.),
                                         roll2=pd.Roll(coor=pd.Coord(x=0., y=0.), alph=0.))

                # Add return-line block index to group parameter list
                blockToAddToGroup = blockToAddToGroup + [nb]

        elif self.group.typexy == 3:
            print('typexy = {}: Connection side: NOT SUPPORTED.'.format(self.group.typexy))

        else:
            print('typexy = {}: NOT SUPPORTED.'.format(self.group.typexy))

        self.group.blocks = self.group.blocks + blockToAddToGroup

        return data

    def applyCoilTransformation(self, coil: pd.Coil = None, trans: pd.Trans = None, verbose: bool = False):
        """
            **Apply shift2 transformation (shift in x and y direction) to a list of blocks,
            apply roll2 transformation (counterclockwise rotation) to a list of blocks**
            Function returns the input list of blocks with the attributes shift2 and roll2 set to new values

            :param trans: transformation data
            :type trans: Trans
            :param coil: blocks and groups data
            :type: coil: Coil
            :param verbose: flag that determines whether the outputs are printed
            :type verbose: bool

            :return: list
        """
        if trans:
            data = coil
            self.trans = trans
        else:
            data = self.roxieData.coil

        if self.trans.act == 0:
            if verbose:
                print('Act on All blocks.')
            for block in data.blocks:
                if self.trans.string == 'SHIFT2':
                    data.blocks[block].shift2.x = self.trans.x
                    data.blocks[block].shift2.y = self.trans.y
                elif self.trans.string == 'ROLL2':
                    data.blocks[block].roll2.coor.x = self.trans.x
                    data.blocks[block].roll2.coor.y = self.trans.y
                    data.blocks[block].roll2.alph = self.trans.alph

        elif self.trans.act == 1:
            if verbose:
                print('Act on All blocks of these groups: {}.'.format(self.trans.bcs))
            for group in data.groups:
                if int(group) in self.trans.bcs:
                    for block in data.blocks:
                        if int(block) in data.groups[group].blocks:
                            if self.trans.string == 'SHIFT2':
                                data.blocks[block].shift2.x = self.trans.x
                                data.blocks[block].shift2.y = self.trans.y
                            elif self.trans.string == 'ROLL2':
                                data.blocks[block].roll2.coor.x = self.trans.x
                                data.blocks[block].roll2.coor.y = self.trans.y
                                data.blocks[block].roll2.alph = self.trans.alph

        elif self.trans.act == 2:
            if verbose:
                print('Act on Parent and offspring blocks of these groups {}: Not supported!'.format(self.trans.bcs))

        elif self.trans.act == 3:
            if verbose:
                print('Act on Specified block only: Block {}'.format(self.trans.bcs))
            for block in data.blocks:
                if int(block) in self.trans.bcs:
                    if self.trans.string == 'SHIFT2':
                        data.blocks[block].shift2.x = self.trans.x
                        data.blocks[block].shift2.y = self.trans.y
                    elif self.trans.string == 'ROLL2':
                        data.blocks[block].roll2.coor.x = self.trans.x
                        data.blocks[block].roll2.coor.y = self.trans.y
                        data.blocks[block].roll2.alph = self.trans.alph

        elif self.trans.act == 4:
            print('Act on Conductors {}. Not supported!'.format(self.trans.bcs))

        else:
            print('Act on N/a: Not supported!')

        return data

    def applySymmetryConditions(self, coil: pd.Coil = None, verbose: bool = False):
        """
            **Returns updated list of blockParametersList objects, and sets attribute blockParametersList**

            Apply symmetry conditions to blocks

            :param coil: blocks, groups, and transformation data
            :type coil: Coil
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        """
        if coil:
            self.roxieData.coil = coil

        data = self.roxieData.coil

        symmetryTypes = {2: 'Dipole', 4: 'Quadrupole', 6: 'Sextupole', 8: 'Octupole', 10: 'Decapole', 12: 'Dodecapole',
                         31: 'Window frame dipole', 33: 'Window frame quadrupole', 41: 'Solenoid',
                         71: 'Periodic structure (wiggler)'}

        # Apply symmetry conditions to blocks
        for g, no in enumerate(data.groups):
            if not data.transs:
                self.no = 1
            else:
                for trans in data.transs:
                    if data.transs[trans].act == 1:
                        if int(no) in data.transs[trans].bcs and data.transs[trans].string == 'SHIFT2':
                            self.no = int(trans)
                        else:
                            self.no = 1
                    elif data.transs[trans].act == 3:
                        self.no = int(trans)

            self.group = data.groups[no]
            if self.group.symm == 0:
                if verbose:
                    print('Group {} has symmetry of type {} --> No symmetry.'.format(self.no, self.group.symm))

            elif 1 < self.group.symm < 13:
                if verbose:
                    print('Group {} has symmetry of type {} --> {} symmetry.'
                          .format(self.no, self.group.symm, symmetryTypes[self.group.symm]))
                self.applyMultipoleSymmetry(verbose=verbose)

            elif self.group.symm > 13:
                if verbose:
                    print('Group {} has symmetry of type {} --> {} symmetry. Not currently supported.'
                          .format(self.no, self.group.symm, symmetryTypes[self.group.symm]))

            else:
                if verbose:
                    print('Group {} has symmetry of type {} --> Not currently supported.'.format(self.no,
                                                                                                 self.group.symm))

        if verbose:
            print('Total number of blocks: {}'.format(len(data.blocks)))
            # Print each BlockParameters object in the list
            for bValue in data.blocks:
                print(bValue.toString())

        return data

    def applyTransformations(self, coil: pd.Coil = None, verbose: bool = False):
        """
            **Returns updated list of blockParametersList objects, and sets attribute blockParametersList**

            Apply transformations to blocks

            :param coil: blocks, groups, and transformation data
            :type coil: Coil
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        """
        if coil:
            self.roxieData.coil = coil

        # Apply transformations to blocks/transformations/conductors
        for no in self.roxieData.coil.transs:
            self.no = int(no)
            self.trans = self.roxieData.coil.transs[no]
            if self.trans.string == 'SHIFT2':
                if verbose:
                    print('trans {} applies a transformation of type {} --> Cartesian shift of x={} mm and y={} mm.'
                          .format(self.no, self.trans.string, self.trans.x, self.trans.y))
                self.applyCoilTransformation(verbose=verbose)

            elif self.trans.string == 'ROLL2':
                if verbose:
                    print('trans {} applies a transformation of type {} -->'
                          'Counterclockwise rotation of alpha={} deg around point x={} mm and y={} mm.'
                          .format(self.no, self.trans.string, self.trans.alph, self.trans.x, self.trans.y))
                self.applyCoilTransformation(verbose=verbose)

            elif self.trans.string == 'CONN2':
                if verbose:
                    print('trans {} applies a transformation of type {} -->'
                          'Connection of block vertices. Not currently supported. '.format(self.no, self.trans.string))

            elif self.trans.string == 'CONN2P':
                if verbose:
                    print('trans {} applies a transformation of type {} -->'
                          'Connection of block vertices to point XY. Not currently supported.'
                          .format(self.no, self.trans.string))

            else:
                if verbose:
                    print('trans {} applies a transformation of type {} --> Not currently supported.'
                          .format(self.no, self.trans.string))

        if verbose:
            print('Total number of blocks: {}'.format(len(self.roxieData.coil.blocks)))

        if verbose:
            # Print each BlockParameters object in the list
            for no in self.roxieData.coil.blocks:
                print(self.roxieData.coil.blocks[no])  # modify for printing content

        return self.roxieData.coil

    def getConductorFromCableDatabase(self, cadata: pd.Cadata = None):
        """
            ** Get the parameters of the selected conductor from an existing CableDatabase object **

            Function returns an outputConductorSigma object with the parameters of the selected conductor

            return: data
        """
        data = self.data.conductor

        if cadata:
            self.rawData.cadata = cadata

        # Import selected conductor data from cadata dictionary
        if self.condName not in data.conductor:
            data.conductor[self.condName] = self.rawData.cadata.conductor[self.condName]
            cond = data.conductor[self.condName]
            if cond.insul not in data.insul:
                data.insul[cond.insul] = self.rawData.cadata.insul[cond.insul]
            if cond.filament not in data.filament:
                data.filament[cond.filament] = self.rawData.cadata.filament[cond.filament]
            if cond.strand not in data.strand:
                data.strand[cond.strand] = self.rawData.cadata.strand[cond.strand]
            if cond.trans not in data.transient:
                data.transient[cond.trans] = self.rawData.cadata.transient[cond.trans]
            if cond.quenchMat not in data.quench:
                data.quench[cond.quenchMat] = self.rawData.cadata.quench[cond.quenchMat]
            if cond.cableGeom not in data.cable:
                data.cable[cond.cableGeom] = self.rawData.cadata.cable[cond.cableGeom]
        else:  # Select conductor by name
            cond = data.conductor[self.condName]

        # Parameters defining Insulation
        cond.parameters.wInsulNarrow = data.insul[cond.insul].radial * 1e-3
        cond.parameters.wInsulWide = data.insul[cond.insul].azimut * 1e-3

        # Parameters defining Filament
        cond.parameters.dFilament = data.filament[cond.filament].fildiao * 1e-6

        # Parameters defining Strand
        cond.parameters.dstrand = data.strand[cond.strand].diam * 1e-3
        cond.parameters.fracCu = data.strand[cond.strand].cu_sc / (1 + data.strand[cond.strand].cu_sc)
        cond.parameters.fracSc = 1 / (1 + data.strand[cond.strand].cu_sc)
        cond.parameters.RRR = data.strand[cond.strand].RRR
        cond.parameters.TupRRR = data.strand[cond.strand].Tref

        # Parameters defining Transient
        if cond.trans == 'NONE':
            cond.parameters.Rc = 0.
            cond.parameters.Ra = 0.
            cond.parameters.fRhoEff = 0.
            cond.parameters.lTp = 0.
        else:
            cond.parameters.Rc = data.transient[cond.trans].Rc
            cond.parameters.Ra = data.transient[cond.trans].Ra
            cond.parameters.fRhoEff = 1.
            cond.parameters.lTp = data.transient[cond.trans].filTwistp

        # Parameters defining Cable
        cond.parameters.wBare = data.cable[cond.cableGeom].height * 1e-3
        cond.parameters.hInBare = data.cable[cond.cableGeom].width_i * 1e-3
        cond.parameters.hOutBare = data.cable[cond.cableGeom].width_o * 1e-3
        cond.parameters.noOfStrands = int(data.cable[cond.cableGeom].ns)
        if cond.parameters.noOfStrands == 1:
            cond.parameters.noOfStrandsPerLayer = 1
            cond.parameters.noOfLayers = 1
        else:  # Rutherford cable assumed
            cond.parameters.noOfStrandsPerLayer = int(cond.parameters.noOfStrands / 2)
            cond.parameters.noOfLayers = 2

        cond.parameters.lTpStrand = data.cable[cond.cableGeom].transp * 1e-3
        cond.parameters.wCore = 0.
        cond.parameters.hCore = 0.
        if cond.parameters.lTpStrand != 0:
            cond.parameters.thetaTpStrand = math.atan2((cond.parameters.wBare - cond.parameters.dstrand),
                                                       (cond.parameters.lTpStrand / 2))
        else:
            cond.parameters.thetaTpStrand = 0.

        cond.parameters.degradation = data.cable[cond.cableGeom].degrd / 100
        cond.parameters.C1 = 0.
        cond.parameters.C2 = 0.
        cond.parameters.fracHe = 0.
        cond.parameters.fracFillInnerVoids = 1.
        cond.parameters.fracFillOuterVoids = 1.

        cond.parameters.Top = cond.T_0

        self.cond_parameter = cond.parameters

        return data

    def findConductorPositions(self, block: pd.Block = None, conductor: pd.CondPar = None, verbose: bool = False):
        """
            **Returns conductor positions**

            Function to find conductor corner x-y positions and conductor current if the block has type "cos-theta"

            :param conductor: conductor parameters
            :type conductor: CondPar
            :param block: block data
            :type block: Block
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: CoilData
        """
        if block:
            self.block = block
            self.data = pd.APIdata()
            self.cond_parameter = conductor
            self.no = 1

        x0 = 0
        y0 = 0
        radius = self.block.radius / 1000  # in [m]
        phi = self.block.phi / 180 * math.pi  # in [rad]
        alpha = self.block.alpha / 180 * math.pi  # in [rad]
        # current = self.block.current
        # imag = block.imag
        turn = self.block.turn / 180 * math.pi  # in [rad]
        # x0Cond = block.radius / 1000  # in [m]
        y0Cond = self.block.phi / 1000  # in [m]
        # xTemp = x0Cond
        yTemp = y0Cond

        shiftX = self.block.shift2.x / 1e3  # in [m]
        shiftY = self.block.shift2.y / 1e3  # in [m]
        x0Roll = self.block.roll2.coor.x / 1e3  # in [m]
        y0Roll = self.block.roll2.coor.y / 1e3  # in [m]
        alphaRoll = self.block.roll2.alph / 180 * math.pi  # in [rad]

        wBare = self.cond_parameter.wBare
        hInBare = self.cond_parameter.hInBare
        hOutBare = self.cond_parameter.hOutBare
        # hBare = (hInBare + hOutBare) / 2
        wInsulNarrow = self.cond_parameter.wInsulNarrow
        wInsulWide = self.cond_parameter.wInsulWide
        nColumns = self.cond_parameter.noOfStrandsPerLayer
        nLayers = self.cond_parameter.noOfLayers

        #     print('conductorSigma.name = {}'.format(conductorSigma.name))
        #     print('wBare = {}'.format(wBare))
        #     print('hInBare = {}'.format(hInBare))
        #     print('hOutBare = {}'.format(hOutBare))
        #     print('wInsulNarrow = {}'.format(wInsulNarrow))
        #     print('wInsulWide = {}'.format(wInsulWide))

        # Define the coefficients of the circle on which the x2 points (bottom-left) of each conductor rest
        # R, x0, and y0 coefficients of the circle, as in: (x-x0)**2 + (y-y0)**2 = R**2
        circle = [radius, x0, y0]

        # Define x/y positions, including conductor rotation of angle=alpha around origin (x0Cond,y0Cond)
        alphaTemp = alpha
        # phiTemp = phi
        if verbose:
            print('Initial alpha = {} deg'.format(alpha / math.pi * 180))
            print('Initial phi = {} deg'.format(phi / math.pi * 180))

        # xBare = []
        # yBare = []
        # x = []
        # y = []
        # xS = []
        # yS = []
        # # I = []

        # Create coil, pole, layer, and winding keys if they are not present
        if self.block.coil not in self.data.coil.coils:
            self.data.coil.coils[self.block.coil] = pd.Pole()
        coil = self.data.coil.coils[self.block.coil]
        coil.bore_center = pd.Coord(x=shiftX, y=shiftY)
        if self.block.pole not in coil.poles:
            coil.poles[self.block.pole] = pd.Layer()
        pole = coil.poles[self.block.pole]
        if self.block.layer not in pole.layers:
            pole.layers[self.block.layer] = pd.Winding()
        layer = pole.layers[self.block.layer]
        if self.block.winding not in layer.windings:
            layer.windings[self.block.winding] = \
                pd.WindingData(nco=self.block.nco, cable_current=float(sigDig(abs(self.block.current))),
                               conductor_name=self.block.condname,
                               strand_current=float(sigDig(abs(self.block.current / self.cond_parameter.noOfStrands))))
        winding = layer.windings[self.block.winding]

        # Initialize object for this block
        winding.blocks[self.no] = pd.BlockData(block_corners=pd.Corner(), current_sign=int(np.sign(self.block.current)))
        block = winding.blocks[self.no]

        for c in range(self.block.nco):
            block.half_turns[c + 1] = pd.HalfTurn(corners=pd.HalfTurnCorner())

            # Calculate coordinates of four corner of bare and insulated conductor
            if self.block.type == 1:  # cos-theta
                xR = radius * math.cos(phi)
                yR = radius * math.sin(phi)
                sinAlpha = math.sin(alphaTemp)
                cosAlpha = math.cos(alphaTemp)

                xBareCable = [xR + wInsulNarrow * cosAlpha - (hInBare + wInsulWide) * sinAlpha,
                              xR + wInsulNarrow * cosAlpha - wInsulWide * sinAlpha,
                              xR + (wBare + wInsulNarrow) * cosAlpha - wInsulWide * sinAlpha,
                              xR + (wBare + wInsulNarrow) * cosAlpha - (hOutBare + wInsulWide) * sinAlpha]
                yBareCable = [yR + wInsulNarrow * sinAlpha + (hInBare + wInsulWide) * cosAlpha,
                              yR + wInsulNarrow * sinAlpha + wInsulWide * cosAlpha,
                              yR + (wBare + wInsulNarrow) * sinAlpha + wInsulWide * cosAlpha,
                              yR + (wBare + wInsulNarrow) * sinAlpha + (hOutBare + wInsulWide) * cosAlpha]

                xCable = [xR - (hInBare + 2 * wInsulWide) * sinAlpha,
                          xR,
                          xR + (wBare + 2 * wInsulNarrow) * cosAlpha,
                          xR - (hOutBare + 2 * wInsulWide) * sinAlpha + (wBare + 2 * wInsulNarrow) * cosAlpha]
                yCable = [yR + (hInBare + 2 * wInsulWide) * cosAlpha,
                          yR,
                          yR + (wBare + 2 * wInsulNarrow) * sinAlpha,
                          yR + (wBare + 2 * wInsulNarrow) * sinAlpha + (hOutBare + 2 * wInsulWide) * cosAlpha]

                # Increase inclination angle by atan( (h2-h1)/w )
                alphaTemp = alphaTemp + math.atan2((hOutBare - hInBare), (wBare + 2 * wInsulNarrow))

                # Find line through points 1 and 4 of the current conductor (top-left and top-right)
                # A, B, and C coefficients of the line, as in: A*x + B*y + C = 0
                line = geometricFunctions.findLineThroughTwoPoints([xCable[0], yCable[0]], [xCable[3], yCable[3]],
                                                                   verbose=verbose)

                # Find the intersection points between the circle and the line just defined
                xy = geometricFunctions.intersectLineCircle(line, circle, verbose=verbose)

                # Find the one of two intersection points that is closest to the x2 point of the current conductor
                if xy[0] == [None, None] and xy[1] == [None, None]:
                    raise ValueError('No intersection points were found! [{},{}] and [{},{}].'
                                     .format(xCable[0], yCable[0], xCable[1], yCable[1]))
                elif xy[0] == [None, None] and xy[1] != [None, None]:
                    next_x2, next_y2 = xy[0][0], xy[0][1]
                    if verbose:
                        print('One intersection point was found and selected: [{},{}].'.format(next_x2, next_y2))
                else:
                    dist1 = math.sqrt((xCable[1] - xy[0][0]) ** 2 + (yCable[1] - xy[0][1]) ** 2)
                    dist2 = math.sqrt((xCable[1] - xy[1][0]) ** 2 + (yCable[1] - xy[1][1]) ** 2)
                    if dist1 <= dist2:
                        next_x2, next_y2 = xy[0][0], xy[0][1]
                    else:
                        next_x2, next_y2 = xy[1][0], xy[1][1]
                    if verbose:
                        print('Two intersection points were found: [{},{}] and [{},{}].'.format(xy[0][0], xy[0][1],
                                                                                                xy[1][0], xy[1][1]))
                        print('The closest point was selected: [{},{}].'.format(next_x2, next_y2))

                # Find new phi angle: the angle between the X-axis and the line joining [next_x2,next_y2] and [x0,y0]
                phi = math.atan2(next_y2 - y0, next_x2 - x0)

                if verbose:
                    print('phi = {} rad'.format(phi))
                    print('phi = {} deg'.format(phi / math.pi * 180))

            elif self.block.type == 2:  # block-coil
                xBareCable = [radius + wInsulNarrow, radius + wInsulNarrow,  # x0Cond + wInsulNarrow
                              radius + (wBare + wInsulNarrow), radius + (wBare + wInsulNarrow)]
                yBareCable = [yTemp + (hInBare + wInsulWide), yTemp + wInsulWide,
                              yTemp + wInsulWide, yTemp + (hInBare + wInsulWide)]

                xCable = [radius, radius,  # x0Cond
                          radius + (wBare + 2 * wInsulNarrow), radius + (wBare + 2 * wInsulNarrow)]
                yCable = [yTemp + (hInBare + 2 * wInsulWide), yTemp,
                          yTemp, yTemp + (hInBare + 2 * wInsulWide)]

                # Update xTemp and yTemp (using insulated conductor positions)
                # xTemp = xTemp
                yTemp = yTemp + (hInBare + 2 * wInsulWide)

            else:
                raise Exception('Block {} is of unknown type: {}. Not supported'.format(self.no, self.block.type))

            if self.block.type == 2:  # block-coil
                # Apply conductor rotation of angle=alpha around origin (x0Cond,y0Cond)
                for i, arg in enumerate(xBareCable):
                    (xBareCable[i], yBareCable[i]) = geometricFunctions.rotatePoint((xBareCable[i], yBareCable[i]),
                                                                                    (radius, y0Cond), alpha)
                    (xCable[i], yCable[i]) = geometricFunctions.rotatePoint((xCable[i], yCable[i]),
                                                                            (radius, y0Cond), alpha)

            # Mirror conductor about the X-axis
            if self.block.imag == 1:
                yBareCable = [-i for i in yBareCable]
                yCable = [-i for i in yCable]
            elif self.block.imag == 0:
                pass
            else:
                raise Exception('Value of variable imag must be either 0 or 1. It is {} instead.'
                                .format(self.block.imag))

            for i, arg in enumerate(xBareCable):
                # Apply conductor rotation of angle=turn around origin (x0,y0)
                (xBareCable[i], yBareCable[i]) = geometricFunctions.rotatePoint((xBareCable[i], yBareCable[i]),
                                                                                (x0, y0), turn)
                (xCable[i], yCable[i]) = geometricFunctions.rotatePoint((xCable[i], yCable[i]), (x0, y0), turn)

                # Apply roll2 counterclockwise rotation transformation
                (xBareCable[i], yBareCable[i]) = geometricFunctions.rotatePoint((xBareCable[i], yBareCable[i]),
                                                                                (x0Roll, y0Roll), alphaRoll)
                (xCable[i], yCable[i]) = geometricFunctions.rotatePoint((xCable[i], yCable[i]), (x0Roll, y0Roll),
                                                                        alphaRoll)

                # Apply shift2 cartesian shift transformation
                xBareCable[i], yBareCable[i] = xBareCable[i] + shiftX, yBareCable[i] + shiftY
                xCable[i], yCable[i] = xCable[i] + shiftX, yCable[i] + shiftY

            # Store cable positions
            block.half_turns[c + 1].corners.insulated = pd.Corner(iL=pd.Coord(x=sigDig(xCable[0]), y=sigDig(yCable[0])),
                                                                  iR=pd.Coord(x=sigDig(xCable[1]), y=sigDig(yCable[1])),
                                                                  oR=pd.Coord(x=sigDig(xCable[2]), y=sigDig(yCable[2])),
                                                                  oL=pd.Coord(x=sigDig(xCable[3]), y=sigDig(yCable[3])))
            block.half_turns[c + 1].corners.bare = pd.Corner(
                iL=pd.Coord(x=sigDig(xBareCable[0]), y=sigDig(yBareCable[0])),
                iR=pd.Coord(x=sigDig(xBareCable[1]), y=sigDig(yBareCable[1])),
                oR=pd.Coord(x=sigDig(xBareCable[2]), y=sigDig(yBareCable[2])),
                oL=pd.Coord(x=sigDig(xBareCable[3]), y=sigDig(yBareCable[3])))

            # if c == self.block.nco - 1:
            #     block.block_corners.iL = pd.Coord(x=sigDig(xCable[0]), y=sigDig(yCable[0]))  # 1
            #     block.block_corners.oL = pd.Coord(x=sigDig(xCable[3]), y=sigDig(yCable[3]))  # 4
            # elif c == 0:
            #     block.block_corners.iR = pd.Coord(x=sigDig(xCable[1]), y=sigDig(yCable[1]))  # 2
            #     block.block_corners.oR = pd.Coord(x=sigDig(xCable[2]), y=sigDig(yCable[2]))  # 3
            # else:
            #     pass
            if c == self.block.nco - 1:
                corner0 = [xCable[0], yCable[0]]  # 1
                corner3 = [xCable[3], yCable[3]]  # 4
            elif c == 0:
                corner1 = [xCable[1], yCable[1]]  # 2
                corner2 = [xCable[2], yCable[2]]  # 3
            else:
                pass

                # pd.BlockData(corner={'1': pd.Coord(x=x[-1][0], y=y[-1][0]),
                #                      '2': pd.Coord(x=x[0][1], y=y[0][1]),
                #                      '3': pd.Coord(x=x[0][2], y=y[0][2]),
                #                      '4': pd.Coord(x=x[-1][3], y=y[-1][3])})
            # xBare.append(xBareCable)
            # yBare.append(yBareCable)
            # x.append(xCable)
            # y.append(yCable)
            # # I.append(current)

            # Find strand positions
            alphaS = math.atan2(yBareCable[2] - yBareCable[1], xBareCable[2] - xBareCable[1])
            sinAlphaS = math.sin(alphaS)
            cosAlphaS = math.cos(alphaS)
            for j in range(nLayers):
                block.half_turns[c + 1].strand_groups[j + 1] = pd.StrandGroup()

                for k in range(nColumns):
                    arg = [wBare / nColumns * (k + 1 / 2),
                           (hInBare + (hOutBare - hInBare) * (k + 1 / 2) / nColumns) * (j + 1 / 2) / nLayers]
                    if self.block.imag == 0:
                        xStrand = xBareCable[1] + arg[0] * cosAlphaS - arg[1] * sinAlphaS
                        yStrand = yBareCable[1] + arg[0] * sinAlphaS + arg[1] * cosAlphaS
                    elif self.block.imag == 1:
                        xStrand = xBareCable[1] + arg[0] * cosAlphaS + arg[1] * sinAlphaS
                        yStrand = yBareCable[1] + arg[0] * sinAlphaS - arg[1] * cosAlphaS
                    else:
                        raise Exception('Value of variable imag must be either 0 or 1. It is {} instead.'
                                        .format(self.block.imag))

                    # Store strand position
                    block.half_turns[c + 1].strand_groups[j + 1].strand_positions[k + 1] = pd.Coord(x=sigDig(xStrand),
                                                                                                    y=sigDig(yStrand))

                    # xS.append(xStrand)
                    # yS.append(yStrand)
                    # # iS.append(currentStrand)

        new_corners_inner = geometricFunctions.intersectLineCircle(
            geometricFunctions.findLineThroughTwoPoints(corner0, corner3),
            [radius, coil.bore_center.x, coil.bore_center.y])
        if min(abs(new_corners_inner[0][0] - corner0[0]),
               abs(new_corners_inner[1][0] - corner0[0])) == abs(new_corners_inner[0][0] - corner0[0]):
            new_inner = new_corners_inner[0]
        else:
            new_inner = new_corners_inner[1]
        outer_radius = (np.sqrt(np.square(corner2[0] - coil.bore_center.x) +
                                np.square(corner2[1] - coil.bore_center.y)))
        new_corners_outer = geometricFunctions.intersectLineCircle(
            geometricFunctions.findLineThroughTwoPoints(corner0, corner3),
            [outer_radius, coil.bore_center.x, coil.bore_center.y])
        if min(abs(new_corners_outer[0][0] - corner0[0]),
               abs(new_corners_outer[1][0] - corner0[0])) == abs(new_corners_outer[0][0] - corner0[0]):
            new_outer = new_corners_outer[0]
        else:
            new_outer = new_corners_outer[1]
        if corner0[0] < corner1[0]:
            block.block_corners.iL = pd.Coord(x=sigDig(new_inner[0]), y=sigDig(new_inner[1]))  # 1
            block.block_corners.oL = pd.Coord(x=sigDig(new_outer[0]), y=sigDig(new_outer[1]))  # 4
            block.block_corners.iR = pd.Coord(x=sigDig(corner1[0]), y=sigDig(corner1[1]))  # 2
            block.block_corners.oR = pd.Coord(x=sigDig(corner2[0]), y=sigDig(corner2[1]))  # 3
        else:
            block.block_corners.iR = pd.Coord(x=sigDig(new_inner[0]), y=sigDig(new_inner[1]))
            block.block_corners.oR = pd.Coord(x=sigDig(new_outer[0]), y=sigDig(new_outer[1]))
            block.block_corners.iL = pd.Coord(x=sigDig(corner1[0]), y=sigDig(corner1[1]))
            block.block_corners.oL = pd.Coord(x=sigDig(corner2[0]), y=sigDig(corner2[1]))

        # ((block.pole % 2 == 0) * np.sign(-I[0]) +
        #  (block.pole % 2 != 0) * np.sign(I[0])) * block.radius / 1e3]

        return self.data.coil

    def getCablePositions(self, blocks: Dict[str, pd.Block] = None, cadata: pd.Cadata = None, verbose: bool = False):
        """
            **Returns insulated and bare conductor positions, and strand positions**

            Find insulated and bare conductor positions, and strand positions

            :param cadata: conductor data
            :type cadata: Cadata
            :param blocks: blocks data
            :type blocks: Dict[str, Block]
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        """
        blockTypes = {1: 'Cos-theta', 2: 'Block-coil'}

        if blocks:
            self.roxieData.coil.blocks = blocks

        for no in self.roxieData.coil.blocks:
            self.no = int(no)
            self.block = self.roxieData.coil.blocks[no]

            # Get desired conductor data
            self.condName = self.block.condname
            self.getConductorFromCableDatabase(cadata=cadata)

            # Calculate x/y positions of the conductor corners and strands
            if verbose:
                print('Block {} is of type {} --> {}.'.format(self.no, self.block.type, blockTypes[self.block.type]))
            self.findConductorPositions(verbose=verbose)

        # if verbose:
        #     print('Total number of conductors (half-turns): {}'.format(len(self.xPos)))

        return self.data.coil

    def getWedgePositions(self, coil: pd.CoilData = None, verbose: bool = False):
        """
            **Returns wedge positions**

            Find wedge positions

            :param coil: coil data
            :type coil: CoilData
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        """
        if coil:
            self.data.coil = coil

        wedge_no = 0
        for coil_nr, coil in self.data.coil.coils.items():
            for pole_nr, pole in coil.poles.items():
                for layer_nr, layer in pole.layers.items():
                    for winding_key, winding in layer.windings.items():
                        if winding_key < max(layer.windings.keys()) and winding_key + 1 in layer.windings.keys():
                            adj_winding = layer.windings[winding_key + 1]
                            blocks = list(winding.blocks.keys())
                            adj_blocks = list(adj_winding.blocks.keys())

                            for block_key, block in winding.blocks.items():
                                wedge_no += 1
                                self.data.wedges[wedge_no] = pd.Wedge()
                                wedge = self.data.wedges[wedge_no]
                                wedge.coil = coil_nr

                                if blocks.index(block_key) == 0:
                                    corners1 = block.block_corners
                                    corners2 = adj_winding.blocks[adj_blocks[0]].block_corners
                                else:
                                    corners2 = block.block_corners
                                    corners1 = adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners

                                if corners1.iR.y >= 0.:
                                    wedge.corners = pd.Corner(iL=corners2.iR, iR=corners1.iL,
                                                              oL=corners2.oR, oR=corners1.oL)
                                else:
                                    wedge.corners = pd.Corner(iL=corners1.iR, iR=corners2.iL,
                                                              oL=corners1.oR, oR=corners2.oL)

                                wedge.corrected_center = pd.CenterShift()
                                inner, outer = arcCenter(C=coil.bore_center, iL=wedge.corners.iL, iR=wedge.corners.iR,
                                                         oL=wedge.corners.oL, oR=wedge.corners.oR)
                                wedge.corrected_center.inner = pd.Coord(x=float(sigDig(inner[0])),
                                                                        y=float(sigDig(inner[1])))
                                wedge.corrected_center.outer = pd.Coord(x=float(sigDig(outer[0])),
                                                                        y=float(sigDig(outer[1])))

        return self.data.wedges

    def getData(self, dir_iron: Path = None, dir_data: Path = None, dir_cadata: Path = None,
                dump_yamls: bool = False, verbose: bool = False):
        """
            **Returns all data**

            :param dir_iron: directory for .iron file
            :type dir_iron: Path
            :param dir_data: directory for .data file
            :type dir_data: Path
            :param dir_cadata: directory for .cadata file
            :type dir_cadata: Path
            :param dump_yamls: flag that determines whether the dictionary is dumped into yaml
            :type dump_yamls: bool
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        """
        # Re-initialize dictionaries
        self.data: pd.APIdata = pd.APIdata()
        self.roxieData: pd.RoxieData = pd.RoxieData()
        self.rawData: pd.RoxieData = pd.RoxieData()

        # Acquire iron yoke data from the .iron Roxie file
        if dir_iron:
            self.dir_iron = dir_iron
            self.getIronYokeDataFromIronFile(verbose=verbose)

        if dir_data and dir_cadata:
            # Acquire conductor data from the .cadata Roxie file
            self.dir_cadata = dir_cadata
            self.getConductorDataFromCadataFile(verbose=verbose)

            # Acquire coil data from the .data Roxie file
            self.dir_data = dir_data
            self.getCoilDataFromDataFile(verbose=verbose)

            # Save raw data from original Roxie files
            if dump_yamls:
                with open('raw_data.yaml', 'w') as yaml_file:
                    yaml.dump(self.rawData.dict(), yaml_file, default_flow_style=False)

            # Apply simmetry conditions and transformations to the original winding blocks
            self.roxieData = self.rawData
            self.applySymmetryConditions(verbose=verbose)
            self.applyTransformations(verbose=verbose)

            # Save comprehensive Roxie data after manipulation (inherits from the raw data)
            if dump_yamls:
                with open('roxie_data.yaml', 'w') as yaml_file:
                    yaml.dump(self.roxieData.dict(), yaml_file, default_flow_style=False)

            # Compute half turn positions (bare conductors, insulated conductors, strands)
            self.getCablePositions(verbose=verbose)

            # Compute wedge positions
            self.getWedgePositions(verbose=verbose)

            # Save data for API
            if dump_yamls:
                with open('data.yaml', 'w') as yaml_file:
                    yaml.dump(self.data.dict(), yaml_file, default_flow_style=False)

        return self.data
