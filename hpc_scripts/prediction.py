import os
import zipfile
import json
import torch
from alignn.models.alignn import ALIGNN, ALIGNNConfig
import tempfile
from alignn.graphs import Graph
import pandas as pd
import time
from jarvis.core.atoms import Atoms


start = time.time()

device = "cpu"
if torch.cuda.is_available():
    device = torch.device("cuda")

def load_model_from_local_zip(path):
    zp = zipfile.ZipFile(path)
    names = zp.namelist()
    chks = []
    cfg = []
    for i in names:
        if "checkpoint_" in i and "pt" in i:
            tmp = i
            chks.append(i)
        if "config.json" in i:
            cfg = i
        if "best_model.pt" in i:
            tmp = i
            chks.append(i)

    print("Using chk file", tmp, "from ", chks)
    print("Path", os.path.abspath(path))
    print("Config", os.path.abspath(cfg))
    config = json.loads(zipfile.ZipFile(path).read(cfg))
    # print("Loading the zipfile...", zipfile.ZipFile(path).namelist())
    data = zipfile.ZipFile(path).read(tmp)
    # model = ALIGNN(
    #    ALIGNNConfig(
    #        name="alignn", output_features=output_features, **config_params
    #    )
    # )
    model = ALIGNN(ALIGNNConfig(**config["model"]))

    new_file, filename = tempfile.mkstemp()
    with open(filename, "wb") as f:
        f.write(data)
    model.load_state_dict(torch.load(filename, map_location=device)["model"])
    model.to(device)
    model.eval()
    if os.path.exists(filename):
        os.remove(filename)
    return model

def predict_single(model, poscar_file_path, device, cutoff=8.0, max_neighbors=12):
    atoms = Atoms.from_poscar(poscar_file_path)
    
    g, lg = Graph.atom_dgl_multigraph(atoms, cutoff=float(cutoff), max_neighbors=max_neighbors)
    lat = torch.tensor(atoms.lattice_mat)

    out_data = (
        model([g.to(device), lg.to(device), lat.to(device)])
        .detach()
        .cpu()
        .numpy()
        .flatten()
        .tolist()
    )
    return out_data

models = ['fe (eV atoms-1)', 'shear (GPa)', 'bulk (GPa)']
poscar_folder = "/scratch/e0726313/intermetallics_2and3_optimized"
results = {}
output_file = f'{poscar_folder}_predictions.csv'

for property in models:
    n = 0
    if property == 'fe (eV atoms-1)':
        path = 'jv_formation_energy_peratom_alignn.zip'
    elif property == 'shear (GPa)':
        path = 'jv_shear_modulus_gv_alignn.zip'
    elif property == 'bulk (GPa)':
        path = 'jv_bulk_modulus_kv_alignn.zip'
    model = load_model_from_local_zip(path)

    for filename in os.listdir(poscar_folder):
        poscar_file_path = os.path.join(poscar_folder, filename)
        if filename.endswith('.vasp'):
            prediction = predict_single(model, poscar_file_path, device)
            if filename not in results:
                results[filename] = {'File Name': filename}
            results[filename][property] = prediction[0]
            n += 1
            print(f'Successfully predicted {n}: {filename}, {property}')
        else:
            print(f'Unable to predict {filename}, {property}')

df = pd.DataFrame.from_dict(results, orient='index')
df['pugh_ratio'] = df['shear (GPa)']/df['bulk (GPa)']
df = df.sort_values(by='File Name', ascending=True)
df.to_csv(output_file, index=False)

end = time.time()
print(f'Total time taken: {end-start} seconds')