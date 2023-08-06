import os
from urllib.parse import urlparse

Downloadable = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".doc", ".xls", ".ppt", ".rar", ".mp3", ".wma", ".wav", ".lrc", ".rmvb", ".rm", ".mp4", ".3gp", ".swf",
                ".exe", ".docx", ".xlsx", ".pptx", ".pdf", ".psd", ".mpeg", ".avi", ".zip", ".jar", ".cab"]


def check_type(url):
    a = urlparse(url)
    file_name = os.path.basename(a.path)
    _, file_suffix = os.path.splitext(file_name)

    if file_suffix in Downloadable:
        return "Download"
    else:
        return None


if __name__ == '__main__':
    check_type('http://aliyuncs.com/ae-pub%2Fve%2FassetImgs%2F20210812190956358825_cover.jpg?OSSAccessKeyId=LTAI5tGb2xU5dmgqu1HdxzpT&Expires=1628853132&Signature=8NVI4NCd2%2BxxwgzgnubLtlHiBTI%3D')