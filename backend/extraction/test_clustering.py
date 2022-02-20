# @Author: michael
# @Date:   2022-02-20T05:17:05-08:00
# @Email:  mnath@stanford.edu
# @Filename: test_clustering.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-20T05:22:53-08:00


from core_extraction import CORE_EXECUTION
import pandas as pd
from kmodes.kprototypes import KPrototypes
from sklearn.cluster import KMeans

# url_one = "https://www.cnn.com/2022/02/18/europe/ukraine-russia-conflict-explainer-cmd-intl/index.html"
# url_two = "https://www.newyorker.com/news/daily-comment/does-the-us-russia-crisis-over-ukraine-prove-that-the-cold-war-never-ended"
# url_three = "https://www.wpri.com/news/street-stories/if-we-lose-local-news-coverage-were-doomed-how-an-ri-newspaper-has-defied-the-digital-age/"
# url_four = "https://www.cnbc.com/2021/07/21/elon-musk-jack-dorsey-speak-about-cryptocurrency-at-b-word-conference.html"
# url_five = "https://www.npr.org/2022/02/19/1081952588/russia-ukraine-harris-sanctions"
# url_six = "https://www.bbc.com/news/business-51706225"

# def cluster_with_kmeans(meta_data_of_documents):
#     doc_insights = []
#     for meta_datum in meta_data_of_documents:
#         data = {
#         "neg_content_sentiment": meta_datum["content_sentiment"]["neg"],
#         "neu_content_sentiment": meta_datum["content_sentiment"]["neu"],
#         "pos_content_sentiment": meta_datum["content_sentiment"]["pos"],
#         }
#         doc_insights.append(data)
#
#     df = pd.DataFrame(doc_insights)
#     kmeans = KMeans(n_clusters=2).fit(df.values)
#     print(kmeans.predict(df.values))

def cluster_with_kprotoype(meta_data_of_documents):
    doc_insights = []
    df = pd.DataFrame(meta_data)
    for meta_datum in meta_data_of_documents:
        top_words = sorted(meta_datum["top_words"], key=lambda x: x["word"])
        top_words_uniq = {}
        for d in top_words:
            dic = {d["word"]: d["type"]}
            top_words_uniq.update(dic)
        top_words = top_words_uniq
        data = {
        "neg_content_sentiment": meta_datum["content_sentiment"]["neg"],
        "neu_content_sentiment": meta_datum["content_sentiment"]["neu"],
        "pos_content_sentiment": meta_datum["content_sentiment"]["pos"],
        }
        i = 1
        for key in top_words.keys():
            if i > 10: break
            data[f"top_words_{i}"] = key
            i += 1
        doc_insights.append(data)
    categorical_idx = [i for i in range(3, len(doc_insights[0]))]
    kproto = KPrototypes(n_clusters=3, max_iter=200).fit(df.values, categorical=categorical_idx)
    clusters = kproto.predict(df.values, categorical=categorical_idx)
    df['cluster'] = list(clusters)
    print(df)
