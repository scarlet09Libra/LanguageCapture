from capture import imageToTexts
from train import languageDict, predict, majority


def prediction(texts):
    result = predict(texts)
    return majority(result)

msg = '''++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
画像のパスを入力することで、対象に含まれる文字列が何語であるかを識別します。
対応言語は下記の通り。

【1】アラビア語  【2】チェコ語  【3】ペルシア語  【4】インドネシア語  【5】イタリア語
【6】オランダ語  【7】ポーランド語  【8】ポルトガル語  【9】スペイン語  【10】トルコ語
【11】ベトナム語
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
print(msg)


filepath = input('SYS> Please enter the path of your image.\n')

texts = imageToTexts(filepath)
result = prediction(texts)

print('\nSYS> Execusion has been completed. Result is shown below.')
print('SYS> This image may contains ' + languageDict[result])
print(texts[result])
