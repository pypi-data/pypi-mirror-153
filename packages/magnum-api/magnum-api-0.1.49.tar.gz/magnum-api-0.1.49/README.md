# Project Overview
The CHART MagNum (Magnum Numerics) aims at introducing advanced design techniques in order to support the design process of superconducting accelerator magnet.
The project responds to the following strategic goals:
- Sustainability

  Ensure that outstanding modeling work will have an impact on present or future designs. This also require that models have clearly defined scope and range of applicability.
- Traceability

  Ensure that the modeler is able to trace back the input parameters, code and script versions, etc., that have been used to produce a particular plot in a ppt or pdf.
  Traceability is even more important in multi-scale and multi-model analysis.
- Repeatability

  Ensure that results presented at, e.g., a Conceptual Design Review can be reproduced at any later time.
  Ensure that as-built models can be re-run at any moment during a potentially decades-long project life cycle.
- Flexibility

  Allow for different labs and collaborators to have/prefer different licenses.
  Enable researchers to implement innovative ideas while building upon existing best practices, but without having to solve legacy issues.
- Usability

  Encapsulate the increased flexibility behind easy-to-use UIs for the standard design work.

The project implements a number of concepts introduced by the MBSE (Model-Based System Engineering) methdology.
In particular, MBSE shifts the focus from documents to models as primary means of communication in complex system design projects.

# Project Architecture
The project is composed of two parts: notebooks and a library with an API (Application Programming Interface).
A notebook combines documentation with source code and results of its execution. As such, it encodes a design step that involves model construction from a parametrized input, its execution and extraction of the figures of merit.
In order to keep the notebooks lean and linear, the model control logic is extracted to the API.
An important pillar of the framework is automation of the modelling process; the automation is achieved with GitLab CI pipelines. To this end, a set of notebooks representing a design process are concatenated into a design workflow.
The workflow is executed for a given model input. The input contains generic part (e.g., material properties, geometry, cable parameters) and model-specific part (e.g., electromagnetic boundary condidtions, definition of mechanical contacts).
As a result, a workflow is immediatelly suited for design optimization, co-simulation, parametric studies, etc.

# User Guide
In the following we discuss the steps needed to obtain and further develop the API. In addition,
the main modules of `magnum-api` are presented:
- Geometry
- Tool Adapters
- Optimization
- Material Properties
- Plotting

## Getting Started
The project is developed with Python 3.6+ and was tested on Windows and Linux machines.
The python project dependencies are stored in `requirements.txt` file and need to be installed prior to API execution.
In order to execute tool adapters for ROXIE and ANSYS, both need to be installed. The API supports ROXIE 10.3 and ANSYS 2020R1.
The code development can be carried out with any IDE (Integrated Development Environment) and the suggested one is PyCharm.
Please consult `CONTRIBUTING.md` file for contribution guidelines.

## Geometry
The geometry module provides classes to handle coil geometry. So far, the 2D cos-theta geometry is implemented.
We follow the ROXIE block definition and reuse the cable data concept. The block definition supports absolute and relative angle definition. The geometry input can be expressed as a list of dictionaries and a pandas DataFrame either as objects or, respectively as json and csv files.

- geometry creation with json file for absolute angle definition

```python
from magnumapi.cadata.CableDatabase import CableDatabase
from magnumapi.geometry.CosThetaGeometry import CosThetaGeometry

json_path = 'input/16T_abs.json'
cadata_path = 'input/roxieold_2.cadata'
cadata = CableDatabase(cadata_path)

geometry = CosThetaGeometry.with_roxie_absolute_angle_definition_json(json_path, cadata)
geometry.build_blocks()
geometry.plotly_geometry_blocks()
```

- geometry creation with json file for relative angle definition

```python
from magnumapi.cadata.CableDatabase import CableDatabase
from magnumapi.geometry.CosThetaGeometry import CosThetaGeometry

json_path = 'input/16T_rel.json'
cadata_path = 'input/roxieold_2.cadata'
cadata = CableDatabase(cadata_path)

geometry = CosThetaGeometry.with_roxie_relative_angle_definition_json(json_path, cadata)
geometry.build_blocks()
geometry.plotly_geometry_blocks()
```

The remaining methods are presented in the UML diagram below.
<img src="figures/CosThetaGeometryUMLClassDiagram.PNG">

## Tool Adapters
A tool adapter provides methods to control a simulation tool. So far, we support ROXIE and ANSYS as show in the diagram below. 
<img src="figures/CosThetaGeometryUMLClassDiagram.PNG">

## Optimization

We implement a genetic optimization algorithm that operates with modelling workflows implemented as notebooks.
The optimization algorithm works as follows:
1. Load design variables table with allowed range of values, its type, and number of bits per variable
2. Load optimization config
3. Load an input model parameter that is updated during the optimization process. Each notebook relies on this input.
4. Randomly initialize starting population of individuals
5. For each generation:
  - Evaluate fitness function for each notebook (in case of errors, a penalty value is applied)
  - Perform tournament selection for mating (if elitism is considered)
  - Execute crossover operator
  - Execute mutation operator

### Design Variables Table
Below we present a sample design variables table. The meaning of columns is
- xl: lower value of a variable
- xu: upper value of a variable
- xs: starting value of a variable
- variable: variable name
- variable_type: numeric variable type
- bits: bits per variable
- bcs: block index

| xl        | xu           | xs  | variable | variable_type | bits | bcs |
| ------------- |-------------| -----| ---- | ------------- | ---- | --- |
| 0 | 3.0 | 10.0 | 3 | phi_r | float | 6 | 2 |
| 1 | 3.0 | 10.0 | 3 | phi_r | float | 6 | 3 |
| 2 | 3.0 | 10.0 | 3 | phi_r | float | 6 | 4 |
| 3 | 3.0 | 10.0 | 3 | phi_r | float | 6 | 6 |
| 4 | 3.0 | 10.0 | 3 | phi_r | float | 6 | 7 |

### Optimization Config
Optimization algorithm is parametrized with a config. The config is represented as a json file.
A sample config is shown below. The meaning of keys is:
- input_folder: an absolute path to an input folder
- output_folder: an absolute path to an output folder
- notebooks: a list of notebook configs
  - notebook_folder: relative notebook folder path
  - notebook_name: full notebook name
  - input_parameters: dictionary of parameters; key is a name for the target notebook and the value is the name from a source notebook
  - output_parameters: list of output parameters
  - input_artefacts: dictionary of parameters; key is a relative artefact path for the target notebook and the value is the relative artefact path from a source notebook
  - output_artefacts: list of output artefacts

```json
{
  "input_folder": "/home/mmaciejewski/gitlab/magnum-nb/",
  "output_folder": "/home/mmaciejewski/gitlab/magnum-nb/output/",
  "notebooks": [
    {
      "notebook_folder": "geometry",
      "notebook_name": "Geometry.ipynb",
      "input_parameters": {},
      "output_parameters": [],
      "input_artefacts": {},
      "output_artefacts": []
    },...
  ]
}
```

## Material Properties

We implemented the following material properties:

- resistivities:
  - calc_rho_cu_nist
- heat capacities:
  - calc_cv_cu_nist
  - calc_cv_nb3sn_nist
- critical current fits:
  - calc_jc_nbti_bottura
  - calc_jc_nb3sn_bordini
  - calc_jc_nb3sn_summers
  - calc_jc_nb3sn_summers_orig

## Plotting
Plotting module contains generic plotting functions. 
