# crismis_gsoc

This repo contains gsoc task for CRISMIS project.

## Getting Started

### Requirements
* python3
* docker (Optional)
* docker-compose (Optional)


### Clone

```bash
git clone https://github.com/leoank/crismis_gsoc.git
```

### Create a python virtual environment

```bash
python -m venv venv     # create python environment
. ./venv/bin/activate    # activate python enviroment
```

if you prefer `conda` then use:
```bash
conda env create -f environment.yml
conda activate crismis_gsoc
```

### Pip install crismis_gsoc

```bash
cd crismis_gsoc
pip install -e .
```

### Use crismis_gsoc cli

```bash
crismis_gsoc --help     # help

 # train model
crismis_gsoc train
crismis_gsoc train --docker # run inside docker

 # test model
crismis_gsoc test
crismis_gsoc test --docker # run inside docker

 # do predictions
crismis_gsoc predict
crismis_gsoc predict --docker # run inside docker

 # download datasets
crismis_gsoc download
crismis_gsoc download --docker # run inside docker
```

## Notebook

Main notebook `cosmic_ray_classification.ipynb` is in `notebooks` folder.
