# FYP
This repository contains scripts and documentations for NUS students to continue the research on using ALIGNN to predict materials properties.
As of 9th May 2025.

# HPC Setup Guide (Vanda Cluster)
1. Register for a HPC account (if you have not done so) at [click here](https://nusit.nus.edu.sg/hpc/get-an-hpc-account/)
2. Follow instructions to ssh into the hpc ip requires [NUS VPN](https://nusit.nus.edu.sg/services/wifi_internet/nvpn/) (search from ntouch applications)
4. Follow the [start up](https://nusit.nus.edu.sg/hpc/introductory-guide-for-new-hpc-users/) guide on HPC – as of time of writing this, the start up guide is still outdated (atlas clusters have been decomissioned, email for new vanda cluster guide if not available)

# SSH into vanda cluster (Read the vanda cluster guide for more info)
1. ssh e0123456@vanda.nus.edu.sg
2. Enter password (if its your first time, you might have to create a new password)

# Setting up ALIGNN on Vanda Cluster
1. Opening in container `singularity exec /app1/common/singularity-img/hopper/pytorch/pytorch_2.1.0_cuda_12.1_ngc_23.07.sif bash`
2. Creating conda environment in container (probably not neccesary and is not recommended but this worked for me) `conda create -n fyp python=3.10`
3. Install pytorch and dgl related libraries
  - `conda install pytorch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 dgl=2.1.0 pytorch-cuda=12.1 -c pytorch -c nvidia -c dglteam`
  - `conda install dglteam/label/cu121::dgl`
5. Install ALIGNN `conda install conda-forge::alignn`
6. Install CUDA enabled DGL `conda install dglteam/label/cu121::dgl`


