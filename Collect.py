import os
import subprocess
import glob
cwd = os.getcwd()


def read_dvfile(file_name):
    params = []
    with open(file_name) as f:
        for line in f:
            if("#" not in line):
                line_ar = line.split(",")
                p = {}
                p['number'] = line_ar[0]
                p['name'] = line_ar[1]
                p['value'] = float(line_ar[-3])
                p['min'] = float(line_ar[-2])
                p['max'] = float(line_ar[-1])
                params.append(p)
    return params
                
    
results = []
for d in [d for d in os.listdir(cwd) if os.path.isdir(d)]:
    os.chdir(os.path.join(cwd, d))
    subdirs = os.listdir(os.path.join(cwd,d))
    if(any(["Case_" in s for s in subdirs]) and "input" in subdirs and "dataDict" in subdirs):
        if("DVFile.txt" in subdirs):
            params = read_dvfile(os.path.join(cwd, d, "DVFile.txt"))
            os.chdir(os.path.join(cwd, d,))

            case_dir = glob.glob("Case*")[0]
            os.chdir(os.path.join(cwd, d, case_dir))

            try:
                print("running summary for %s" % d)
                subprocess.call("/apps/ford/aero/fordcfd/v2.4.4/bin/fordcfd-post summary --forward-ave-start 1.0", shell = True)
            except:
                print("error", d)
                pass

            if(os.path.exists("summary.csv")):            
                with open("summary.csv") as f:
                    for line in f:
                        if("Cd," in line):
                            Cd = line.split(",")[-1]
                            try: 
                                Cd = float(Cd)                        
                                results.append((params, Cd, d))
                            except:
                                pass

with open(os.path.join(cwd, "results.csv"), "w") as f:    

    values = [p["name"] for p in results[0][0]]
    line =  ", ".join(values)
    line += ", Cd" 
    line += ", Run \n"
    f.write(line)
    for r in results:
        params = r[0]
        Cd = r[1]
        values = [p["value"] for p in params]
        line =  ", ".join(map(str, values))
        line += ", %f" % Cd
        line += ", %s\n" % r[2]
        f.write(line)
