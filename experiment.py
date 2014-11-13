from gensim.models import word2vec
from wordnetter import synononymous
from wordnetter import hypernomous
from wordnetter import not_in_wordnet
from wordnetter import holonymous
from wordnetter import meronymous
from wordnetter import hyoponomous
from nltk.corpus import wordnet as wn
from nltk.corpus import reuters
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import random
import argparse
import os

try:
    os.remove("textfiles/results.txt")
except OSError:
    pass

model = word2vec.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
stemmer = SnowballStemmer("english")
parser = argparse.ArgumentParser()
parser.add_argument('--out', '-o')
args = vars(parser.parse_args())

def same_stem(one, two):
	if stemmer.stem(one) == stemmer.stem(two):
		return True
	else:
		return False

def printout(line):
    if args['out']:
        writeto = "textfiles/" + args['out']
        with open(writeto, "a") as results:
            results.write('\n' + line)

def inStopWords(w):
    if s in stopwords.words('english'):
        return True
    return False

words = list(set(reuters.words()))

random.shuffle(words)

words = set(words)

words = [s for s in words if not inStopWords(s)]

parts_of_speech = [wn.VERB, wn.ADJ, wn.NOUN, wn.ADV]

counter = 0
for r in words:
    counter = counter + 1
    r = r.encode('ascii', 'ignore')
    try:
        k = 0
        sims = model.most_similar(positive=[r], topn=200)

        for s in sims:
            k = k + 1
            for pos in parts_of_speech:
                #print "counter: " + str(counter) + "-" + str(k)
                s = (s[0].encode("ascii", 'ignore'), s[1])
                hit = False
                search = True
                if same_stem(s[0], r):
                    search = False
                    printout(",".join(['same stem', str(model.similarity(s[0], r)), s[0], r, str(s[1]), str(k) + "-" + str(counter), str(1)]))
                if not_in_wordnet(r, pos):
                    search = False
                    printout(",".join(['not_in_wordnet', str(model.similarity(s[0], r)), s[0], r, str(s[1]), str(k) + "-" + str(counter), str(1)]))
                if search:
                    hyper = hypernomous(s[0], r, pos)
                    hypo = hyoponomous(s[0], r, pos)
                    syno = synononymous(s[0], r, pos)
                    holo = holonymous(s[0], r, pos)
                    mero = meronymous(s[0], r, pos)
                    if hyper > 0 and hyper < 1:
                        printout(",".join(['hyper', pos, str(model.similarity(s[0], r)), s[0], r, str(s[1]), str(k) + "-" + str(counter), str(hyper)]))
                    if hypo > 0 and hypo < 1:
                        printout(",".join(['hypo', pos, str(model.similarity(s[0], r)), s[0], r, str(s[1]), str(k) + "-" + str(counter), str(hypo)]))
                    if syno > 0 and syno < 1:
                        printout(",".join(['syn', pos, str(model.similarity(s[0], r)), s[0], r, str(s[1]), str(k) + "-" + str(counter), str(syno)]))
                    if holo > 0 and holo < 1:
                        printout(",".join(['holo', pos, str(model.similarity(s[0], r)), s[0], r, str(s[1]), str(k) + "-" + str(counter), str(holo)]))
                    if mero > 0 and mero < 1:
                        printout(",".join(['mero', pos, str(model.similarity(s[0], r)), s[0], r, str(s[1]), str(k) + "-" + str(counter), str(mero)]))
                    if (((hyper + hypo + syno + holo + mero) == 0) or ((hyper + hypo + syno + holo + mero) == 5)):
                        printout(",".join(['none', pos, str(model.similarity(s[0], r)), s[0], r, str(s[1]), str(k) + "-" + str(counter)]))
    except KeyError:
        print printout(",".join(['KeyError', r]))
        pass