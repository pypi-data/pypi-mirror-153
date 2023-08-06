from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mlflow-deploifai",
    version="0.0.2",
    author="Deploifai Limited",
    description="Deploifai plugin for MLflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deploifai/mlflow-deploifai-plugin",
    python_requires=">=3.7",
    packages=find_packages(),
    # Require MLflow as a dependency of the plugin, so that plugin users can simply install
    # the plugin & then immediately use it with MLflow
    install_requires=["mlflow"],
    entry_points={
        "mlflow.request_header_provider":
            "unused=mlflow_deploifai.request_header_provider:DeploifaiRequestHeaderProvider"
    },
)
