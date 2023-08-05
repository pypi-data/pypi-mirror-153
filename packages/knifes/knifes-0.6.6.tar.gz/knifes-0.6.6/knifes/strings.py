def desensitizePhone(phone):
    """
    废弃
    """
    return '****'.join([phone[:3], phone[7:]])


# 手机号脱敏
def blur_phone(phone):
    if not phone or len(phone) < 11:
        return phone
    return phone[:3] + '****' + phone[7:]


def abbreviate(text, max_len=2, marker='...'):
    return text[0:max_len] + marker if len(text) > max_len else text
