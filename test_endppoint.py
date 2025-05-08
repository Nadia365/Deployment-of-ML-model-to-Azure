import requests
import numpy as np

scoring_uri = "http://685503b0-ee8b-4488-b438-b33e5508183e.uksouth.azurecontainer.io/score"
# Generate a single sequence of 50 timesteps, 1 feature
payload = {
    "data": [[[0.5] for _ in range(50)]],  # Shape (1, 50, 1)
    "params": {"deployment_name": "default"}
}
headers = {"Content-Type": "application/json"}
try:
    response = requests.post(scoring_uri, json=payload, headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Error:", str(e))