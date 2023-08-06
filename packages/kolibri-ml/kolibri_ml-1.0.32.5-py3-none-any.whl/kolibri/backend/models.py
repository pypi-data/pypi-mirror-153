# -*- coding: utf-8 -*-
# Author: XuMing <xuming624@qq.com>
# Brief:

from kdmt.file import read_json_file
from pathlib import Path
from kolibri.data.ressources import resources

sklearn_classifier_path= resources.get(str(Path('models', 'sklearn', 'classifiers.json'))).path
sklearn_models=read_json_file(sklearn_classifier_path)
sklearn_models_names=list(sklearn_models.keys())


def get_model(model_name, weights=None, bakend='tensorflow'):
    if isinstance(model_name, list) and len(model_name)>1:
        models_ = [sklearn_models.get(model, None) for model in model_name]

        if weights is None:
            weights = [1 for model in model_name]
        model_cict={
      "class": "sklearn.ensemble.VotingClassifier",
      "name": "voting_classifier",
      "parameters": {
        "estimators": {
          "value": models_
        },
        "voting": {
          "value": "soft",
          "type": "categorical",
          "values": ["soft", "hard"]
        },
        "weights": {
          "value": weights
        },
        "n_jobs":{
            "value": -1
        }
      }
    }

        return model_cict

    elif isinstance(model_name, list) and len(model_name)==1:
        model= sklearn_models.get(model_name[0], None)
    else:
        model= sklearn_models.get(model_name, None)

    if model is None:
        raise ModuleNotFoundError("Model named: "+model_name+" was  not found")

    return model



if __name__=="__main__":
    models_=["LogisticRegression", "knn"]
    models_=[get_model(m) for m in models_]
    print(models_)