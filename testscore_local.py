'''
import os
import json
import numpy as np
from score import init_model, run  # Import from your score.py

# 1. Set up test environment
os.environ['AZUREML_MODEL_DIR'] = 'MLmodels'  # Point to your models folder

# 2. Initialize the model
print("Initializing model...")
try:
    init_model()
    print("✅ Model initialized successfully")
except Exception as e:
    print(f"❌ Init failed: {str(e)}")
    exit(1)

def generate_test_sample():
    """Generate test data matching model's expected shape"""
    return {
        "data": [
            [[float(i)] for i in range(50)],  # Sample 1: 50 timesteps, 1 feature
            [[float(i+1)] for i in range(50)]  # Sample 2
        ]
    }

# Then update your test code:
test_input = generate_test_sample()
# 3. Prepare test input (modify according to your model's requirements)
test_input = generate_test_sample()

# 4. Test scoring
print("\nTesting scoring...")
try:
    result = run(json.dumps(test_input))
    print("✅ Scoring successful!")
    print("Result:", result)
except Exception as e:
    print(f"❌ Scoring failed: {str(e)}")
    '''
import os
import json
import numpy as np
from score import init, run  # Import from your score.py

# 1. Set up test environment
os.environ['AZUREML_MODEL_DIR'] = 'MLmodels'  # Point to your models folder

# 2. Initialize the model
print("Initializing model...")
try:
    init()  # Changed from init_model() to init()
    print("✅ Model initialized successfully")
except Exception as e:
    print(f"❌ Init failed: {str(e)}")
    exit(1)

def generate_test_sample():
    """Generate test data matching model's expected shape"""
    return {
        "data": [
            [[float(i)] for i in range(50)],  # Sample 1: 50 timesteps, 1 feature
            [[float(i+1)] for i in range(50)]  # Sample 2
        ]
    }

# 3. Prepare test input
test_input = generate_test_sample()

# 4. Test scoring
print("\nTesting scoring...")
try:
    result = run(json.dumps(test_input))
    print("✅ Scoring successful!")
    print("Result:", result)
except Exception as e:
    print(f"❌ Scoring failed: {str(e)}")