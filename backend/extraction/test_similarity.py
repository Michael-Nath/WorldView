from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
from core_extraction import SIMILARITY_HELPER
from re import sub
from gensim.utils import simple_preprocess
import gensim.downloader as api
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from gensim.similarities import SoftCosineSimilarity
import numpy as np


# Download stopwords list
nltk.download('punkt')
nltk.download('omw-1.4')
stop_words = set(stopwords.words('english')) 

class LemmaTokenizer:
    ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc) if t not in self.ignore_tokens]

def preprocess(doc):
    # Tokenize, clean up input document string
    doc = sub(r'<img[^<>]+(>|$)', " image_token ", doc)
    doc = sub(r'<[^<>]+(>|$)', " ", doc)
    doc = sub(r'\[img_assist[^]]*?\]', " ", doc)
    doc = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", doc)
    return [token for token in simple_preprocess(doc, min_len=0, max_len=float("inf")) if token not in stop_words]




def determine_similarity_tfidf(documents):
    tokenizer=LemmaTokenizer()
    token_stop = tokenizer(' '.join(stop_words))
    vectorizer = TfidfVectorizer(stop_words=token_stop, tokenizer=tokenizer)
    doc_vectors = vectorizer.fit_transform(documents)
    cosine_similarities = linear_kernel(doc_vectors, doc_vectors)
    print(cosine_similarities)

url_one = "https://www.cnn.com/2022/02/18/europe/ukraine-russia-conflict-explainer-cmd-intl/index.html"
url_two = "https://www.newyorker.com/news/daily-comment/does-the-us-russia-crisis-over-ukraine-prove-that-the-cold-war-never-ended"
url_three = "https://www.wpri.com/news/street-stories/if-we-lose-local-news-coverage-were-doomed-how-an-ri-newspaper-has-defied-the-digital-age/"
url_four = "https://www.cnbc.com/2021/07/21/elon-musk-jack-dorsey-speak-about-cryptocurrency-at-b-word-conference.html"
url_five = "https://www.npr.org/2022/02/19/1081952588/russia-ukraine-harris-sanctions"
url_six = "https://www.bbc.com/news/business-51706225"
urls = [url_one, url_two, url_three, url_four, url_five, url_six]


def determine_similarity_gensim(documents):
    # Load the model: this is a big file, can take a while to download and open
    glove = api.load("glove-wiki-gigaword-50")    
    similarity_index = WordEmbeddingSimilarityIndex(glove)
    corpus = [preprocess(document) for document in documents]
    # Build the term dictionary, TF-idf model
    dictionary = Dictionary(corpus)
    tfidf = TfidfModel(dictionary=dictionary)
    similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, tfidf)
    index = SoftCosineSimilarity(
            tfidf[[dictionary.doc2bow(document) for document in corpus]],
            similarity_matrix)
    query_tf = tfidf[dictionary.doc2bow(corpus[0])]
    index = SoftCosineSimilarity(
            tfidf[[dictionary.doc2bow(document) for document in corpus]],
            similarity_matrix)
    doc_similarity_scores = index[query_tf]
    sorted_indexes = np.argsort(doc_similarity_scores)[::-1]
    for idx in sorted_indexes:
        print(f'{idx} \t {doc_similarity_scores[idx]:0.3f} \t {documents[idx]}')

documents = []
for url in urls:
    meta_datum = SIMILARITY_HELPER(url)
    documents.append(" ".join(meta_datum))
# determine_similarity_tfidf(documents)
determine_similarity_gensim(documents)