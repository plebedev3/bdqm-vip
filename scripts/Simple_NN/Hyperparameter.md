## Setup Environment for Simple-NN in Pace-ice

1. Setup Conda Environment for Simple-NN
2. Testing Enviroment with Interactive Environment
3. Submitting jobs with Pace-ice

**Requirements: conda and pace-ice**

# 1. Setup Conda Environment for Simple-NN

**ssh in to Pace-ice:**

```
ssh -x <GTID>@pace-ice.pace.gatech.edu
```

**create conda env:**

- clone repo:
**WARNING: URL should be changed after folked repo has been pushed to master.**

```
https://github.com/plebedev3/bdqm-vip.git
```

- create conda environment with a.yml
```
cd ./bdqm-vip/scripts/Simple_NN
```
```
conda env create -f a.yml
```

- test if conda environment is exist using:

```
conda activate tf32
```

- if (tf32) appears in front of your user id, it is successfully built.

# 2. Testing Enviroment with Interactive Environment

```
qsub -l walltime=00:30:00 -l nodes=1:ppn=1:gpus=1 -q pace-ice-gpu -I 
```
