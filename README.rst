TAUP_DATKit
============

Overview
--------
TAUP_DATKit (*TAU Protein - Data Analysis Tool Kit*) is a package designed for data analysis on chromatographic data. It includes various functions for:

- Loading data from different sources, such as CSV and Excel files.
- Merging data and homogenizing spectra using data interpolation techniques.
- Complex filtering of elements.
- Representation and visualization of distances and similarities between elements.

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
        -  #TODO
    - "docs/": Documentation for using the package and understanding its functionality.
        -  #TODO
    - "properties/": #TODO
        -  #TODO
    - "tools/": #TODO
        -  #TODO
    - "utils/": #TODO
        -  #TODO

For detailed instructions on installation and usage, see the documentation in the **docs/** directory.

