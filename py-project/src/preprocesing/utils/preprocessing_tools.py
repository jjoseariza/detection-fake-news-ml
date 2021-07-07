import re
import nltk 
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from config import config
import pickle
import string
from bs4 import BeautifulSoup


def ReplaceDiatrics(strText):
    strText = re.sub(r"Á|Â|À|Ä", u"A", strText)
    strText = re.sub(r"â|à|á|ä", u"a", strText)

    strText = re.sub(r"É|Ê|È|Ë", u"E", strText)
    strText = re.sub(r"ê|è|é|ë", u"e", strText)

    strText = re.sub(r"Í|Î|Ì|Ï", u"I", strText)
    strText = re.sub(r"î|ì|í|ï", u"i", strText)

    strText = re.sub(r"Ó|Ô|Ò|Ö", u"O", strText)
    strText = re.sub(r"ô|ò|ó|ö", u"o", strText)

    strText = re.sub(r"Ú|Û|Ù|Ü", u"U", strText)
    strText = re.sub(r"û|ù|ú|ü", u"u", strText)
    return strText


def PunctRemove(strPrepro):
    strRemove = ".·:,;\"'“”¡!¿?[]<>\(\)\\{}+-*/^=|\\#$%&@`~"
    strPrepro = "".join(c if c not in strRemove else " " for c in strPrepro)
    strPrepro = re.sub(r"\s[\-\_\']+\s", " ", strPrepro)
    strPrepro = re.sub(r"[\s]+", " ", strPrepro).strip()
    return strPrepro


def PreprocessText(text_df, field):
    df_proc = text_df
    df_proc[field] = df_proc[field].str.lower()
    stop = stopwords.words(config["preprocessing"]["stopwords-language"])
    df_proc[field] = df_proc[field].apply(
        lambda x: " ".join([item for item in str(x).split() if item not in stop])
    )
    df_proc[field] = df_proc[field].map(lambda x: ReplaceDiatrics(x))
    df_proc[field] = df_proc[field].map(lambda x: PunctRemove(x))
    return df_proc


def Tfidf_transform(documents, load_transform_model):
    if not load_transform_model:
        tfidfconverter = TfidfVectorizer(
            max_features=config["preprocessing"]["vec-max-featues"]
        )

        X = tfidfconverter.fit(documents)

        pickle.dump(tfidfconverter, open(config["preprocessing"]["output_path"], "wb"))
    else:
        tfidfconverter = pickle.load(open(config["preprocessing"]["output_path"], "rb"))

    X = tfidfconverter.transform(documents)
    return X


def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def remove_between_square_brackets(text):
    return re.sub("\[[^]]*\]", "", text)


def remove_between_square_brackets(text):
    return re.sub(r"http\S+", "", text)


def remove_stopwords(text):
    stop = set(stopwords.words("english"))
    punctuation = list(string.punctuation)
    stop.update(punctuation)

    final_text = []
    for i in text.split():
        if i.strip().lower() not in stop:
            final_text.append(i.strip())
    return " ".join(final_text)


def denoise_text(text):
    text = str(text)
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text = remove_stopwords(text)
    return text
