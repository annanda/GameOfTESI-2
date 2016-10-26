import nltk 
import string
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

class URIAnalyser(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        self.stemmer = nltk.stem.RSLPStemmer()
        self.stopwords = nltk.corpus.stopwords.words("portuguese")
            
    def __call__(self, doc):
        #Tokenize words:
        doc = word_tokenize(doc)
        
        #Remove small words:
        doc = [t for t in doc if len(t) > 2]
        
        #Get alpha strings:
        doc = [t for t in doc if t.isalpha()]
        
        #Remove stopwords:
        doc = [t for t in doc if t not in self.stopwords]
        
        #Stem words:
        doc = [self.stemmer.stem(t) for t in doc]
        
        #print(doc)
        return doc

def tfIdfMatrix(corpus):
    vect = TfidfVectorizer(analyzer=URIAnalyser(),norm="l1")
    tfIdfmatrix = vect.fit_transform(corpus).toarray()
    terms = vect.get_feature_names()
    #newDoc = ["acho quero"]
    #r = vect.transform(newDoc).toarray()
    return tfIdfmatrix, terms
