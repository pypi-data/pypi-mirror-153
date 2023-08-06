# 2022.6.4  at the top of the hill  => at the peak | a big amount of =>a sizeable/considerable/colossal/prodigious amount of
import en, sys

matcher = en.phrase_matcher('pp', [[{'POS': 'ADP'},{"POS": {"IN": ["DET","NUM","ADJ",'PUNCT','CONJ']}, "OP": "*"},{"POS": {"IN": ["NOUN","PART"]}, "OP": "+"}]])
''' for name, ibeg,iend in matcher(doc) : print(spacy.nlp.vocab[name].text, doc[ibeg:iend].text) '''

def _cands(doc): 
	arr = [ {"kp":doc[ibeg:iend].text, "tag":spacy.nlp.vocab[name].text , "ibeg": ibeg, "iend":iend,  "wordlist": doc[ibeg:iend].text, } for name, ibeg,iend in matcher(doc)]
	return {ar['kp']: ar for ar in arr} 

def walk(doc, hitf=lambda cands={'at the top of the hill':{'ibeg':1},} : {'at the top of the hill':"at the peak",}):  
	cands	= _cands(doc) 
	hitted	= hitf(cands) 
	for k,v in hitted.items():  
		if k in cands: 
			#ar = cands[k] 
			doc.user_data[f"{k}@r_exphrase"] = dict(cands[k], **{"cate": "r_exphrase", "short_msg": 
				f"[{k}]: <a target='_blank' href='http://www.cluesay.com/exphrase?q={k}'>{v}</a>"   })

if __name__ == "__main__":  
	doc = spacy.nlp("I am at the top of the hill.")
	walk(doc) 
	print (doc.user_data)