default_codec = '嗷呜啊~'


class BeastFormatError(Exception):
    pass


def _clean_content(content):
    first = content.find('~呜嗷')
    last = content.rfind('啊')
    if first != -1 and last != -1 and last > first:
        return content[first:last + 1]

    first = content.find('~嗷汪')
    last = content.rfind('呜')
    if first != -1 and last != -1 and last > first:
        return content[first:last + 1]

    return content


def to_beast(content: str, codec: str = None):
    if not content:
        return None
    codec = codec if (codec and len(codec) == 4) else default_codec
    return codec[3] + codec[1] + codec[0] + _hex_to_beast(_to_hex(content), codec) + codec[2]


def from_beast(content: str):
    # 剔除无关数据
    content = _clean_content(content)
    # 校验格式
    if not content or len(content) < 4 or len(set(content)) != 4:
        raise BeastFormatError
    codec_list = [content[2], content[1], content[-1], content[0]]
    if len(set(codec_list)) != 4:
        raise BeastFormatError
    return _from_hex(_beast_to_hex(content[3:-1], ''.join(codec_list)))


def _from_hex(hex_str: str):
    result = ''
    j = 0
    for i in range(4, len(hex_str) + 1, 4):
        result += chr(int(hex_str[j:i], 16))
        j += 4
    return result


def _to_hex(content: str):
    hex_str = ''
    for i in range(len(content)):
        hex_str += format(ord(content[i]), 'x').rjust(4, '0')
    return hex_str


def _beast_to_hex(content: str, codec: str):
    hex_str = ''
    for i in range(0, len(content) - 1, 2):
        int_1 = 0
        int_2 = 0

        str_1 = content[i]
        while int_1 <= 3 and str_1 != codec[int_1]:
            int_1 += 1

        str_1 = content[i + 1]
        while int_2 <= 3 and str_1 != codec[int_2]:
            int_2 += 1

        int_2 = int_1 * 4 + int_2 - i // 2 % 16
        int_1 = (int_2 + 16) if int_2 < 0 else int_2
        hex_str += format(int_1, 'x')
    return hex_str


def _hex_to_beast(hex_str: str, codec: str):
    result = ''
    for i in range(len(hex_str)):
        num = int(hex_str[i], 16) + i % 16
        num = (num - 16) if num >= 16 else num
        result += '{}{}'.format(codec[num // 4], codec[num % 4])
    return result

