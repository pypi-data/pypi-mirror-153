# 22-6-5, cp from dsk/uvirun.py 
import json,os,uvicorn,time,sys, fastapi,requests,traceback,redis
import dsk,pipe
app	= fastapi.FastAPI() 

@app.post('/redis/getgecs')
def getgecs(snts:list=["She has ready.","It are ok."],timeout:int=5): 
	''' snts -> gecs, 2022.6.5 '''
	if not snts : return {}
	id  = redis.r.xadd("xsnts", {"snts":json.dumps(snts)})
	res	= redis.r.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout)
	return {} if res is None else json.loads(res[1])

@app.get('/')
def home(): return fastapi.responses.HTMLResponse(content=f"<h2>gec 8180</h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br> 2022.6.5")

@app.post('/gecv1/local')
def local_gecv1(snts:list=["She has ready.","It are ok."], max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
	''' gecv1 local version '''
	return pipe.gecsnts(snts, max_length=max_length,do_sample=do_sample, batch_size =batch_size, unchanged_ratio=unchanged_ratio, len_ratio = len_ratio, model =model, device=device)

@app.post('/redis/dsk')
def redis_dsk(arr:dict={'essay_or_snts':"She has ready. It are ok."} ):
	''' '''
	return dsk.essay_to_dsk(arr)

@app.get('/dsk/webgec')
def todsk_wrapper(essay_or_snts:str="She has ready. It are ok.", asdsk:bool=True, dskhost:str='gpu120.wrask.com:7095' , gechost:str='gpu120.wrask.com:8180'  , debug:bool= False):
	''' gechost and dskhost'''
	return dsk.todsk(essay_or_snts, asdsk=asdsk, dskhost=dskhost, gec_func = lambda snts: requests.post(f"http://{gechost}/redis/getgecs", json=snts).json () )

@app.get('/dsk/localgec')
def todsk_local(essay_or_snts:str="She has ready. It are ok.", asdsk:bool=True, dskhost:str='172.17.0.1:7095',max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
	''' localgec + dskhost '''
	return dsk.todsk(essay_or_snts, asdsk=asdsk, dskhost=dskhost, gec_func = lambda snts: pipe.gecsnts(snts,max_length, do_sample, batch_size, unchanged_ratio, len_ratio, model, device) )

@app.get('/essay/sntbr')
def nlp_sntbr(text:str="The quick fox jumped over the lazy dog. Justice delayed is justice denied.", trim:bool=True, with_pid:bool=False, with_offset:bool=False):
	''' '''
	import en 	#return spacy.sntpidoff(text) if with_offset else spacy.sntpid(text) if with_pid else spacy.snts(text, trim) 
	return en.sntbr(text, trim, with_pid) 

def run(wwwport, host:str="172.17.0.1", port:int=6311, db:int=0): # redis 6379 + spacy311  => 6311
	''' python3 -m pipe.redisgec8180 8180 '''
	redis.r = redis.Redis(host=host,port=port, decode_responses=True)
	uvicorn.run(app, host='0.0.0.0', port=wwwport)

if __name__ == '__main__': 
	import fire
	fire.Fire(run)	