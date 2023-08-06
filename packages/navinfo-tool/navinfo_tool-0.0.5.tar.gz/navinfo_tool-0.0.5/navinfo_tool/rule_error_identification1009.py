#! -*- coding:utf-8 -*-
import fairies as fa
from xpinyin import Pinyin
import re
import pylcs
import json
import csv
import collections
from tqdm import tqdm
from xlsxwriter.workbook import Workbook
from navinfo_tool import end_words, same_stroke

pinyin = Pinyin()

# 结尾关键词
common_words = end_words.end_words

# 形似字
same_stroke = same_stroke.same_stroke
same_stroke_dict = collections.defaultdict(list)
for strokes in same_stroke:
    strokes = list(strokes)
    for s in strokes:
        for sc in strokes:
            if sc != s and sc not in same_stroke_dict[s]:
                same_stroke_dict[s].append(sc)

# 需要去掉的形似字
sameinone = ["烧烤", "木材", "疼痛", "鲜羊", "鲜鱼", "翻羽", "景京", "林村", "马驰", "检验", "酿酒", "配酒", "酒西", "百北",
             "板饭", "月育", "份分", "大夫", "大六", "大天", "林木", "动力", "科料", "起超", "股投", "山技", "星家", "设投",
             "元园", "运动", "阁门", "林材"]

def rm_common_words(text, common_words):
    """
    如果地址的结尾在关键词中，则去掉结尾
    :param text:地址文本
    :param common_words:结尾关键词
    :return:去掉关键词的文本
    """
    for cw in common_words:
        if text.endswith(cw):
            text = re.sub(cw, '', text)
    return text

def subdu(text):
    """将°C换为度"""
    if re.findall('[0-9]+[°度][Cc]*', text):
        text = re.sub('[°度][Cc]*', '度', text)
    return text

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring

def bignum2num(text):
    """大写转小写"""
    chinese_num = {'零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    text = list(text)
    for c in chinese_num:
        while c in text:
            text[text.index(c)] = str(chinese_num[c])
    return ''.join(text)

def convertStrToPinyin(text):
    """获取文本对应的拼音list"""
    res = pinyin.get_pinyin(text, ' ')
    return res.split(' ')

def find_disorder(text_list):
    """查找是否有倒序错误"""
    texts = [t for t in text_list if len(t) > 0]
    if len(texts) <= 1:
        return {}
    cl = len(texts)
    flaga = False
    flagb = False
    rstr = ''
    prstr = ''
    for i in range(cl-1):
        for j in range(i+1, cl):
            a = texts[i]
            b = texts[j]
            if a == b:
                continue
            if len(a) > len(b):
                a, b = b, a

            coml = pylcs.lcs(a, b)

            reversestr = ''
            preversestr = ''
            maxcoml = coml
            for window in range(2, 5):
                if len(a) >= window:
                    for start in range(len(a) - window + 1):
                        reversea = a[:start] + ''.join(list(reversed(a[start: start + window]))) + a[start + window:]
                        revcomlen = pylcs.lcs(reversea, b)
                        if revcomlen > maxcoml:
                            maxcoml = revcomlen
                            flagb = True
                            preversestr = a[start: start + window]
                        tmpreverse = ''.join(list(reversed(a[start: start + window])))
                        if tmpreverse in b and len(tmpreverse) > len(reversestr):
                            if tmpreverse != ''.join(list(reversed(tmpreverse))):
                                reversestr = tmpreverse
                                flaga = True


            if flaga and len(reversestr) > len(rstr):
                rstr = reversestr
            if flagb and len(preversestr) > len(prstr):
                prstr = preversestr
    if flaga and flagb and (rstr == prstr or ''.join(list(reversed(rstr))) == prstr):
        rt = rstr
        urt = ''.join(list(reversed(rt)))


        if re.findall('[a-zA-Z]', rstr):
            if len(rt) == 2 and len(re.sub('[a-zA-Z]', '', rt)) == 0:
                return {}
            ents = [(''.join(re.findall(r'[A-Za-z]', t))).lower() for t in texts]
            if rstr not in ents:
                return {}

        if re.findall('[0-9]', rstr):
            return {}

        if re.findall('[东南西北]', rstr):
            if len(re.sub('[东南西北]', '', rstr)) <= 1:
                return ''

        flagallin = False
        for t in text_list:
            if rt in t and urt in t:
                if t.index(rt) - t.index(urt) > 1 or t.index(rt) - t.index(urt) < -1:
                    flagallin = True

        if flagallin:
            return {}

        comw = ['胎', '发', '印', '粮', '家', '祛', '地', '米', '纹', '食', '雷', '手', '烤', '具', '衣', '皮', '章',
                '蹄', '砂', '服', '国', '垫', '彩', '机', '腾', '球', '画', '田', '锁', '果', '海', '邮', '洗', '美',
                '饼', '暖', '生', '车', '区', '品', '炒', '壁', '村', '加', '灸', '修', '鞋', '汽', '租', '电', '摄',
                '艺', '墙', '名', '童', '装', '磨', '油', '羊', '多', '出', '房', '餐', '凉', '肉', '养', '专', '花',
                '柜', '桃', '渔', '寿', '牛', '活', '布', '子']
        flaglr = False
        if len(rstr) == 3 and rstr[1] in comw:
            lrt = rt[1] + rt
            rrt = rt + rt[1]
            for t in texts:
                if lrt in t or rrt in t:
                    flaglr = True
        if flaglr:
            return {}

        if not (rt in texts or urt in texts):
            lwords = set()
            rwords = set()
            for t in texts:
                if not (rt in t and urt in t):
                    if rt in t:
                        idx = t.index(rt)
                        if idx != 0:
                            lwords.add(t[idx - 1])
                        if idx != len(t) - len(rt):
                            rwords.add(t[idx + len(rt)])
                    if urt in t:
                        idx = t.index(urt)
                        if idx != 0:
                            lwords.add(t[idx - 1])
                        if idx != len(t) - len(urt):
                            rwords.add(t[idx + len(urt)])
            if len(lwords) > 1 or len(rwords) > 1 and len(rt) == 2:
                return {}
            if len(lwords) > 1 or len(rwords) > 1 and len(rt) > 2:
                return {}

        res = {}
        for t in texts:
            if rt in t:
                res[t] = (rt, rt, t.index(rt))
            if urt in t:
                res[t] = (urt, urt, t.index(urt))
        return res
    else:
        return {}


def find_sames(text1, text2):
    """查找是否有同形错误"""
    if text1 == text2:
        return []
    if not fa.is_chinese(text1) and not fa.is_chinese(text2):
        return []
    if len(text1) > len(text2):
        text1, text2 = text2, text1
    if len(text1) < 2:
        return []

    # 用来保存同型的文本
    txtexts = []

    # 遍历text1
    for i in range(len(text1)):
        word = text1[i]
        if word in same_stroke_dict:
            word_sames = same_stroke_dict[word]
            for ws in word_sames:
                if ws in text2:
                    for ti2, t2 in enumerate(text2):
                        if t2 == ws:
                            wsidx = ti2
                            if i == 0:
                                if wsidx != len(text2)-1:
                                    if text1[i + 1] == text2[wsidx + 1]:
                                        txtexts.append(tuple(sorted([(word, i), (ws, wsidx)], key=lambda x: x[0])))
                            elif i == len(text1) - 1:
                                if wsidx != 0:
                                    if text1[i - 1] == text2[wsidx - 1]:
                                        txtexts.append(tuple(sorted([(word, i), (ws, wsidx)], key=lambda x: x[0])))
                            else:
                                pre = ''
                                suf = ''
                                if wsidx == 0:
                                    suf = text2[wsidx + 1]
                                elif wsidx == len(text2)-1:
                                    pre = text2[wsidx - 1]
                                else:
                                    pre = text2[wsidx - 1]
                                    suf = text2[wsidx + 1]
                                if text1[i-1] == pre or text1[i+1] == suf:
                                    txtexts.append(tuple(sorted([(word, i), (ws, wsidx)], key=lambda x: x[0])))
    if len(txtexts) > 0:
        txtexts = txtexts[0]
    return txtexts

def find_tongxing(text_list):
    """查找是否有同形错误"""
    texts = [t for t in text_list if len(t) > 0]
    res_d = {}
    # 要输出span 和具体到字 一样多不确定
    res = []
    for i in range(len(texts) - 1):
        for j in range(i + 1, len(texts)):
            if texts[i] != texts[j]:
                answer = find_sames(texts[i], texts[j])
                if len(answer) > 0:
                    res.append(answer)

    res_idx = list(set(res))
    res = set()
    for r in res_idx:
        res.add((r[0][0], r[1][0]))
    res = list(res)

    if len(res) > 0:
        rmr = []
        for r in res:
            for t in texts:
                if r[0] in t and r[1] in t:
                    if ''.join(r) in sameinone or ''.join([r[1], r[0]]) in sameinone:
                        rmr.append(r)
        rmr = list(set(rmr))
        for r in rmr:
            res.remove(r)

        rmr = []
        for r in res:
            for t in texts:
                if r[0] in t and r[1] in t:
                    r0idx = t.index(r[0])
                    r1idx = t.index(r[1])
                    pre0 = t[r0idx - 1] if r0idx > 0 else ''
                    pre1 = t[r1idx - 1] if r1idx > 0 else ''
                    sub0 = t[r0idx + 1] if r0idx < len(t) - 1 else ''
                    sub1 = t[r1idx + 1] if r1idx < len(t) - 1 else ''
                    if pre0 == pre1 or sub0 == sub1:
                        rmr.append(r)
        rmr = list(set(rmr))
        for r in rmr:
            res.remove(r)

        if len(res) > 0:
            for ri in res_idx:
                if ri[0][0] == res[0][0] and ri[1][0] == res[0][1]:
                    for t in text_list:
                        if len(t) > ri[0][1] and t[ri[0][1]] == ri[0][0]:
                            res_d[t] = (res[0][0], res[0][0], t.index(res[0][0]))
                        if len(t) > ri[1][1] and t[ri[1][1]] == ri[1][0]:
                            res_d[t] = (res[0][1], res[0][1], t.index(res[0][1]))
                    break
            return res_d

    return res_d


def compare_tongyin(text1, text2):
    """查找是否有同音错误"""
    # text1作为短文本
    if len(text1) > len(text2):
        text1, text2 = text2, text1
    # text1和text2拼音list
    text1_py = convertStrToPinyin(text1)
    text2_py = convertStrToPinyin(text2)
    # text2拼音组成的字符串
    text2_py_str = ''.join(text2_py)
    # text2拼音字符串对应每个文本的开始位置
    text2_py_idx = [0]
    for tp in text2_py:
        text2_py_idx.append(text2_py_idx[-1] + len(tp))

    # 如果只有一个字，则过滤
    if len(text1) < 2:
        return []

    # 用来保存同音的文本
    tytexts = []
    # 每两个字判断是否有同音
    flaga = False
    # 每三个字判断是否有同音
    flagb = False
    flagstart = False
    for i in range(len(text1) - 1):
        tmp = text1[i: i + 2]
        tmp_py = ''.join(text1_py[i: i + 2])
        if len(tmp_py) > 0 and tmp_py in text2_py_str and tmp not in text2:
            t2pystart = text2_py_str.index(tmp_py)
            if t2pystart in text2_py_idx:
                t2start = text2_py_idx.index(t2pystart)
                if (len(''.join(text2_py[t2start: t2start + len(tmp)])) - len(tmp_py)) <= 1:
                    t2tmp = text2[t2start: t2start + 2]
                    repeats = sorted([tmp, t2tmp])
                    tytexts.append(tuple(repeats))
                    flaga = True
        elif len(tmp_py) > 0 and (re.sub('un', 'ong', tmp_py) in text2_py_str or re.sub('ong', 'un',
                                                                                        tmp_py) in text2_py_str) and tmp not in text2:
            if re.sub('un', 'ong', tmp_py) in text2_py_str:
                t2pystart = text2_py_str.index(re.sub('un', 'ong', tmp_py))
            else:
                t2pystart = text2_py_str.index(re.sub('ong', 'un', tmp_py))
            if t2pystart in text2_py_idx:
                t2start = text2_py_idx.index(t2pystart)
                if (len(''.join(text2_py[t2start: t2start + len(tmp)])) - len(tmp_py)) <= 1:
                    flaga = True

    if len(text1) > 2:
        for i in range(len(text1) - 2):
            tmp = text1[i: i + 3]
            tmp_py = ''.join(text1_py[i: i + 3])
            if len(tmp_py) > 0 and tmp_py in text2_py_str and tmp not in text2:
                t2pystart = text2_py_str.index(tmp_py)
                if t2pystart in text2_py_idx:
                    t2start = text2_py_idx.index(t2pystart)
                    if (len(''.join(text2_py[t2start: t2start + len(tmp)])) - len(tmp_py)) <= 1:
                        t2tmp = text2[t2start: t2start + 2]
                        repeats = sorted([tmp, t2tmp])
                        flagb = True
            elif len(tmp_py) > 0 and (re.sub('un', 'ong', tmp_py) in text2_py_str or re.sub('ong', 'un',
                                                                                            tmp_py) in text2_py_str) and tmp not in text2:
                if re.sub('un', 'ong', tmp_py) in text2_py_str:
                    t2pystart = text2_py_str.index(re.sub('un', 'ong', tmp_py))
                else:
                    t2pystart = text2_py_str.index(re.sub('ong', 'un', tmp_py))
                if t2pystart in text2_py_idx:
                    t2start = text2_py_idx.index(t2pystart)
                    if (len(''.join(text2_py[t2start: t2start + len(tmp)])) - len(tmp_py)) <= 1:
                        flagb = True
    else:
        flagb = True

    if flaga and flagb:
        return tytexts
    else:
        return []

def find_tongyin(text_list):
    """查找是否有同音错误"""
    texts = [re.sub("[a-zA-Z0-9]", '', t) for t in text_list]
    texts = [t for t in texts if len(t) > 0]
    # 遍历获取所有的同音不同形的两字
    res = []
    if len(texts) > 1:
        for i in range(len(texts) - 1):
            for j in range(i + 1, len(texts)):
                if texts[i] != texts[j]:
                    add = compare_tongyin(texts[i], texts[j])
                    if len(add) > 0:
                        res.extend(add)

    res = list(set(res))
    if len(res) == 0:
        return {}

    # 保存错误的字和对应正确的字
    errorwords = []
    for r in res:

        # 获取公共字，即非错误的字
        publicword = list(set(r[0]).intersection(set(r[1])))
        # 如果没有公共字，则不处理
        if len(publicword) == 0:
            continue
        # 去掉公共字
        lr0 = list(r[0])
        lr1 = list(r[1])
        for c in publicword:
            while c in lr0:
                lr0.remove(c)
            while c in lr1:
                lr1.remove(c)
        # 如果去完公共字后长度不为1，则不处理
        if len(lr0) != 1 or len(lr1) != 1:
            continue

        errwords = [''.join(lr0), ''.join(lr1)]

        # 如果common_words同时在文本中，则过滤
        flagws0 = False
        flagws1 = False
        common_words = [('陕西', '山西'), ('公司', '工程'), ('公厕', '公共'), ('家具', '家居'), ('民宿', '民俗')]
        common_word = ["电店", "厂场", "务屋", "具居", "一壹", "二贰", "三叁", "四肆", "五伍", "六陆", "七柒", "八捌", "九玖", "十拾", "定订", "潢璜", "器气", "厨橱", "手授", "喜囍", "坊房"]
        for cws in common_words:
            if (errwords[0] in cws[0] and errwords[1] in cws[1]) or (errwords[1] in cws[0] and errwords[0] in cws[1]):
                for t in texts:
                    if cws[0] in t:
                        flagws0 = True
                    if cws[1] in t:
                        flagws1 = True
        if flagws0 and flagws1:
            return {}
        # 如果common_word同时在文本中，则过滤
        flagw = False
        for cw in common_word:
            if errwords[0] in cw and errwords[1] in cw:
                flagw = True
                break
        if flagw:
            continue

        # 如果两个字的拼音相差太远，则不处理
        flag = False
        for er0, er1 in zip(lr0, lr1):
            er0p = convertStrToPinyin(er0)[0]
            er1p = convertStrToPinyin(er1)[0]
            if er0p != er1p and (len(er0p)<3 or len(er1p) < 3 or 'a' in er0p or 'a' in er1p or 'u' in er0p or er0p[0] != er1p[0]):
                flag = True
                continue
        if flag:
            continue

        # 如果和前面处理的错字相同，则不处理
        if tuple(errwords) in errorwords or tuple(reversed(errwords)) in errorwords:
            continue
        errorwords.append(tuple(errwords))

    # 如果错字数量大于1，判断是否相邻，如果相邻则组合
    if len(errorwords) > 1:
        errws = ''.join([e[0] for e in errorwords])
        if len(texts) > 0:
            for t in texts:
                if errws in t:
                    errorwords = [[''.join([e[0] for e in errorwords]), ''.join([e[1] for e in errorwords])]]
                if ''.join(list(reversed(errws))) in t:
                    errorwords = [[''.join(list(reversed([e[0] for e in errorwords]))), ''.join(list(reversed([e[1] for e in errorwords])))]]

    res_list = []
    if len(errorwords) > 0:
        for ew in errorwords:
            for r in res:
                if ew[0] in r[0] and ew[1] in r[1]:
                    res_d = {}
                    for t in text_list:
                        if r[0] in t:
                            res_d[t] = (ew[0], ew[0], t.index(r[0]) + r[0].index(ew[0]))
                        if r[1] in t:
                            res_d[t] = (ew[1], ew[1], t.index(r[1]) + r[1].index(ew[1]))
                    res_list.append(res_d)

        # 相同拼音错误中找到最多的文本
        err_temp = {}
        for rli in res_list:
            k = tuple(sorted(list(set([v[0] for k, v in rli.items()]))))
            if k not in err_temp:
                err_temp[k] = len(rli)
            else:
                if len(rli) > err_temp[k]:
                    err_temp[k] = len(rli)
        res_list_final = []
        final_k = []
        for rli in res_list:
            k = tuple(sorted(list(set([v[0] for k, v in rli.items()]))))
            if k not in final_k and len(rli) == err_temp[k]:
                res_list_final.append(rli)
                final_k.append(k)
        return res_list_final

    return res_list


def is_common_sequence(sub, text, diff_span=1):
    """
        判断是否满足1个字区别的共同子序列
        sub 来自其他字符串的子序列
        text 目标字符串
        diff_span 差异跨度

    """
    while sub[0] in text:

        wrong_text, diff = '', 0
        temp_text = text[text.find(sub[0]) + 1:]
        start = text.find(sub[0])
        end = start
        for i, s in enumerate(sub[1:]):
            if temp_text != '' and s == temp_text[0]:
                if diff == diff_span:
                    if text.count(sub[0]) > 1:
                        break
                    else:
                        dif_res = text[start:end]
                        for s in sub:
                            if s not in dif_res:
                                dif_res += s
                        if dif_res in text:
                            return False, sub, wrong_text, dif_res

                temp_text = temp_text[1:]
                end += 1
            elif len(temp_text) > 1 and s == temp_text[1]:

                if i != len(sub[1:]) - 1:
                    diff += 1
                wrong_text = temp_text[0]
                temp_text = temp_text[2:]
                end += 2

                if diff > diff_span:
                    break
            else:
                break
            if i == len(sub[1:]) - 1 and diff == diff_span:
                dif_res = text[start:end]
                for s in sub:
                    if s not in dif_res:
                        dif_res += s
                    if dif_res in text:
                        return False, sub, wrong_text, dif_res
                return False, sub, wrong_text, dif_res
        text = text[text.find(sub[0]) + 1:]
    return True, '', '', ''


def find_same_span(text1, text2):
    num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    alpha = 'abcdefghijklmnopqrestuvwxwz'
    stop_words = ['省', '市', '县', '区', '镇', '路', '村', '院', '站', '东', '南', '西', '北', '修']
    first_stop = ["大", "术", "学", "员", "第", "新", "老", "和", "城", "部", "园", "总", "的", "国", "业", "分", "理", "与", "鲜", "中",
                  "楼", "店", "号", "车", "肉", "房", "金", "医", "局", "风", "大", "术", "学", "员", "第", "新", "老", "和", "城", "部",
                  "园", "总", "的", "国", "业", "分", "理", "与", "鲜", "中", "楼", "店", "号", "车", "肉", "房", "金", "医", "局", "风",
                  "式", "党", "街", "售", "料", "馆", "易", "障", "杀", "里", "道", "の", "电", "委", "社", "度", "菜", "童", "会", "水",
                  "甲", "蹈", "乡", "桥", "展", "际", "茶", "下", "生", "育", "牌", "门", "钢", "务", "加", "名", "羊", "蔬", "师", "器"]

    # 如果字符串中不包含中文则不寻找
    if not fa.is_chinese(text1) and not fa.is_chinese(text2):
        return True, '', '', ''

    if text1 == text2:
        return True, '', '', ''

    if len(text1) > len(text2):
        long, short = text1, text2
    else:
        long, short = text2, text1

    if short in long:

        """
            解决(哈哈,哈哈哈哈)
                (悠土鸡蛋直销 土鸡蛋直销)
                (烘焙坊 1烘焙坊)
        """

        if short == long[:len(short)]:
            return True, '', '', ''

    if len(short) + 1 == len(long):
        for position,i in enumerate(long):
            new = long.replace(i,'')

            if short == new and i not in stop_words and i not in first_stop and i not in num:
                if position < 3:
                    temp_long = long[:position+3]
                elif position > len(long)-2:
                    temp_long = long[position-3:]
                else:
                    temp_long = long[position-2:position+2]

                if len(temp_long) > 3:
                    temp_short = temp_long.replace(i,'')
                    return False, temp_short, i, temp_long

    for i in range(len(short)):
        for j in range(i + 1, len(short) + 1):
            if short[i:j] not in long:
                # 在这里限制前后的相同的长度 前2后1 或者前1后2等
                if (short[i:j][:2] in long and short[i:j][-1:] in long) or (
                        short[i:j][:1] in long and short[i:j][-2:] in long):
                    res, keyword, text, dif_res = is_common_sequence(short[i:j], long)
                    if not res:

                        if text in stop_words:
                            return True, '', '', ''

                        # 只有在开头的保留 其他的去掉
                        if text in first_stop:
                            if text1[0] == text or text2[0] == text:
                                return res, keyword, text, dif_res
                            else:
                                return True, '', '', ''

                        # 去掉不在开头的数字
                        if text in num:
                            if text1[0] not in num or text2[0] not in num:
                                return True, '', '', ''
                        elif text in alpha:
                            if text1[0] in alpha or text2[0] in alpha:
                                return True, '', '', ''
                            elif text in text1 and text1[-1] != text and text in text2 and text2[-1] != text:
                                if (text1[text1.find(text) - 1] not in alpha and text1[
                                    text1.find(text) + 1] not in alpha) or (
                                        text2[text2.find(text) - 1] not in alpha and text2[text2.find(text) + 1] not in alpha):
                                    return res, keyword, text, dif_res
                            else:
                                return True, '', '', ''

                        jieba_list = fa.jieba_cut(short)
                        isLegal = False
                        for k in range(len(jieba_list)):
                            if k != len(jieba_list) - 1:
                                temp = jieba_list[k] + jieba_list[k + 1]
                                if short[i:j] == temp:
                                    isLegal = True
                                    break
                        if not isLegal:
                            continue

                        return res, keyword, text, dif_res

    long, short = short, long
    for i in range(len(short)):
        for j in range(i + 1, len(short) + 1):
            if short[i:j] not in long:
                # 在这里限制前后的相同的长度 前2后1 或者前1后2等
                if (short[i:j][:2] in long and short[i:j][-1:] in long) or (
                        short[i:j][:1] in long and short[i:j][-2:] in long):
                    res, keyword, text, dif_res = is_common_sequence(short[i:j], long)
                    if not res:

                        if text in stop_words:
                            return True, '', '', ''

                        # 去掉不在开头的数字
                        if text in first_stop:
                            if text1[0] == text or text2[0] == text:
                                return res, keyword, text, dif_res
                            else:
                                return True, '', '', ''

                        if text in num:
                            if text1[0] not in num or text2[0] not in num:
                                return True, '', '', ''
                        elif text in alpha:
                            if text1[0] in alpha or text2[0] in alpha:
                                return True, '', '', ''
                            elif text in text1 and text1[-1] != text and text in text2 and text2[-1] != text:
                                if (text1[text1.find(text) - 1] not in alpha and text1[
                                    text1.find(text) + 1] not in alpha) or (
                                        text2[text2.find(text) - 1] not in alpha and text2[text2.find(text) + 1] not in alpha):
                                    return res, keyword, text, dif_res
                            else:
                                return True, '', '', ''

                        jieba_list = fa.jieba_cut(short)
                        isLegal = False
                        for k in range(len(jieba_list)):
                            if k != len(jieba_list) - 1:
                                temp = jieba_list[k] + jieba_list[k + 1]
                                if short[i:j] == temp:
                                    isLegal = True
                                    break
                        if not isLegal:
                            continue
                        return res, keyword, text, dif_res

    long, short = short, long

    if short[1:3] == long[:2] and short[:2] != long[:2]:
        if short[0] not in stop_words:
            return False, short[:3], short[0], long[:2]
    if long[1:3] == short[:2] and long[:2] != short[:2]:
        if long[0] not in stop_words:
            return False, long[:3], long[0], short[:2]

    return True, '', '', ''


def find_moreless(text1, text2):
    """查找是否有多字少字错误"""
    ds_dict = {}
    res, keyword, text, dif_res = find_same_span(text1, text2)
    if len(keyword) > len(dif_res):
        keyword, dif_res = dif_res, keyword
    if not res:
        ds_dict = {}
        if dif_res in text1:
            ds_dict[text1] = (text, dif_res, text1.find(dif_res))
            ds_dict[text2] = ('', keyword, text2.find(keyword))
        else:
            ds_dict[text1] = ('', keyword, text1.find(keyword))
            ds_dict[text2] = (text, dif_res, text2.find(dif_res))
    return ds_dict


def find_typo(text1, text2):
    """查找是否有错字错误"""
    if not fa.is_chinese(text1) and not fa.is_chinese(text2):
        return {}
    if len(text1) > len(text2):
        text1, text2 = text2, text1
    if len(text1) < 3:
        return {}

    prenum = 2
    subnum = 2

    # 用来保存错别字
    typowords = []
    if len(text1) == 3 and len(text2) == 3:
        eqnum = 0
        uneqwords = []
        for t1w, t2w in zip(text1, text2):
            if t1w == t2w:
                eqnum += 1
            else:
                uneqwords.append([(t1w, text1), (t2w, text2)])
        if eqnum == 2:
            typowords.extend(uneqwords)
    elif len(text1) == 4 and len(text2) == 4:
        eqnum = 0
        uneqwords = []
        for t1w, t2w in zip(text1, text2):
            if t1w == t2w:
                eqnum += 1
            else:
                uneqwords.append([(t1w, text1), (t2w, text2)])
        if eqnum == 3:
            typowords.extend(uneqwords)
    elif len(text1) >= prenum + subnum + 1:
        flag = True
        for i in range(len(text1) - prenum - subnum):
            if flag:
                t1tmp = text1[i: i + prenum + subnum + 1]
                for j in range(len(text2) - prenum - subnum):
                    t2tmp = text2[j: j + prenum + subnum + 1]
                    eqnum = 0
                    uneqidx = 0
                    uneqwords = []
                    for idx, (t1w, t2w) in enumerate(zip(t1tmp, t2tmp)):
                        if t1w == t2w:
                            eqnum += 1
                        else:
                            uneqwords.append([(t1w, t1tmp), (t2w, t2tmp)])
                            uneqidx = idx
                    if eqnum == prenum + subnum and uneqidx >= 1 and uneqidx <= 3:
                        typowords.extend(uneqwords)
                        flag = False
                        break

    exclude_words = '东西南北小城村区大的电儿一二三四五六七八九发服分社美睫甲乙服汽京业上下家学政营卖容面国路街桥园校厦修饰车开换直地洗海保出入生院山人处の分解维部水县里鲜商乐篮活体配务技男女工产媒播前后所馆侧旁边外内贸民房利居烫楼扶庆披比食管烧烤动酒饭住农式会市网动足门公养菜蔬快画热暖际板装钢验刘李张赵果墙壁初高陈王郭纪料线衣展宾旅猫孕狗店孙牛羊鸭接招康恢药魏定订镇乡寺母器杂坊私行材肉具讯潢璜喜囍厨橱'

    res_d = {}
    if len(typowords) > 0:
        res_typo = typowords[0]
        wss = res_typo[0][0] + res_typo[1][0]
        if re.findall('[a-zA-Z0-9]', wss):
            return res_d
        for ew in exclude_words:
            if ew in wss:
                return res_d
        res_d[text1] = (res_typo[0][0], res_typo[0][1], text1.index(res_typo[0][1]))
        res_d[text2] = (res_typo[1][0], res_typo[1][1], text2.index(res_typo[1][1]))
        return res_d

    return res_d


def error_identification(text_list):
    """
    查找text_list中多个文本中的错误，包含：倒序、同形、同音、多字少字、错别字
    :param text_list: 文本组成的list
    :return: 如果没有错误，返回空字典
            如果有错误，返回字典为：
                {
                    "errors": [{
                                "type": '错误类型',     # 错误类型包括：倒序、同形、同音、多字少字、错别字
                                "err": '',              #   如果包含两种类型的数量一样多，则为：不好确定，否则为空
                                "wrong_text": '熳',      #    可能的错字
                                "right_text": '漫'       #   可能正确的字
                                }, ...]
                    "err_dict": [{                      #   与errors一一对应
                                "text1": ('错误(正确)文本', '文本对应片段', 片段所在位置), ...
                                如： '漫漫烤肉啤酒': ('漫', '漫', 0),
                                }]
                    "origin_text": ['原始文本1', '原始文本2', ...]
                    "right": '推荐正确的文本'
                }
    """

    # 如果文本数量大于10，则不处理
    if len(text_list) >= 10 or len(text_list) < 2:
        return {}
    # 全角和半角转换
    data_list_q2b = [strQ2B(subdu(str(s))) for s in text_list]
    # 去括号
    data_list_rmbkt = [re.sub(u"\(.*?\)|（.*?）|\{.*?\}|\[.*?\]|\<.*?\>", "", s) for s in data_list_q2b]
    # 去符号
    data_list_rmsymb = [re.sub("[\s+\.\!\/_, $%^*(+\"\')]|[+—－\-()?【】“”！，。？:：、~@#￥%……&*（）\|「」▏·`▪•۰・●⁺°～’\[\➕;〔〕《–‖﹢〖〗‘》［］◆❤×『\]』｡×\\\️=；²∙﹙′★◎〉─③ⅳ―☆㎡〇ⅲ⊂♡⑧℃⑤︱╮₂ⅴⅱ³»①〈╭✘ ※❥･﹚､ⅰ<>›ܶ│丨‧丶]", "", s) for s in data_list_rmbkt]
    # 繁体转简体
    data_list_simch = [fa.cht_2_chs(s) for s in data_list_rmsymb]
    # 全部转小写
    data_list = [s.lower() for s in data_list_simch]
    # 去除常见尾部
    data_list_rmtail = [rm_common_words(s, common_words) for s in data_list]
    data_list_res = [s for s in data_list_rmtail if s != '']
    # 如果重复文本，则不处理
    if len(set(data_list_res)) == 1:
        return {}
    data_list_rmrepeet = list(set(data_list))

    origin_texts = text_list
    origin2text = data_list

    if len(data_list_rmrepeet) < 2:
        return {}

    # 分别保存 倒序、同形、同音、多字少字、错字 的dict
    d_dict = find_disorder(data_list_rmrepeet)
    tx_dict = find_tongxing(data_list_rmrepeet)
    ty_dict = find_tongyin(data_list_rmrepeet)

    errwords_all = []
    ws_tx = [v[0] for k, v in tx_dict.items()]
    ws_tx = tuple(sorted(list(set(ws_tx))[:2]))
    errwords_all.append(ws_tx)

    for tyi in ty_dict:
        ws_ty = [v[0] for k, v in tyi.items()]
        ws_ty = tuple(sorted(list(set(ws_ty))[:2]))
        if ws_ty not in errwords_all:
            errwords_all.append(ws_ty)

    ds_dict, cz_dict = {}, {}
    # 两两遍历文本，分别判断是否存在对应错误
    for i in range(len(data_list_rmrepeet) - 1):
        for j in range(i + 1, len(data_list_rmrepeet)):
            if data_list_rmrepeet[i] != data_list_rmrepeet[j]:
                moreless_dict = find_moreless(data_list_rmrepeet[i], data_list_rmrepeet[j])
                typo_dict = find_typo(data_list_rmrepeet[i], data_list_rmrepeet[j])

                if len(moreless_dict) > 0:
                    for k, v in moreless_dict.items():
                        ds_dict[k] = v
                if len(typo_dict) > 0:
                    ws_cz = [v[0] for k, v in typo_dict.items()]
                    ws_cz = tuple(sorted(list(set(ws_cz))[:2]))
                    if ws_cz not in errwords_all:
                        for k, v in typo_dict.items():
                            cz_dict[k] = v


    out_res = {}
    out_res['errors'] = []
    out_res['err_dict'] = []
    out_res['origin_text'] = text_list             #原始数据

    output_dict = {}
    output_dict['type'] = ''   #错误类型
    output_dict['err'] = ''    #错误是否可以判断,可以判断为空,不可以判断则填入不好判断
    output_dict['wrong_text'] = ''     #错误的字
    output_dict['right_text'] = ''     #正确的字


    # 倒序 > 同形 > 同音 > 多字少字 > 错别字
    res_dict = {}
    if len(d_dict) > 0:
        res_dict = d_dict
        output_dict['type'] = '倒序'
        out_res['errors'].append(output_dict.copy())
        out_res['err_dict'].append(res_dict.copy())
    elif len(tx_dict) > 0:
        res_dict = tx_dict
        output_dict['type'] = '同形'
        out_res['errors'].append(output_dict.copy())
        out_res['err_dict'].append(res_dict.copy())
    if len(ty_dict) > 0:
        for tyi in ty_dict:
            res_dict = tyi
            output_dict['type'] = '同音'
            out_res['errors'].append(output_dict.copy())
            out_res['err_dict'].append(res_dict.copy())
    if len(ds_dict) > 0:
        res_dict = ds_dict
        output_dict['type'] = '多字少字'
        out_res['errors'].append(output_dict.copy())
        out_res['err_dict'].append(res_dict.copy())
    if len(cz_dict) > 0:
        res_dict = cz_dict
        output_dict['type'] = '错别字'
        out_res['errors'].append(output_dict.copy())
        out_res['err_dict'].append(res_dict.copy())




    if len(res_dict) == 0:
        return res_dict
    
    # wrong_count_dict = {}
    # for text, wrong in res_dict.items():
    #
    #     #例子 {'丰巢快递柜': ('巢', '丰巢快', 0), '丰巢巢快递柜': ('巢', '丰巢巢快', 0)}
    #     wrong_span = wrong[1]
    #     for o_text in origin2text:
    #         if wrong_span in o_text:
    #             if wrong_span not in wrong_count_dict:
    #                 wrong_count_dict[wrong_span] = 0
    #             else:
    #                 wrong_count_dict[wrong_span] += 1
    #
    # final_dict = sorted(wrong_count_dict.items(),key=lambda x:x[1],reverse=False)

    distinguish_spans = []
    for res_dict, output_dict in zip(out_res['err_dict'], out_res['errors']):
        wrong_count_dict = {}
        for o_text in origin2text:
            if o_text in res_dict:
                wrong_span = res_dict[o_text][1]
                if wrong_span not in wrong_count_dict:
                    wrong_count_dict[wrong_span] = 0
                else:
                    wrong_count_dict[wrong_span] += 1
        final_dict = sorted(wrong_count_dict.items(),key=lambda x:x[1],reverse=False)

        if len(final_dict) <= 1:
            return {}
        else:
            if len(final_dict) > 1:
                if final_dict[0][1] == final_dict[-1][1]:
                    output_dict['err'] = '不好确定'
            final_wrong_span = final_dict[0][0]
            final_right_span = final_dict[-1][0]
            if (final_right_span, final_wrong_span) not in distinguish_spans:
                distinguish_spans.append((final_right_span, final_wrong_span))

            # 修正包含关系
            if final_right_span in final_wrong_span:
                if final_dict[0][1] * 2  > final_dict[-1][1]:
                    final_wrong_span,final_right_span = final_right_span,final_wrong_span

            # 找到错误的字
            if output_dict['type'] == '多字少字':
                for text, wrong in res_dict.items():
                    if wrong[0] != '':
                        output_dict['wrong_text'] = wrong[0]
                        break

                if final_wrong_span in final_right_span:
                    output_dict['type'] = '少字'
                    output_dict['right_text'] = output_dict['wrong_text']
                    output_dict['wrong_text'] = ''

                elif final_right_span in final_wrong_span:
                    output_dict['type'] = '多字'
                    output_dict['wrong_text'] = output_dict['wrong_text']
                    output_dict['right_text'] = ''

                elif len(final_wrong_span) > len(final_right_span):
                    output_dict['type'] = '多字'
                    output_dict['wrong_text'] = output_dict['wrong_text']
                    output_dict['right_text'] = ''
                else:
                    output_dict['type'] = '少字'
                    output_dict['right_text'] = output_dict['wrong_text']
                    output_dict['wrong_text'] = ''

            else:
                for text, wrong in res_dict.items():
                    if res_dict[text][1] == final_wrong_span:
                        output_dict['wrong_text'] = res_dict[text][0]
                    if res_dict[text][1] == final_right_span:
                        output_dict['right_text'] = res_dict[text][0]


        # 寻找最可能的poi
        # res = {}
        # for i,o in enumerate(origin2text):
        #     if final_right_span in o and final_wrong_span not in o:
        #         if origin_texts[i] not in res:
        #             res[origin_texts[i]] = 1
        #         else:
        #             res[origin_texts[i]] += 1
        #
        #
        # res = sorted(res.items(),key=lambda x:x[1],reverse=True)
        #
        # output_dict['right'] = res[0][0]
    # 寻找最可能的poi
    resa = {}
    resb = {}
    for i,o in enumerate(origin2text):
        flagi1 = True
        flagi2 = True
        for di in distinguish_spans:
            if di[0] not in o:
                flagi1 = False
            if di[1] in o:
                flagi2 = False
        if flagi1 and flagi2:
            if origin_texts[i] not in resa:
                resa[origin_texts[i]] = 1
            else:
                resa[origin_texts[i]] += 1
        if flagi1:
            if origin_texts[i] not in resb:
                resb[origin_texts[i]] = 1
            else:
                resb[origin_texts[i]] += 1

    resa = sorted(resa.items(),key=lambda x:x[1],reverse=True)
    resb = sorted(resb.items(),key=lambda x:x[1],reverse=True)
    if len(resa) > 0:
        out_res['right'] = resa[0][0]
    elif len(resb) > 0:
        out_res['right'] = resb[0][0]
    else:
        out_res['right'] = origin2text[0]

    return out_res



# if __name__ == '__main__':

#     # ts = ["漫漫烤肉啤酒", "漫漫烤肉啤酒", "漫漫烤肉啤酒"]
#     ts = ["漫熳烤肉啤酒小店狗蝎子", "漫漫烤肉啤酒小店狗蝎子", "漫漫烤肉皮酒小店蝎子"]
#     tres = error_identification(ts)
#     print(len(tres))
#     for k, v in tres.items():
#         if type(v) == list:
#             print(k)
#             for vi in v:
#                 print('\t{}'.format(vi))
#         else:
#             print(k, v)


























































