import jieba
import sys
from gensim import corpora, models, similarities

# 读入文本内容
def get_content(file_path):
    f = open(file_path, 'r', encoding = "UTF-8")

    line = f.readline()
    text = ""

    while line:
        text += line
        line = f.readline()

    f.close()

    return text

# 把文章分成若干个句子
def split_sentence(text):
    word = ""  # 用来存储文章中的每一个句子
    sentences = []  # 存储每一个句子的数组

    for i in range(len(text)):
        if text[i] >= "\u4e00" and text[i] <= "\u9fa5":  # 当前字符在中文的编码范围内
            word += text[i]  # 提取当前字符
        elif text[i] == "，":  # 中文逗号
            sentences.append(word)  # 划分出一个句子，加入到数组中
            word = ""

    if word != "":  # 不要忘记最后一句
        sentences.append(word)

    return sentences

# 对句子进行分词
def split_word(text):
    return [[word for word in jieba.lcut(sentence)] for sentence in text]  # 利用jieba.luct对句子进行分词

# 计算相似度
def cal_similiarity(origin_txt, check_txt):
    sim_value = []  # 相似度列表
    word_lenth = []  # 长度列表
    total_sum = 0  # 总权值和

    origin_list = split_word(origin_txt)  # 对原句子进行分词
    check_list = split_word(check_txt)  # 对比较句子进行分词

    dictionary = corpora.Dictionary(origin_list)  # 生成词典
    corpus = [dictionary.doc2bow(word) for word in origin_list]  # 通过doc2bow稀疏向量生成语料库
    tf = models.TfidfModel(corpus)  # 根据TF模型算法计算TF值

    num_features = len(dictionary.token2id.keys())  # 通过token2id得到特征数
    idx = similarities.MatrixSimilarity(tf[corpus], num_features=num_features)  # 计算稀疏矩阵相似度并建立索引

    size = 0  # 每个句子的总长度

    for i in range(len(check_list)):
        new_vector = dictionary.doc2bow(check_list[i])  # 新的稀疏向量
        sim_list = idx[tf[new_vector]]  # 算出文章的相似度
        sim_value.append(max(sim_list))  # 选出最大相似度并加入到相似度列表

        word_size = len(check_list[i])  # 相似文章每句长度值
        size += word_size
        word_lenth.append(word_size)  # 加入到长度列表

    for i in range(len(word_lenth)):
        total_sum += word_lenth[i] * sim_value[i]

    return total_sum / size  # 返回加权平均值

# 比较两个文本并得到相似度
def compare_text(origin_path, check_path):
    # 读取文本并将文本分离出若干个句子
    origin_text = split_sentence(get_content(origin_path))
    check_text = split_sentence(get_content(check_path))

    similarity = cal_similiarity(origin_text, check_text)  # 计算相似度
    ret = round(similarity.item(), 2)  # 将结果转化为float类型，结果精确到小数点后两位

    return ret

if __name__ == '__main__':
    check_file_path = ".\\check_file\\"
    check_file_name = ["orig_0.8_add.txt", "orig_0.8_del.txt", "orig_0.8_dis_1.txt",
                       "orig_0.8_dis_10.txt", "orig_0.8_dis_15.txt"]

    # 读取文本并将文本分离出若干个句子
    orig_file = split_sentence(get_content(".\\original_file\\orig.txt"))
    for fname in check_file_name:
        path = check_file_path + fname
        check_file = split_sentence(get_content(path))

        similarity = cal_similiarity(orig_file, check_file)

        # 转化为float，再取小数点后两位
        ret = round(similarity.item(), 2)
        print(fname + "的相似度为: " + str(ret))

        f = open(".\\result_file\\file_similarity.txt", 'a', encoding="UTF - 8")
        f.write("文章 " + fname + " 的相似度为: " + str(ret) + '\n')
        f.close()