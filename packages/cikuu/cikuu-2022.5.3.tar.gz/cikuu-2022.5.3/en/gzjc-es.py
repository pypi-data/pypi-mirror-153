# 2022-6-1  cp from so/__main__.py 
import json,fire,sys, os, hashlib ,time 
import warnings
warnings.filterwarnings("ignore")

import en  
from en import terms,verbnet,spacybs
from en.dims import docs_to_dims
attach = lambda doc: ( terms.lempos_type(doc), verbnet.attach(doc), doc.user_data )[-1]  # return ssv, defaultdict(dict)

def index_doc(did, doc):  
	''' arr: additional attr, such as filename , '''
	import en  
	from en import terms,verbnet
	from en.dims import docs_to_dims
	attach = lambda doc: ( terms.attach(doc), verbnet.attach(doc), doc.user_data )[-1]  # return ssv, defaultdict(dict)

	arr  = {} #{"did": did}
	snts = [snt.text for snt in doc.sents]
	docs = [snt.as_doc() for snt in doc.sents] #spacy.getdoc(snt)

	if len(docs) > 1 : # at least 2 snts will be treated as a document
		dims = docs_to_dims(snts, docs)
		dims.update({'type':'doc', "sntnum":len(snts), "wordnum": sum([ len(snt) for snt in snts]), 'tm': time.time()})
		arr[did] = dims 

	for idx, sdoc in enumerate(docs):
		arr[f"{did}-{idx}"] = {'type':'snt', 'snt':snts[idx], 'pred_offset': en.pred_offset(sdoc), 
				'postag':' '.join([f"{t.text}_{t.lemma_}_{t.pos_}_{t.tag_}" if t.text == t.text.lower() else f"{t.text}_{t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}" for t in sdoc]),
				'src': f"{did}-{idx}",  'tc': len(sdoc)} # src = sentid 
		ssv = attach(sdoc) 
		for id, sour in ssv.items():
			sour.update({"src":f"{did}-{idx}"}) # sid
			arr[f"{did}-{idx}-{id}"] = sour
	return arr

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
			doc = en.from_docbin(bs) 
			sid = f"{idxname}-{rowid}"
			actions.append( {'_op_type':'index', '_index':idxname, '_id': sid, '_source': 
				{'type':'snt', 'snt':snt, 'pred_offset': en.pred_offset(doc), 'src': sid,  'tc': len(doc), 
				'postag':' '.join([f"{t.text}_{t.lemma_}_{t.pos_}_{t.tag_}" if t.text == t.text.lower() else f"{t.text}_{t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}" for t in doc]),
				} } )

			[ actions.append( {'_op_type':'index', '_index':idxname, '_id': f"{sid}-tok-{t.i}", '_source': 
				{"type":"tok", "src":sid, 'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_} }) for t in doc ]
			[ actions.append( {'_op_type':'index', '_index':idxname, '_id': f"{sid}-NP-{sp.start}", '_source': 
				{"type":"NP", "src":sid,  'lem':doc[sp.end-1].lemma_, 'pos':doc[sp.end-1].pos_, 'chunk':sp.text.lower(), 'start':sp.start, 'end':sp.end} }) for sp in doc.noun_chunks ]
			[ actions.append( {'_op_type':'index', '_index':idxname, '_id': f"{sid}-{id}", '_source': dict(sour, **{"src":sid}) } ) 
				for id, sour in attach(doc).items() if not id.startswith('tok-') and not id.startswith('trp-')]

			actions.append( {'_op_type':'index', '_index':idxname, '_id': f"{sid}-stype", '_source': {"type":"stype", "tag": "simple_snt" if en.simple_sent(doc) else "complex_snt", "src":sid} } )
			if en.compound_snt(doc) : actions.append( {'_op_type':'index', '_index':idxname, '_id': f"{sid}-stype-compound", '_source': {"type":"stype", "tag": "compound_snt", "src":sid} } )

			if len(actions) > batch: 
				helpers.bulk(client=self.es,actions=actions, raise_on_error=False)
				print ( actions[-1], flush=True)
				actions = []
		if actions : helpers.bulk(client=self.es,actions=actions, raise_on_error=False)
		print(f"{infile} is finished, \t| using: ", time.time() - start) 

	def addfolder(self, folder:str, pattern=".txt", idxname=None): 
		''' folder -> docbase, 2022.1.23 '''
		if idxname is None : idxname=  folder
		print("addfolder started:", folder, idxname, self.es, flush=True)
		if not self.es.indices.exists(index=idxname): self.es.indices.create(index=idxname, body=config)
		for root, dirs, files in os.walk(folder):
			for file in files: 
				if file.endswith(pattern):
					self.add(f"{folder}/{file}", idxname = idxname) 
					print (f"{folder}/{file}", flush=True)
		print("addfolder finished:", folder, idxname, self.es, flush=True)

	def loadsnt(self, infile, idxname=None):
		''' add doc only , 2022.3.25 '''
		if idxname is None : idxname = infile.split('.')[0] 
		if not self.es.indices.exists(index=idxname): self.es.indices.create(index=idxname, body=config)
		start = time.time()
		for idx, line in enumerate(open(infile, 'r').readlines()): 
			ssv  = index_doc(idx, spacy.nlp(line.strip()))
			for id, sv in ssv.items(): 
				try:
					self.es.index(index = idxname, id = id, document = sv) #https://github.com/elastic/elasticsearch-py/issues/1698
				except Exception as ex:
					print(">>add ex:", ex, id, sv)
		print(f"{infile} is finished, \t| using: ", time.time() - start) 
	
	def init(self, idxname):
		''' init a new index '''
		if self.es.indices.exists(index=idxname):self.es.indices.delete(index=idxname)
		self.es.indices.create(index=idxname, body=config) #, body=snt_mapping
		print(">>finished " + idxname )

	def load(self, infile, idxname, batch=100000): 
		''' python3 -m so load essaydm.json essaydm 
		load id-source-file into index, 2022.4.2 '''
		print(">>started: " , infile, idxname, flush=True )
		actions=[]
		for line in readline(infile): 
			try:
				arr = json.loads(line) 
				#arr.update({'_op_type':'index', '_index':idxname,}) 
				actions.append( {'_op_type':'index', '_index':idxname, '_id': arr.get('_id',None), '_source': arr.get('_source',{}) } )
				if len(actions) > batch: 
					helpers.bulk(client=self.es,actions=actions, raise_on_error=False)
					print ( actions[-1], flush=True)
					actions = []
			except Exception as e:
				print("ex:", e)	
		if actions : helpers.bulk(client=self.es,actions=actions, raise_on_error=False)
		print(">>finished " , infile, idxname )

if __name__ == '__main__':
	fire.Fire(ES)