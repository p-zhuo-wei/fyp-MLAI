import argparse
import sys
from jarvis.core.atoms import Atoms
import re
import time

# from jarvis.core.graphs import Graph
start = time.time()
from alignn.ff.ff import (
    default_path,
    ev_curve,
    surface_energy,
    vacancy_formation,
    ForceField,
    get_interface_energy,
)
import numpy as np
import os 

folder = '/scratch/e0726313/intermetallics_2and3'

# temperature_K = float(args.temperature_K)
# initial_temperature_K = 0.1
# timestep = float(args.timestep)
# steps = int(args.md_steps)

n = 0
for filename in os.listdir(folder):
    print(f'processing {filename}: ')
    t1 = time.time()
    files = os.path.join(folder, filename)
    atoms = Atoms.from_poscar(files)
    ff = ForceField(
            jarvis_atoms=atoms,
            model_path = model_path
            #model_path='/home/svu/e0726313/miniconda3/envs/fyp/lib/python3.10/site-packages/alignn/ff/v12.2.2024_dft_3d_307k'
            # if model_path = model_path doesnt work then put the v12.2.2024_dft_3d_307k file inside this location^
        )
    
    #opt, en, fs = ff.optimize_atoms(steps = 5000, trajectory = f'/scratch/e0726313/outputs/{filename}.traj', logfile = f'/scratch/e0726313/outputs/{filename}.log')
    opt, en, fs = ff.optimize_atoms(steps = 100)


    output_folder = f'{folder}_optimized'
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, f"{filename}")
    opt.write_poscar(output_file)
    n += 1
    print(n)
    t2 = time.time()
    print(f'time taken to optimize {filename}: {t2-t1}')
     

end = time.time()
print(f'Successfully optimized {n} files in {end-start} seconds')
