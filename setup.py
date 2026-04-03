from setuptools import setup, find_packages

setup(
    name="recursive-logic-engine",
    version="1.0.0",
    description="Self-correcting reasoning specialist using GRPO and RLVR",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "numpy>=1.21.0",
        "pyyaml>=6.0",
        "wandb>=0.15.0",
        "tqdm>=4.60.0",
        "scikit-learn>=1.0.0",
    ],
)
