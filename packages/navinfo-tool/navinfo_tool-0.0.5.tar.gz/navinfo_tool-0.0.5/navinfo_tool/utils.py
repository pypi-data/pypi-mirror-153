import configparser
import re
import csv
import os
from tqdm import tqdm



def read_config(conf_path):
    """
    根据配置文件的路径读取配置文件，并返回配置文件内容组成的dict
        配置文件格式：
            [conn_config]
            # sql连接配置
            host=172.19.50.66
            port=5432
            user=fpcdpc
            password=PASSWORD
            database=dpc_db
    :param conf_path: 配置文件路径
    :return: 配置文件组成的dict
    """
    conf_dict = {}
    cf = configparser.ConfigParser()
    cf.read(conf_path, encoding='utf-8')
    secs = cf.sections()
    for s in secs:
        items = cf.items(s)
        for i in items:
            conf_dict[i[0]] = i[1]
    return conf_dict


def check_and_creat_dir(file_url):
    '''
    判断文件目录是否存在，文件目录不存在则创建目录
    :param file_url: 文件路径，包含文件名
    :return:不存在则返回False， 存在True
    '''
    file_gang_list = file_url.split('/')
    if len(file_gang_list) > 1:
        [fname, fename] = os.path.split(file_url)
        print(fname, fename)
        if not os.path.exists(fname):
            os.makedirs(fname)
            return False
        else:
            return True
        # 还可以直接创建空文件

    else:
        return True



def getPolygonArea(points):
    """
    计算多边形面积
    :param points: [[x1, y1], [x2, y2], [x3, y3], [x4, y4], ...]
    :return: 面积
    """

    sizep = len(points)
    if sizep<3:
        return 0.0

    area = points[-1][0] * points[0][1] - points[0][0] * points[-1][1]
    for i in range(1, sizep):
        v = i - 1
        area += (points[v][0] * points[i][1])
        area -= (points[i][0] * points[v][1])

    return abs(0.5 * area)


def get_bracketed_content(text):
    """
    获取文本中所有小括号中的内容组成的list
    如：
        香港特(别行）政区（北京点）
        return：
            ['别行', '北京点']
    :param text: 文本
    :return: 括号中内容组成的list
    """
    res = re.findall(r'[（(](.*?)[）)]', text)
    return res


def rm_bracketed(text):
    """
    去除文本中的括号，包括括号中的内容，返回去括号后的文本
    如：
        香港特(别行）政区（北京点）
        return：
            香港特政区
    :param text:文本
    :return:去括号后的文本
    """
    res = re.sub(u"[（(](.*?)[）)]|\{.*?\}|\[.*?\]|\<.*?\>", "", text)
    return res


def rm_symbol(text):
    """
    去除文本中的所有符号，返回去符号后的文本
    如：
        香港特(别·行）政，区（北京-点）
        return：
            香港特别行政区北京点
    :param text:
    :return:
    """
    res = re.sub(
        "[\s+\.\!\/_, $%^*(+\"\')]|[ \t\r\n\\\\+—－\-()?【】“”！，。？:：、~@#￥%……&*（）\|「」▏·`▪•۰・●⁺°～’\[\➕;〔〕《–‖﹢〖〗‘》［］◆❤×『\]』｡×\\\️=；²∙﹙′★◎〉─③ⅳ―☆㎡〇ⅲ⊂♡⑧℃⑤︱╮₂ⅴⅱ³»①〈╭✘ ※❥･﹚､ⅰ<>›ܶ│丨‧丶]",
        "", text)
    return res


def read_csv(file_path):
    """
    读取csv数据，返回格式为每行作为元素的list， 其中第一个元素为表头的信息
    返回数据格式：
        [
            ['class','name','sex','height','year'],
            [1,'xiaoming','male',168,23],
            [2,'xiaohong','female',162,22],
            [3,'xiaozhang','female',163,21],
            [4,'xiaoli','male',158,21]
        ]
    :param file_path:csv文件路径
    :return:每行作为元素的list
    """
    res = []
    with open(file_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            for l in reader:
                if len(l) == 0:
                    continue
                res.append(l)
        except Exception as e:
            print("\033[1;31m 警告：读取csv时发生错误，已经读取到：{} 条数据， 错误内容： {}\033[0m".format(len(res), e))
    return res



def write2csv(filename, data):
    """
        将数组的内容写到csv中
        data格式：
            data = [
                        ['class','name','sex','height','year'],
                        [1,'xiaoming','male',168,23],
                        [2,'xiaohong','female',162,22],
                        [3,'xiaozhang','female',163,21],
                        [4,'xiaoli','male',158,21]
                    ]
    :param filename: 需要写入的csv文件路径
    :param data:数组格式的文件内容
    """
    f = open(filename, 'w', encoding='utf-8', newline='')
    writer = csv.writer(f)
    for i in tqdm(data):
        writer.writerow(i)
    f.close()

