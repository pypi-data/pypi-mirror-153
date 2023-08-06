def fwrite(path: str, text, encoding=None):
    """
    Args:
        path (str): file path
        text (str | Any): any textable object.
        encoding (str, optional): encoding type. Defaults to None.
    """

    text = str(text)
    
    if not text:
        text += '\n'
    elif text[-1] != '\n':
        text += '\n'
    
    try:
        with open(path, 'a', encoding=encoding) as f:
            f.write(text)
    except UnicodeEncodeError:
        try:
            with open(path, 'a', encoding='cp949') as f:
                f.write(text)
        except UnicodeEncodeError:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(text)


def distinct(myList: list):
    '''리스트 중복 제거'''
    return list(dict.fromkeys(myList))


def ip_change2():
    """Change IP.
    USB Tethering is Needed.

    Returns:
        bool: True if success, False otherwise.
    """
    import requests
    import subprocess
    try:
        old_ip = requests.get('http://wkwk.kr/ip').text
    except:
        while True:
            try:
                old_ip = requests.get('http://wkwk.kr/ip').text
            except:
                pass
            else:
                break
    subprocess.run(['c:\\adb\\adb', 'shell', 'am', 'start', '-a', 'android.intent.action.MAIN', '-n', 'com.mmaster.mmaster/com.mmaster.mmaster.MainActivity'])
    result_flag = False
    for cnt in range(90):
        print('인터넷 접속대기중 - {}초'.format(cnt+1))
        try:
            cur_ip = requests.get('http://wkwk.kr/ip', timeout = 1).text
            if old_ip == cur_ip:
                print('아이피가 변경되지 않았습니다.')
                return result_flag
            else:
                print(f'{old_ip} -> {cur_ip} 변경 완료.')
                result_flag = True
                return result_flag
        except:
            pass
    print('아이피가 변경되지 않았습니다.')
    return result_flag


def http_remove(link: str):
    '''url의 http(s) 제거'''
    import re
    link = re.sub("(http|https)\:\/\/",'', link).strip('/')
    return link


def http_append(link: str):
    '''url에 https 추가'''
    return link if link.startswith('http') else "http://" + link