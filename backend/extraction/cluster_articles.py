# @Author: michael
# @Date:   2022-02-20T05:25:14-08:00
# @Email:  mnath@stanford.edu
# @Filename: cluster_articles.py
# @Last modified by:   shounak
# @Last modified time: 2022-03-25T13:38:19-06:00


import pandas as pd
from kmodes.kprototypes import KPrototypes
from sklearn.cluster import KMeans

# def cluster_with_kmeans(meta_data_of_documents):
#     doc_insights = []
#     for url in meta_data_of_documents.keys():
#         meta_datum = meta_data_of_documents[url]
#         data = {
#         "url": url,
#         "neg_content_sentiment": meta_datum["content_sentiment"]["neg"],
#         "neu_content_sentiment": meta_datum["content_sentiment"]["neu"],
#         "pos_content_sentiment": meta_datum["content_sentiment"]["pos"],
#         }
#         doc_insights.append(data)
#
#     df = pd.DataFrame(doc_insights)
#     df_to_fit = df.drop(columns=["url"])
#     kmeans = KMeans(n_clusters=5).fit(df_to_fit.values)
#     df["cluster"] = kmeans.predict(df_to_fit.values)
#     # print(kmeans.predict(df_to_fit.values))
#     # print(df)

def cluster_with_kprotoype(meta_data_of_documents):
    MAX_CLUSTERS = len(meta_data_of_documents)

    doc_insights = []
    for doc in meta_data_of_documents:
        meta_datum = doc["data"]
        top_words = sorted(meta_datum["top_words"], key=lambda x: x["word"])
        top_words_uniq = {}
        for d in top_words:
            dic = {d["word"]: d["type"]}
            top_words_uniq.update(dic)
        top_words = top_words_uniq
        data = {
        "url": meta_datum["url"],
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
    df = pd.DataFrame(doc_insights)
    df_to_fit = df.drop(columns=["url"])
    categorical_idx = [i for i in range(3, len(doc_insights[0]) - 1)]
    kproto = KPrototypes(n_clusters=int(MAX_CLUSTERS/3), max_iter=200).fit(df_to_fit.values, categorical=categorical_idx)
    clusters = kproto.predict(df_to_fit.values, categorical=categorical_idx)
    df['cluster'] = list(clusters)
    extracted_df = pd.DataFrame()
    extracted_df["url"] = df["url"]
    extracted_df["cluster"] = df["cluster"]
    dict_to_return = {}
    for index, row in extracted_df.iterrows():
        dict_to_return[row["url"]] = row["cluster"]
    return dict_to_return
