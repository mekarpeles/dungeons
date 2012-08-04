import string

def is_punctuated(txt):
    return any([punc in txt for punc in set(string.punctuation)])

def punctuate(txt):
    # If there's no punctuation,     
    if not is_punctuated(txt):
        return txt + "."
    return txt

def sentence_type(txt):
    for punc, stype in [("?", "asks"), ("!", "exclaims"),
                        (".", "says"), ("", "says")]:
        if punc in txt:
            return stype
    return "says"

