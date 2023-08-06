from kolibri.core import modules
from kolibri.logger import get_logger
import datetime
from kolibri.metadata import Metadata
from kolibri.core.pipeline import Pipeline
from kdmt.file import create_dir
from kdmt.objects import module_path_from_object
from pathlib import Path
from kolibri.core.modules import validate_requirements
from kolibri.optimizers.optuna.objective import PipelineObjective
from kolibri.utils.parallel import create_dask_client, close_dask_client
import os
import pandas as pd
import psutil
import uuid
from kolibri.optimizers.optuna.tuner import OptunaTuner
import time
from kolibri.config import ModelConfig


logger = get_logger(__name__)

MINIMUM_COMPATIBLE_VERSION = "0.0.1"


class ModelTrainer(object):
    """Trainer will load the texts and train all components.

    Requires a pipeline specification and configuration to use for
    the training."""

    SUPPORTED_LANGUAGES = ["fr", "en", "nl"]

    config={
        'save-evaluation-output': True,
        'evaluate-performance': False,
        'max-time-for-learner': 3600,
        'max-time-for-optimization': 3600,
        'random-state': 42,
        'ml-task': None,
        'explain-level': 2,
        'opt-metric-name': 'f1-score',
        'optimize-pipeline': False,
        'optimizer': 'optuna',
        'output-folder': '.',
        'n-jobs':-1
    }

    def __init__(self, params, skip_validation=False):

        self._dask_client=None
        self.override_default_parameters(params.as_dict())

        if psutil.cpu_count()>1 and(self.config['n-jobs']>1 or  self.config['n-jobs']==-1):
            self._dask_client=create_dask_client(cpu_count = self.config['n-jobs'] if self.config['n-jobs'] > 1 else psutil.cpu_count() if self.config[
                                                                                                  'n-jobs'] == -1 else 1)
        if self.config['evaluate-performance']==False:
            self.config['save-evaluation-output']=False

        if self.config['save-evaluation-output']==True:
            try:
                import openpyxl
            except:
                raise Exception("The library 'openpyxl' in not installed. To save evaluation result, You must install 'openpyxl' or chaange 'save-evaluation-output' to False")
        logger.debug("ModelTrainer.__init__")
        self.uid = str(uuid.uuid4())
        if not isinstance(params, ModelConfig):
            raise ValueError("Config erro: Configuration object is not of type ModelConfig")

        for i in ["pipeline", "model"]:  # mandatory parameters
            if i not in params:
                msg = "Missing {0} parameter in Model Trainer params".format(i)
                logger.error(msg)
                raise ValueError(msg)

        self._explain_level = params.get("explain-level")

        self.train_time = None
        self.final_loss = None
        self.metric_name = None
        self._threshold = None  #for binary classifiers

        # the automl random state from AutoML constructor, used in Optuna optimizer
        self._random_state = params.get("random-state")


#        self.config



        # Before instantiating the component classes, lets check if all
        # required packages are available
        if not skip_validation:
            validate_requirements(params['pipeline'])
        self.performance_data=None
        # build pipeline

        self.pipeline = self._build_pipeline(params)

    @staticmethod
    def _build_pipeline(params):
        """Transform the passed names of the pipeline components into classes"""

        steps = []
        # Transform the passed names of the pipeline components into classes
        for component_name in params['pipeline']:
            component = modules.create_component_by_name(
                component_name, params)
            steps.append((component_name, component))

        return Pipeline(steps)

    def fit(self, X, y, X_val=None, y_val=None):
        """Trains the underlying pipeline using the provided training texts."""
        logger.debug(f"ModelTrainer.fit {self.config.get('models')}")
        start_time = time.time()
        if self.config.get('optimize-pipeline'):
            logger.debug(f"ModelTrainer.fit - optimizing pipeline")
            self.optimize(X, y)

        self.pipeline.fit(X, y, X_val, y_val)

        if self.config['save-evaluation-output']==True and self.pipeline.estimator.validatation_data is not None:
            self.performance_data=pd.DataFrame(X)
            self.performance_data['class']=y
            self.performance_data['prediction']=self.pipeline.estimator.validatation_data[:,0]
            self.performance_data['probability']=self.pipeline.estimator.validatation_data[:,1]

        self.train_time=time.time()-start_time
        close_dask_client(self._dask_client)
        return self.pipeline.estimator

    def objective(self, X, y):
        objective=PipelineObjective(X, y, self.pipeline, None, eval_metric=self.config['opt-metric-name'],n_jobs=-1, random_state=42)
        return objective


    def optimize(self, X, y):
        try:
            optimizer = OptunaTuner(
                    self.config['output-folder'],
                    eval_metric=self.config['opt-metric-name'],
                    time_budget=self.config['max-time-for-optimization'],
                    init_params={},
                    verbose=True,
                    n_jobs=-1,
                    random_state=self.config['random-state'],
                )

            start_time = time.time()
            self.hyperparameters = optimizer.optimize(
                objective=self.objective(X, y),
                learner_params=self.pipeline.hyperparameters
            )
            self.optimization_time=time.time()-start_time


        except Exception as e:
            raise Exception('Could not optimize model. Exception raised: '+str(e))

    def override_default_parameters(self, custom):

        if custom:
            if isinstance(custom, dict):
                for key in self.config:
                    v= custom.get(key,None )
                    if v:
                        self.config[key]=v


    def get_train_time(self):
        return self.train_time

    def persist(self, path, fixed_model_name=None):
        """Persist all components of the pipeline to the passed path.

        Returns the directory of the persisted model."""


        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        metadata = {
            "pipeline": [],
        }

        if fixed_model_name:
            model_name = fixed_model_name
        else:
            model_name = "model_" + timestamp

        path = Path(path).resolve()
        dir_name = os.path.join(path, model_name)

        create_dir(dir_name)

        #        if self.training_data:
        #            metadata.update(self.training_data.persist(dir_name))

        for component in self.pipeline.steps.values():
            update = component.persist(dir_name)
            component_meta = component.hyperparameters
            if update:
                component_meta.update(update)
            component_meta["label"] = module_path_from_object(component)
            component_meta["name"] = component.name

            metadata["pipeline"].append(component_meta)

        Metadata(metadata, dir_name).persist(dir_name)

        if self.performance_data is not None:
            try:
                self.performance_data.to_excel(os.path.join(path, 'validatation_data_.xlsx'))
            except:
                pass

        logger.info("Successfully saved model into "
                    "'{}'".format(os.path.abspath(dir_name)))
        return dir_name



