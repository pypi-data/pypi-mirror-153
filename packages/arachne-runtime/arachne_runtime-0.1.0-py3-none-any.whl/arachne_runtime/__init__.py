import importlib
import tarfile
from logging import getLogger
from typing import Dict, Optional

import yaml
from packaging.version import Version

import arachne_runtime.rpc
from arachne_runtime.module import RuntimeModuleBase, RuntimeModuleFactory
from arachne_runtime.utils.version_utils import (
    get_cuda_version,
    get_cudnn_version,
    get_tensorrt_version,
)

logger = getLogger(__name__)


def validate_environment(env: dict) -> bool:
    """Validate library versions by comparing current execution environment and input environment.

    Args:
        env (dict): environment info to validate

    Returns:
        bool: whether the validation is success or not.
    """
    valid = True
    for dep in env["dependencies"]:
        if "cuda" in dep:
            cuda_version = get_cuda_version()
            if cuda_version != dep["cuda"]:
                logger.warning(
                    f"The CUDA version:{cuda_version} is not the same as the version specified in env.yaml:{dep['cuda']}"
                )
                valid = False
        if "cudnn" in dep:
            cudnn_version = get_cudnn_version()
            if cudnn_version != dep["cudnn"]:
                logger.warning(
                    f"The cudnn version:{cudnn_version} is not the same as the version specified in env.yaml:{dep['cudnn']}"
                )
                valid = False
        if "tensorrt" in dep:
            tensorrt_version = get_tensorrt_version()
            if tensorrt_version != dep["tensorrt"]:
                logger.warning(
                    f"The tensorrt version:{tensorrt_version} is not the same as the version specified in env.yaml:{dep['tensorrt']}"
                )
                valid = False
        if "pip" in dep:
            for pkg in dep["pip"]:
                for name in pkg.keys():
                    mod = importlib.import_module(name)
                    runtime_version = Version(mod.__version__)
                    dep_version = Version(pkg[name])
                    if (
                        runtime_version.major != dep_version.major
                        or runtime_version.minor != dep_version.minor
                        or runtime_version.micro != dep_version.micro
                    ):
                        logger.warning(
                            f"A python package:{name} version is not the same as the version specified in env.yaml"
                        )
                        valid = False
    return valid


def init(
    runtime: str,
    package_tar: Optional[str] = None,
    model_file: Optional[str] = None,
    model_dir: Optional[str] = None,
    env_file: Optional[str] = None,
    rpc_info: Optional[Dict] = None,
    **kwargs,
) -> RuntimeModuleBase:
    """Initialize RuntimeModule.

    The arguments to be passed as model file are different for runtime:

    - ONNX/TfLite:   set :code:`model_file`
    - TVM: set :code:`package_tar` or set both :code:`model_file` and :code:`env_file`

    Args:
        runtime (str): runtime name
        package_tar (Optional[str], optional): TVM package filepath archived by arachne.tools.tvm. Defaults to None.
        model_file (Optional[str], optional): ONNX/TfLite/TVM model filepath. Defaults to None.
        env_file (Optional[str], optional): environment file :code:`env.yaml`. Defaults to None.

    Returns:
        RuntimeModule: ONNX/TfLite/TVM RuntimeModule
    """
    assert (
        package_tar is not None or model_file is not None or model_dir is not None
    ), "package_tar, model_file, model_dir should not be None"

    if rpc_info is not None:
        kwargs["package_tar"] = package_tar
        kwargs["model_file"] = model_file
        kwargs["model_dir"] = model_dir
        kwargs["env_file"] = env_file
        return RuntimeModuleFactory.get(
            name="rpc",
            rpc_info=rpc_info,
            runtime=runtime,
            **{k: v for k, v in kwargs.items() if v is not None},
        )

    if model_dir is not None:
        return RuntimeModuleFactory.get(name=runtime, model=model_dir, **kwargs)

    if package_tar is not None:
        with tarfile.open(package_tar, "r:gz") as tar:
            for m in tar.getmembers():
                if m.name == "env.yaml":
                    env_file = m.name
                else:
                    model_file = m.name
            tar.extractall(".")

    assert model_file is not None

    env: dict = {}
    if env_file is not None:
        with open(env_file) as file:
            env = yaml.safe_load(file)

        if not validate_environment(env):
            logger.warning("Some environment dependencies are not satisfied")

    return RuntimeModuleFactory.get(name=runtime, model=model_file, **env, **kwargs)
