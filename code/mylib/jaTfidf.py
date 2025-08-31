# IT-IDF を計算する
from math import log

class JaTfidf:
    def __init__(self) -> None:
        pass

    def tf(self, t:str, d:list[str]) -> int:
        return d.count(t) / len(d)

    def df(self, t:str, docs:list[list[str]]) -> int:
        df = 0
        for doc in docs:
            df += 1 if t in doc else 0
        return df

    def idf(self, t:str, docs:list[list[str]]) -> float:
        N = len(docs)
        return log(N/self.df(t, docs)) + 1
    
    # 文章ごとのTF-IDFを求める
    def vectorizer_transform(self, text:list[list[str]]) -> list[tuple]:
        # 単語を生成
        words = []
        for t in text:
            words += t
        words = list(set(words))
        words.sort()
        print(words)

        tf_idf = []
        for txt in text:
            line_tf_idf = []
            for w in words:
                # tfを計算
                tf_v = self.tf(w, txt)
    
                # idfを計算
                idf_v = self.idf(w, text)

                # tfとidfを乗算
                line_tf_idf.append((w, tf_v * idf_v))
            tf_idf.append(line_tf_idf)
        
        return tf_idf

    # 文書全体のTF-IDFを求める
    def whole_docs(self, text: list[list[str]], sort: bool = True) -> list[tuple]:
        tf_idf = self.vectorizer_transform(text)
        docs_tf_idf = {}
        words = [x[0] for x in tf_idf[0]]
        for w in words:
            docs_tf_idf[w] = 0

        for line in tf_idf:
            for t in line:
                docs_tf_idf[t[0]] += t[1]
        
        # 辞書内の全ての値を単語数で割る
        docs_tf_idf = {k: v/len(docs_tf_idf) for k, v in docs_tf_idf.items()}

        return sorted(docs_tf_idf.items(), key=lambda x:x[1], reverse=True) if sort else list(docs_tf_idf.items())

# # ベクトル化する文字列
# text = [
#     ['発色', 'よく', '潤い', '他', '色', 'ほしい'],
#     ['韓国', '行け', '購入', 'よかっ'],
#     ['テクスチャー', 'リップ', '探し', '気に入り']
#     ]

# jaTfidf = JaTfidf()

# # 文書全体のTF-IDF
# docs_tf_idf = jaTfidf.whole_docs(text)
# print(docs_tf_idf)