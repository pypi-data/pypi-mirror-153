import re
from w3lib.html import remove_tags


def check(text):
    if isinstance(text, str):
        return text
    else:
        return str(text)


def get_text(data: str) -> str:
    if isinstance(data, str):
        pattern = re.compile(r'<[^>]+>', re.S)
        result = pattern.sub('', data)
        # result = result.replace('\n', ' ')
        # result = result.replace('\r', '')
        return result
    return ''


def remove_line(data: str) -> str:
    if isinstance(data, str):
        # soup = BS(data, 'html.parser')
        # result = soup.get_text()

        pattern = re.compile(r'\n[\s| ]*\r', re.S)
        result = pattern.sub('', data)
        return result
    return ''


def remove_url(data: str) -> str:
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', data, flags=re.MULTILINE)
    return text


def remove_html_tag(text):
    if isinstance(text, str):
        text = remove_tags(text)
    return text


def remove_email(text):
    EMAIL_REGEX = re.compile(r"[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}", re.IGNORECASE)
    text = re.sub(EMAIL_REGEX, "", text)
    return text


def remove_weibo_at(text):
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
    return text


def remove_emoji(text, expression_len=(1, 6)):
    """
    :param text:
    :param expression_len: 假设表情的表情长度范围，不在范围内的文本认为不是表情，不加以清洗，如[加上特别番外荞麦花开时共五册]。设置为None则没有限制
    :return:
    """
    # 去除括号包围的表情符号
    # ? lazy match避免把两个表情中间的部分去除掉
    if type(expression_len) in {tuple, list} and len(expression_len) == 2:
        # 设置长度范围避免误伤人用的中括号内容，如[加上特别番外荞麦花开时共五册]
        lb, rb = expression_len
        text = re.sub(r"\[\S{" + str(lb) + r"," + str(rb) + r"}?\]", "", text)
    else:
        text = re.sub(r"\[\S+?\]", "", text)
    # text = re.sub(r"\[\S+\]", "", text)
    # 去除真,图标式emoji
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    # emoji_uf = re.compile(r'[\\]+[u][f][a-z0-9]+')
    emoji_uf = re.compile(r'[\uf000-\uffff]+')
    text = emoji_uf.sub(r'', text)
    return text


def remove_weibo_topic(text):
    text = re.sub(r"#\S+#", "", text)  # 去除话题内容
    return text


def remove_deduplicate_space(text):
    text = re.sub(r"(\s)+", r"\1", text)  # 合并正文中过多的空格
    return text


def remove_puncts(text):
    # 移除所有标点符号
    allpuncs = re.compile(
        r"[，\_《。》、？；：‘’＂“”【「】」·！@￥…（）—\,\<\.\>\/\?\;\:\'\"\[\]\{\}\~\`\!\@\#\$\%\^\&\*\(\)\-\=\+]")
    text = re.sub(allpuncs, "", text)
    return text


if __name__ == '__main__':
    text = '油价又要上涨'
    text = remove_emoji(text)
    print()
