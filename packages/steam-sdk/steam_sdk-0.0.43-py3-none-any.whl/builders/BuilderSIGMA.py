import os
from pathlib import Path
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import wrappers.java.SIGMA.WrapperSIGMA as ws

import plotters.PlotterSIGMA as p

from data import DataRoxieParser as pd
from data.DataModel import DataModel


class BuilderSIGMA:
    """
        Class to generate SIGMA models
    """

    def __init__(self, input_model_data: DataModel = None, input_roxie_data: pd.APIdata = None,
                 settings_dict: dict = None, output_path: str = None, flag_build: bool = True, verbose: bool = True):
        self.verbose: bool = verbose
        self.model_data: DataModel = input_model_data
        self.roxie_data: pd.APIdata = input_roxie_data
        self.settings_dict: dict = settings_dict
        self.output_path: str = output_path

        self.g = ws.GatewaySIGMA()
        self.a = ws.ArraysSIGMA

        self.conductor_name = str
        self.cableParameters = pd.CondPar
        # self.wedge_elements =
        # self.model =
        self.coil = []
        self.elements = {}
        self.coil_areas = []
        self.wedge_areas = []
        self.show_halfTurns = True  # to be provided by the yaml in the future

        if (not self.model_data or not self.roxie_data) and flag_build:
            raise Exception('Cannot build model without providing DataModel and RoxieData')
        elif flag_build:
            self.model_name = f"{self.model_data.GeneralParameters.magnet_name}_Model"

            self.bh_curve_database = os.path.join(Path(__file__).parent.parent.parent,
                                                  "steam_models", "magnets", "bh_curve_database.txt")

            self.COMSOL_exe_path = self.settings_dict['comsolexe_path']
            self.java_jdk_path = self.settings_dict['JAVA_jdk_path']

            self.COMSOL_compile_path = f"{self.COMSOL_exe_path[:-4]}compile.exe"
            self.COMSOL_batch_path = f"{self.COMSOL_exe_path[:-4]}batch.exe"

            self.model_java_file_path_save = f"{os.path.join(self.output_path, self.model_name)}.java"
            self.compile_batch_file_path = f"{os.path.join(self.output_path, self.model_name)}_Compile_and_Open.bat"
            self.model_java_file_path_bat = f"{os.path.join(self.output_path, self.model_name)}.java"
            self.model_class_file_path = f"{os.path.join(self.output_path, self.model_name)}.class"

            self.build_magnet()
            self.save_model_java()
            self.save_compile_and_open_bat()
            #self.plot_magnet()

    def build_magnet(self):
        self.coil_domain()
        self.iron_yoke_domain()
        self.wedge_domain()
        # # self.bh_curve()

    def mirrorXY(self, area):
        ar2 = area.mirrorY()
        return area, ar2, ar2.mirrorX(), area.mirrorX()

    def iron_yoke_domain(self):
        iron = self.roxie_data.iron

        keyPointsCOMSOL = {}
        hyperLinesCOMSOL = {}
        hyperAreasCOMSOL = {}

        for i in iron.key_points:
            keyPointsCOMSOL[i] = self.g.Point.ofCartesian(iron.key_points[i].x, iron.key_points[i].y)

        for i in iron.hyper_lines:
            if iron.hyper_lines[i].type == 'line':
                hyperLinesCOMSOL[i] = self.g.Line.ofEndPoints(keyPointsCOMSOL[iron.hyper_lines[i].kp1],
                                                              keyPointsCOMSOL[iron.hyper_lines[i].kp2])

            elif iron.hyper_lines[i].type == 'arc':
                hyperLinesCOMSOL[i] = self.g.Arc.ofThreePoints(keyPointsCOMSOL[iron.hyper_lines[i].kp1],
                                                               keyPointsCOMSOL[iron.hyper_lines[i].kp3],
                                                               keyPointsCOMSOL[iron.hyper_lines[i].kp2])

            elif iron.hyper_lines[i].type == 'ellipticArc':
                hyperLinesCOMSOL[i] = self.g.EllipticArc.ofEndPointsAxes(keyPointsCOMSOL[iron.hyper_lines[i].kp1],
                                                                         keyPointsCOMSOL[iron.hyper_lines[i].kp2],
                                                                         iron.hyper_lines[i].arg1,
                                                                         iron.hyper_lines[i].arg2)

            elif iron.hyper_lines[i].type == 'circle':
                hyperLinesCOMSOL[i] = self.g.Circumference.ofDiameterEndPoints(keyPointsCOMSOL[iron.hyper_lines[i].kp1],
                                                                               keyPointsCOMSOL[iron.hyper_lines[i].kp2])
            else:
                raise ValueError('Hyper line {} not supported'.format(iron.hyper_lines[i].type))

        for i in iron.hyper_areas:
            arg = [hyperLinesCOMSOL[j] for j in iron.hyper_areas[i].lines]  # lines for areas
            hyperAreasCOMSOL[i] = self.mirrorXY(self.g.Area.ofHyperLines(
                self.a.create_hyper_line_array(self.g.gateway, tuple(arg))))

        for i in hyperAreasCOMSOL:
            arg = []  # elements
            for j, ar in enumerate(hyperAreasCOMSOL[i]):
                arg.append(self.g.Element(f"IY{iron.hyper_areas[i].material[2:]}_{i}_El{j}", ar))

            self.elements[i] = self.a.create_element_array(self.g.gateway, tuple(arg))

    def cable_domain(self):
        self.g.cable.setLabel(self.conductor_name)
        self.g.cable.setwInsulNarrow(self.cableParameters.wInsulNarrow)
        self.g.cable.setwInsulWide(self.cableParameters.wInsulWide)
        self.g.cable.setdFilament(self.cableParameters.dFilament)
        self.g.cable.setDstrand(self.cableParameters.dstrand)
        self.g.cable.setFracCu(self.cableParameters.fracCu)
        self.g.cable.setFracSc(self.cableParameters.fracSc)
        self.g.cable.setRRR(self.cableParameters.RRR)
        self.g.cable.setTupRRR(self.cableParameters.TupRRR)
        self.g.cable.setTop(self.cableParameters.Top)
        self.g.cable.setRc(self.cableParameters.Rc)
        self.g.cable.setRa(self.cableParameters.Ra)
        self.g.cable.setfRhoEff(self.cableParameters.fRhoEff)
        self.g.cable.setlTp(self.cableParameters.lTp)
        self.g.cable.setwBare(self.cableParameters.wBare)
        self.g.cable.sethInBare(self.cableParameters.hInBare)
        self.g.cable.sethOutBare(self.cableParameters.hOutBare)
        self.g.cable.setNoOfStrands(self.cableParameters.noOfStrands)
        self.g.cable.setNoOfStrandsPerLayer(self.cableParameters.noOfStrandsPerLayer)
        self.g.cable.setNoOfLayers(self.cableParameters.noOfLayers)
        self.g.cable.setlTpStrand(self.cableParameters.lTpStrand)
        self.g.cable.setwCore(self.cableParameters.wCore)
        self.g.cable.sethCore(self.cableParameters.hCore)
        self.g.cable.setThetaTpStrand(self.cableParameters.thetaTpStrand)
        self.g.cable.setC1(self.cableParameters.C1)
        self.g.cable.setC2(self.cableParameters.C2)
        self.g.cable.setFracHe(self.cableParameters.fracHe)
        self.g.cable.setFracFillInnerVoids(self.cableParameters.fracFillInnerVoids)
        self.g.cable.setFractFillOuterVoids(self.cableParameters.fracFillOuterVoids)
        self.g.cable.setCriticalSurfaceFit(self.g.Cable.CriticalSurfaceFitEnum.Ic_NbTi_GSI)
        self.g.cable.setInsulationMaterial(self.g.MatDatabase.MAT_KAPTON)
        self.g.cable.setMaterialInnerVoids(self.g.MatDatabase.MAT_VOID)
        self.g.cable.setMaterialOuterVoids(self.g.MatDatabase.MAT_VOID)
        self.g.cable.setMaterialCore(self.g.MatDatabase.MAT_VOID)
        self.g.cable.setResitivityCopperFit(self.g.Cable.ResitivityCopperFitEnum.rho_Cu_CUDI)

    def coil_domain(self):
        poles = ()
        for coil_nr, coil in self.roxie_data.coil.coils.items():
            for pole_nr, pole in coil.poles.items():
                windings = ()
                for layer_nr, layer in pole.layers.items():
                    for winding_key, winding in layer.windings.items():
                        self.conductor_name = winding.conductor_name
                        self.cableParameters = self.roxie_data.conductor.conductor[winding.conductor_name].parameters
                        self.cable_domain()
                        areas = ()
                        currents = ()
                        for block_key, block in winding.blocks.items():
                            currents += (block.current_sign,)

                            kp0 = self.g.Point.ofCartesian(coil.bore_center.x, coil.bore_center.y)
                            arg = [self.g.Point.ofCartesian(block.block_corners.iL.x, block.block_corners.iL.y),
                                   self.g.Point.ofCartesian(block.block_corners.iR.x, block.block_corners.iR.y),
                                   self.g.Point.ofCartesian(block.block_corners.oR.x, block.block_corners.oR.y),
                                   self.g.Point.ofCartesian(block.block_corners.oL.x, block.block_corners.oL.y)]

                            areas += (self.g.Area.ofHyperLines(
                                self.a.create_hyper_line_array(self.g.gateway,
                                                               (self.g.Arc.ofEndPointsCenter(arg[0], arg[1], kp0),
                                                                self.g.Line.ofEndPoints(arg[1], arg[3]),
                                                                self.g.Arc.ofEndPointsCenter(arg[3], arg[2], kp0),
                                                                self.g.Line.ofEndPoints(arg[0], arg[2])))),)

                        self.coil_areas += [areas[0], areas[1]]
                        windings += (self.g.Winding.ofAreas(self.a.create_area_array(self.g.gateway, areas),
                                                            self.a.create_int_array(self.g.gateway, currents),
                                                            winding.nco, winding.nco, self.g.cable),)

                poles += (self.g.Pole.ofWindings(self.a.create_winding_array(self.g.gateway, windings)),)

        self.coil = self.g.Coil.ofPoles(self.a.create_pole_array(self.g.gateway, poles))

    # self.coil_areas = area + areaY
    # coil_areas_mirrored = []
    # for ar in self.coil_areas:
    #     new_ar = ar.mirrorX()
    #     coil_areas_mirrored.append(new_ar)
    # self.coil_areas = self.coil_areas + coil_areas_mirrored

    def wedge_domain(self):
        wedges = self.roxie_data.wedges

        elements = []
        for i in wedges:
            kp0_inner = self.g.Point.ofCartesian(wedges[i].corrected_center.inner.x, wedges[i].corrected_center.inner.y)
            kp0_outer = self.g.Point.ofCartesian(wedges[i].corrected_center.outer.x, wedges[i].corrected_center.outer.y)
            arg = [self.g.Point.ofCartesian(wedges[i].corners.iL.x, wedges[i].corners.iL.y),
                   self.g.Point.ofCartesian(wedges[i].corners.iR.x, wedges[i].corners.iR.y),
                   self.g.Point.ofCartesian(wedges[i].corners.oL.x, wedges[i].corners.oL.y),
                   self.g.Point.ofCartesian(wedges[i].corners.oR.x, wedges[i].corners.oR.y)]

            area = self.g.Area.ofHyperLines(self.a.create_hyper_line_array(
                self.g.gateway, (self.g.Arc.ofEndPointsCenter(arg[0], arg[1], kp0_inner),
                                 self.g.Line.ofEndPoints(arg[1], arg[3]),
                                 self.g.Arc.ofEndPointsCenter(arg[3], arg[2], kp0_outer),
                                 self.g.Line.ofEndPoints(arg[0], arg[2]))))
            self.wedge_areas += [area]

            elements.append(self.g.Element(f"Wedge_El{i}", area))

        self.wedge_elements = self.a.create_element_array(self.g.gateway, tuple(elements))

    def save_model_java(self):
        orderedElements = list(self.elements)
        # change order of generated domains to override correctly
        for hyper_hole_key, hyper_hole in self.roxie_data.iron.hyper_holes.items():
            index = [orderedElements.index(hyper_hole.areas[0]),
                     orderedElements.index(hyper_hole.areas[1])]
            if index[0] < index[1]:
                orderedElements.insert(index[1], orderedElements.pop(index[0]))

        # MAT_AIR, MAT_COIL, MAT_COPPER, MAT_KAPTON, MAT_GLASSFIBER, MAT_INSULATION_TEST, MAT_STEEL, MAT_IRON1,
        # MAT_IRON2, MAT_VOID, MAT_NULL, MAT_COIL_TEST, MAT_G10

        self.iron_yoke = [
            self.g.IronDomain(i, self.bh_curve_database, self.roxie_data.iron.hyper_areas[i].material, self.elements[i])
            for i in orderedElements]  # domains
        domains = self.iron_yoke

        domains.append(self.g.CoilDomain("CO", self.g.MatDatabase.MAT_COIL, self.coil))

        domains.append(self.g.WedgeDomain("W", self.g.MatDatabase.MAT_COPPER, self.wedge_elements))

        # Create magnet model
        cfg = self.g.ConfigSigma()

        cfg.setOutputModelPath(self.model_java_file_path_save)
        cfg.setExternalCFunLibPath(self.settings_dict['CFunLibPath'])

        srv = self.g.TxtSigmaServer(cfg.getOutputModelPath(), cfg.getComsolBatchPath())
        srv.connect(cfg.getComsolBatchPath())
        self.model = self.g.MagnetMPHBuilder(cfg, srv)

        self.model.buildMPH(self.a.create_domain_array(self.g.gateway, tuple(domains)))
        self.model.save()

        with open(self.model_java_file_path_save) as java_file:
            max_no_lines = 6e4
            public_indexes = []
            files = []
            content = java_file.readlines()
            for i, line in enumerate(content):
                if "public static" in line:
                    public_indexes += [i]

            no_lines = public_indexes[-1] - public_indexes[0]
            no_files = int(np.ceil(no_lines / max_no_lines))
            max_no_lines = round(no_lines / no_files)
            real_indexes = [public_indexes[i] - public_indexes[0] for i in range(len(public_indexes))]
            closest = [min(real_indexes, key=lambda x: abs(x - max_no_lines * (i + 1))) + public_indexes[0]
                       for i in range(no_files)]
            no_run = [int(content[i][content[i].index('run') + 3:content[i].index('(')]) for i in closest[0:-1]]
            no_run += [int(content[public_indexes[-2]][content[public_indexes[-2]].index('run')
                                                       + 3:content[public_indexes[-2]].index('(')]) + 1]
            additional_lines = {}
            for i in range(no_files):
                file_path = os.path.join(self.output_path, self.model_name)
                files += [open(file_path + '_%d.java' % i, 'w')]
                name = self.model_name + '_%d' % i
                # self.split_java_file_path_save += [f"{os.path.join(self.bat_path, self.model_name + '_%d' % i)}.java"]
                files[i].writelines(content[0:public_indexes[0] - 2] + ['public class ' + name + ' {\n', '\n'])
                if i == 0:
                    files[i].writelines('\tpublic static Model run1(Model mph) {\n')
                    files[i].writelines(content[public_indexes[0] + 2:closest[i]] + ['}\n'])
                    additional_lines[name] = {'start': 2, 'end': no_run[i] - 1}
                elif i + 1 == no_files:
                    files[i].writelines(content[closest[i - 1]:public_indexes[-1]] + ['}\n'])
                    additional_lines[name] = {'start': no_run[i - 1], 'end': len(public_indexes) - 1}
                else:
                    files[i].writelines(content[closest[i - 1]:closest[i]] + ['}\n'])
                    additional_lines[name] = {'start': no_run[i - 1], 'end': no_run[i] - 1}
                files[i].close()

        with open(self.model_java_file_path_save, 'w') as java_file:
            content = content[0:public_indexes[0] + 2] + ['\n'] + \
                      content[public_indexes[-1]:public_indexes[-1] + 2] + ['\t}\n'] + ['}\n']
            content.insert(public_indexes[0] + 2, '\t\tmph = ' + self.model_name + '_0.run1(mph);\n')
            ll = 1
            for name, item in additional_lines.items():
                for j in range(item['end'] - item['start'] + 1):
                    content.insert(public_indexes[0] + 2 + ll + j,
                                   '\t\tmph = ' + name + '.run' + str(item['start'] + j) + '(mph);\n')
                ll += j + 1
            content.insert(public_indexes[0] + 2 + ll, '\t\treturn mph;\n')
            content.insert(public_indexes[0] + 3 + ll, '\t}\n')
            java_file.writelines(content)

    def plot_magnet(self):
        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes()
        ax.set_xlim(0., 0.2)
        ax.set_ylim(-.1, 0.1)
        # p.plot_multiple_areas(ax, self.air_far_field_areas)  # air far field
        # p.plot_multiple_areas(ax, self.air_areas)  # air
        # p.plot_multiple_areas(ax, self.iron_yoke_areas)  # iron yoke
        # p.plot_multiple_areas(ax, self.wedges_areas)  # wedges
        if self.show_halfTurns:
            for coil_nr, coil in self.roxie_data.coil.coils.items():
                for pole_nr, pole in coil.poles.items():
                    for layer_nr, layer in pole.layers.items():
                        for winding_key, winding in layer.windings.items():
                            for block_key, block in winding.blocks.items():
                                for halfTurn_nr, halfTurn in block.half_turns.items():
                                    iL = halfTurn.corners.insulated.iL
                                    iR = halfTurn.corners.insulated.iR
                                    oL = halfTurn.corners.insulated.oL
                                    oR = halfTurn.corners.insulated.oR
                                    ax.add_line(lines.Line2D([iL.x, iR.x], [iL.y, iR.y], color='red'))
                                    ax.add_line(lines.Line2D([oL.x, oR.x], [oL.y, oR.y], color='red'))
                                    ax.add_line(lines.Line2D([oR.x, iR.x], [oR.y, iR.y], color='red'))
                                    ax.add_line(lines.Line2D([iL.x, oL.x], [iL.y, oL.y], color='red'))

        p.plot_multiple_areas(ax, self.coil_areas)
        p.plot_multiple_areas(ax, self.wedge_areas, color='blue')
        # #
        # ax.set_xlim(-self.input['air']['r'] * self.input['air']['r_ffs'],
        #             self.input['air']['r'] * self.input['air']['r_ffs'])
        # ax.set_ylim(-self.input['air']['r'] * self.input['air']['r_ffs'],
        #             self.input['air']['r'] * self.input['air']['r_ffs'])
        plt.show()

    def plot_bh_curve(self):
        hb = self.iron_yoke[0].getMaterial().getProperties()[3].getValue()
        b = []
        h = []
        for s in hb:
            b.append(float(s[0]))
            h.append(float(s[1]))
        df = pd.DataFrame(b, h)
        # df.plot()
        # print(df)

    def save_compile_and_open_bat(self):
        script_lines = [
            f'"{self.COMSOL_compile_path}" -jdkroot "{self.java_jdk_path}" "{self.model_java_file_path_bat}"',
            f'"{self.COMSOL_batch_path}" -inputfile "{self.model_class_file_path}" '
            f'-outputfile "{os.path.join(self.output_path, self.model_data.GeneralParameters.magnet_name)}.mph"',
            f'"{self.COMSOL_exe_path}" -open "{os.path.join(self.output_path, self.model_name)}.mph"']

        with open(self.compile_batch_file_path, "w") as outfile:
            outfile.write("\n".join(str(line) for line in script_lines))


if __name__ == "__main__":
    from parsers.ParserRoxie import ParserRoxie

    magnet_name = 'MQXF_V2'  # 'MQY_2in1'  #
    current_path = Path(__file__).parent
    path = Path.joinpath(current_path.parent, 'tests', 'builders', 'input', magnet_name)
    file_model_data = Path.joinpath(path, 'modelData_' + magnet_name + '.yaml')
    with open(file_model_data, "r") as stream:
        dictionary_yaml = yaml.safe_load(stream)
        model_data = DataModel(**dictionary_yaml)
    path_iron = Path.joinpath(path, model_data.Sources.iron_fromROXIE)
    path_data = Path.joinpath(path, model_data.Sources.coil_fromROXIE)
    path_cadata = Path.joinpath(path.parent, model_data.Sources.conductor_fromROXIE)

    roxie_parser = ParserRoxie()
    roxie_data = roxie_parser.getData(dir_data=path_data, dir_cadata=path_cadata, dir_iron=path_iron)
    # with open('../tests/parsers/references/cadata_REFERENCE.yaml', 'w') as yaml_file:
    #   yaml.dump(roxie_data.conductor.dict(), yaml_file, default_flow_style=False, sort_keys=False)

    bs = BuilderSIGMA(input_model_data=model_data, input_roxie_data=roxie_data)
    bs.build_magnet()
    bs.save_model_java()
    bs.save_compile_and_open_bat()
    bs.plot_magnet()
