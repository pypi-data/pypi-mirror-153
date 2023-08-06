from kolibri.data import load
from kolibri.data.downloader import get_subpackages
from pathlib import Path
import types


__all__=["get_available_domains"]


patterns_directory=get_subpackages('intents')


def __available_doamins():
    """
    Given a wordlist name, return a dictionary of intent domain names to filenames,
    representing all the domains in which an intent is available.
    """


    available = {}
    if patterns_directory is None:
        return available

    for filename in patterns_directory:
        list_name = filename.split('.')[0]

        available[list_name] = str(filename)

    return available


def get_available_domains():
    return [k for k, v in __available_doamins().items()]


def import_code(code, name, add_to_sys_modules=True):
    # create blank module
    module = types.ModuleType(name)
    # populate the module with code
    exec(code, module.__dict__)
    if add_to_sys_modules:
        globals()[name] = module



code_template = """
from kolibri.task.text.intents.intent_expressions import IntentExpression

intent_generator=IntentExpression(intents="{}")

def get_intent_expression(text, langauge):
    return intent_generator.get_intent_expression(text, langauge)"""

for domain, file in __available_doamins().items():
    import_code(code=code_template.format(file), name=domain)


#payments.get_intent_expression("ma facture est tres elevée", "fr")