import fasttext
import collections
from kolibri.data.ressources import resources
from pathlib import Path

light_model_loc=resources.get(str(Path('modules', 'language_detector', 'lid.176.ftz'))).path
large_model_loc=resources.get(str(Path('modules', 'language_detector', 'lid.176.bin')), external_url="https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin").path


small_model = None
large_model = None
model=None


def detect_language(text, num_laguages=2, use_large_model=True):
    global small_model, large_model, model
    if small_model is None:
        small_model=fasttext.load_model(light_model_loc)
    if large_model is None:
        large_model=fasttext.load_model(large_model_loc)

    model=small_model
    if use_large_model:
        model=large_model

    sentences=text.split('\n')

    predictions = collections.Counter()

    for sentence in sentences:
        predictions.update(__detect_language_one_sentence(sentence, num_laguages))

    #sort and select top num_langages
    predictions = dict(list(sorted(predictions.items(), key=lambda kv: -kv[1]))[:num_laguages])

    #normalize
    factor = sum(predictions.values())
    predictions = {k: v/factor for k, v in predictions.items()}

    return predictions

def __detect_language_one_sentence(text, num_laguages=2):


    if model is not None:
        predeiction = model.predict(text, k=num_laguages)
        results=[]

        results.append([p.replace('__label__', '') for p in predeiction[0]])
        results.append(predeiction[1])



        return dict(zip(results[0], results[1]))

    return {}



print(detect_language(""" Please
    29-APR-2019
    add the 'Statutory > NL-Sick Leave' => See table below.
    Company
    UPI
    Legal Name - Last Name
    Preferred Name - First Name
    Type of Leave
    Start of Leave
    Estimated Last Day of Leave
    Actual Last Day of Leave
    6079 AbbVie BV Commercial
    10373417
    Bosua
    Rosanna
    Statutory > NL-Sick Leave
    28-APR-2020
    6079 AbbVie BV Commercial
    1035A552B6
    Scholtes
    Monique
    Statutory > NL-Sick Leave
    26-NOV-2018
    25-NOV-2019
    Thanks!
    Met vriendelijke groet"""))