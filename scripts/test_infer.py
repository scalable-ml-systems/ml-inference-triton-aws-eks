import numpy as np
import tritonclient.http as httpclient

# No "http://" in the URL
TRITON_URL = "ae1b65c6d5ca44af88cc615b6dfcdc2e-1590824262.us-east-1.elb.amazonaws.com:8000"

client = httpclient.InferenceServerClient(url=TRITON_URL)

# Dummy input tensor of zeros with correct shape [1,3,224,224]
input_data = np.zeros((1, 3, 224, 224), dtype=np.float32)

inputs = [httpclient.InferInput("data", input_data.shape, "FP32")]
inputs[0].set_data_from_numpy(input_data)

outputs = [httpclient.InferRequestedOutput("resnetv24_dense0_fwd")]

response = client.infer("resnet50", inputs=inputs, outputs=outputs)
print(response.as_numpy("resnetv24_dense0_fwd"))
