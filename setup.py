import sys
import glob
import os
import shutil
import argparse

parser = argparse.ArgumentParser(description = "set up a DOE given ANSA DOE folder and a pre-existing run setup")
parser.add_argument("--DOE-dir", help = "ANSA DOE dir, containing Exp_N folders, each of which have a .obj.gz or .stl geometry file and a DV_File")
parser.add_argument("--run-dir", help = "A run template directory, with an input directory and dataDict")
args = parser.parse_args()

ansa_doe_dir = args.DOE_dir
base_dir = args.run_dir
cwd = os.getcwd()


files_obj = glob.glob(ansa_doe_dir+ "/Exp_*/*.obj.gz")
files_stl = glob.glob(ansa_doe_dir+ "/Exp_*/*.stl")
files = files_obj + files_stl

for f in files:
    run_dir = "_".join(f.split("/")[:2])
    print("Setting up %s" % run_dir)
    if(not os.path.exists(run_dir)):
        os.mkdir(run_dir)
        os.mkdir(os.path.join(run_dir, "input"))
    for d in os.listdir(os.path.join(cwd, base_dir, "input")):
        shutil.copy(os.path.join(cwd, base_dir, "input", d), os.path.join(cwd, run_dir, "input"))
    shutil.copy(os.path.join(cwd, base_dir, "dataDict"), os.path.join(cwd, run_dir))
    shutil.copy(os.path.join(cwd, f), os.path.join(cwd,run_dir, "input"))
    dv_file = os.path.join(os.path.dirname(f), "DVFile.txt")
    shutil.copy(os.path.join(cwd, dv_file), os.path.join(cwd,run_dir))
    with open(os.path.join(cwd, run_dir, "dataDict")) as f:
        dd = []
        for line in f:
            if("caseName" in line):
				line = "                                         caseName : %s       :" % run_dir
            dd.append(line) 

        with open(os.path.join(cwd, run_dir, "dataDict"), 'w') as f:
            for l in dd:
                f.write(l)
    
