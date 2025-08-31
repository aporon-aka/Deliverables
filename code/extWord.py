# 入力文から単語を抽出
import spacy
# 自作ライブラリ
from mylib.mecabSimple import MeCabSimple
import mylib.aporonlib as aplib
# 入力文
text = '冬ブルベでパーティに付けていけるしっとり感のあるリップを教えてください。'
# text = '私は敏感肌で、唇が乾燥しやすく皮むけしてしまう悩みがあるため、できるだけ刺激の少ない優しい処方で、ヒアルロン酸や植物オイルなどの保湿成分がしっかり配合されたものを探しております。可能であれば、無香料、アルコールフリー、パラベンフリーの製品ですと大変嬉しいです。パーソナルカラーがブルーベース夏のため、色味はローズピンクやモーヴ、ラズベリーといった青みのある涼しげで穏やかなものを希望しており、黄みの強いオレンジやコーラル系の色は避けています。仕上がりについては、透明感のあるツヤタイプや透け感のあるシアーなものが好みですが、もしマットリップでおすすめがございましたら、乾燥しにくいソフトマットな質感を希望します。必須ではございませんが、ティント効果やUVカット機能があればさらに魅力的です。'

# GiNZAモデルをロード
nlp = spacy.load("ja_ginza")

# === 固有表現抽出　===
# テキストを処理
doc = nlp(text)

# 抽出された固有表現をループで表示
print("抽出された固有表現:")
for ent in doc.ents:
    # ent.text: 固有表現のテキスト
    # ent.label_: 固有表現のラベル（種類）
    print(f"- {ent.text} ({ent.label_})")

# === 関係抽出 ===
# text = "Appleは新しいiPhoneを発表した。"

doc = nlp(text)

subject = ""
verb = ""
object = ""

# 各単語（トークン）の係り受け関係を調べる
for token in doc:
    # token.dep_ で係り受けの種類がわかる
    if token.dep_ == "nsubj": # nsubj: 主語
        subject = token.text
    elif token.dep_ == "obj": # obj: 目的語
        object = token.text
    # 主語や目的語が係っている動詞（述語）を探す
    if token.dep_ in ["nsubj", "obj"]:
        verb = token.head.text # head: 係り先の単語

if subject and verb and object:
    print(f"抽出された関係: ({subject}) ---[{verb}]---> ({object})")
else:
    print("単純なSVO関係は見つかりませんでした。")


# # 形態素解析して名詞、形容詞、副詞を抽出
# ms = MeCabSimple(text)
# tag = ms.filter_pos('名詞', '形容詞', '副詞')
# print(tag)
# print(ms.parse)

# # 使わない単語を削除
# removewords = ['感', 'め']
# tag = aplib.remove_multiple(tag, removewords)
# print(tag)
