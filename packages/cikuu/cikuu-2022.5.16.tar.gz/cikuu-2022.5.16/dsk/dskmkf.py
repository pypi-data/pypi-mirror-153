# 2022.5.30
import json, en, requests,time,sys, traceback

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

if __name__ == '__main__':
	res = todsk("I overcame the difficulties.", polish_f = polish_func, debug=True)
	#{'feedback': 'overcome difficulty/dobj_VERB_NOUN@r_polish:3': {'conquer difficulty': 1, 'short_msg': 'conquer, surmount', 'ibeg': 3}}, 'meta': {'pid': 0, 'ske': ['n_v_n'], 'para_id': 0, 'sid': 0, 'tc': 5, 'sub_cnt': 1, 'pos_rewrite': '[^/^, I/PRP, overcame/VBD, the/DT, difficulties/NNS, ./.]', 'pred_lemma': 'overcome', 'postag': '^_^_^ I_prp_prp_no_n_sb_I overcame_vbd_pastten_v_overcome the_dt_n2_the difficulties_nns_n_difficulty ._._.', 'snt': 'I overcame the difficulties.', 'lex_list': 'I overcame the difficulties .', 'vpat': ['overcome _n'], 'tense': ''}}
	print ( res['snt'][0] ) 
	print ( res['info']['tim'])

# cp __init__.py /home/ubuntu/.local/lib/python3.8/site-packages/dsk