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

**Create conda env:**

- add git module:

```
module load git
```

- clone repo:
**WARNING: URL should be changed after folked repo has been pushed to master.**

```
git clone https://github.com/plebedev3/bdqm-vip.git
```

- add conda module (You'll have to do this everytime you ssh into pace-ice and want to activate the conda env):

```
module load anaconda3/2019.03
```

- navigate to directory with a.yml

```
cd ./bdqm-vip/scripts/Simple_NN
```

- create conda environment with a.yml
```
conda env create -f a.yml
```

- test if conda environment exists using:

```
conda activate tf32
```

- If (tf32) appears in front of your user id, it is successfully built.

**Set up conda environment**

- Navigate to your home directory

```
cd ~
```

- clone repo:

```
git clone https://github.com/medford-group/SIMPLE-NN.git
```

- Navigate to directory with setup.py

```
cd SIMPLE-NN
```

- Install setup:

```
python setup.py install
```

# 2. Testing Enviroment with Interactive Environment

```
qsub -l walltime=00:30:00 -l nodes=1:ppn=1:gpus=1 -q pace-ice-gpu -I 
```

**Something a little more complex:**
- Navigate to home directory
```
cd ~
```

- Create directory for qsub jobs, and navigate into it
```
mkdir jobs
cd jobs
```

- Create directory for output logs
```
mkdir outputs
```

- Create qsub job
```
touch example.sh
cp ~/bdqm-vip/scripts/Simple_NN/example.sh example.sh
nano example.sh
```
- Then, swap `{gtusername}` with your username everywhere in the file

- Schedule the job:
```
qsub example.sh
```

- You can now do `qstate -u [username]` to view your scheduled job, and the output log will be located in `~/scripts/outputs` as `output-default.log`

