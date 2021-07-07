import re
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


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
    
    strRemove = '.·:,;\"\'“”¡!¿?[]<>\(\)\\{}+-*/^=|\\#$%&@`~' 
    strPrepro = "".join(c if c not in strRemove else ' ' for c in strPrepro)
    strPrepro = re.sub(r"\s[\-\_\']+\s", ' ', strPrepro) # when not alone, remove multiple - ' _
    strPrepro = re.sub(r"[\s]+", ' ', strPrepro).strip() # replace multiple spaces with a single one
    return(strPrepro)

def PreprocessText(text_df):
    print("-----Text Preprocessing Started-----")
    df_proc=text_df
    df_proc["text_0"]=df_proc["text_0"].str.lower()
    print(" ----Removing Stopwords---- ")
    stop = stopwords.words('english')
    df_proc['text_0'] = df_proc['text_0'].apply(lambda x: ' '.join([item for item in str(x).split() if item not in stop]))
    print(" ----Removing Diatrics---- ")
    df_proc['text_0'] =df_proc['text_0'].map(lambda x: ReplaceDiatrics(x))
    print(" ----Removing Punctuation---- ")
    df_proc['text_0'] =df_proc['text_0'].map(lambda x: PunctRemove(x))
    print("-----Text Preprocessing Finished-----")
    return(df_proc)

def Tfidf_fit(documents):
    print("-----Tfidf fitting-----")
    tfidfconverter = TfidfVectorizer(max_features=5000)
    X = tfidfconverter.fit(documents)
    pickle.dump(tfidfconverter, open('vectorizer.sav', 'wb'))
    return X

def Tfidf_transform(documents):
    print("-----Tfidf transforming-----")
    tfidfconverter=pickle.load(open('vectorizer.sav', 'rb'))
    X=tfidfconverter.transform(documents)
    return X

