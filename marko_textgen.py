from janome.tokenizer import Tokenizer
import markovify


def text_cleansing(text):
    # 改行、スペース、問題を起こす文字の置換
    table = str.maketrans({
        '。': '.',
        '\n': '',
        '\r': '',
        '…': '',
        '、': '',
        '々': '',
        '「': '',
        '」': '.',
        '(': '（',
        ')': '）',
        '[': '［',
        ']': '］',
        '"': '”',
        "'": "’",
    })
    text = text.translate(table)
    print(text)
    t = Tokenizer()
    result = t.tokenize(text, wakati=True)
    result = list(result)
    # 1単語毎に間に半角スペース、文末には改行を挿入
    splitted_text = ""
    for i in range(len(result)):
        splitted_text += result[i]
        if result[i] != '。' and result[i] != '！' and result[i] != '？':
            splitted_text += ' '
        else:
            splitted_text += '\n'
    return splitted_text


with open('bocchan.txt', mode='r', encoding='shift_jis') as f:
    text = f.read()

# テキストを単語毎に分割して記号を除去
splitted_text = text_cleansing(text)

# データセットの量が不足していると確率でnoneが返ってくるので、生成結果が返るまでループさせる
sentence = None
while sentence == None:
    # モデル生成
    text_model = markovify.NewlineText(splitted_text, state_size=2)
    # モデルから文章を生成
    sentence = text_model.make_sentence(tries=100)

print(sentence)
with open('sentence.txt', mode='a') as f:
    f.write(sentence)
