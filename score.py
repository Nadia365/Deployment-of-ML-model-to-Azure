import os
import json
import numpy as np
import tensorflow as tf

def init():
    global model
    try:
        model_dir = os.getenv('AZUREML_MODEL_DIR')
        if not model_dir:
            raise ValueError("AZUREML_MODEL_DIR not set")
        model_path = None
        for file_name in os.listdir(model_dir):
            if file_name.endswith('.h5'):
                model_path = os.path.join(model_dir, file_name)
                break
        if not model_path:
            raise ValueError(f"No .h5 models found in {model_dir}")
        print(f"Loading model from: {model_path}")
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully")
    except Exception as e:
        print(f"Init failed: {str(e)}")
        raise

def run(raw_data):
    try:
        input_data = json.loads(raw_data)['data']
        data = np.array(input_data, dtype=np.float32)
        if data.shape[-1] != 1 or len(data.shape) != 3:
            if len(data.shape) == 2:
                data = data.reshape((data.shape[0], data.shape[1], 1))
            elif len(data.shape) == 1:
                data = data.reshape((1, data.shape[0], 1))
            else:
                raise ValueError(f"Unexpected input shape: {data.shape}")
        if data.shape[1] != 50 or data.shape[2] != 1:
            raise ValueError(f"Input must be shape (n, 50, 1), got {data.shape}")
        predictions = model.predict(data).tolist()
        return {'predictions': predictions}
    except Exception as e:
        return {'error': str(e)}
    

