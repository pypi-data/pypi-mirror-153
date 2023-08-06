from .deep_text import BPE

class Length(object):
    """
    number of characters in a string.
    eg. length("I am rima") results 9
    """
    def __init__(self):
        pass
    def apply(self, value):
        if value is None:
            return value
        return len(str(value))

class CountDigits(object):
    """
    count the number of digits in a string.
    eg. CountDigits("I am Rima 7") results in 1
    """
    def __init__(self):
        pass
    def apply(self, value):
        return sum(c.isdigit() for c in str(value))


class CountWord(object):
    """
    count the appearances of a word in a string.
    eg. CountWord("I am Rima 7", "Rima") results is 1
    """
    def __init__(self, word):
        self.word = word
    def apply(self, value):
        return value.lower().count(self.word.lower())

class StandardName(object):
    """
    checks if a name is a standard english name.
    expects an array of standard english names.
    """
    def __init__(self, standard_names):
        self.names = standard_names #fill from api or cache.
    def apply(self, name):
        name = str(name)
        # some names have questions marks in them, killing the regex!
        s = name.replace("?","").replace('(', '').replace(')', '').split(' ')
        if len(s):
            s = s[0]
        #return standard_names_df.name.str.contains(s, case=False).any()
        return bool(s in self.names)


class Tokenize(object):
    """
    Apply the BEP Tokenizer to the provided text
    """
    def __init__(self):
        self.tokenizer = BPE()
        
    def apply(self, value):
        return self.tokenizer.encode(text=value, padding=True, seq_len=len(value))


instructions_map = {
    "Length": Length,
    "CountDigits": CountDigits,
    "CountWord": CountWord,
    "StandardName": StandardName,
    "Tokenize": Tokenize
}
