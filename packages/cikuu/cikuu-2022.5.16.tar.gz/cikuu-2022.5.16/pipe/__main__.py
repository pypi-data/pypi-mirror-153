# 2022.6.3  python -m pipe uvirun 7085       http://{gechost}:7085/gecv1,  json=snts =>  sntdic 
import json, pipe

def uvirun(port): 
	''' python -m pipe uvirun 7085 '''
	import fastapi,uvicorn
	app	= fastapi.FastAPI()

	@app.post('/gecv1')
	def gecv1(snts:list=["She has ready.","It are ok."] , local:bool= False, local_as_backoff:bool=True
			, xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5
			, max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
		''' main gec api, 1. redis_gec  2. when failed , call local_gec, 2022.6.3 '''
		return pipe.getgecs_with_backoff(snts, local, local_as_backoff
			, xname, host, port, db, timeout
			, max_length,  do_sample, batch_size, unchanged_ratio, len_ratio, model, device)

	@app.get('/')
	def home():  return fastapi.responses.HTMLResponse(content=f"<h2> gecsnts,  1. redis_gec  2. when failed, local_gec as the backoff  </h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>last update: 2022.6.3")

	@app.get('/redis/test_gecv1')
	def redis_gecv1(snts:str="She has ready.|It are ok.", xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5):
		''' testing only, used by the health monitor '''
		return pipe.redis_getgecs(snts.split("|"), xname = xname, host=host, port=port, db=db, timeout=timeout)

	@app.get('/local/test_gecv1')
	def local_gecv1(snts:str="She has ready.|It are ok.", max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
		''' testing only, used by the health monitor '''
		return pipe.gecsnts(snts.split("|"), max_length=max_length,do_sample=do_sample, batch_size =batch_size, unchanged_ratio=unchanged_ratio, len_ratio = len_ratio, model =model, device=device)

	uvicorn.run(app, host='0.0.0.0', port=port)

def testredis(snts:list=["She has ready.","It are ok."], xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5):
	''' test redis gec '''
	import time
	start = time.time()
	res = pipe.redis_getgecs(snts, xname, host, port, db, timeout)
	print (res, "\ttiming:", time.time() - start) 

if __name__ == '__main__':  #{'She has ready.': 'She is ready.', 'It are ok.': 'It is ok.'}
	import fire
	fire.Fire({"uvirun":uvirun, 
	"testredis":	testredis, 
	'getgecs8180':	lambda : print(pipe.getgecs() ), 
	'remoteredis':	lambda: print(pipe.redis_getgecs(host='gpu120.wrask.com')),  
	'testlocal':	lambda: print(pipe.gecsnts())})