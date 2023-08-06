# 2022.6.4
import re, json, math #torch
from transformers import pipeline #None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.

token_split	= lambda sent: re.findall(r"[\w']+|[.,!?;]", sent) # return list
def common_perc(snt="She has ready.", trans="She is ready."): 
	toks = set(token_split(snt))
	return len([t for t in token_split(trans) if t in toks]) / (len(toks)+0.01)

def gecsnts(snts:list=["She has ready.","It are ok."],  max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
	''' LOCAL version 
	batch_size needs to be used on the pipe call, not on the pipeline call. |https://github.com/huggingface/transformers/issues/14613
	return {'She has ready.': 'She is ready.'}, 'It are ok.': 'It is ok.'}	'''
	if not hasattr(gecsnts, 'pipe'): gecsnts.pipe = pipeline("text2text-generation", model=model, device=device)
	snts = [snt for snt in snts if snt.count(' ') + 10 < max_length ] # skip extra long sents 	# check the extreme long sent ?  truncate it ? 2022.4.3 
	dic = {} #{'hello world': 'Hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello', 'I am ok.': 'I am ok.'}
	sntslen = len(snts) 
	offset = 0 
	while offset < sntslen: # added 2022.4.5
		for snt, tgt in zip(snts, gecsnts.pipe(snts[offset:offset + batch_size],  max_length=max_length, do_sample=do_sample, batch_size=batch_size)):
			trans = tgt['generated_text']  # todo : if token change > 50% , skip the trans
			if not ' ' in trans or not ' ' in snt.strip(): # ' ' => "generated_text": "Then, a few years later, the saga began."
				dic[snt] = snt # keep unchanged
			elif common_perc(snt, trans) < unchanged_ratio or abs(math.log( len(snt)/len(trans))) > len_ratio:
				dic[snt] = snt # changed too much, -> discard 
			else:
				dic[snt] = trans
		offset = offset + batch_size
	return dic

def getgecs(snts:list=["She has ready.","It are ok."], gechost:str='gpu120.wrask.com:8180', rport:int=6379, timeout:int=5
	,  max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1): 
	''' 2022.6.4 '''
	import requests 
	sntdic	=  requests.post(f"http://{gechost}/redis/getgecs", params={"port":rport, "timeout":timeout}, json=snts).json () 
	if not sntdic :  # failed, backoff
		sntdic = gecsnts(snts, max_length=max_length,do_sample=do_sample, batch_size =batch_size, unchanged_ratio=unchanged_ratio, len_ratio = len_ratio, model =model, device=device)
	return sntdic 

## wrapper web api for uvicorn, NOT used 

def redis_getgecs(snts:list=["She has ready.","It are ok."], xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5): # put into the ufw white ip list 
	''' snts -> gecs '''
	import redis
	try:
		if not hasattr(redis, 'r'): redis.r = redis.Redis(host=host,port=port, db=db, decode_responses=True)
		id  = redis.r.xadd(xname, {"snts":json.dumps(snts)})
		res	= redis.r.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout)
		return {} if res is None else json.loads(res[1])
	except Exception as e:
		print ("redis_getgecs ex:", e, snts) 
		return {}

def getgecs_with_backoff(snts:list=["She has ready.","It are ok."] , local:bool= False, local_as_backoff:bool=True
			, xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5
			, max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
	''' main gec api, 1. redis_gec  2. when failed , call local_gec, 2022.6.3 '''
	if not snts: return {} 
	if local: return gecsnts(snts, max_length=max_length,do_sample=do_sample, batch_size =batch_size, unchanged_ratio=unchanged_ratio, len_ratio = len_ratio, model =model, device=device)

	sntdic = redis_getgecs(snts, xname=xname, host=host, port=port, db=db, timeout=timeout ) #
	if not sntdic and local_as_backoff:  # failed , call the local version as backoff
		sntdic = gecsnts(snts, max_length=max_length,do_sample=do_sample, batch_size =batch_size, unchanged_ratio=unchanged_ratio, len_ratio = len_ratio, model =model, device=device)
	return sntdic

if __name__ == "__main__":   #{'She has ready.': 'She is ready.', 'It are ok.': 'It is ok.'}
	print ( "local gecsnts",  gecsnts() )
	print ("http_getgecs", getgecs()  ) 