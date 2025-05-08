# 🚀 Keras Model Deployment on Azure ML  

*This repository contains scripts and configuration files to deploy Keras models (in .h5 format) as web services using Azure Machine Learning (AzureML) on Azure Container Instances (ACI). The workflow automates model registration, environment setup, and deployment, with a scoring script to handle inference requests.*  

---

## 📌 Table of Contents  
- [Overview]
- [Prerequisites]
- [Repository Structure]
- [Setup & Deployment]
- [Scoring Script]
- [Environment Configuration]

---

## 🌟 Overview  
Automates:  
✅ Model registration (.h5 → AzureML)  
✅ Environment setup (TensorFlow 2.15.0)  
✅ Deployment to Azure Container Instances (ACI)  
✅ Inference via REST API  

---

## ⚙️ Prerequisites  
1. **Azure Account** with ML workspace access.  
2. **`config.json`** from your AzureML workspace.  
3. **Python 3.10** and `azureml-sdk`:  
   ```bash
   pip install azureml-sdk

---

## Repository Structure

├── MLmodels/                       # Directory containing .h5 model files
 
├── conda_dependencies.yml         # Conda environment specification

├── deploy.py                      # Deployment script for AzureML

├── score.py                       # Scoring script for inference

├── config.json                   # AzureML workspace configuration (not included)

└── README.md               

## Workflow 


### 1. Set Up AzureML Workspace:

* Create an AzureML workspace in the Azure portal.
  
* Download the config.json file from the workspace and place it in the repository root.


### 2. Prepare Models:

* Place your Keras model files (.h5 format) in the MLmodels directory.

* Ensure models are compatible with TensorFlow 2.15.0.


### 3. Install AzureML SDK (local machine):
pip install azureml-sdk

## 🔍 Deployment Workflow
The deploy.py script automates the deployment process:

-Workspace Connection: Connects to the AzureML workspace using config.json.

-Environment Creation: Builds an environment from conda_dependencies.yml.

-Model Registration: Registers each .h5 model in the MLmodels directory.

-Service Deployment: Deploys each model as a web service on ACI with 1 CPU core and 1 GB memory.

-Output: Prints the scoring URI for each deployed service.

To run the deployment:

python deploy.py

## 🔍 Scoring Script
The score.py script runs within the deployed web service:

Initialization (init): Loads the .h5 model from the AZUREML_MODEL_DIR environment variable.

Inference (run): Processes JSON input with a data field, expecting an array of shape (n, 50, 1). Reshapes input if necessary and returns predictions as JSON.

Error Handling: Returns error messages for invalid inputs or exceptions.

## Expected Input Format:
{
  "data": [[...], [...], ...]  // Array of shape (n, 50) or (n, 50, 1)
}

Output Format:
{
  "predictions": [[...], [...], ...]  // Model predictions
}

or
{
  "error": "Error message"
}

## 🐍 Environment Configuration
The conda_dependencies.yml file defines the environment:
## name: keras-env
## channels:
  - conda-forge
## dependencies:
  - python=3.10
  - pip=23.3.2
  - pip:
    - tensorflow==2.15.0
    - numpy==1.23.5
    - pandas==1.3.5
    - flask==2.3.1
    - azureml-defaults==1.59.0
    - Werkzeug==3.1.*


## 🛠️ Key Dependencies:
-TensorFlow 2.15.0 for model loading and inference.

-Flask and Werkzeug for the web service.

-AzureML defaults for integration with AzureML.



