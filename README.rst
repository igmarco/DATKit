TAUP_DATKit
============

Overview
--------
TAUP_DATKit (*TAU Protein - Data Analysis Tool Kit*) is a package designed for data analysis on chromatographic data. It includes various functions for:

- Loading data from different sources, such as CSV and Excel files.
- Merging data and homogenizing spectra using data interpolation techniques.
- Complex filtering of elements.
- Representation and visualization of distances and similarities between elements.

Current Version
---------------
TAUP_DATKit 0.5.0

Project Context
---------------
This package is part of the *TAU Protein*: "Systematic manipulation of tau protein aggregation: bridging biochemical and pathological properties".

Library Structure
-----------------
The library structure of TAUP_DATKit is organized as follows:

- "TAUP_DATKit/": The main directory containing the core functionality of the package.
    - "analysis_reporting.py": Functions for the generation of the PDF report based in the results of the analysis.
    - "data_filtering.py": Functions for filtering chromatographic data elements by inclusion/exclusion or by distance to other elements.
    - "data_integration.py": Functions for integrating data from different sources.
    - "data_loading.py": Functions for loading CSV or Excel data.
    - "data_visualization.py": Functions for the representation and visualization of distances and similarities.
    - "distance_computing.py": Functions for the calculation of distances and linkage of chromatographic elements.
    - "demo/": Directory containing a simple demo for the library functionality.
        - "Data/": Example input data.
        - "Saves/": Example output information.
        - "example_process.py": Script that defines all the required parameters and use the main functions of the library.
        - "log.log": Example log of the execution.
    - "docs/": Documentation for using the package and understanding its functionality.
        - "build/": Documentation generated.
            - "html/": Documentation in HTML format.
        - "rst/": Documentation in .rst format.
        - "source/": Configuration of the documentation generation.
    - "properties/": Functions that allow defining and applying the basic configuration of the library.
        -  "config_prop_loader.py": Script that loads the configuration parameters from "config.properties".
        -  "config.properties": Configuration properties.
        -  "process_prop_loader.py": Script that loads the processing parameters from "process.properties".
        -  "process.properties": Execution properties.
        -  "prop_parser.py": Function for parsing config parameters from .properties files.
    - "tools/": 
        -  "chart_tools.py": Functions for generating plots.
    - "utils/": Functions to manage other resources.
        -  "image_utils.py": Functions for managing images.
        -  "interpolation_utils.py": Functions for defining interpolation algorithms.
        -  "metrics_utils.py": Function for the calculation of different metrics.

Requirements
------------
DATKit requires the following libraries to work properly. Please ensure that you install the versions indicated (or those within the specified ranges) to avoid compatibility issues:

- **CairoSVG**: approximately version 2.7.1 (`~=2.7.1`)
- **matplotlib**: approximately version 3.10.0 (`~=3.10.0`)
- **numpy**: version between 1.26.0 (inclusive) and 2.0.0 (exclusive) (`>=1.26.0, <2.0.0`)
- **openpyxl**: version between 3.0.10 (inclusive) and 3.1.5 (inclusive) (`>=3.0.10, <=3.1.5`)
- **pandas**: version between 2.2.2 (inclusive) and 2.3.0 (exclusive) (`>=2.2.2, <2.3.0`)
- **reportlab**: approximately version 4.2.5 (`~=4.2.5`)
- **scikit_learn**: approximately version 1.6.0 (`~=1.6.0`)
- **scipy**: version between 1.7.0 (inclusive) and 1.14.0 (exclusive) (`>=1.7.0, <1.14.0`)
- **seaborn**: approximately version 0.13.2 (`~=0.13.2`)
- **setuptools**: version 60.0.0 or higher (`>=60.0.0`)

::

    CairoSVG~=2.7.1
    matplotlib~=3.10.0
    numpy>=1.26.0,<2.0.0
    openpyxl>=3.0.10,<=3.1.5
    pandas>=2.2.2,<2.3.0
    reportlab~=4.2.5
    scikit_learn~=1.6.0
    scipy>=1.7.0,<1.14.0
    seaborn~=0.13.2
    setuptools>=60.0.0

Some features of the DATKit library, such as converting SVG images to PNG, require system-level dependencies that are not installed via ``pip``.

In particular, the `Cairo` graphics library must be available on your system, as it is used internally by ``cairosvg``.

Installation instructions by platform:

- **Linux (Debian/Ubuntu-based)**::

    sudo apt update
    sudo apt install libcairo2

- **macOS (using Homebrew)**::

    brew install cairo

- **Windows**:

  It is recommended to install the Cairo runtime using one of the following options:

  - Using Chocolatey::

      choco install gtk-runtime

  - Using Conda (if available in your environment)::

      conda install -c conda-forge cairo

If `libcairo` is not available, importing modules like ``DATKit.utils.image_utils`` or any functionality depending on ``cairosvg`` may fail, especially during documentation builds with Sphinx.

