# tendrils api
Cosmic `tendrils` is a fully type annoted Python API wrapper for both FLOWS 
[pipeline](https://github.com/SNflows/flows/ ) 
and [project](https://flows.phys.au.dk). 

Currently, tendrils is reliant on the flows project webserver. However, the functionality is 
there for it to interface with any remote server providing an API with given URLS. all URLS can be modified
in `utils/urls.py` to point to a different API, and tendrils can be used to interface with it.

Homepage: https://github.com/SNflows/tendrils   
PYPI: https://pypi.org/project/tendrils/
# installation

`pip install tendrils`

### Requirements:
`astropy, numpy, requests, tqdm`   
`python >= 3.10`
# Before you begin [IMPORTANT!]

You will need to populate the included template `config.ini` with the right paths and flows API 
token. To do so, you can use the tools provided in `tendrils.utils`. There is:
 - a guided method that queries you in the command line for each field.
 - a function for copying from an already filled out (e.g., previous) config.ini file.
 - functions for setting each attribute separately (if you only need the API token for example)

using python shell (or ipython, or a script):
```
import tendrils

# Option 1
tendrils.utils.create_config()  # will also ask for location of where to store flows photometry.

# Option 2
tendrils.utils.copy_from_other_config('<path_to_other_config>')

# Option 3
# can also be called without any arguments to query for manually inputting the token.
tendrils.utils.set_api_token(token = 'my_long_token')  

```
After doing any of the above, your config.ini will have your API token, and all API calls will now use that token.

# Dev

After cloning from the github repo, use the provided pyproject.toml file. Install using `flit` (`pip install flit`):
`flit install --symlink` to install in EDITABLE mode. A legacy `setup.py` is also provided for installing with 
`pip install -e .` from the root directory. Important, do not upload you `config.ini`! Make sure all values are None
as in the template from Pypi. We welcome all PRs.
