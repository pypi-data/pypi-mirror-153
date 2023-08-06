from os import times
from sys import getswitchinterval, exit


from jsonrpcserver import async_dispatch
import json
import asyncio
import websockets
import hashlib
import aiohttp
import traceback
from aiohttp import web

from gear.utils.compat import meter_log_convert_to_eth_log
from .rpc import make_version
from json.decoder import JSONDecodeError
from .meter.account import (
    solo,
    keystore as _keystore,
)
import logging, logging.config
from .log import  LOGGING_CONFIG

from .utils.types import (

    encode_number
)
from .meter.client import meter
import requests
import click
from datetime import datetime


res_headers = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Connection": "keep-alive",
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger('gear' )

SUB_ID = '0x00640404976e52864c3cfd120e5cc28aac3f644748ee6e8be185fb780cdfd827'
async def checkHealth(request, logging=False, debug=False):
    r = {"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":8545}
    response = await async_dispatch(json.dumps(r), basic_logging=logging, debug=debug)
    return web.json_response(response.deserialized(), headers=res_headers, status=response.http_status)

async def handle(request, logging=False, debug=False):
    jreq = await request.json()
    reqStr = json.dumps(jreq)
    arrayNeeded = True
    if not isinstance(jreq, list):
        jreq = [jreq]
        arrayNeeded = False

    responses = []
    method = jreq[0]['method'] if jreq and len(jreq)>=1 else 'unknown'
    id = jreq[0]['id'] if jreq and len(jreq)>=1 else 'unknown'
    logger.info("http req #%s: %s", id, reqStr)
    for r in jreq:
        # request = await request.text()
        response = await async_dispatch(json.dumps(r), basic_logging=logging, debug=debug)
        if response.wanted:
            # logger.info("Response #%s:"%(str(r['id'])), json.dumps(response.deserialized()))
            logger.info("http res #%s: DONE", str(r['id']))
            responses.append(json.loads(json.dumps(response.deserialized())))
        if response.http_status != 200:
            logger.error("http res #%s: %s %s", str(r['id']), str(response.http_status),json.dumps(response.deserialized()))


    if len(responses):
        if arrayNeeded:
            return web.json_response(responses, headers=res_headers, status=response.http_status)
        else:
            return web.json_response(responses[0], headers=res_headers, status=response.http_status)
    else:
        return web.Response(headers=res_headers, content_type="text/plain")









async def handleRequest(request, logging=False, debug=False):
   
    jreq = request
    
    reqStr = json.dumps(jreq)
    arrayNeeded = True
    if not isinstance(jreq, list):
        jreq = [jreq]
        arrayNeeded = False

    responses = []
    id = jreq[0]['id'] if jreq and len(jreq)>=1 else 'unknown'
    logger.info("ws req #%s: %s", id, reqStr)
    for r in jreq:
        method = r['method']
        # request = await request.text()
        response = await async_dispatch(json.dumps(r), basic_logging=logging, debug=debug)
        if response.wanted:
            if method in ['eth_getBlockByNumber', 'eth_call']:
                logger.info("ws res #%s: DONE", str(r['id']))
            else:
                logger.info("ws res #%s: %s", str(r['id']), json.dumps(response.deserialized()))
            responses.append(json.loads(json.dumps(response.deserialized())))
            

    if len(responses):
        if arrayNeeded:
            return web.json_response(responses, headers=res_headers, status=response.http_status).text
           
            
        else:
            return web.json_response(responses[0], headers=res_headers, status=response.http_status,
             content_type='application/json', dumps=json.dumps
            ).text
           
    else:
        
        return web.Response(headers=res_headers, content_type="text/plain").text


BLOCK_FORMATTERS = {
   
   
    "timestamp": encode_number,
    "gasLimit": encode_number,
    "gasUsed": encode_number,
    "epoch":encode_number,
    "k":encode_number
    
}



def meter_block_convert_to_eth_block(block):
    # sha3Uncles, logsBloom, difficaulty, extraData are the required fields. nonce is optional
    if not ('nonce' in block):
        block['nonce'] = 0
    n = block["nonce"]
    if n == 0:
        block["nonce"] = '0x0000000000000000'
    else:
        block["nonce"] = encode_number(n, 8)
    if not ('mixHash' in block):
        block['mixHash'] = '0x0000000000000000000000000000000000000000000000000000000000000000'

    # sha3Uncles is always empty on meter
    block['sha3Uncles'] = '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347'
    if not ('transactions' in block):
        block['transactions'] = []
    # TODO: fix "fake" transactions root
    if len(block['transactions']) ==0:
        block['transactionsRoot'] = '0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421'
    #block['logsBloom'] = '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    block['difficulty'] = '0x0'
    block['extraData'] = '0x'
    # block['baseFeePerGas'] = '0x0'
    if 'kblockData' in block:
        del block['kblockData']
    if 'powBlocks' in block:
        del block['powBlocks']
    if 'committee' in block:
        del block['committee']
    if 'qc' in block:
        del block['qc']
    for key, value in block.items():
        if key in BLOCK_FORMATTERS:
           block[key] =  encode_number(value).decode()
    return block

    

newHeadListeners = {} # ws connection id -> ws connection
logListeners = {} # ws connection id -> { ws: ws connection, filters: filters }
# WSURL_NHEADS = 'ws://127.0.0.1:8669/subscriptions/beat'

def hash_digest(param):
    h = hashlib.sha224(param.encode())
    digest = h.hexdigest()
    return digest

async def run_new_head_observer(endpoint):
    ws_endpoint = endpoint.replace('https', 'ws').replace('http','ws')+'/subscriptions/beat'
    while True:
        try:
            async with websockets.connect(ws_endpoint) as beatWS:
                async for msg in beatWS:
                    for key in list(newHeadListeners.keys()):
                        ws = newHeadListeners[key]
                        r = json.loads(msg)
                        if r.get("number"):
                            num = int(r.get("number"), 16)
                            logger.info("forward block %d to ws %s",num,key)
                        else:
                            logger.info('forward to ws %s', key)
                        blk = meter_block_convert_to_eth_block(r)
                        try:
                            out = json.dumps({"jsonrpc": "2.0", "method":"eth_subscription" ,"params":{"subscription":SUB_ID, "result":blk}})
                            logger.info('res: %s', out)
                            await ws.send_str(out)
                        except Exception as e:
                            del newHeadListeners[key]
                            logger.error('error happend for client ws %s, ignored: %s', key, e)
        except Exception as e:
            logger.error('error happened in head observer: %s', e)
            logger.error('retry in 10 seconds')
            await asyncio.sleep(10)

def match_filter(log, filters):
    for filter in filters:
        addressMatch = True
        topicsMatch = True
        if 'address' in filter:
            address = filter['address'].lower()
            if address != log['address'].lower():
                addressMatch = False
    
        if 'topics' in filter and isinstance(filter['topics'], list) and len(filter['topics'])>0:
            topics = filter['topics']
            for index, topic in enumerate(topics):
                if len(log['topics']) < index+1 or topic and topic != log['topics'][index]:
                    topicsMatch = False
                    break
        if addressMatch and topicsMatch:
            return True
    return False
        

async def run_event_observer(endpoint):
    ws_endpoint = endpoint.replace('https', 'ws').replace('http','ws')+'/subscriptions/event'
    while True:
        try:
            async with websockets.connect(ws_endpoint) as eventWS:
                async for msg in eventWS:
                    for key in list(logListeners.keys()):
                        info = logListeners[key]
                        ws = info['ws']
                        filters = info['filters']
                        log = json.loads(msg)
                        if not match_filter(log, filters):
                            logger.info('not match filter, skip now for key %s', key)
                            continue
                        result = meter_log_convert_to_eth_log(log)
                        result['logIndex'] = result['logIndex'].decode('utf-8')
                        result['transactionIndex'] = result['transactionIndex'].decode('utf-8')
                        result['blockNumber'] = result['blockNumber'].decode('utf-8')
                        try:
                            out = json.dumps({"jsonrpc": "2.0", "method":"eth_subscription" ,"params":{"subscription":SUB_ID, "result":result}})
                            await ws.send_str(out)
                        except Exception as e:
                            del logListeners[key]
                            logger.error('error happend: %s for client ws: %s ', e, key)
        except Exception as e:
            logger.error('error happend in event observer: %s', e)
            logger.error('log: %s', log)
            logger.error('filters: %s', filters)
            logger.error('retry in 10 seconds')
            await asyncio.sleep(10)

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    key = request.headers.get("sec-websocket-key", "")
    async for msg in ws:
        # logger.info('ws req: %s', msg)
        if msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())
            await ws.close(code=ws.close_code, message=msg.extra)
            if key in newHeadListeners:
                del newHeadListeners[key]
            return
        elif msg.type == aiohttp.WSMsgType.TEXT and msg.data.strip():
            if msg.data == 'close':
                print('close message received, close right now')
                await ws.close()
                return
            # if is a valid json request
            jreq = json.loads(msg.data)

            # handle batch requests
            if isinstance(jreq, list):
                ress = []
                for r in jreq:
                    res = await handleRequest(r, False, False)
                    ress.append(json.loads(res))
                await ws.send_str(json.dumps(ress))
                continue

            if 'method' not in jreq or 'id' not in jreq:
                # not a valid json request
                continue
            
            id = jreq['id']

            if jreq['method'] == "eth_subscribe":
                # handle subscribe
                if isinstance(jreq['params'], list):
                    params = jreq['params']
                    if params[0] == 'newHeads':
                        # if key in newHeadListeners:
                        # continue
                        newHeadListeners[key] = ws
                        logger.info("SUBSCRIBE to newHead: %s", key)
                        #send a subscription id to the client
                        await ws.send_str(json.dumps({"jsonrpc": "2.0" ,"result":SUB_ID, "id":id}))
                    
                    if params[0] == 'logs':
                        # if key in logListeners:
                        # continue
                        digest = hash_digest(str(params[1:]))
                        newkey = key+'-'+digest
                        logListeners[key+"-"+digest] = {"ws":ws, "filters":params[1:]}
                        logger.info("SUBSCRIBE to logs: %s, filter: %s",newkey, params[1:])
                        await ws.send_str(json.dumps({"jsonrpc": "2.0" ,"result":SUB_ID, "id":id}))

                #begin subscription
                # while True:
                
                #     res = await handleRequest( json.loads(msg.data), False, False)
                #     copy_obj = copy.deepcopy(json.loads(res))
                #     # convert the subscription object into an appropriate response
                #     result = meter_block_convert_to_eth_block(copy_obj['result'])
                    
                #     res_obj = {"jsonrpc": copy_obj["jsonrpc"] , "method":"eth_subscription", "params":{"result":result, "subscription":SUB_ID}}
                #     await ws.send_str(json.dumps(res_obj))
            elif (jreq['method'] == "eth_unsubscribe"):
                # handle unsubscribe
                await ws.send_str(json.dumps({"jsonrpc": "2.0" ,"result":True, "id":id}))
                if key in newHeadListeners:
                    del newHeadListeners[key]
                if key in logListeners:
                    del logListeners[key]
                logger.info("UNSUBSCRIBE: %s", key)
                await ws.close()
                return
            else:
                # handle normal requests
                res = await handleRequest(json.loads(msg.data), False, False)
                logger.info("forward response to ws %s",key)
                await ws.send_str(res)
                # await ws.send_str(json.dumps({"jsonrpc":"2.0", "result":json.loads(res), "id":count}))
            
        elif msg.type == aiohttp.WSMsgType.BINARY:
            await ws.send_str(msg.data)
            
        else:
            logger.warning("Unknown REQ: %s", msg)
            pass
            # await ws.send_str(json.dumps({"jsonrpc": "2.0" ,"result":"", "id":count}))
    
    print('websocket connection closed: ', key)
    return ws
           

def get_http_app(host, port, endpoint, keystore, passcode, log, debug, chainid):
    try:
        response = requests.options(endpoint)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        logger.error("Unable to connect to Meter-Restful server.")
        return

    meter.set_endpoint(endpoint)
    meter.set_chainid(chainid)
    if keystore == "":
        meter.set_accounts(solo())
    else:
        meter.set_accounts(_keystore(keystore, passcode))

    app = web.Application()
    
    # app.router.add_get("/",lambda r:  websocket_handler(r))
    app.router.add_get("/", lambda r: web.Response(headers=res_headers))
    app.router.add_post("/", lambda r: handle(r, log, debug))
    app.router.add_options("/", lambda r: web.Response(headers=res_headers))
    app.router.add_get(
        "/health", lambda r: checkHealth(r,log,debug))
    # web.run_app(app, host=host, port=port)
    return app


def get_ws_app(host, port, endpoint, keystore, passcode, log, debug, chainid):
    try:
        response = requests.options(endpoint)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        logger.error("Unable to connect to Meter-Restful server.")
        return

    meter.set_endpoint(endpoint)
    meter.set_chainid(chainid)
    if keystore == "":
        meter.set_accounts(solo())
    else:
        meter.set_accounts(_keystore(keystore, passcode))

    app = web.Application()
    
    app.router.add_get("/",lambda r:  websocket_handler(r))
    # app.router.add_get("/", lambda r: web.Response(headers=res_headers))
    # app.router.add_post("/", lambda r: handle(r, log, debug))
    app.router.add_options("/", lambda r: web.Response(headers=res_headers))
    app.router.add_get(
        "/health", lambda r: web.Response(headers=res_headers, body="OK", content_type="text/plain"))
    # web.run_app(app, host=host, port=port)
    return app


async def run_server(host, port, endpoint, keystore, passcode, log, debug, chainid):
    http_app = get_http_app(host, port, endpoint, keystore, passcode, log, debug, chainid)

    if http_app == None:
        logger.error("Could not start http server due to connection problem, check your --endpoint settings")
        exit(-1)
    http_runner = web.AppRunner(http_app)
    await http_runner.setup()
    http = web.TCPSite(http_runner, host, port)
    await http.start()
    logger.info("HTTP server started: http://%s:%s", host, port)

    ws_app = get_ws_app(host, port, endpoint, keystore, passcode, log, debug, chainid)
    if ws_app == None:
        logger.error("Could not start http server due to connection problem, check your --endpoint settings")
        exit(-1)
    ws_runner = web.AppRunner(ws_app)
    await ws_runner.setup()
    ws = web.TCPSite(ws_runner, host, int(port)+1)
    await ws.start()
    logger.info("Websocket server started: ws://%s:%s", host, int(port)+1)

    head_observer = asyncio.create_task(run_new_head_observer(endpoint))
    event_observer = asyncio.create_task(run_event_observer(endpoint))
    await head_observer
    # while True:
        # await asyncio.sleep(3600)  # sleep forever


@click.command()
@click.option(
    "--host",
    default="0.0.0.0",
)
@click.option(
    "--port",
    default=8545,
    type=int,
)
@click.option(
    "--endpoint",
    default="http://127.0.0.1:8669",
)
@click.option(
    "--keystore",
    default="",
)
@click.option(
    "--passcode",
    default="",
)
@click.option(
    "--log",
    default=False,
    type=bool,
)
@click.option(
    "--debug",
    default=False,
    type=bool,
)
@click.option(
    "--chainid",
    default="0x53"
)
def main(host, port, endpoint, keystore, passcode, log, debug, chainid):
    chainIdHex = chainid
    if not chainid.startswith('0x'):
        chainIdHex = hex(int(chainid))

    asyncio.run(run_server(host, port, endpoint, keystore, passcode, log, debug, chainIdHex))

    

if __name__ == '__main__':
    main()