import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="callisto-jupyter-d1",
    version="0.0.4",
    author="Oak City Labs",
    author_email="team@oakcity.io",
    description="Jupyter D1 Server for Callisto",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://callistoapp.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "wsgidav>=3.0.3",
        "fastapi>=0.52.0",
        "asyncblink>=0.3.2",
        "uvicorn[standard]>=0.11.3",
        "python-dotenv>=0.13.0",
        "nbformat>=5.0.4",
        "python-jose>=3.1.0",
        "watchdog>=2.1.7",
        "jupyter>=1.0.0",
        "jupyter_client>=6.1.6",
        "jupyter_console>=6.1.0",
        "jupyter_core>=4.6.3",
        "jupyter_kernel_gateway>=2.4.0",
        "zsh-jupyter-kernel>=3.2",
        "bash_kernel>=0.7.2",
        "pynvml==8.0.4",
        "callisto-python==0.0.2",
    ],
    extras_require={
        "full": ["psutil==5.7.2"]
    },
    scripts=["start_jupyter_d1", "jupyter_d1_test",
             "jupyter_d1_install_kernels"]
)
