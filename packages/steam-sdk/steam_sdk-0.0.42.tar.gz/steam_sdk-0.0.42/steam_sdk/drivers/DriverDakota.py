import sys
sys.path.append(r"E:\Python\steam-notebook-api")        # this is needed for PyLEDET imports to find steam_nb_api
pyL_path = r"E:\Python\pyLEDET"
sys.path.append(pyL_path)
import os
from runLEDET import Run_LEDET
import dakota.interfacing as di
import shutil
from pathlib import Path

LEDET_folder_path = r"D:\LEDET\LEDET_v2_01_27"
py_pro_path = r'C:\Dakota\bin\pyprepro.py'

params, result_for_dakota = di.read_parameters_file()


# make a separate copy of LEDET
LEDET_v = f"{os.path.normpath(LEDET_folder_path).split(os.sep)[-1]}"
LEDET_EXE = f"{LEDET_v}.exe"
new_LEDET_folder_path = f"{LEDET_folder_path}_{params['circuit_name']}_{params.eval_num}"
new_LEDET_EXE = f"{LEDET_v}_{params['circuit_name']}_{params.eval_num}.exe"
if not os.path.exists(new_LEDET_folder_path):
    os.makedirs(new_LEDET_folder_path)
    shutil.copy(os.path.join(LEDET_folder_path, LEDET_EXE), new_LEDET_folder_path)
    os.rename(os.path.join(new_LEDET_folder_path, LEDET_EXE), os.path.join(new_LEDET_folder_path, new_LEDET_EXE))

# run Dakota
circuit_template_file = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), f"circuit.{params['circuit_name']}.template.yaml")
conductor_template_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))), f"conductor.W1.template.yaml")
os.system(f"python {py_pro_path} -I params.in {circuit_template_file} circuit.{params['circuit_name']}.yaml")
os.system(f"python {py_pro_path} -I params.in {conductor_template_file} conductor.W1.yaml")
r = Run_LEDET(params['circuit_name'], params.eval_num, f"{new_LEDET_folder_path}")
sim_result = r.run_case(delete_mat_file=True, flag_generateReport=False, json_path=pyL_path, copy_to_folder=os.getcwd())
#print(sim_result)

if os.path.exists(os.path.join(new_LEDET_folder_path, new_LEDET_EXE)):
   os.remove(os.path.join(new_LEDET_folder_path, new_LEDET_EXE))
jpeg_result = os.path.join(new_LEDET_folder_path, 'LEDET', params['circuit_name'],f"{params['circuit_name']}_{params.eval_num}-summary.jpg")
if os.path.exists(jpeg_result):
   shutil.move(jpeg_result, Path(os.getcwd()).parent)
for i, label in enumerate(result_for_dakota):
        if result_for_dakota[label].asv.function:
            result_for_dakota[label].function = sim_result[label]
result_for_dakota.write()
