# # -*- coding: utf-8 -*-
# """
# -------------------------------------------------
#    File Name：     __init__.py
#    Author :       junjie.zhang
# -------------------------------------------------
# """
# import jieba
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder

# RANDOM_SEED = 2018
# NGRAM = 2


# def split_text(texts, ngram=1):
#     results = []
#     for t in texts:
#         # split text according to jieba segmentation
#         seg_words = []
#         for w in jieba.cut(t):
#             seg_words.append(w)
#         seg_txt = u' '.join(seg_words)
#         # split text according to ngram
#         txt_list = [seg_txt]
#         for n in range(1, ngram + 1):
#             char = u' '.join([t[c_i:c_i + n] for c_i in range(len(t) - n + 1)])
#             txt_list.append(char)
#         txt = u' '.join(txt_list)
#         results.append(txt)
#     return results


# def _train_count_vector(data):
#     from sklearn.feature_extraction.text import CountVectorizer
#     count_vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 2))
#     count_vectorizer.fit(data)
#     return count_vectorizer


# def _get_raw_df(file):
#     '''
#     columns:[sentence,label,file_name]
#     :param file: 
#     :return: 
#     '''
#     print('load raw data from {}'.format(file))
#     df = pd.read_excel(file)
#     return df


# def get_data(file):
#     df = _get_raw_df(file)

#     df['raw_label'] = df.label
#     df['split'] = split_text(df.sentence, NGRAM)

#     c_v = _train_count_vector(df.split)

#     le = LabelEncoder()
#     df.label = le.fit_transform(df.label)

#     X = c_v.transform(df.split)
#     y = df.label
#     return X, y, le, c_v


# __all__ = ['get_data']
