# aporonの自作ライブラリ
'''
リスト操作系
'''
# リストから一致する複数の要素を削除
def remove_multiple(li:list, removelist:list) -> list:
    for r in removelist:
        li = [s for s in li if s != r]
    return li

# リストの重複要素を削除
def remove_duplication(li:list) -> list:
    return list(set(li))
