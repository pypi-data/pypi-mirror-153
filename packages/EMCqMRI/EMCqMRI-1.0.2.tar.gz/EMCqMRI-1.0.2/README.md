# **EMCqMRI**

The EMCqMRI is a PyTorch-based package designed with the goal to accelerate initial developments in the field of quantitative MRI (qMRI).

It provides the base classes for the implementation of task-specific custom modules and offers a framework for training Deep Learning inference models and prediction of quantitative maps.

Validated qMRI methods, including signal models, likelihood functions and inference methods, are already included within this package.

<br>

# **Installing**

### Preparing the development enviroment

- Create a virtual environment for the project: `python3 -m venv venv_example_project`

- Activate the virtual environment: `. venv_example_project/bin/activate`

- Upgrade pip and install wheel: `pip3 install --upgrade pip wheel` (this will make sure you have no errors and warnings during installations with pip)

### Installing PyTorch

- MacOS without CUDA support: `pip3 install torch torchvision`

- MacOS with CUDA support: follow instructions at this URL: https://github.com/pytorch/pytorch#from-source

- Linux with CUDA support: `pip3 install torch torchvision`

- Windows with CUDA support: `pip3 install torch==1.7.1 torchvision==0.8.2 -f https://download.pytorch.org/whl/torch_stable.html`

### Installing the EMCqMRI package with PIP

- After activating your virtual enviroment, run: `pip3 install EMCqMRI`.

### Validating the installation

Once installed, you can verify if everything is running correctly.
- Start a Python session in your terminal: `python3`
- Import the EMCqMRI package: `import EMCqMRI`
- Verify the package version: `print(EMCqMRI.__version__)`

<br>

# **Support**
The following configurations were used and proved to work. Please, let us know if you tested the packaged in a different OS, Python version or PyTorch version.
### &nbsp; OS
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![macOS](https://img.shields.io/badge/macOS%20Catalina-10.15.6-blue)
![macOS](https://img.shields.io/badge/macOS%20Mojave-10.14.6-blue)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Linux](https://img.shields.io/badge/Linux%20Ubuntu-20.04.1-green)
![Linux](https://img.shields.io/badge/Linux%20Ubuntu-19.10-green)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Windows](https://img.shields.io/badge/Windows%207_64b-SP1-orange)

### &nbsp; Python
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/Python-3.6.5-red) 
![Python](https://img.shields.io/badge/Python-3.6.8-red) 
![Python](https://img.shields.io/badge/Python-3.7.1-red) 
![Python](https://img.shields.io/badge/Python-3.8.0-red) 

### &nbsp; PyTorch
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Python](https://img.shields.io/badge/PyTorch-1.4-blueviolet) 
![Python](https://img.shields.io/badge/PyTorch-1.6-blueviolet) 
![Python](https://img.shields.io/badge/PyTorch-1.7.1-blueviolet) 
![Python](https://img.shields.io/badge/PyTorch-1.8.1-blueviolet) 
![Python](https://img.shields.io/badge/PyTorch-1.9.0-blueviolet) 

<br>


# **Projects using the EMCqMRI**

- https://gitlab.com/e.ribeirosabidussi/emcqmri_relaxometry
- https://gitlab.com/e.ribeirosabidussi/emcqmri_dti
- https://gitlab.com/e.ribeirosabidussi/emcqmri_relaxometry_resmotion
- https://gitlab.com/e.ribeirosabidussi/emcqmri_motion_relaxometry
- https://gitlab.com/e.ribeirosabidussi/ipim_inverse_problems_rim
<br>

# **Using the EMCqMRI in your project**

The documentation for the APIs and implemented modules can be found at: https://emcqmri.readthedocs.io/en/latest/
### **APIs**

- **Signal Model**: It provides an interface for the implementation of custom signal models for model-based inference of quantitative MRI parameters.

- **Likelihood Model**: This interface allows for the implementation of custom likelihood models for model-based inference methods. In many cases, this model is also referred to as the data consistency model.

- **Inference Model**: Interface for the implementation of custom inference models. The EMCqMRI supports model-drive, data-drive and hibrid (data/model-driven) methods.

- **Dataset Model**: Interface for the construction of custom dataset models. These might include the generation of simulated data, loading of existing training and testing datasets, pre-processing and data augmentation techniques, etc.

<br>

## **Creating custom modules and configuration**

The creation of custom modules is straighforward using the EMCqMRI APIs. You can follow this [short tutorial](./project_tutorial.md) to create the basis of a new project, and learn how to link custom modules to the EMCqMRI core.

You can read more about the configuration files required to use the EMCqMRI here: [Configuration Files](./configuration_files.md)

<br>


# Contributing / Reporting issues
Please refer to the project's coding and documentation style for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

1. Fork the repo on GitHub
2. Clone the project to your own machine
3. Commit changes to your own branch
4. Push your work back up to your fork
5. Submit a Pull request so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

<br>

# Requirements

The EMCqMRI package is based on **Python** and **PyTorch**.
External dependencies are automatically installed with the package.

<br>

# Known bugs

There might be differences when using the EMCqMRI with Windows, MacOS and Linux, due to different conventions in the Path style. Please report them by creating an issue on this project.
<br>

# License
[MIT](https://choosealicense.com/licenses/mit/)

