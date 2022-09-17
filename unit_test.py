import unittest
import os
from main import get_content, split_sentence, cal_similiarity

class MyTestCase(unittest.TestCase):
    def test(self):
        check_file_path = ".\\check_file\\"
        check_file_name = ["orig_0.8_add.txt", "orig_0.8_del.txt", "orig_0.8_dis_1.txt",
                           "orig_0.8_dis_10.txt", "orig_0.8_dis_15.txt"]

        # 读取文本并将文本分离出若干个句子
        orig_file = split_sentence(get_content(".\\original_file\\orig.txt"))
        check_path(".\\original_file\\orig.txt") # 检查合法性
        check_empty(orig_file) # 检查合法性

        for fname in check_file_name:
            path = check_file_path + fname
            check_file = split_sentence(get_content(path))
            check_path(path)  # 检查合法性
            check_empty(check_file)  # 检查合法性

            similarity = cal_similiarity(orig_file, check_file)

            # 转化为float，再取小数点后两位
            ret = round(similarity.item(), 2)
            print(fname + "的相似度为: " + str(ret))

            f = open(".\\result_file\\file_similarity.txt", 'a', encoding="UTF - 8")
            f.write("文章 " + fname + " 的相似度为: " + str(ret) + '\n')
            f.close()

# 如果传入路径的目标文件不存在则抛出异常
def check_path(path):
    if not os.path.isfile(path):
        print(path + "文件路径不存在！")
        exit(0)

# 如果传入的文件内容为空则抛出异常
def check_empty(text):
    if not len(text):
        print("文件内容为空！")
        exit(0)

if __name__ == '__main__':
    unittest.main()