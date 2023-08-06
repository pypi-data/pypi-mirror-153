#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'mohamedbenhaddou'

import regex as re
from kolibri.tokenizers.tokenizer import Tokenizer
from kolibri.stopwords import get_stop_words
from kdmt.dict import update
import numpy as np
from kolibri.data.ressources import resources
from pathlib import Path
from kdmt.file import read_json_file
from kolibri.tools import regexes as common_regs
from kolibri.tools._regex import Regex
from kolibri.tools.scanner import Scanner

patterns_file=resources.get(str(Path('modules', 'tokenizers', 'default_regexes.json'))).path
regexes=read_json_file(patterns_file)





class KolibriTokenizer(Tokenizer):
    provides = ["tokens"]

    defaults = {
        "fixed": {
        },

        "tunable": {
            "abstract-entities": {
                "value": True,
                "type": "categorical",
                "values": [True, False]
            },
            "group-entities": {
                "value": False,
                "type": "categorical",
                "values": [True, False]
            }

        }
    }

    def __init__(self, hyperparameters=None):
        super().__init__(hyperparameters)

        for (name, regex_variable) in regexes.items():
            setattr(self, name, Regex(regex_variable["label"], regex_variable["value"], regex_variable["flags"] if "flags" in regex_variable else 0) )



        self.stopwords = None
        if "language" in self.hyperparameters:
            self.language = self.hyperparameters["fixed"]["language"]
            self.stopwords = get_stop_words(self.language)


        lang=self.language.upper()


        patterns =[self.CANDIDATE, self.EXCEPTIONS, common_regs.URL, common_regs.MONEY]
        if lang in common_regs.DATE:
            patterns.append(common_regs.DATE[lang])

        patterns.append(common_regs.TIME)
        if lang in common_regs.MONTH:
            patterns.append(common_regs.MONTH[lang])

        if lang in common_regs.DURATION:
            patterns.append(common_regs.DURATION[lang])

        patterns.extend([self.OPENPARENTHESIS, self.CLOSEPARENTHESIS, self.WS, self.MULTIPLEWORD, self.ACORNYM, self.NUM, self.PLUS, self.MINUS, self.ELLIPSIS, self.DOT, self.TIMES, self.EQ,
                 self.QUESTION,
                 self.EXLAMATION, self.COLON, self.COMA, self.SEMICOLON, self.OPENQOTE, self.ENDQOTE, self.DOUBLEQOTE, self.SINGLEQOTE, self.PIPE,  self.WORD, self.OTHER,])

        self.scanner=Scanner(patterns)


    def tokenize(self, text):
        text = str(text).replace(r'\u2019', '\'')
        tokens=self.scanner.scan(text)

        tokens= [token for token in tokens if token[0] not in ['WS']]

        if self.get_parameter("abstract-entities"):
            tokens=['__'+t[0]+'__' if t[0] in ['WA', 'EMAIL', 'MONEY', 'DATE', 'MONTH', 'DURATION', 'NUMBER', 'FILE'] else t[1] for t in tokens]
        else:
            tokens=[(t[1], t[1])  for t in tokens]
        return tokens

    def transform(self, X):
        if not isinstance(X, list) and not isinstance(X, np.ndarray):
            X=[X]
        return [self.tokenize(x) for x in X]


    def update_default_hyper_parameters(self):
        self.defaults=update(self.defaults, KolibriTokenizer.defaults)
        super().update_default_hyper_parameters()



from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(KolibriTokenizer.name, KolibriTokenizer)



if __name__=='__main__':
    tokenizer = KolibriTokenizer({"abstract-entities":True})
    text = """
    Please
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
    Met vriendelijke groet"""
    tokens = tokenizer.tokenize(text)

    [print(t) for t in tokens]