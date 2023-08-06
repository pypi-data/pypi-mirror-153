# 22-6-5, port to be: 8180  | # 22-4-7  engine worker on every cvm   
import json,os,uvicorn,time,sys, fastapi,requests,traceback
import dsk,pipe
app	= fastapi.FastAPI() 

@app.get('/')
def home(): return fastapi.responses.HTMLResponse(content=f"<h2>dsk engine worker in each cvm, wrapper of dsk-7095</h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br> 2022.6.5")

@app.get('/dsk/webgec')
def todsk_wrapper(essay_or_snts:str="She has ready. It are ok.", asdsk:bool=True, dskhost:str='172.17.0.1:7095' , gechost:str='cpu76.wrask.com:8180'  , debug:bool= False):
	''' gechost and dskhost'''
	return dsk.todsk(essay_or_snts, asdsk=asdsk, dskhost=dskhost, gec_func = lambda snts: requests.post(f"http://{gechost}/redis/getgecs", json=snts).json () )

@app.get('/dsk/localgec')
def todsk_local(essay_or_snts:str="She has ready. It are ok.", asdsk:bool=True, dskhost:str='172.17.0.1:7095',max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
	''' localgec + dskhost '''
	return dsk.todsk(essay_or_snts, asdsk=asdsk, dskhost=dskhost, gec_func = lambda snts: pipe.gecsnts(snts,max_length, do_sample, batch_size, unchanged_ratio, len_ratio, model, device) )

@app.post('/gecv1/local')
def local_gecv1(snts:list=["She has ready.","It are ok."], max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
	''' gecv1 local version '''
	return pipe.gecsnts(snts, max_length=max_length,do_sample=do_sample, batch_size =batch_size, unchanged_ratio=unchanged_ratio, len_ratio = len_ratio, model =model, device=device)

def run(port):
	''' python3 -m dsk.uvirun 8180 '''
	uvicorn.run(app, host='0.0.0.0', port=port)

if __name__ == '__main__': 
	import fire
	fire.Fire(run)	

'''
@app.get('/dsk/redisgec')
def redisgec(essay_or_snts:str="She has ready. It are ok.", asdsk:bool=True, dskhost:str='172.17.0.1:7095', xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5):
	import redis
	if not hasattr(redisgec, 'r'): 
		redisgec.r	= redis.Redis(host=host,port=port, db=db, decode_responses=True)
		redisgec.bs = redis.Redis(host=host,port=port, db=db, decode_responses=False)
	return dsk.todsk(essay_or_snts, asdsk=asdsk, dskhost=dskhost, redis_r = redisgec.r, redis_bs = redisgec.bs, 
		gec_func = lambda snts: pipe.redis_getgecs(snts, xname, host, port,db,timeout) )

@app.get('/dsk/gec_with_backoff')
def todsk_getgecs_with_backoff(essay_or_snts:str="She has ready. It are ok.", asdsk:bool=True, dskhost:str='172.17.0.1:7095', local:bool= False, local_as_backoff:bool=True
			, xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5
			, max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
	return dsk.todsk(essay_or_snts, asdsk=asdsk, dskhost=dskhost, gec_func = lambda snts: pipe.getgecs_with_backoff(snts, False, True, xname, host, port,db,timeout,max_length, do_sample, batch_size, unchanged_ratio, len_ratio, model, device) )	

@app.get('/essay/sntbr')
def nlp_sntbr(text:str="The quick fox jumped over the lazy dog. Justice delayed is justice denied.", trim:bool=True, with_pid:bool=False, with_offset:bool=False):
	import en 	#return spacy.sntpidoff(text) if with_offset else spacy.sntpid(text) if with_pid else spacy.snts(text, trim) 
	return en.sntbr(text, trim, with_pid) 
'''