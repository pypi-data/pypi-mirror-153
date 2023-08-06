from kolibri.config import TaskType

class ModulesRegistry:

    registry = {
        'Estimators':{
        },
        'kolibri':{}
    }

    for task_type in TaskType:
        registry['Estimators'][task_type.name]={}


    @staticmethod
    def add_algorithm(
        task_name,
        model_class,
        model_params,
        required_preprocessing,
        additional,
        default_params,
    ):
        model_information = {
            "class": model_class,
            "params": model_params,
            "required_preprocessing": required_preprocessing,
            "additional": additional,
            "default_params": default_params,
        }
        ModulesRegistry.registry['Estimator'][task_name][
            model_class.algorithm_short_name
        ] = model_information

    @staticmethod
    def add_module(
        module_name,
        module_class,
    ):
        ModulesRegistry.registry['kolibri'][module_name] = {'class':module_class}


from kolibri.tokenizers.word_tokenizer import WordTokenizer
from kolibri.tokenizers.regex_tokenizer import RegexpTokenizer
from kolibri.features.text.tf_idf_featurizer import TFIDFFeaturizer
from kolibri.tokenizers.sentence_tokenizer import SentenceTokenizer
from kolibri.preprocess.text.email_cleaner import EmailCleaner
from kolibri.tokenizers.kolibri_tokenizer import KolibriTokenizer
from kolibri.tokenizers.char_tokenizer import CharTokenizer
from kolibri.task.classification.sklearn_estimator import SklearnEstimator
from kolibri.autolearn.model_zoo.zoo_estimator import ZooEstimator