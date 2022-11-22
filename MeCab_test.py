import MeCab
#import glob2 as gb
from collections import defaultdict
import gensim
from gensim.models import Word2Vec

'''
filepaths = gb.glob('./*.txt') #读取
print(filepaths)
path1 = filepaths[0]
with open(path1,'r') as f:
    txt = f.read()
print(txt)
tagger = MeCab.Tagger()
print(tagger.parse(txt))
'''
f=open('./ngsk.txt','r',encoding = 'utf-8')


txt = f.read()

#print(txt)
tagger = MeCab.Tagger()


print("===================分词====================")

tagger_wakati = MeCab.Tagger('-Owakati')
#print(tagger_wakati.parse(txt)[8])


print("================词性区分=======================")


parsed_txt = tagger.parse(txt) #内容使用使用正则表达式表示
elements = parsed_txt.split('\n')[:-2] #把字符串装入elements列表，再将最后的两个eos和空格去掉
#print(elements[:15])
element = elements[1]
print(type(elements))
print(type(element))
print(element)



print("===============词性遍历=====================")
results = []

for element in elements:
    parts = element.split('\t') #把elements列表中的每个字符串按照\t分开，分开的元素放入parts列表
    surface,pos,base = parts[0],parts[4],parts[3]
    results.append(dict(表層形=surface,基本形=base,品詞=pos))#append 函数 将dict装入results列表

#print(results)

print("=================动词查询=======================")

#result = results[0]

surface_verbs = set()
for result in results:
    if result['品詞'] == '動詞-一般':
        surface_verbs.add(result['表層形'])
    elif result['品詞'] == '動詞-非自立可能':
        surface_verbs.add(result['表層形'])
        
#print(surface_verbs)

base_verbs = set()
for result in results:
    if result['品詞'] == '動詞-一般':
        base_verbs.add(result['基本形'])
    elif result['品詞'] == '動詞-非自立可能':
        base_verbs.add(result['基本形'])
                
#print(base_verbs)

print("======================单词频率=================")

word_freq = defaultdict(int)

for result in results:
     word_freq[result['基本形']] += 1
#print(word_freq)
#print(word_freq.items())
sorted_word_freq=sorted(word_freq.items(),key=lambda x:x[1],reverse=True)
#print(sorted_word_freq)
#print(sorted_word_freq[:10])
keys_t10 = [_[0] for _ in sorted_word_freq[:10]]
values_t10 = [_[1] for _ in sorted_word_freq[:10]]
#print(keys_t10)
#print(values_t10)

print("=====================n-gram========================")
def ngram(text,n):
    return [text[i:i+n] for i in range(len(text)-n-1)]

#print(ngram(txt,2))

words=tagger_wakati.parse(txt).split(' ')[:-1]
#print(ngram(words,2))

print('==================================================')
outcome = []

for element in elements:
    parts = element.split('\t')
    surface = parts[0]
    outcome.append(surface)

#print(outcome)


txt_p=txt.split('。')
#print(txt_p)
#print(txt_p[0])
lines = []
for i in range(len(txt_p)):
    #print(tagger_wakati.parse(txt_p[i]))
    lines.append(tagger_wakati.parse(txt_p[i]))

#print(lines)
#print(lines[0])

#print(lines[0].split(' ')[:-1])

sentences=[]
for i in range(len(lines)):
    sentences.append(lines[i].split(' ')[:-1])


#print(sentences)
#print(sentences[0])
#print(sentences[0][5])

#word2vec训练

model = Word2Vec(sentences,vector_size = 200, window = 5 , min_count=3,epochs = 7,negative=10)

def output(s_w):
    print(model.wv[s_w])
    print(model.wv.most_similar(s_w, topn=15))


output('動く')










