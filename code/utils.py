import time
import numpy as np


def __str_repeat(s1,s2):
    _repeat = 0
    for i in range(min(len(s1),len(s2))):
        if s1[i] == s2[i]:
            _repeat += 1
        else:
            return _repeat
    return _repeat


def str_similarity(str1,str2):
    # 返回两个字符串中都存在的最长字串
    len_str1 = len(str1)
    len_str2 = len(str2)
    if len_str1 == 0 or len_str2 == 0:
        return 0
    max_repeat = 0
    for i in range(len_str1):
        for j in range(len_str2):
            _repeat = __str_repeat(str1[i:],str2[j:])
            if _repeat > max_repeat:
                max_repeat = _repeat
    return max_repeat


def sort_by_date(time_list):
    # input ['9_Feb_2019','7_Dec_2018',...]
    # return 时间升序对应索引号
    def tstamp(_):
        try:
            return time.mktime(time.strptime(_,'%d_%b_%Y'))
        except ValueError:
            return 0
    tlist = [tstamp(_) for _ in time_list]
    return np.argsort(tlist)


def sort_by_index(dir_list):
    # input ['0_cnns','1_detections',...]
    # return 编号升序对应索引号
    def __parse(_):
        try:
            return int(_.split('_')[0])
        except Exception:
            return -1
    index = [__parse(_) for _ in dir_list]
    return np.argsort(index)


if __name__ == "__main__":
    ret = sort_by_index(['ddd','9dad019','ddd_','28_Feb_2015'])
    print(ret)