import regex as re
from kolibri.data.ressources import resources
from pathlib import Path
from kdmt.file import read_json_file
from kolibri.tokenizers import SentenceTokenizer
from kolibri.task.intents.intent_expressions import __get_intent_expression

patterns_file=resources.get(str(Path('modules', 'regexes', 'intents_payments.json'))).path
patterns=read_json_file(patterns_file)

intent_patterns={}

tokenize=SentenceTokenizer({'multi-line':False})


def __compile_patterns_in_dictionary(dictionary):
    """
    Replace all strings in dictionary with compiled
    version of themselves and return dictionary.
    """
    for name, regex_str in dictionary.items():

        if isinstance(regex_str, str):
            dictionary[name] = re.compile(regex_str, re.IGNORECASE|re.UNICODE)
        elif isinstance(regex_str, list):
            for i, reg_str in enumerate(regex_str):
                dictionary[name+'_'+str(i)] = re.compile(reg_str, re.IGNORECASE|re.UNICODE)
        elif isinstance(regex_str, dict):
            __compile_patterns_in_dictionary(regex_str)
    return dictionary

for (lang, regex_set) in patterns.items():
    intent_patterns[lang]={}
    for (name, regex_variable) in regex_set.items():
        if isinstance(regex_variable, str):
            # The regex variable is a string, compile it and put it in the
            # global scope
            intent_patterns[lang][name] = re.compile(regex_variable, re.IGNORECASE|re.UNICODE)
        elif isinstance(regex_variable, list):
            intent_patterns[lang][name]=[]
            for reg in regex_variable:
                intent_patterns[lang][name].append(re.compile(reg, re.IGNORECASE|re.UNICODE))
        elif isinstance(regex_variable, dict):
            # The regex variable is a dictionary, convert all regex strings
            # in the dictionary to their compiled versions and put the variable
            # in the global scope
            intent_patterns[lang][name] = __compile_patterns_in_dictionary(regex_variable)



def get_intent_expression(text, language):
    return __get_intent_expression(text, intent_patterns[language])



