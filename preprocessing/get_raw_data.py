# -*- coding: utf-8 -*-
"""
File Name：     _get_data
Author :       peng.he
-------------------------------------------------
"""
import os
import glob
import re
import pandas as pd
import numpy as np

data_dir = 'D:\work\智能保顾\insurance-data\/annotation\sentence_paragraph'
_sentence_error = 0
_paragraph_error = 0

NONE = 'None'


def is_sentence(line):
    m = re.search('Senten', line)
    if m:
        return True
    return False


# 删除 <t location="2">  </t> 段落位置标识符
def del_para_location(text):
    m = re.search('^<t location="\d+">(.+?)</t>', text)
    if m:
        return m.group(1)
    else:
        return text


def get_line_sentence(file_name, one_line_sentence, show_error=False):
    global _sentence_error
    m = re.search('/Senten\d+(.+?)Senten\d+—.*\\\\', one_line_sentence)
    if m:
        text = m.group(1)
    else:
        if show_error:
            print('ERROR file:{}, one_line_sentence TEXT :{}'.format(file_name, one_line_sentence))
        text = NONE
    text = del_para_location(text)
    m1 = re.search('Senten\d+—(.+?)\\\\', one_line_sentence)
    if m1:
        label = m1.group(1)
    else:
        if show_error:
            print('ERROR file:{}, one_line_sentence LABEL :{}'.format(file_name, one_line_sentence))
        label = NONE
    if text == NONE or label == NONE:
        _sentence_error += 1
    return [text, label]


def is_one_line_paragraph(line):
    m = re.search('/Para(.+?)Para—.*\\\\', line)
    if m:
        return True
    else:
        return False


def get_file_name(path):
    m = re.search('sentence_paragraph\\' + '\(.+?)$', path)
    return m.group(1)


# 单行段落的文本和标签
def get_one_line_paragraph(file_name, one_line_paragraph, show_error=False):
    global _paragraph_error
    m1 = re.search('Para—(.+?)\\\\', one_line_paragraph)
    if m1:
        label = m1.group(1)
    else:
        if show_error:
            print('ERROR file:{},one_line_paragraph LABEL :{}'.format(file_name, one_line_paragraph))
        label = NONE
    m2 = re.search('/Para(.+?)Para—.*\\\\', one_line_paragraph)
    if m2:
        text = m2.group(1)
    else:
        if show_error:
            print('ERROR file:{},one_line_paragraph TEXT :{}'.format(file_name, one_line_paragraph))
        text = NONE
    text = del_para_location(text)
    if text == NONE or label == NONE:
        _paragraph_error += 1
    return [text, label]


# 抽取句子标注数据
def get_sentence_label(file_name, lines, show_error=False, type='all'):
    data = []
    for line in lines:
        if type == 'sen':
            if is_sentence(line):
                d = get_line_sentence(file_name, line, show_error)
                if NONE not in d:
                    data.append(d)
        elif type == 'para':
            if is_one_line_paragraph(line):
                d = get_one_line_paragraph(file_name, line, show_error)
                if NONE not in d:
                    data.append(d)
        else:
            if is_one_line_paragraph(line):
                d = get_one_line_paragraph(file_name, line, show_error)
                if NONE not in d:
                    data.append(d)
            elif is_sentence(line):
                d = get_line_sentence(file_name, line, show_error)
                if NONE not in d:
                    data.append(d)

    df = pd.DataFrame(data, columns=['sentence', 'label'])
    df['file_name'] = get_file_name(file_name)
    return df


def get_file_dfs(show_error=True, type='all'):
    files = glob.glob(os.path.join(data_dir, '**/**/*.txt'), recursive=True)
    file_sentences = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            df = get_sentence_label(file, lines, show_error, type)
            file_sentences[file] = df
    print('文件数:{}'.format(len(files)))
    return file_sentences


def exclude_labels(df):
    _exclude_labels = ['other',
                       NONE,
                       '合同抬头',
                       '段落分割',
                       '合同目录标题',
                       '合同目录项',
                       '指代词解释',
                       '段落标题',
                       '页脚',
                       '？']
    df = df[~df.label.isin(_exclude_labels)]
    df = df[~df.label.str.contains('释义|标题', na=False)]
    return df


def _get_data(show_error=False, type='all'):
    file_dfs = get_file_dfs(show_error, type)
    file_sentences = list(file_dfs.values())
    if show_error:
        print('段落标注错误数：{}，句子标注问题数：{}'.format(_paragraph_error, _sentence_error))
    data = pd.concat(file_sentences)
    data = exclude_labels(data)
    return data


def get_label_distribution(df):
    label_distri = df.groupby('label').count()
    dic = label_distri.T.to_dict('list')
    from collections import OrderedDict
    dic = OrderedDict(sorted(dic.items(), key=lambda x: x[0]))
    _dict = {}
    for k in dic:
        _dict[k] = dic[k][0]
    return _dict


def get_current_label_dis():
    df = _get_data(type='sen')
    dis = get_label_distribution(df)

    print('current label distribution:')
    for label in dis:
        print('{}{}:{}'.format(' ' * 22, label, dis[label]))


def sample_from_paragraph(sen):
    para = _get_data(type='para')
    labels = np.unique(sen.label.values)
    # sentences = np.unique(sen.sentence.values)
    para = para[para.label.isin(labels)]
    # para = para[~para.sentence.isin(sentences)]
    print('sample {} from paragraph data'.format(para.shape[0]))
    return para


def merge_save(file, sen, para):
    df = sen
    if para is not None:
        df = pd.concat([sen, para])
    # df = df.drop_duplicates('sentence')
    print('after re-sample,we have {} samples'.format(df.shape[0]))
    writer = pd.ExcelWriter(file)
    df.to_excel(writer, index=False)
    writer.save()


def get_raw_data(file, sample_from_para=True):
    if os.path.isfile(file):
        df = pd.read_excel(file)
        return df
    else:
        sen = _get_data(type='sen')
        para = None
        if sample_from_para:
            para = sample_from_paragraph(sen)
        merge_save(file, sen, para)


if __name__ == '__main__':
    get_raw_data('D:\work\智能保顾\intelli-extract-sentence\data\data.xlsx')
