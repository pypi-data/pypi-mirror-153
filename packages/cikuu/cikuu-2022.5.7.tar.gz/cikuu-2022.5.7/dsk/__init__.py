# 2022.5.30
import json, en, requests,time,sys, traceback

def topk_info(snts, docs,  topk, default_dims = {"internal_sim":0.2} ): 
	''' info computing with topk snts, upon those long essay '''
	from dsk import score, pingyu
	from en.dims import docs_to_dims
	
	info = {}
	dims = docs_to_dims(snts[0:topk], docs[0:topk]) # only top [0:topk] snts are considered for scoring 
	for k,v in default_dims: 
		if not k in dims: 
			dims[k] = v # needed by formular 

	info.update(score.dims_score(dims))
	info['pingyu'] = pingyu.get_pingyu(dims)
	info['dims']   = dims  # new dsk format , /doc -> /info/dims 
	return info 

import difflib
trans_diff		= lambda src, trg:  [] if src == trg else [s for s in difflib.ndiff(src, trg) if not s.startswith('?')] #src:list, trg:list
trans_diff_merge= lambda src, trg:  [] if src == trg else [s.strip() for s in "^".join([s for s in difflib.ndiff(src, trg) if not s.startswith('?')]).replace("^+","|+").split("^") if not s.startswith("+") ]

def mkf_input(snts, docs, tokenizer, sntdic:dict={},diffmerge:bool=False): 
	''' mkf input for 7095 java calling '''
	srcs	= [ [t.text for t in doc] for doc in docs]
	tgts	= [ [t.text for t in doc] if ( snt not in sntdic or snt == sntdic.get(snt,snt) ) else [t.text for t in tokenizer(sntdic.get(snt,snt))] for snt, doc in zip(snts, docs)]
	input	= [ {"pid":0, "sid":i, "snt":snts[i], "tok": [t.text for t in doc],  
				"pos":[t.tag_ for t in doc], "dep": [t.dep_ for t in doc],"head":[t.head.i for t in doc],  
				"seg":[ ("NP", sp.start, sp.end) for sp in doc.noun_chunks] + [ (np.label_, np.start,np.end) for np in doc.ents] , 
				"gec": sntdic.get(snts[i],snts[i]), "diff": trans_diff_merge( srcs[i] , tgts[i]) if diffmerge else  trans_diff( srcs[i] , tgts[i] )	}
				for i, doc in enumerate(docs)]
	return input #mkfs	= requests.post(f"http://172.17.0.1:7095/parser", data={"q":json.dumps(input).encode("utf-8")}).json()

def todsk(essay_or_snts:str="She has ready. It are ok.", asdsk:bool=True, dskhost:str='gpu120.wrask.com:7095'  
		, debug:bool= False
		, redis_r	= None # xadd, redis.r		= redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=True) 
		, redis_bs	= None # bs cache, bytes, redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=False) 
		, gec_func	= lambda snts: requests.post(f"http://gpu120.wrask.com:8180/redis/getgecs", json=snts).json () 
		, nlp_func	= lambda snt: spacy.nlp(snt)
		, polish_f	= lambda doc, dsk, idx: None): # extending polishment terms
	''' online version gec, no pipe imported, 2022.5.30 '''
	try:
		tims	= [ ("start", time.time(), 0)] # tag, tm, delta 
		snts	= json.loads(essay_or_snts) if essay_or_snts.startswith("[") else en.sntbr(essay_or_snts)
		if redis_r: [redis_r.xadd('xsntbytes', {'snt':snt}) for snt in snts] # notify spacy snt parser

		sntdic	= gec_func(snts) #{'She has ready.': 'She is ready.', 'It are ok.': 'It is ok.'}
		if debug : tims.append( ("gec", time.time(), round(time.time() - tims[-1][1],2))  )
		docs	= [ en.getdoc(snt, redis_bs.get(f"bytes:{snt}") ) if redis_bs else nlp_func(snt) for snt in snts ] 
		if debug : tims.append( ("nlp", time.time(), round(time.time() - tims[-1][1],2))  )
		input	= mkf_input(snts, docs, spacy.nlp.tokenizer, sntdic)
		dsk		= requests.post(f"http://{dskhost}/parser", data={"q":json.dumps({"snts":input, "rid":"10"} if asdsk else input).encode("utf-8")}).json()
		if debug : tims.append( ("dsk", time.time(), round(time.time() - tims[-1][1], 2))  )
		if debug and isinstance(dsk, dict) and 'info' in dsk : dsk['info']['tim'] = tims #[('start', 1653811771.030599, 0), ('gec', 1653811776.2294545, 5.2), ('nlp', 1653811776.2439919, 0.01), ('dsk', 1653811776.275237, 0.03)]

		[polish_f(doc, dsk, idx ) for idx, doc in enumerate(docs) ]
		return dsk  #docker run -d --restart=always --name dsk17095 -v /data/dct:/dct -p 7095:7095 wrask/gec:dsk8 java -Xmx4096m -jar pigai_engine8.jar --database-no-encrypt --server-addr dsk.wrask.com --server-port 7095  --database-type sqlite --sqlite-file dct/sqlite/pigai_spss.sqlite3 --thread-num 2 --gec-snts-address http://wrask.com:33000/gec/essay_or_snts
	except Exception as ex: 
		print(">>todsk Ex:", ex, "\t|", essay_or_snts)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)

def localgec_todsk(essay_or_snts:str="She has ready. It are ok.", device:int=-1, asdsk:bool=True, dskhost:str='172.17.0.1:7095', debug:bool=False): 
	''' essay -> dsk, with local gec model support, |  2022.5.28 '''
	import pipe #pip install torch transformers| cp model
	return todsk(essay_or_snts, asdsk=asdsk, dskhost=dskhost, debug=debug, gec_func = lambda snts: pipe.gecsnts(snts, device=device))

def init_dskmkf_table(cursor):
	cursor.execute('''CREATE TABLE if not exists `dsk` (
  `eidv` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '{eid}-{ver}',
  `eid` int NOT NULL DEFAULT '0',
  `ver` int NOT NULL DEFAULT '0',
  `rid` int NOT NULL DEFAULT '0',
  `uid` int NOT NULL DEFAULT '0',
  `score` float NOT NULL DEFAULT '0',
  `snts` json DEFAULT NULL,
  `doc` json DEFAULT NULL,
  `info` json DEFAULT NULL,
  `tm` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`eidv`),
  UNIQUE KEY `eidv` (`eid`,`ver`),
  KEY `rid` (`rid`),
  KEY `uid` (`uid`)
) ENGINE=Innodb DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ''')

	cursor.execute('''CREATE TABLE if not exists `mkf` (
  `sntmd5` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `snt` text COLLATE utf8mb4_unicode_ci,
  `kps` text COLLATE utf8mb4_unicode_ci,
  `tok` json DEFAULT NULL,
  `chunk` json DEFAULT NULL,
  `meta` json DEFAULT NULL,
  `feedback` json DEFAULT NULL,
  `tm` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sntmd5`),
  FULLTEXT KEY `sntkps` (`snt`,`kps`)
) ENGINE=Innodb DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci''')

import hashlib
md5snt	= lambda text: hashlib.md5(text.encode("utf-8")).hexdigest()

doc_tok	= lambda doc:  [ {'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_} for t in doc]
doc_chunk	= lambda doc:  [ {"lem": doc[sp.end-1].lemma_, "start":sp.start, "end":sp.end, "pos":"NP", "chunk":sp.text} for sp in doc.noun_chunks]
feedback	= lambda arr : [ {"cate":v.get('cate',''), "ibeg": v.get('ibeg',-1), "msg":v.get("short_msg","")} for k,v in arr.items() if v.get('cate','').startswith("e_") or v.get('cate','').startswith("w_")]

def submit_dskmkf(dsk, cursor): 
	''' '''
	snts  = [ ar.get('meta',{}).get('snt','').strip() for ar in dsk.get('snt',[])] # to md5
	info = dsk.get("info", {})
	eid,rid,uid,ver = int( info.get('essay_id',0) ),int( info.get('rid',0) ),int( info.get('uid',0) ),int( info.get('e_version',0) )
	score = float( info.get('final_score',0) ) # added 2022.2.15
	cursor.execute("insert ignore into dsk(eidv,eid,ver,rid,uid, score, snts, doc, info) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
		(f"{eid}-{ver}",eid,ver,rid,uid, score, json.dumps([md5snt(snt) for snt in snts]), json.dumps(dsk.get('doc',{})), json.dumps(info)))

	for idx, snt in enumerate(snts) : 	
		if not snt: continue
		sntmd5 = md5snt(snt)
		cursor.execute(f"select * from mkf where sntmd5 = '{sntmd5}' limit 1")
		result=cursor.fetchone ()
		if result and len(result) > 0 : continue  #if sntmd5 in snts_known: continue #snts_known.add(sntmd5) 

		doc = spacy.nlp(snt)
		for ar in dsk['snt']:
			fd , meta = ar.get('feedback',{}), ar.get('meta',{})
			fds = feedback(fd)
			kps = [ f"{t.pos_}_{t.lemma_}" for t in doc] + [ f"{t.tag_}_{t.lemma_}" for t in doc] + [ f"{t.dep_}_{t.head.pos_}_{t.pos_}_{t.head.lemma_}_{t.lemma_}" for t in doc if t.pos_ not in ('PRON','PUNCT') and t.dep_ in ('dobj','nsubj','advmod','acomp','amod','compound','xcomp','ccomp')]
			[ kps.append( ar.get('cate','').replace('.','_')) for ar in fds if ar.get('cate','')] # e_prep.wrong -> e_prep_wrong

			cursor.execute("insert ignore into mkf(sntmd5, snt, kps, tok, chunk, meta, feedback) values(%s,%s,%s,%s,%s,%s,%s)", (sntmd5, snt, ' '.join(kps),
			json.dumps(doc_tok(doc)), json.dumps(doc_chunk(doc)), json.dumps(meta), json.dumps(fds)  ) 	) #, spacy.tobs(doc)

def polish_func(doc, dsk, idx): 
	''' '''
	lookup	= {"overcome difficulty/dobj_VERB_NOUN": {"conquer difficulty":1, 'short_msg': 'conquer, surmount'}}
	mkf		= dsk['snt'][idx] 
	for t in doc: 
		term = f"{t.head.lemma_} {t.lemma_}/{t.dep_}_{t.head.pos_}_{t.pos_}"
		if term in lookup: 
			mkf['feedback'].update({ f"{term}@r_polish:{t.i}": dict(lookup[term], **{"ibeg":t.i}) } )

if __name__ == '__main__':
	res = todsk("I overcame the difficulties.", polish_f = polish_func, debug=True)
	#{'feedback': 'overcome difficulty/dobj_VERB_NOUN@r_polish:3': {'conquer difficulty': 1, 'short_msg': 'conquer, surmount', 'ibeg': 3}}, 'meta': {'pid': 0, 'ske': ['n_v_n'], 'para_id': 0, 'sid': 0, 'tc': 5, 'sub_cnt': 1, 'pos_rewrite': '[^/^, I/PRP, overcame/VBD, the/DT, difficulties/NNS, ./.]', 'pred_lemma': 'overcome', 'postag': '^_^_^ I_prp_prp_no_n_sb_I overcame_vbd_pastten_v_overcome the_dt_n2_the difficulties_nns_n_difficulty ._._.', 'snt': 'I overcame the difficulties.', 'lex_list': 'I overcame the difficulties .', 'vpat': ['overcome _n'], 'tense': ''}}
	print ( res['snt'][0] ) 
	print ( res['info']['tim'])

# cp __init__.py /home/ubuntu/.local/lib/python3.8/site-packages/dsk