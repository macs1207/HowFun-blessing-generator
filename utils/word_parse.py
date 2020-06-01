from pypinyin import pinyin, lazy_pinyin, Style

def get_bopomofo(words):
    bopomofo = pinyin(words, style=Style.BOPOMOFO)
    return bopomofo

if __name__ == "__main__":
    print(get_bopomofo("測試"))
