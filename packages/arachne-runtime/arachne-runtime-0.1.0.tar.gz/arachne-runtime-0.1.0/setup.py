# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python'}

packages = \
['arachne_runtime',
 'arachne_runtime.module',
 'arachne_runtime.rpc',
 'arachne_runtime.rpc.client',
 'arachne_runtime.rpc.client.stubmgr',
 'arachne_runtime.rpc.protobuf',
 'arachne_runtime.rpc.servicer',
 'arachne_runtime.rpc.utils',
 'arachne_runtime.utils']

package_data = \
{'': ['*'], 'arachne_runtime.rpc.protobuf': ['definition/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'grpcio-tools<1.45.0',
 'grpcio<1.45.0',
 'numpy<1.22.3',
 'packaging>=21.3,<22.0']

setup_kwargs = {
    'name': 'arachne-runtime',
    'version': '0.1.0',
    'description': 'A thin library for executing different types of DNN models from a common API',
    'long_description': '# Arachne Runtime\n\nArachne Runtime is a thin Python library for executing different types of DNN models from a common Python API.\nIt wraps original DNN library runtime and absorbs the differences among DNN libraries.\nNow, we support three types of DNN models as its inputs (e.g., tflite, onnx, and tvm).\nIt also supports RPC feature to help testing DNN models on remote edge devices such as Jetson devices.\n\n## Installation\n\n```sh\npip install arachne-runtime\n```\n\nIn addition to the above command, you need to install the DNN library runtimes.\n\n### TFLite\n\n```sh\npip install tensorflow\n```\n\n### ONNX Runtime\n\n```sh\npip install onnxruntime\n```\n\n### TVM\n\nTVM requires you to build its library.\nPlease follow [the official document](https://tvm.apache.org/docs/install/index.html)\n\n## Usage\n\n### Local Execution\n\nTo execute a DNN model via Arachne Runtime, first init a runtime module by `arachne_runtime.init`.\nThen, you can set `numpy.ndarray` as inputs by a `set_input` method.\nAfter setting all inputs, a `run` method executes the inference.\nThe outputs of inference results can be retrieved by a `get_output` method.\n\n```python\nimport arachne_runtime\n\n# TFLite\ntflite_interpreter_opts = {"num_threads": 4}\nruntime_module = arachne_runtime.init(\n    runtime="tflite", model_file="/path/to/model.tflite", **tflite_interpreter_opts\n)\nruntime_module.set_input(0, input_data)\nruntime_module.run()\nout = runtime_module.get_output(0)\n\n# ONNX Runtime\n\nort_opts = {"providers": ["CPUExecutionProvider"]}\nruntime_module = arachne_runtime.init(\n    runtime="onnx", model_file="/path/to/model.onnx", **ort_opts\n)\nruntime_module.set_input(0, input_data)\nruntime_module.run()\nout = runtime_module.get_output(0)\n\n# TVM Graph Executor\n\nruntime_module = arachne_runtime.init(\n    runtime="tvm", model_file="/path/to/tvm_model.tar", env_file="/path/to/env.yaml"\n)\nruntime_module.set_input(0, input_data)\nruntime_module.run()\naout = runtime_module.get_output(0)\n```\n\nNote that, in the case of TVM, users have to pass an additional YAML file (`env.yaml`) to the API.\nThis is because models compiled by TVM does not contains [the model signature](https://mlflow.org/docs/latest/models.html#tensor-based-signature-example) which is required by Arachne Runtime.\nThe type of `tvm.runtime.device` which is needed by the TVM Graph Executor has to be specified by users as well.\nTypically, the YAML file looks like below.\n\n```yaml\nmodel_spec:\n  inputs:\n  - dtype: float32\n    name: input_1\n    shape:\n    - 1\n    - 224\n    - 224\n    - 3\n  outputs:\n  - dtype: float32\n    name: predictions/Softmax:0\n    shape:\n    - 1\n    - 1000\ntvm_device: cpu\n```\n\n### Remote Execution\n\nWith RPC, you can train and build a DNN model on your local machine then run it on the remote device.\nIt is useful when the remote device resource are limited.\n\nTo try the RPC feature, first you have to follow the installation step and start a RPC server on the remote device.\n\n```sh\n# Remote device\npython -m arachne_runtime.rpc.server --port 5051\n```\n\nThen, you can init a RPC runtime module by `arachne_runtime.rpc.init` on the local machine.\nThe rest of APIs is similar to the local execution.\n\n```python\nimport arachne_runtime\n\n# TFLite\ntflite_interpreter_opts = {"num_threads": 4}\nruntime_module = arachne_runtime.init(\n    runtime="tflite", model_file="/path/to/model.tflite", rpc_info={"host": "hostname", "port": 5051}, **tflite_interpreter_opts\n)\n```\n\n## License\n\nArachne Runtime is licensed under the [MIT](https://github.com/fixstars/arachne-runtime/blob/main/LICENSE) license.\n',
    'author': 'Takafumi Kubota',
    'author_email': 'takafumi.kubota@fixstars.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fixstars/arachne-runtime',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.3,<3.10',
}


setup(**setup_kwargs)
