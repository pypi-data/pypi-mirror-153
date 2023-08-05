# Arachne Runtime

Arachne Runtime is a thin Python library for executing different types of DNN models from a common Python API.
It wraps original DNN library runtime and absorbs the differences among DNN libraries.
Now, we support three types of DNN models as its inputs (e.g., tflite, onnx, and tvm).
It also supports RPC feature to help testing DNN models on remote edge devices such as Jetson devices.

## Installation

```sh
pip install arachne-runtime
```

In addition to the above command, you need to install the DNN library runtimes.

### TFLite

```sh
pip install tensorflow
```

### ONNX Runtime

```sh
pip install onnxruntime
```

### TVM

TVM requires you to build its library.
Please follow [the official document](https://tvm.apache.org/docs/install/index.html)

## Usage

### Local Execution

To execute a DNN model via Arachne Runtime, first init a runtime module by `arachne_runtime.init`.
Then, you can set `numpy.ndarray` as inputs by a `set_input` method.
After setting all inputs, a `run` method executes the inference.
The outputs of inference results can be retrieved by a `get_output` method.

```python
import arachne_runtime

# TFLite
tflite_interpreter_opts = {"num_threads": 4}
runtime_module = arachne_runtime.init(
    runtime="tflite", model_file="/path/to/model.tflite", **tflite_interpreter_opts
)
runtime_module.set_input(0, input_data)
runtime_module.run()
out = runtime_module.get_output(0)

# ONNX Runtime

ort_opts = {"providers": ["CPUExecutionProvider"]}
runtime_module = arachne_runtime.init(
    runtime="onnx", model_file="/path/to/model.onnx", **ort_opts
)
runtime_module.set_input(0, input_data)
runtime_module.run()
out = runtime_module.get_output(0)

# TVM Graph Executor

runtime_module = arachne_runtime.init(
    runtime="tvm", model_file="/path/to/tvm_model.tar", env_file="/path/to/env.yaml"
)
runtime_module.set_input(0, input_data)
runtime_module.run()
aout = runtime_module.get_output(0)
```

Note that, in the case of TVM, users have to pass an additional YAML file (`env.yaml`) to the API.
This is because models compiled by TVM does not contains [the model signature](https://mlflow.org/docs/latest/models.html#tensor-based-signature-example) which is required by Arachne Runtime.
The type of `tvm.runtime.device` which is needed by the TVM Graph Executor has to be specified by users as well.
Typically, the YAML file looks like below.

```yaml
model_spec:
  inputs:
  - dtype: float32
    name: input_1
    shape:
    - 1
    - 224
    - 224
    - 3
  outputs:
  - dtype: float32
    name: predictions/Softmax:0
    shape:
    - 1
    - 1000
tvm_device: cpu
```

### Remote Execution

With RPC, you can train and build a DNN model on your local machine then run it on the remote device.
It is useful when the remote device resource are limited.

To try the RPC feature, first you have to follow the installation step and start a RPC server on the remote device.

```sh
# Remote device
python -m arachne_runtime.rpc.server --port 5051
```

Then, you can init a RPC runtime module by `arachne_runtime.rpc.init` on the local machine.
The rest of APIs is similar to the local execution.

```python
import arachne_runtime

# TFLite
tflite_interpreter_opts = {"num_threads": 4}
runtime_module = arachne_runtime.init(
    runtime="tflite", model_file="/path/to/model.tflite", rpc_info={"host": "hostname", "port": 5051}, **tflite_interpreter_opts
)
```

## License

Arachne Runtime is licensed under the [MIT](https://github.com/fixstars/arachne-runtime/blob/main/LICENSE) license.
