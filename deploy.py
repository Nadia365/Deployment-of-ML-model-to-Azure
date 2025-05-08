#####Deployment Script
from azureml.core import Workspace, Model, Environment
from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig
import os

# Initialize workspace
ws = Workspace.from_config()

# Create environment - let AzureML handle gunicorn
env = Environment.from_conda_specification(
    name='keras-tf3.15-env',
    file_path='conda_dependencies.yml'
)

# Configure inference
inference_config = InferenceConfig(
    entry_script='score.py',
    environment=env
)

# Deployment configuration
deployment_config = AciWebservice.deploy_configuration(
    cpu_cores=1,
    memory_gb=1,
    tags={'framework': 'tensorflow'},
    description='Keras model deployment'
)

def deploy_model(model_path, model_name):
    try:
        # Register model
        model = Model.register(ws, model_path, model_name)
        
        # Create safe service name
        service_name = f"keras-{model_name[:16]}-svc".lower().replace('_','-')
        
        # Deploy
        service = Model.deploy(
            workspace=ws,
            name=service_name,
            models=[model],
            inference_config=inference_config,
            deployment_config=deployment_config,
            overwrite=True
        )
        
        service.wait_for_deployment(show_output=True)
        print(f"Success! Service URL: {service.scoring_uri}")
        return service
    except Exception as e:
        print(f"Error deploying {model_name}: {str(e)}")
        return None

# Deploy all H5 models
for model_file in os.listdir('MLmodels'):
    if model_file.endswith('.h5'):
        print(f"\nDeploying {model_file}...")
        deploy_model(
            model_path=os.path.join('MLmodels', model_file),
            model_name=os.path.splitext(model_file)[0]
        )
