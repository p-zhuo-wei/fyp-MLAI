# FYP
This repository contains scripts and documentations for NUS students to continue the research on using ALIGNN to predict materials properties.
This project laid the foundations of ALIGNN, learning how to use ALIGNN to train models, evaluate the models and use these models to help predict properties of materials.
The main structure studied in this project is a High Entropy Alloy consisting of Mo, V, Ti, Nb, Zr
The labelling conventions are as follows:
1. 1010101014-3: 10Mo, 10V, 10Ti, 10Nb, 14Zr, with a UID of 3, which represents the different arrangements of atoms this structure
2. 12328-3: 1Mo, 2V, 3Ti, 2Nb, 8Zr, UID of 1

Key conclusions that this project gained were:
1. Formation Energy and Bandgap pre trained models are about 95% accurate
2. Structure Optimization:
   - Only the size of the structure significantly affected the time required for optimization
   - A good estimate for the amount of steps required for optimization is around 200 steps, for structures up to 256 atoms
3. Pugh ratio predictions were less accurate than expected – further hypertuning is required for better classification
4. Classification task in ALIGNN was tested, in an attempt to better predict the ductile/brittle materials but model was entirely wrong (can look into classification tasks in ALGINN, but currently only allows for binary outcomes)

As of 9th May 2025.

# HPC Setup Guide (Vanda Cluster – NUS students)
1. Register for a HPC account (if you have not done so) at [here](https://nusit.nus.edu.sg/hpc/get-an-hpc-account/)
2. Follow instructions to ssh into the hpc ip requires [NUS VPN](https://nusit.nus.edu.sg/services/wifi_internet/nvpn/) (search from ntouch applications)
4. Follow the [start up](https://nusit.nus.edu.sg/hpc/introductory-guide-for-new-hpc-users/) guide on HPC – as of time of writing this, the start up guide is still outdated (atlas clusters have been decomissioned, email relevant parties in NUS computing/ntouch for new vanda cluster guide if not available/pdf guide is attached in this repo)

# Connect into vanda cluster (Read the [vanda cluster guide](Vanda_Cluster_User_Guide_27Jan25.pdf) for more info)
1. Connect to vanda cluster
   ```bash
   # replace eXXXXXXX with your own NUS id
   ssh e0123456@vanda.nus.edu.sg
   ```
2. Enter password (if its your first time, you might have to create a new password)

# Setting up ALIGNN on Vanda Cluster
1. Opening in container 
   ```
   singularity exec /app1/common/singularity-img/hopper/pytorch/pytorch_2.1.0_cuda_12.1_ngc_23.07.sif
   ```
2. Creating conda environment in container (probably not neccesary and is not recommended but this worked for me)
   ```
   bash conda create -n fyp python=3.10
   ```
3. Install pytorch and dgl related libraries
   ```
   conda install pytorch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 dgl=2.1.0 pytorch-cuda=12.1 -c pytorch -c nvidia -c dglteam
   bash conda install dglteam/label/cu121::dgl
   ```
4. Install ALIGNN
   ```
   conda install conda-forge::alignn
   ```
5. Install CUDA enabled DGL
   ```
   conda install dglteam/label/cu121::dgl
   ```
# Breakdown of this Github Repository

## Data Folder
- Contains all data files that was used in this project
  
| Files/Folders | Comments | Usage |
|:-|:-|:-
| jv_XXXX | Pre-trained models by alignn | Used to further tune and improve model or plot parity plots |
| logfiles/XXX.log | Records of the structure optimization process | Used to extract Energy and fmax at specific number of steps, to observe convergence of fmax/energy|  |
| logfiles/XXX.traj | Records of the structure at different steps in the optimization process | Used to extract the coordinates of structure at different steps |
| pugh_model | Self-Trained pugh model | Used to further tune and improve model or plot parity plots |
| structure_folder | Structures of all HEA produced (unoptimized) | To study the optimization process and pugh ratio prediction |
| traj_structure | Structures of optimized HEA at 0-500 optimization steps (intervals of 20), from logfiles/XXX.traj | Predict pugh ratios at different steps to determine effect of the different structures on pugh ratio |
| V12.2.2024_dft_3d_307k | Configuration and model path for optimization process | To be injected into alignn/ff if optimization does not work, and specify the path accordingly |
| XXX.csv | Predictions done by bulk and shear modulus models/pugh ratio model and timetaken for optimization at different number of steps | Used to evaluate and plot graphs | 


