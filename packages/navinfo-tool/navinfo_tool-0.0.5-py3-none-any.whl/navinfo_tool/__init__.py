from fairies.read import (
    read,
    read_json,
    read_txt,
    read_npy
)

from fairies.write import (
    write_json,
    write_txt,
    write_npy
)

from fairies.classification_utils import (
    random_split_data,
    count_label,
    # split_data,
    # analysis_res
)

from fairies.nlp_utils import (
    label2id,
    is_chinese,
    find_lcs,
    long_substr,
    split_to_paragraph,
    split_to_sents,
    split_to_subsents,
    get_slide_window_text,
    get_cut_window_text
)

from fairies.nlp_jieba_utils import(
    jieba_init,
    jieba_add_words,
    jieba_cut,
    find_co_occurrence_word
)

from fairies.knowledge import(
    get_tongyin,
    get_tongxing,
    get_hanzi,
    get_stop_word
)

from fairies.nlp_clean_data import (
    removeLineFeed,
    cht_2_chs, # 繁体到简体
    chs_2_cht, # 简体到繁体
    strQ2B,
)


from navinfo_tool.rule_error_identification1009 import (
    error_identification
)

from navinfo_tool.utils import (
    read_config,    # 读取配置文件
    check_and_creat_dir,    # 判断文件目录是否存在，文件目录不存在则创建目录
    getPolygonArea,    # 计算多边形面积
    get_bracketed_content,    # 获取文本中所有小括号中的内容组成的list
    rm_bracketed,    # 去除文本中的括号，包括括号中的内容
    rm_symbol,    # 去除文本中的所有符号
    read_csv,    # 读取csv文件
    write2csv    # 将数组的内容写到csv中

)