import nltk

'''
sentence = "Today Bob went to the shop and bought 10 hotdogs."
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)
print(tagged)
'''


nltk.download('tagsets')
nltk.help.upenn_tagset('MD')
nltk.help.upenn_tagset('DT')
nltk.help.upenn_tagset('JJ')
nltk.help.upenn_tagset('NNS')
nltk.help.upenn_tagset('CD')
