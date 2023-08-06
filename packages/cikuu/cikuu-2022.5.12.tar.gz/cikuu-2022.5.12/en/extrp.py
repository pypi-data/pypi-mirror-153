# 2022.6.4 overcome difficulty -> overcome ( surmount/conquer) .. difficulty 
import en, sys

def _cands(doc): 
	arr = [ {"kp":f"{t.dep_}_{t.head.pos_}_{t.pos_}/{t.head.lemma_} {t.lemma_}", "gov": t.head.lemma_, "dep":t.lemma_,  "ibeg": t.head.i, "wordlist": t.head.lemma_, } for t in doc if t.pos not in ('PUNCT',"PROPN")]
	return {ar['kp']: ar for ar in arr} # dobj_VERB_NOUN/overcome difficulty

def walk(doc, hitf=lambda cands={'dobj_VERB_NOUN/overcome difficulty':{'ibeg':1},} : {'dobj_VERB_NOUN/overcome difficulty':"surmount,conquer",}):  
	''' It will make it simple to utilize the tools.   * dead  * super,  2022.2.10 '''
	cands	= _cands(doc) 
	hitted	= hitf(cands) 
	for k,v in hitted.items():  
		if k in cands: 
			ar = cands[k] #{'dobj_VERB_NOUN/overcome difficulty@r_extrp': {'kp': 'dobj_VERB_NOUN/overcome difficulty', 'gov': 'overcome', 'dep': 'difficulty', 'ibeg': 1, 'wordlist': 'overcome', 'cate': 'r_extrp', 'short_msg': "overcome (<a target='_blank' href='http://www.cluesay.com/extrp?q=dobj_VERB_NOUN/overcome difficulty'>surmount,conquer</a>) .. difficulty"}}
			doc.user_data[f"{k}@r_extrp"] = dict(cands[k], **{"cate": "r_extrp", "short_msg": f"{ar['gov']} (<a target='_blank' href='http://www.cluesay.com/extrp?q={k}'>{v}</a>) .. {ar['dep']}"   })

if __name__ == "__main__":  
	doc = spacy.nlp("I overcome the difficulties.")
	walk(doc) 
	print (doc.user_data)