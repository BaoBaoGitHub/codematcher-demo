import util
import operator
import re
from bisect import bisect_right  # 新增导入，用于二分查找

def matcher_name(words, line, cmd):
    """
    用论文中的方程1计算Sname
    :param words: 查询词列表
    :param line: 查询结果中的方法
    :param cmd: es查询用的正则表达式
    :return: Sname的值
    """
    cmd = str(cmd).replace('.*', ' ').strip().split(' ')
    line = str(line).replace('\n', '')

    word_usage = len(cmd) / len(words) if len(words) > 0 else 0
    line_coverage = len(''.join(cmd)) / len(line) if len(line) > 0 else 0
    score = word_usage * line_coverage
    return score

def longest_sequence_length(seq):
    """
    计算查询词在文本中按顺序出现的最长序列长度
    :param seq: 二维列表，每个子列表是查询词在文本中的出现位置
    :return: 最长序列长度
    """
    if not seq:
        return 0
    prev = -1  # 前一个位置，初始为-1
    k = 0      # 序列长度
    for group in seq:
        if not group:  # 如果某个词没有匹配位置，停止
            break
        idx = bisect_right(group, prev)  # 找到大于prev的最小位置
        if idx < len(group):
            prev = group[idx]
            k += 1
        else:
            break
    return k

def matcher_api(query, line, jdk):
    """
    :param query: 查询词列表
    :param line: 返回结果中"parsed"对应的内容
    :param jdk: jdk文件反序列化的对象
    :return: 评分值
    """
    line = str(line).replace('\n', '').lower()
    index = []
    freq = 0
    count = 0
    for word in query:
        pattern = re.compile(word.lower())
        wi = [i.start() for i in pattern.finditer(line)]
        if len(wi) > 0:
            freq += len(wi) * len(word)
            count += 1
            index.append(wi)
    word_usage = count / len(query) if len(query) > 0 else 0
    line_coverage = freq / len(line) if len(line) > 0 else 0
    max_sequence = longest_sequence_length(index) / len(query) if len(query) > 0 else 0

    apis = line.split(',')
    api_count = 0
    jdk_count = 0
    for api in apis:
        if '.' in api:
            api_count += 1
            if '(' in api or '[' in api or '<' in api:
                api = api[:api.rfind('.')]
            if api in jdk:
                jdk_count += 1
    jdk_percent = jdk_count / api_count if api_count > 0 else 0

    score = word_usage * line_coverage * max_sequence * jdk_percent
    return score

def reranking(query_parse, data, cmds, jdk):
    """
    :param query_parse: 一个列表，列表中的第一个元素为处理后的查询词列表，第二个元素为单词列表的importance
    :param data: 模糊查询结果列表
    :param cmds: 模糊查询结果列表对应的查询正则表达式
    :return: 展示给用户的结果
    """
    query = query_parse[0]
    lines = []
    scores = []

    # 第一阶段：基于方法名评分并取前100
    for j in range(len(data)):
        res = data[j]['_source']
        line = res['method']
        cmd = cmds[j]
        scores.append([j, matcher_name(query, line, cmd)])
    scores.sort(key=operator.itemgetter(1), reverse=True)
    scores = scores[:100]

    # 第二阶段：基于API评分并排序
    for j in range(len(scores)):
        idx = scores[j][0]
        res = data[idx]['_source']
        line = res['parsed']
        scores[j].append(matcher_api(query, line, jdk))
    scores.sort(key=operator.itemgetter(1, 2), reverse=True)

    # 取前10个结果并处理源码
    count = min(10, len(data))
    for j in range(count):
        idx = scores[j][0]
        line = str(data[idx]['_source']['source'])

        token = 'for (int'
        if token in line:
            l = ''
            ds = line.split(token)
            l += ds[0]
            for k in range(1, len(ds)):
                db = str(ds[k])
                di = db.find('{')
                d = db[:di - 1]
                key = d[:d.find('=') - 1].strip()
                dd = d.split(key)
                keyy = '@ ' + key
                kk = ''
                for m in range(1, len(dd) - 1):
                    if dd[m-1][-1].isalnum() and dd[m][0].isalnum():
                        kk += key + dd[m]
                    else:
                        kk += keyy + dd[m]
                kk += dd[-1]
                l += token + ' ' + key + kk + db[di:]
            line = l

        lines.append(line)

    return lines