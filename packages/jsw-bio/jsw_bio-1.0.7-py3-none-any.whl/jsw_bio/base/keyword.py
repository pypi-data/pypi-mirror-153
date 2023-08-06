import nltk


def keyword(in_string, **kwargs):
    sentences = nltk.sent_tokenize(in_string)
    selector = kwargs.get('selector', lambda item: 'NNP' == item[1])
    callback = kwargs.get('callback', lambda item: item[0].lower())
    res = []
    data = []

    for sent in sentences:
        data = data + nltk.pos_tag(nltk.word_tokenize(sent))
    for word in data:
        if selector(word):
            res.append(callback(word))

    return res
