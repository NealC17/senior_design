#!/bin/bash

# Set the environment name
ENV_NAME=".signal"

# Create the conda environment in the current directory
conda create --prefix ./$ENV_NAME -y

# Activate the environment
source activate ./$ENV_NAME

# Install the required packages
conda install pandas matplotlib plotly numpy scikit-learn jupyterlab scipy -y

# Deactivate the environment after installation
conda deactivate

echo "Environment '$ENV_NAME' created and packages installed!"
echo "Type conda activate ./.signal to activate the virtual env" 
