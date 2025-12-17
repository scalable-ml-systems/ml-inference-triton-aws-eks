## Setup Guide: ResNet50 Model Repository for Triton Inference Server

This document explains how to prepare and configure the ResNet50 model repository for use with NVIDIA Triton Inference Server.

1. Directory Structure 

Triton requires a specific layout for each model:

```
Code
resnet50/
├── config.pbtxt        # Model configuration
└── 1/                  # Versioned subdirectory
    └── model.onnx      # Actual model file
config.pbtxt must be placed at the root of the model directory.

Model binaries (model.onnx, model.plan, etc.) must be placed inside numbered version folders (1/, 2/, …).

2. Download the ResNet50 ONNX Model
Obtain a validated ResNet50 ONNX model from the official ONNX Model Zoo:

bash
wget https://github.com/onnx/models/raw/main/validated/vision/classification/resnet/model/resnet50-v2-7.onnx -O model.onnx
Move the file into the versioned folder:

bash
mkdir -p resnet50/1
mv model.onnx resnet50/1/
3. Create the config.pbtxt
The configuration file describes the model’s inputs, outputs, and runtime settings. Example for ResNet50 ONNX:

text
name: "resnet50"
platform: "onnxruntime_onnx"
max_batch_size: 8

input [
  {
    name: "data"              # Must match ONNX input tensor name
    data_type: TYPE_FP32
    format: FORMAT_NCHW
    dims: [3, 224, 224]
  }
]

output [
  {
    name: "prob"              # Must match ONNX output tensor name
    data_type: TYPE_FP32
    dims: [1000]
  }
]

instance_group [
  {
    kind: KIND_GPU
    count: 1
  }
]
Verify Input/Output Names
Inspect the ONNX file to confirm tensor names:

bash
python -c "import onnx; m=onnx.load('resnet50/1/model.onnx'); \
print('Inputs:', [i.name for i in m.graph.input]); \
print('Outputs:', [o.name for o in m.graph.output])"
Update config.pbtxt so input.name and output.name match exactly.

4. Deploy with Triton
Once the directory is populated:

Code
resnet50/
├── config.pbtxt
└── 1/
    └── model.onnx
Mount this directory into your Triton container (e.g., via PVC at /models). Triton will automatically load the model at startup.

```

5. Notes and Best Practices
Always keep config.pbtxt at the model root, not inside version folders.

Use numbered subdirectories (1/, 2/, …) for versioning.

Triton can serve multiple versions simultaneously if additional subdirectories are added.

Ensure tensor names in config.pbtxt match the ONNX graph exactly, or Triton will log errors.

6. ONNX Overview
Definition: ONNX (Open Neural Network Exchange) is a standardized format for ML models.

Purpose: Created to enable interoperability across frameworks (PyTorch, TensorFlow, MXNet) and inference engines (Triton, TensorRT).

File extension: .onnx files contain the computation graph, weights, and metadata.

Why it matters:

Portability: Train in PyTorch, export to ONNX, deploy in Triton.

Standardization: Defines operators so inference engines know how to execute them.

Deployment: Triton natively supports ONNX models (platform: "onnxruntime_onnx").

7. Helper Script: Inspect Model I/O
Use this Python script to generate input/output details:

```
python
import onnx
from onnx import mapping

m = onnx.load("resnet50.onnx")

print("\n=== MODEL INPUTS ===")
for inp in m.graph.input:
    dims = [d.dim_value for d in inp.type.tensor_type.shape.dim]
    dtype = mapping.TENSOR_TYPE_TO_NP_TYPE[inp.type.tensor_type.elem_type]
    print(f" • {inp.name:25s} shape={dims} dtype={dtype}")

print("\n=== MODEL OUTPUTS ===")
for out in m.graph.output:
    dims = [d.dim_value for d in out.type.tensor_type.shape.dim]
    dtype = mapping.TENSOR_TYPE_TO_NP_TYPE[out.type.tensor_type.elem_type]
    print(f" • {out.name:25s} shape={dims} dtype={dtype}")

```

✅ Summary
This setup guide ensures your ResNet50 ONNX model is correctly structured and configured for Triton Inference Server. Following these steps guarantees reproducibility, proper model loading, and smooth deployment in Kubernetes with PVC-mounted EFS storage.