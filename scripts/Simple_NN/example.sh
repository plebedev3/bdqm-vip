
#!/bin/bash
#PBS -l nodes=1:ppn=4:gpus=1
#PBS -l walltime=8:00:00
#PBS -q pace-ice-gpu
#PBS -N bdqm-nn-1
#PBS -o stdout1
#PBS -e stderr1

cd /scratch/
module load git
mkdir {gtusername}
cd /scratch/{gtusername}
rm -rf bdqm-vip/
git clone https://github.com/medford-group/bdqm-vip.git
cd /scratch/{gtusername}/bdqm-vip/scripts/Simple_NN/
module load anaconda3/2019.03
conda activate tf32
python run.py
cp LOG /nv/pace-ice/{gtusername}/jobs/outputs/output-default.log