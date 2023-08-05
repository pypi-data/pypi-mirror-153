punctuations = ['(', ')', ';', ':', '[', ']', ',']
stop_words = ['', ' ']


def get_words(text):
    tokens = text.split(" ")
    keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
    return keywords
