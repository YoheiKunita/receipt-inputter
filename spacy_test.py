import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span

class take_price:
    def __init__(self):
        # Spacyの設定
        self.nlp = spacy.load('ja_ginza')

    def extract_dates(self, text):
        # 文字データを改行コードで分割
        lines = text.split('\n')
        dates = []

        # テキストを解析して日付エンティティを取得
        for i, line in enumerate(lines):
            doc = self.nlp(line)

            for ent in doc.ents:
                 if ent.label_ == 'Date':
                    dates.append(ent.text)
        return dates

    def extract_price_line(self, text):
        matcher = Matcher(self.nlp.vocab)

        price_pattern = [{"TEXT":"\\"},{"IS_DIGIT":True, "OP":"+"}]
        matcher.add("match_price", [price_pattern])

        date_pattern = [{"IS_DIGIT":True, "OP":"+"},{"TEXT":"\\"},{"IS_DIGIT":True, "OP":"+"}]
        matcher.add("match_price", [price_pattern])

        # 購入日付を取得する変数
        date = ""

        # 結果を格納する。結果は[[品目],[値段]]のリストで格納する
        result = []

        # 文字データを改行コードで分割
        lines = text.split('\n')

        # 分割された各行を順番に処理
        for i, line in enumerate(lines):
            # 何らかの金額(￥100 など)が含まれる行を抽出する
            doc = self.nlp(line)
            matches = matcher(doc)

            # 抽出した結果を表示,格納
            for match_id, start, end in matches:
                string_id = self.nlp.vocab.strings[match_id] 
                result.append([doc[0:start].text, doc[start+1:end].text])

        return result

'''
import locale

# テスト。
path = r'C:\\Users\\water\\Python\\data\\resutl_OCR.txt'

# ファイルを読み込みモードで開いて、textに格納
default_encoding = locale.getpreferredencoding()
with open(path, "r", encoding=default_encoding) as file:
    text = file.read()

# 正規表現で読み込み
test = take_price().extract_price_line(text)
date = take_price().extract_dates(text)

# テスト表示
print(type(test[0][0]))
print(test)

print(type(date), date)


'''