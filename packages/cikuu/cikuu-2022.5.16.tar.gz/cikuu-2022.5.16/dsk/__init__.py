# 2022.6.5
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

def wrapper(essay_or_snts:str="She has ready. It are ok.", asdsk:bool=True, debug:bool= False, timeout:int=5, gechost:str='172.17.0.1:8180' , dskhost:str='172.17.0.1:7095'): 
	''' simple wrapper for debug only, 2022.6.5 '''
	snts	= json.loads(essay_or_snts) if essay_or_snts.startswith("[") else en.sntbr(essay_or_snts)
	sntdic	= requests.post(f"http://{gechost}/getgecs", params={"timeout":timeout}, json=snts).json ()
	docs	= [spacy.nlp(snt) for snt in snts ] 
	input	= mkf_input(snts, docs, spacy.nlp.tokenizer, sntdic)
	return	requests.post(f"http://{dskhost}/parser", data={"q":json.dumps({"snts":input, "rid":"10"} if asdsk else input).encode("utf-8")}).json()

def todsk(arr:dict={'essay_or_snts':"She has ready. It are ok.", # arr from mq 
				'formula':{ 
				"ast":[9.9, 11.99, 15.3, 18.51, 25.32,				2,0.0882, 0.3241],
				"awl":[3.5, 4.1, 4.56, 5.1, 6.0,					3,0.0882, 0.5],
				"b3":[0, 0.03, 0.08, 0.12, 0.15 ,					1, 0.0956, 0.2096],
				"cl_sum":[1, 6.68, 12, 16, 26,						2,0.0441, 0.1621],
				"grammar_correct_ri":[0.6, 0.85, 0.92, 0.97,1.0,	2,0.0368, 0.1352],
				"internal_sim":[0.0, 0.08, 0.2, 0.3, 0.4,			4, 0.0735, 0.7688],
				"kp_correct_ri":[0.7, 0.9, 0.95, 0.97, 1,			1, 0.0368, 0.0807],
				"mwe_pv":[0.01,8.03, 12, 20.21, 25,					4, 0.0221, 0.2312],
				"pred_diff_max3":[3.84, 5.11, 6.51, 7.9, 10.09 ,	1, 0.0368, 0.0807],
				"prmods_ratio":[0.06, 0.21, 0.3, 0.4, 0.5,			2, 0.0294, 0.108],
				"prmods_tc":[1.1, 2.76, 4.75, 6.76, 10.0,			2, 0.0368, 0.1352],
				"simple_sent_ri":[0.4, 0.65, 0.9, 0.95, 1,			2, 0.0368, 0.1352],
				"snt_correct_ratio":[0.01, 0.2, 0.45, 0.75, 1,		1, 0.0368, 0.0807],
				"spell_correct_ratio":[0.8, 0.9, 0.97, 0.99, 1,		1, 0.1471, 0.3226],
				"ttr1":[3.43, 4.28, 5.2, 6, 6.8,					3, 0.0882, 0.5],
				"word_diff_avg":[4.47, 4.73, 5.25,5.8, 6.6,			1, 0.0441, 0.0967],
				"word_gt7":[0.11, 0.19, 0.3, 0.42, 0.49,			1, 0.0588, 0.1289]}}
		, asdsk:bool=True, debug:bool= False, timeout:int=5
		, gechost:str=None # localversion, return {'She has ready.': 'She is ready.', 'It are ok.': 'It is ok.'}
		, dskhost:str='172.17.0.1:7095' 
		, redis_r	= None # xadd, redis.r = redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=True) 
		, redis_bs	= None # bs cache, bytes, redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=False) 
		, nlp_func	= lambda snt: spacy.nlp(snt)
		, polish_f	= lambda doc, dsk, idx: None): # extending polishment terms
	''' '''
	import pipe
	from dsk import score 
	try:
		tims	= [ ("start", time.time(), 0)] # tag, tm, delta 
		essay_or_snts = arr.get("essay_or_snts","")
		snts	= json.loads(essay_or_snts) if essay_or_snts.startswith("[") else en.sntbr(essay_or_snts)
		if redis_r and snts: [redis_r.xadd('xsntbytes', {'snt':snt}) for snt in snts] # notify spacy snt parser

		sntdic	= requests.post(f"http://{gechost}/getgecs", params={"timeout":timeout}, json=snts).json () if gechost else pipe.gecsnts(snts) # local version by default 
		if debug : tims.append( ("gec", time.time(), round(time.time() - tims[-1][1],2))  )
		docs	= [ en.getdoc(snt, redis_bs.get(f"bytes:{snt}") ) if redis_bs else nlp_func(snt) for snt in snts ] 
		if debug : tims.append( ("nlp", time.time(), round(time.time() - tims[-1][1],2))  )
		input	= mkf_input(snts, docs, spacy.nlp.tokenizer, sntdic)
		res		= requests.post(f"http://{dskhost}/parser", data={"q":json.dumps({"snts":input, "rid":"10"} if asdsk else input).encode("utf-8")}).json()
		if debug : tims.append( ("dsk", time.time(), round(time.time() - tims[-1][1], 2))  )
		if isinstance(res, dict) and 'info' in res:
			if debug  : res['info']['tim'] = tims #[('start', 1653811771.030599, 0), ('gec', 1653811776.2294545, 5.2), ('nlp', 1653811776.2439919, 0.01), ('dsk', 1653811776.275237, 0.03)]
			if 'formula' in arr : res['info'].update(  score.dims_score(res['doc'], arr['formula'])) # reset the score 

		[polish_f(doc, res, idx ) for idx, doc in enumerate(docs) ]
		return res  #docker run -d --restart=always --name dsk17095 -v /data/dct:/dct -p 7095:7095 wrask/gec:dsk8 java -Xmx4096m -jar pigai_engine8.jar --database-no-encrypt --server-addr dsk.wrask.com --server-port 7095  --database-type sqlite --sqlite-file dct/sqlite/pigai_spss.sqlite3 --thread-num 2 --gec-snts-address http://wrask.com:33000/gec/essay_or_snts
	except Exception as ex: 
		print(">>todsk Ex:", ex, "\t|", arr )
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)

def polish_func(doc, dsk, idx): 
	''' '''
	lookup	= {"overcome difficulty/dobj_VERB_NOUN": {"conquer difficulty":1, 'short_msg': 'conquer, surmount'}}
	mkf		= dsk['snt'][idx] 
	for t in doc: 
		term = f"{t.head.lemma_} {t.lemma_}/{t.dep_}_{t.head.pos_}_{t.pos_}"
		if term in lookup: 
			mkf['feedback'].update({ f"{term}@r_polish:{t.i}": dict(lookup[term], **{"ibeg":t.i}) } )

if __name__ == '__main__':
	print (wrapper())
	#res = todsk(polish_f = polish_func, debug=True)
	#{'feedback': 'overcome difficulty/dobj_VERB_NOUN@r_polish:3': {'conquer difficulty': 1, 'short_msg': 'conquer, surmount', 'ibeg': 3}}, 'meta': {'pid': 0, 'ske': ['n_v_n'], 'para_id': 0, 'sid': 0, 'tc': 5, 'sub_cnt': 1, 'pos_rewrite': '[^/^, I/PRP, overcame/VBD, the/DT, difficulties/NNS, ./.]', 'pred_lemma': 'overcome', 'postag': '^_^_^ I_prp_prp_no_n_sb_I overcame_vbd_pastten_v_overcome the_dt_n2_the difficulties_nns_n_difficulty ._._.', 'snt': 'I overcame the difficulties.', 'lex_list': 'I overcame the difficulties .', 'vpat': ['overcome _n'], 'tense': ''}}
	#print ( res['snt'][0] ) 
	#print ( res['info']['tim'])

# cp __init__.py /home/ubuntu/.local/lib/python3.8/site-packages/dsk

'''
def localgec_todsk(essay_or_snts:str="She has ready. It are ok.", device:int=-1, asdsk:bool=True, dskhost:str='172.17.0.1:7095', debug:bool=False): 
	import pipe #pip install torch transformers| cp model
	return todsk(essay_or_snts, asdsk=asdsk, dskhost=dskhost, debug=debug, gec_func = lambda snts: pipe.gecsnts(snts, device=device))
'''