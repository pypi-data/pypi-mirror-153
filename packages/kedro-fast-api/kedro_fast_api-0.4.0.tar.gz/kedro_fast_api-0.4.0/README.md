README.md

# Kedro Fast API
kedro fast-api is a kedro plugin to easily create a fast-api for a kedro project for models' deployment.


## Instalation
To install kedro fast-api, run the following command in your bash terminal within the kedro project's folder:

```bash
pip install kedro-fast-api
```

## Initialize 
To initiate kedro fast-api, run the following command in your bash terminal in the same folder:

```bash
kedro fast-api init
```

This command will generate:

* A api_config.yml config file
* A catalog.yml file to save the predictor
* A new kedro pipeline (one node in one pipeline) with a predictor template.

## Predictor: what it is and how it works
The kedro fast-api will create a new kedro pipeline to create a prediction node. This predictor will be saved using kedro's structure and will be able to encapsulate a prediction file, which will perform predictions in an API.

### Main files

#### src/api_pipeline/nodes.py

The default api_pipeline nodes file is:

```python
import pandas as pd


class MLPredictor:
    def __init__(self, model):
        self.model = model

    def predict(self, args_API: pd.DataFrame):
        df_args = args_API
        prediction = self.model.predict(df_args)
        return {"prediction": prediction}


def save_predictor(model):
    predictor = MLPredictor(model)
    return predictor
```

This node does note performs any feature engineering in the API's input data. However, this file can be customized with any feature engineering or data preparation before running the predict function. 
The output can be also customized to any format needed, or even have more than one output.

#### src/api_pipeline/pipeline.py

The default pipeline file is:

```python
from kedro.pipeline import Pipeline, node

from .nodes import save_predictor


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=save_predictor,
                name="save_predictor",
                inputs="model",  ### Replace with model's name
                outputs="MLPredictor",
            )
        ]
    )
```

The node's input should gets the model catalog name. This model must have a "predict" method, such as scikit learn models or scikit learn pipelines.  

As this is a default pipeline, there is only one model being inputted, however, it is possible to edit this file to input more than one model, or even inputs other dataframes to perform any data preparation (remember to prepare your nodes.py file to properly match inputs and outputs needed).

#### conf/base/api_pipeline/catalog.yml

The predictor will be saved using kedro framework, as a pickle dataset, which encapsulates it to be used by the API. The defauilt predictor is at the catalog, as it follows:

```yaml
MLPredictor:
  type: pickle.PickleDataSet
  filepath: data/09_predictor/MLPredictor.pickle
  versioned: true
```

### After Init

After creating all files before running the API you must execute at least one time the api_pipeline, the API will try to load the pickle file from the catalog, if there is nothing there the API will not work. 

## api.yml: what it is and how it works

This file has the Fast-API properties to properly create the API. It specify the routes for the API. Every route is a name for the APIs, which will come after the / in the URL. There can be also more than one route within the same kedro project, e.g:

*  localhost:8000/model_API/

Each route will be specified to have a predictor, created using the predictornode and saved with the predictor pipeline in the kedro catalog path. 

Also, it is required to specify the input parameters (which are the predictor predict method inputs). The default api.yml is:

```yaml
routes:
  model_API:
    # Catalog reference to .pickle model
    predictor: MLPredictor
    # Inputs passed as a python dictionary
    # allowed types int, float, str, bool and enum
    parameters:
      input_1:
        # enum type requires options (numbers as options won't work)
        type: enum
        options:
          - some
          - options
          - here
      input_2:
        type: int
      input_3:
        type: float
      input_4:
        type: bool
      input_5:
        type: str
```

Remember that feature engineering can be made within predictor if needed. However, if the API inputs are the actual model's features, beware that the order they come in the API and their names are essential for a scikit learn model to run a prediction.

## Security
To add a security X-token to your API you need to add security keyword on api.yml file:
```yaml
security: True
routes:
  model_API:
    # Catalog reference to .pickle model
    predictor: MLPredictor
    # Inputs passed as a python dictionary
    # allowed types int, float, str, bool and enum
    parameters:
      input_1:
        # enum type requires options (numbers as options won't work)
        type: enum
        options:
          - some
          - options
          - here
      input_2:
        type: int
      input_3:
        type: float
      input_4:
        type: bool
      input_5:
        type: str
```

This keyword uses your enviroment varible API_SECRET_KEY to validate the request

## Creating the API

After setting all files, the API creation itself is made with the following command in bash:

```bash
kedro fast-api run
```

If no saving API path is provided, the default file will be saved in 

```yaml
conf/api.yml
```

If there is need to change the file path (or name), please use:

```bash
kedro fast-api run -p path_to_file/API_file_name.yml
```


