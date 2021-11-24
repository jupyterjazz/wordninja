import gzip, os
from .constants import *
from math import log


class Wordninja(object):
    """Probabilistically splits concatenated words using NLP based on uni-gram frequencies.
    Forked from https://github.com/keredson/wordninja
    Main additions:
    * Works for Georgian language.
    * Allows you to modify model's behaviour by adding or removing specific words.
    * Allows you to save and reuse modified models. 
    """
    def __init__(self, model_name=DEFAULT_MODEL):
        cfd = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(cfd, MODELS_DIR, model_name + FORMAT)
        with gzip.open(path) as f:
            words = f.read().decode().split()
        self._word_costs = self._score_words(words)
        self._max_length = max(len(word) for word in words)

    @staticmethod
    def _score_words(words):
        """Assuming Zipf's law holds, we can assign `1/(nlogN)`
        probability to the words where `n` is the rank of the word
        (i.e. how frequent it is) and `N` is the number of words 
        in the dictionary.
        """
        word_costs = dict(
            (word, log((position + 1) * log(len(words))))
            for position, word in enumerate(words)
        )
        return word_costs

    def add_word(self, word):
        if word in self._word_costs:
            return
        tokens = self.split(word)
        max_cost = max([self._word_costs[token] for token in tokens])
        modified_cost = max_cost * COEFFICIENT
        self._word_costs[word] = modified_cost

    def remove_word(self, word):
        self._word_costs.pop(word, None)

    def save_model(self, model_name=MODIFIED_MODEL):
        sortd = [
            word
            for word, cost in sorted(self._word_costs.items(), key=lambda item: item[1])
        ]
        sortd_str = "\n".join(sortd)
        compr = gzip.compress(sortd_str.encode())
        cfd = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(cfd, MODELS_DIR, model_name + FORMAT)
        with open(path, "wb") as f:
            f.write(compr)

    def split(self, string):
        nested_output = [self._split_string(substr) for substr in string.split(" ")]
        output = [token for sublist in nested_output for token in sublist]
        return output

    def _find_best_match_for_substring(self, costs, string, index):
        """Finds the best match for the current substring 
        (i.e. string[:index]) based on the best matches 
        for previous substrings (i.e. string[:index-1], string[:index-2], etc.)
        """
        candidates = enumerate(
            reversed(costs[max(0, index - self._max_length) : index])
        )
        return min(
            (
                cost
                + self._word_costs.get(
                    string[index - length - 1 : index].lower(), 9e999
                ),
                length + 1,
            )
            for length, cost in candidates
        )

    def _split_string(self, string):
        """Splits the string using dynamic programming."""
        costs, lengths = [0], [0]
        for index in range(1, len(string) + 1):
            cost, length = self._find_best_match_for_substring(costs, string, index)
            costs.append(cost)
            lengths.append(length)

        output = []
        index = len(string)
        while index > 0:
            length = lengths[index]
            new_token = True
            if (
                len(output) > 0
                and string[index - 1].isdigit()
                and output[-1][0].isdigit()
            ):
                output[-1] = string[index - length : index] + output[-1]
                new_token = False

            if new_token:
                output.append(string[index - length : index])

            index -= length
        return reversed(output)
