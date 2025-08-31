# 商品レビューから商品の特徴をタグ付けする
from pathlib import Path
import json
import collections
# 自作ライブラリ
import mylib.aporonlib as aplib
from mylib.mecabSimple import MeCabSimple
from mylib.jaTfidf import JaTfidf

def tagProduct(di_prdt: dict, id: str, stopwords: list[str], taglen: int = 40) -> dict:
    result = {
        'id':id,
        'name':di_prdt[0]['全体の商品名'],
        'tag':[], # １つの商品のTF-IDF上位単語を格納
    }
    # 形態素解析したレビュー文を格納するリスト
    li_rev = []
    for rev in di_prdt :
        # レビュー文を形態素解析して名詞、形容詞、副詞を抽出
        ms = MeCabSimple(rev['レビュー本文'])
        li_token = ms.filter_pos('名詞','動詞','形容詞') # '名詞', '形容詞', '副詞'
        # ストップワードを削除してリストに追加
        li_token = aplib.remove_multiple(li_token, stopwords)
        if li_token != []:
            li_rev.append(li_token)
    # TF-IDFを計算
    jaTfidf = JaTfidf()
    tfidf = jaTfidf.whole_docs(li_rev)[:taglen]
    result['tag'] = [x[0] for x in tfidf]
    return result


# 絶対パスを取得
cur = Path.cwd()

# jsonファイル名を取得
li_inpPath= [str(p) for p in list(Path(cur/'json/lip').glob('*.json'))]
print(li_inpPath)

# 書き出し先のフォルダを作成
out = Path(cur/'json/tf-idf')
out.mkdir(exist_ok=True)

# ストップワードの読み込み
with open(cur/'stopword/stopword.txt', 'r', encoding='utf-8') as f:
    stopwords = f.read().split('\n')
# 自作のストップワードを追加
with open(cur/'stopword/mystopword.txt', 'r', encoding='utf-8') as f:
    stopwords += f.read().split('\n')
# ストップワードの重複を削除
stopwords = aplib.remove_duplication(stopwords)

# 結果を格納するリスト
li_tagprdt = []

# jsonファイルごとに処理
for inpPath, i in zip(li_inpPath, range(len(li_inpPath))):
    with open(inpPath, 'r', encoding='utf-8') as f:
        di_prdt = json.load(f)
    id = str(Path(inpPath).stem)
    li_tagprdt.append(tagProduct(di_prdt, id, stopwords))
    print(f'{i+1} 個目の商品が処理完了。')
print(li_tagprdt)
with open(out/'taggedPrdt_1.json', 'w', encoding='utf-8') as f:
        json.dump(li_tagprdt, f, indent=4, ensure_ascii=False)
