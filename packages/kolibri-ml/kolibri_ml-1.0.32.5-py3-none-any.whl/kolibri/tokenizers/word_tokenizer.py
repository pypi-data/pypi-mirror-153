import time

from kolibri.tokenizers.regex_tokenizer import RegexpTokenizer
from kolibri.tokenizers.tokenizer import Tokenizer
from kolibri.config import ModelConfig
from kdmt.dict import update

class WordTokenizer(Tokenizer):
    defaults = {
        "fixed": {
            'whitespace': False,
            'regex': None,
            'filters': '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
            'split': " "
        },

        "tunable": {
        }
    }
    def __init__(self, parameters={}):
        """
            filters: list (or concatenation) of characters to filter out, such as
            punctuation. Default: ``!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\\t\\n``,
            includes basic punctuation, tabs, and newlines.
            lower: boolean. Whether to convert the input to lowercase.
            split: str. Separator for word splitting.

        :param config:
        """
        super().__init__(parameters)

        tknzr = RegexpTokenizer(parameters=parameters)
        self._tokenize=tknzr.tokenize
        self.do_lower_case=self.get_parameter('do-lower-case')
        self.split=self.get_parameter("split")
        self.filters=self.get_parameter("filters")

        if self.get_parameter('whitespace'):
            self._tokenize=self.whitespace_tokenize
        if self.get_parameter('regex') is not None:
            toknizr=RegexpTokenizer({'pattern':self.get_parameter('regex')})
            self._tokenize=toknizr.tokenize



    def update_default_hyper_parameters(self):
        self.defaults=update(self.defaults, WordTokenizer.defaults)
        super().update_default_hyper_parameters()


    def fit(self, training_data, target):
        return self

    def tokenize(self, text):
        """Tokenizes a piece of text."""
        text=super(WordTokenizer, self).tokenize(text)
        orig_tokens = self._tokenize(text)
        split_tokens = []
        for token in orig_tokens:
            if self.do_lower_case:
                token = token.lower()
            if self.remove_stopwords and token.lower() in self.stopwords:
                continue
            if self.get_parameter('split-on-punctuation'):
                split_tokens.extend(self._run_split_on_punc(token))
            else:
                split_tokens.append(token)


        return split_tokens

    def whitespace_tokenize(self, text):
        """Converts a text to a sequence of words (or tokens).

        # Arguments
            text: Input text (string).
        # Returns
            A list of words (or tokens).
        """

        translate_dict = {c: self.split for c in self.filters}
        translate_map = str.maketrans(translate_dict)
        text = text.translate(translate_map)

        seq = text.split(self.split)
        return [i for i in seq if i]

    def transform(self, texts, **kwargs):

        return [self.tokenize(d) for d in texts]

    def get_info(self):
        return "word_tokenizer"


from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(WordTokenizer.name, WordTokenizer)
