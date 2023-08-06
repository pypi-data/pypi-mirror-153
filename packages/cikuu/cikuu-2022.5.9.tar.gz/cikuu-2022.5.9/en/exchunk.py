# 2022.6.4 pay attention to -> pay _jj attention to  # 2022.2.10  uvicorn exchunk:app --host 0.0.0.0 --port 7058 --reload 
import en , traceback, sys

#conn	= sqlite3.connect("grampos.svdb", check_same_thread=False)  # how to set readonly ? 
#getdb	= lambda keys=['pay _jj attention to','is _rb beautiful'] : { row[0] : row[1] for row in conn.execute("select s,v from sv where s in ('"+"','".join([k for k in keys])+"')") } # in ('one','two')
#conn.execute(f'CREATE TABLE IF NOT EXISTS sv (s varchar(512) PRIMARY KEY, v blob)')
NP_start= {"ENT_TYPE": "NP", "IS_SENT_START": True}
VERB	= {"POS": {"IN": ["VERB"]}}
VBN		= {"TAG": {"IN": ["VBN"]}}
NOUN	= {"POS": {"IN": ["NOUN"]}}
DET		= {"POS": {"IN": ["DET"]}}
TO		= {"TAG": {"IN": ["TO"]}}
BE		= {"LEMMA": "be"}
NN		= {"TAG": {"IN": ["NN"]}}
JJ		= {"TAG": {"IN": ["JJ"]}}
ADP		= {"POS": {"IN": ["ADP"]}}
PUNCT	= {"IS_PUNCT": True}

matcher = en.new_matcher()  # :1 , verb's offset 
matcher.add("1:_jj:pay attention to", [[VERB,NOUN,ADP]]) # make use of , pay attention to -> pay _jj attention to 
matcher.add("1:_rb:is pretty/destroyed", [[BE,JJ],[BE,VBN]])
matcher.add("2:_rb:finished homework", [[VERB,NOUN,PUNCT]])
matcher.add("3:_rb:solve the problem", [[VERB,DET,NOUN,PUNCT]])
matcher.add("1:_rb:to open the door", [[TO,VERB,DET,NOUN],[TO,VERB,NOUN],[TO,VERB,{"POS":"PRP$"}]])  
matcher.add("2:_jj:make it *dead simple to", [[VERB,{"LEMMA": "it"},JJ,TO]]) #It will make it *dead simple to utilize the tools.

def chunk_ex(doc):
	for name, ibeg, iend in matcher(doc):
		offset, tag = spacy.nlp.vocab[name].text.split(':')[0:2]
		offset = int(offset) 
		yield { "ibeg":ibeg, "iend":iend, "tag":tag, "offset": offset, "pattern": " ".join( doc[i].text.lower() if i - ibeg != offset else  tag + " " + doc[i].text.lower() for i in range(ibeg, iend)) }

def chunkex(doc): 
	''' It will make it simple to utilize the tools.  
	* dead  * super,  2022.2.10 '''
	res = list(chunk_ex(doc))
	for np in doc.noun_chunks:
		if doc[np.start].pos_ == 'DET' : 
			if len(np) == 2  and doc[np.start+1].pos_ == 'NOUN': 
				res.append( {"ibeg":np.start, "iend":np.end, "tag":'_jj' , "offset":1, "pattern": doc[np.start].text.lower() + " _jj " +  doc[np.start+1].text.lower() } ) 
			elif len(np) == 3  and doc[np.start+1].tag_ == 'JJ'  and doc[np.start+2].pos_ == 'NOUN': 
				res.append( {"ibeg":np.start, "iend":np.end, "tag":'_rb' , "offset":1, "pattern": doc[np.start].text.lower() + " _rb " +  doc[np.start+1:np.start+3].text.lower() } ) 
	return res  #[(1, 4, '_jj', 1, 'paid _jj attention to'), (9, 11, '_jj', 1, 'is _jj beautiful')]


def exchunk_hit(doc, getf=lambda keys=['pay _jj attention to','is _rb beautiful'] : {}):  # {row[0]:row[1]}
	''' It will make it simple to utilize the tools.  
	* dead  * super,  2022.2.10 '''
	patterns = chunkex(doc) 
	hitted = getf(patterns) 

	dic = getdb([ar['pattern'] for ar in res]) 
	[ ar.update({"cands": dic[ ar['pattern'] ]}) for ar in res if ar['pattern'] in dic ]
	return res if verbose else [ar for ar in res if 'cands' in ar ] 

if __name__ == "__main__":  
	#print (list(chunk_ex(doc))) #[(1, 4, '_jj', 1, 'paid _jj attention to'), (9, 11, '_jj', 1, 'is _jj beautiful')]
	print( exchunk_snt("It will make it simple to utilize the tools.", True))