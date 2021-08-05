import os
import subprocess
import glob
import argparse

cwd = os.getcwd()

parser = argparse.ArgumentParser(description = "Run multicase and submit simulations directoires with an input and dataDict")
parser.add_argument("--trim-commands", help = "trim the commands.info file of everything after pisoFoam", action = 'store_true')

parser.add_argument("--tunnel", default = "dtf", help = "tunnel used in set up of multicase")

parser.add_argument("--ground", default = "static", help = "ground type used in set up of multicase")
parser.add_argument("--multicase-version", default = "4.1.0", help = "multicase version")
parser.add_argument("--multicase-sub-version", default = "1", help = "multicase version")
parser.add_argument("--program", required = True, help = "multicase version")
args = parser.parse_args()


for d in [d for d in os.listdir(cwd) if os.path.isdir(d)]:
    os.chdir(os.path.join(cwd, d))
    subdirs = os.listdir(os.path.join(cwd,d))
    if(not any(["Case_" in s for s in subdirs]) and "input" in subdirs and "dataDict" in subdirs):
        os.chdir(os.path.join(cwd, d))
        subprocess.call("/apps/iconcfd/bin/multicase-%s -v %s --tunnel dtf --turb-model sa-ddes --ground %s -v 1 --tunnel %s --turb-model sa-ddes --ground static " % (args.multicase_version, args.multicase_sub_version, args.ground, args.tunnel), shell = True)
        case_dir = glob.glob("Case*")[0]
        os.chdir(os.path.join(cwd, d, case_dir))
        if(args.trim_commands != None):
            lines = []
            with open("commands.info") as f:
                for line in f:
                    lines.append(line)
                    if('Piso' in line):
                        break
            with open("commands.info" ,"w") as f:
                for line in lines:
                    f.write(line)

        subprocess.call("runiconcfd -c commands.info -V %s -P %s -post off" % (args.multicase_version, args.program), shell = True)
