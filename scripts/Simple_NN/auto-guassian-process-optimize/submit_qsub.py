import os
import random
import string
import tempfile
import subprocess
import time

def random_id(length=8):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

TEMPLATE_SERIAL = """
#!/bin/bash
#PBS -l nodes=1:ppn=4:gpus=1
#PBS -l walltime=6:00:00
#PBS -q pace-ice-gpu
#PBS -N bdqm-nn-1
#PBS -o stdout1
#PBS -e stderr1

cd /scratch/
module load git
rm -rf bdqm-vip/
git clone https://github.com/medford-group/bdqm-vip.git
cd /scratch/bdqm-vip/scripts/Simple_NN/
cp /nv/pace-ice/plebedev3/GPjobs/{} ./input.yaml
module load anaconda3/2019.03
conda activate tf32
python run.py
cp LOG /nv/pace-ice/plebedev3/GPjobs/outputs/{}
"""

def submit_simple_nn_job_and_wait_sync(yaml, name="job", logfile="output.$JOB_ID", errfile="error.$JOB_ID", cleanup=False, prefix="input-", slots=1):
    id_num = random_id()
    base = prefix + "submit_{0}".format(id_num)
    yaml_name = base + ".yaml"
    open("/nv/pace-ice/plebedev3/GPjobs/" + yaml_name, 'w').write(yaml)
    logfile_name = "output-{}.log".format(id_num)
    open("/nv/pace-ice/plebedev3/GPjobs/" + base + '.qsub', 'w').write(TEMPLATE_SERIAL.format(yaml_name,logfile_name))
    job_done = False
    min_force =10000
    try:
        output = str(subprocess.check_output('qsub ' + "/nv/pace-ice/plebedev3/GPjobs/"+ base + '.qsub', shell=True))
        jobid = output.split(".")[0]
        jobid = jobid[2:len(jobid)]
        time.sleep(5)
    finally:
        if cleanup:
            os.remove(base + '.qsub')
        while(not job_done):
            try:
                results = str(subprocess.check_output("qstat", shell=True)).split("\n")
                correctline = ""
                for line in results:
                    if (jobid in line):
                        correctline = line
                        break
                if(correctline == ""):
                    job_done = True
                jobIndexStatus = correctline.find("pace-ice-gpu")-2
                if(jobIndexStatus>0):
                    if(correctline[jobIndexStatus] == "C"):
                        job_done = True
                time.sleep(5)
            except subprocess.CalledProcessError:
                time.sleep(5)
        try:
            results = open("/nv/pace-ice/plebedev3/GPjobs/outputs/" + logfile_name, "r")
            print("job done!")
            min_force = parse_results(results.read())
        except IOError:
            print("Results did not finish or job did not get submitted sucessfully")
            print("Giving min score possible")
            return(10000)
        return min_force

def parse_results(results):
    force_string = "F RMSE(T V) = "
    example_res = "4.9706e-01"
    lines = results.split("\n")
    min_force = 10000
    for line in lines:
        index = line.find(force_string)
        if(not (index < 0)):
            index_val = index+len(force_string)
            string_val = line[index_val:index_val+len(example_res)]
            float_val = float(string_val)
            if(float_val < min_force):
                min_force = float_val
    if(min_force == 10000):
        print("it probably shouldn't do this")
        return min_force
    return min_force
