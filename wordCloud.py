from collections import Counter
import urllib
import random
import webbrowser

from konlpy.tag import Okt
from lxml import html
import pytagcloud
# requires Korean font support
import sys


def r(): return random.randint(0, 255)  # 글씨의 랜덤색깔


def color(): return (r(), r(), r())


def get_tags(text, ntags=50, multiplier=7):  # 전에 했던 명사 탐색
    spliter = Okt()
    nouns = spliter.nouns(text)
    count = Counter(nouns)
    return [{'color': color(), 'tag': n, 'size': round((c*multiplier)/2)}
            for n, c in count.most_common(ntags)]


def draw_cloud(tags, filename, fontname='korean',  size=(800, 600)):
    pytagcloud.create_tag_image(tags, filename, fontname=fontname,  size=size)
    webbrowser.open(filename)
# 그림 그리기


def main():
    # result.txt에 분석할 본문 파일 넣기 원본파일 말함
    text_file = open("result.txt", "r", encoding="utf8")
    text = text_file.read()
    tags = get_tags(text)
    draw_cloud(tags, 'wordcloud.png')
    text_file.close()


if __name__ == "__main__":
    main()
