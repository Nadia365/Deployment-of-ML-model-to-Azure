#####Deployment Script
#Wihtout image reuse and it is successful 

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

'''
#To use final with image of gentle_cup_y1gzt2jl OK Final USE 
#####FINNNEE 
from azureml.core import Workspace, Model, Environment
from azureml.core.webservice import AciWebservice, Webservice
from azureml.core.model import InferenceConfig
from azureml.core.image import ContainerImage
from azureml.core.run import Run
import os
import re
import traceback
import time
import tempfile
import shutil

# Initialize workspace
ws = Workspace.from_config()

def get_image_from_run(run_id):
    """Retrieve the container image from a specific run ID"""
    try:
        run = Run.get(ws, run_id)
        if run.get_status() == "Completed":
            # Check if the run produced an image
            image_details = run.get_details().get('output', {}).get('image', {})
            image_id = image_details.get('imageId')
            if image_id:
                print(f"Found image with ID: {image_id} from run {run_id}")
                return image_id
        print(f"No valid image found for run {run_id}")
    except Exception as e:
        print(f"Error retrieving image from run {run_id}: {str(e)}")
    return None

def delete_existing_service(service_name):
    """Delete an existing service if it exists"""
    try:
        service = Webservice(workspace=ws, name=service_name)
        if service:
            print(f"Deleting existing service: {service_name}")
            service.delete()
            time.sleep(10)  # Wait for deletion to complete
    except Exception as e:
        print(f"No existing service {service_name} found or error deleting: {str(e)}")

def deploy_with_image_reuse(model_path, model_name, image_run_id="imgbldrun_b63e670"):
    try:
        # Sanitize model name to avoid invalid characters
        safe_model_name = re.sub(r'[^a-zA-Z0-9_-]', '_', model_name)[:32]
        print(f"Registering model with name: {safe_model_name}")

        # Register model
        model = Model.register(ws, model_path, safe_model_name)
        print(f"Model registered: {model.name}")

        # Create safe service name
        service_name = f"keras-{safe_model_name[:16]}-svc".lower().replace('_', '-')
        print(f"Deploying service: {service_name}")

        # Delete existing service to avoid immutable property conflicts
        delete_existing_service(service_name)

        # Use existing environment
        try:
            env = Environment.get(workspace=ws, name='keras-tf2.15-env')
            print("Using existing environment: keras-tf2.15-env")
        except:
            print("Environment keras-tf2.15-env not found. Please ensure it exists or create it.")
            env = Environment.from_conda_specification("keras-tf2.15-env", "conda_dependencies.yml")
            env.register(ws)
            print("Created and registered new environment: keras-tf2.15-env")

        # Create temporary UTF-8 encoded score.py
        temp_dir = tempfile.mkdtemp()
        temp_score_path = os.path.join(temp_dir, 'score.py')
        with open('score.py', 'r', encoding='utf-8') as f:
            content = f.read()
        with open(temp_score_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Temporary score.py created with UTF-8 encoding")

        # Inference config
        inference_config = InferenceConfig(
            entry_script=temp_score_path,
            environment=env
        )

        # Deployment config
        deployment_config = AciWebservice.deploy_configuration(
            cpu_cores=1,
            memory_gb=1,
            tags={'framework': 'tensorflow', 'version': '2.15'},
            description='Keras model deployment with TensorFlow 2.15'
        )

        # Get image ID from specified run
        image_id = get_image_from_run(image_run_id)
        if not image_id:
            print(f"Could not retrieve image for run {image_run_id}. Deploying with new image build.")

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
        print(f"Service state: {service.state}")
        print(f"Success! Service URL: {service.scoring_uri}")

        # Retry fetching logs
        for _ in range(10):
            logs = service.get_logs()
            if logs:
                print("Deployment logs:\n", logs)
                break
            print("Logs not available, retrying in 10 seconds...")
            time.sleep(10)
        else:
            print("No logs retrieved after retries")

        return service

    except Exception as e:
        print(f"Error deploying {model_name}: {str(e)}")
        traceback.print_exc()
        if 'service' in locals():
            for _ in range(10):
                logs = service.get_logs()
                if logs:
                    print("Error logs:\n", logs)
                    break
                print("Logs not available, retrying in 10 seconds...")
                time.sleep(10)
            else:
                print("No error logs retrieved after retries")
        return None
    finally:
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)

# Deploy all H5 models
model_dir = 'MLmodels'
for model_file in os.listdir(model_dir):
    if model_file.endswith('.h5'):
        print(f"\nDeploying {model_file}...")
        deploy_with_image_reuse(
            model_path=os.path.join(model_dir, model_file),
            model_name=os.path.splitext(model_file)[0],
            image_run_id="imgbldrun_998b797"
        )
        '''