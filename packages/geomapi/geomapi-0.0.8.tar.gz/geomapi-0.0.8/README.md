![geomapiLogo](https://geomatics.pages.gitlab.kuleuven.be/research-projects/geomapi/_images/geomapi_logo_B.png)
# GeomAPI

A joint API to standardize geomatic data storage and processing.

[[_TOC_]]

## Installation

Use the package manager [pip](https://pypi.org/project/geomapi) to install geomapi.

```bash
pip install geomapi
```

## Documentation

You can read the full API reference here:
[Documentation](https://geomatics.pages.gitlab.kuleuven.be/research-projects/geomapi/)

## Usage

The main use of this API is importing standardized RDF data into easy to use python classes.
These python classes have a number of fuctions to analyse, edit and combine the most common types of data including:
- Images (pinhole or panoramic)
- Meshes
- Point clouds
- BIM models

## Variable Standards

This library relies on a RDF based standardisation of data storage, Below are some of the more important variables:

- `cartesianTransform`: A 4x4 transformation matrix 
- Paths
  - `resourcePath` or `path`: the relative path from the graph folder to the asset of the node.
  - `sessionPath`: the absolute path of the graph folder

### Paths
Each node has a number of different relevant paths.
- Runtime: We need to know the location of the asset and the graph.ttl file, for this functions `get_resource_path()`

### .ttl vs. Node
Data that is stored on the RDF graph is not always useful for the Node and vise versa.
This is why some variables should not be stored in the graph:
- `sessionPath`: since the folder can be moved around and not all operatins systems use the same folder structure, we can not assume the folderpath will be correct. They are defined in the Node Class during initialisation is a graphPath is given. 

## Development

Testing the package is done in the tests folder with:
```py
from context import geomapi
```

## Licensing

The code in this project is licensed under GNU license.
