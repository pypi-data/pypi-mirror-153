# 2022-6-1  cp from so/__main__.py 
import json,fire,sys, os, hashlib ,time 
import warnings
warnings.filterwarnings("ignore")

import en  
from en import terms,verbnet,spacybs
from en.dims import docs_to_dims
attach = lambda doc: ( terms.lempos_type(doc), verbnet.attach(doc), doc.user_data )[-1]  # return ssv, defaultdict(dict)

def sntdoc_idsour(sid, snt, doc, actions): 
	''' '''
	actions.append( {'_id': sid, '_source': 
		{'type':'snt', 'snt':snt, 'pred_offset': en.pred_offset(doc), 'src': sid,  'tc': len(doc), 
		'postag':' '.join([f"{t.text}_{t.lemma_}_{t.pos_}_{t.tag_}" if t.text == t.text.lower() else f"{t.text}_{t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}" for t in doc]),
		} } )
	[ actions.append( {'_id': f"{sid}-tok-{t.i}", '_source': 
		{"type":"tok", "src":sid, 'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_} }) for t in doc ]
	[ actions.append( {'_id': f"{sid}-np-{sp.start}", '_source': 
		{"type":"np", "src":sid,  'lempos':doc[sp.end-1].lemma_  + "/" + doc[sp.end-1].pos_, 'chunk':sp.text.lower(), 'start':sp.start, 'end':sp.end} }) for sp in doc.noun_chunks ]
	[ actions.append( {'_id': f"{sid}-{id}", '_source': dict(sour, **{"src":sid}) } ) 
		for id, sour in attach(doc).items() if not id.startswith('tok-') and not id.startswith('trp-')]
	actions.append( { '_id': f"{sid}-stype", '_source': {"type":"stype", "tag": "simple_snt" if en.simple_sent(doc) else "complex_snt", "src":sid} } )
	if en.compound_snt(doc) : actions.append( { '_id': f"{sid}-stype-compound", '_source': {"type":"stype", "tag": "compound_snt", "src":sid} } )

def index_text(did, text):  
	'''  '''
	doc  = spacy.nlp(text) 
	snts = [snt.text for snt in doc.sents]
	docs = [snt.as_doc() for snt in doc.sents] 
	acts = []
	[sntdoc_idsour(f"{did}-{idx}", snts[idx], sdoc, acts) for idx, sdoc in enumerate(docs)]

	dims = docs_to_dims(snts, docs)
	acts.append( {"_id": did, "_source": {"type":"doc", "filename": did, "sntnum":len(snts), "wordnum": sum([ len(doc) for doc in docs]), 'tm': time.time(), "dims": json.dumps(dims)} })
	return acts

from so import * # config
class ES(object):
	def __init__(self, host='127.0.0.1',port=9200): 
		self.es = Elasticsearch([ f"http://{host}:{port}" ])  

	def toes(self, infile, idxname=None, refresh:bool=True, batch:int=700000):
		''' submit gzjc.spacybs to ES , 2022.6.1 '''
		if idxname is None : idxname = infile.split('.')[0] 
		if refresh and self.es.indices.exists(index=idxname) : self.es.indices.delete(index=idxname)
		if not self.es.indices.exists(index=idxname): self.es.indices.create(index=idxname, body=config)
		print ('start to load :', infile, flush=True)
		start = time.time()
		actions=[]
		for rowid, snt, bs in spacybs.Spacybs(infile).items() :
			doc		= en.from_docbin(bs) 
			sid		= rowid # to connect with: SELECT dictGet('snt_gzjc', 'snt', 7000), | f"{idxname}-{rowid}"
			sntdoc_idsour(sid, snt, doc, actions)
			if len(actions) > batch: 
				helpers.bulk(client=self.es,actions=[ dict(ar, **{'_op_type':'index', '_index':idxname}) for ar in actions], raise_on_error=False)
				print ( actions[-1], flush=True)
				actions = []
		if actions : helpers.bulk(client=self.es,actions=[ dict(ar, **{'_op_type':'index', '_index':idxname}) for ar in actions], raise_on_error=False)
		print(f"{infile} is finished, \t| using: ", time.time() - start) 

	def loadtxt(self, infile, idxname:str="testidx"):
		''' add  text file only , 2022.6.1 '''
		if not self.es.indices.exists(index=idxname): self.es.indices.create(index=idxname, body=config)
		start = time.time()
		acts = index_text(infile, open(infile, 'r').read())
		if acts : helpers.bulk(client=self.es,actions=[ dict(ar, **{'_op_type':'index', '_index':idxname}) for ar in acts], raise_on_error=False)
		print(f"{infile} is loaded, \t| using: ", time.time() - start) 

	def loadfolder(self, folder:str, pattern=".txt", idxname=None, refresh:bool=True): 
		''' folder -> docbase, 2022.1.23 '''
		if idxname is None : idxname=  folder
		if refresh and self.es.indices.exists(index=idxname) : self.es.indices.delete(index=idxname)
		print("addfolder started:", folder, idxname, self.es, flush=True)
		if not self.es.indices.exists(index=idxname): self.es.indices.create(index=idxname, body=config)
		for root, dirs, files in os.walk(folder):
			for file in files: 
				if file.endswith(pattern):
					self.loadtxt(f"{folder}/{file}", idxname = idxname) 
		print("addfolder finished:", folder, idxname, self.es, flush=True)
	
if __name__ == '__main__':
	fire.Fire(ES)