from pypinyin import pinyin, lazy_pinyin, Style
from utils import word_parse

def get_bopomofo(words):
    bopomofo = pinyin(words, style=Style.BOPOMOFO)
    bopomofo = list(map(lambda x: x[0], bopomofo))
    return bopomofo

if __name__ == "__main__":
    print(get_bopomofo("測試"))
