# MeCab で形態素解析
import MeCab
import ipadic

class MeCabSimple:
    # MeCabインスタンスを作成。インストールした辞書(ipadic)を指定
    mecab = MeCab.Tagger(ipadic.MECAB_ARGS)  

    def __init__(self, text:str) -> None:
        self.text = text
        self.node = MeCabSimple.mecab.parseToNode(self.text)
        self.parse = MeCabSimple.mecab.parse(self.text)
    
    # テキストのトークン化
    def tokenize(self):
        node = self.node
        token = []
        while node:
            if node.surface != '':
                token.append(node.surface)
            node = node.next
        return token
        
    # 特定の品詞のフィルタリング
    def filter_pos(self, *part:tuple) -> list[str]:
        # 形態素解析
        node = self.node
        # 結果を格納するリスト
        output = []
        while node:
            word_type = node.feature.split(',')[0]
            if word_type in part:
                if not node.surface.isdigit():
                    output.append(node.surface.upper())
            node = node.next
        return output
'''
使用例
'''
# # 形態素解析するテキスト
# text = 'ブルベ冬です。薄づきですがするーっとしたテクスチャー、ぴたっとフィットしてくれます。透け感がありつつも、色味はしっかりでてくれます。スーッと少しだけひんやりして、気持ち良い。'
# # インスタンス作成
# ms = MeCabSimple(text)

# # 解析結果の取得
# print(ms.parse)

# # トークン化したテキストの取得
# tokens = ms.tokenize()
# print(tokens)

# # 特定の品詞を取得
# result = ms.filter_pos('名詞','形容詞','副詞')
# print(result)
