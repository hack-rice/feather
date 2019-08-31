
class Normalizer:
    """A class that normalizes strings, so that we can quickly tell if an
    input that hasn't been normalized is valid.

    For example, we want to accept "Accept" as being equal to "accept". This
    class abstracts some of that ugliness away. (Note: in this example, "accept"
    is considered the normalized string.
    """
    @staticmethod
    def _normalize(word: str) -> str:
        # remove white space from input word and make all characters lower case
        # this is how we describe a normalized word
        return "".join(section.strip().lower() for section in word.split())

    def __init__(self, *words: str):
        # normalize the inputs
        self._words = [self._normalize(word) for word in words]

    def matches(self, word: str):
        """
        :param word: a string to be tested against our stored inputs
        :return: whether or not the input word can be normalized to one
            of the words stored in the Normalizer.
        """
        normalized_word = self._normalize(word)
        return normalized_word in self._words
