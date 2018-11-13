import asyncio
import collections 
import json

import aiohttp
from aiohttp import web
import tqdm

from flags2_common import main, Result, HTTPStatus, save_flag

# coroutine with threads num controlling
# add error handling: where to handle

DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

class FetchError(Exception):
    def __init__(self, cc):
        self.cc = cc

async def http_req(url):
    #resp = await aiohttp.request('GET', url)
    #resp = await aiohttp.ClientSession().get(url)
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url)
    if resp.status == 200:
        if resp.headers.get('Content-Type') == 'json':
            data = await resp.json()
        else:
            data = await resp.read()
        return data 
    elif resp.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.HttpProcessingError(
        code=resp.status,message=resp.reason,
        headers=reps.headers)

@asyncio.coroutine
def get_flag(cc, base_url):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    return (yield from http_req(url))

@asyncio.coroutine
def get_country(cc, base_url):
    url = '{}/{cc}/metadata.json'.format(base_url, cc=cc.lower())
    metadata = yield from http_req(url)
    metadata = json.loads(str(metadata, encoding='utf-8'))
    return metadata['country']

@asyncio.coroutine
def download_one(cc, base_url, verbose, semaphore):
    try:
        with (yield from semaphore):
            image = yield from get_flag(cc, base_url)
        with (yield from semaphore):
            country = yield from get_country(cc, base_url)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc: 
        raise FetchError(cc) from exc
    else:
        country = country.replace(' ', '_')
        filename = '{}-{}.gif'.format(country, cc.lower())
        #loop = asyncio.new_event_loop()
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, save_flag, image, filename)
        status = HTTPStatus.ok
        msg = 'ok'
    if verbose and msg:
        print(cc, msg)
    return Result(status, cc)

@asyncio.coroutine
def downloader_cor(cc_list, base_url, verbose, concur_req):
    semaphore = asyncio.Semaphore(value=concur_req)
    counter = collections.Counter()
    to_do_iter = [download_one(cc, base_url, verbose, semaphore) for cc in cc_list]
    done_iter = asyncio.as_completed(to_do_iter)
    if not verbose:
        done_iter = tqdm.tqdm(done_iter, total=len(cc_list))
    for future in done_iter:
        try:
            res = yield from future 
        except FetchError as exc:
            country_code = exc.cc
            try:
                error_msg = exc.__cause__.args[0] 
                raise
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__
                raise
            if verbose and error_msg:
                print('***Error for {}: {}'.format(country_code, error_msg))
            status = HTTPStatus.error 
        else:
            status = res.status
        counter[status] += 1
    return counter 


def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.get_event_loop()
    cor = downloader_cor(cc_list, base_url, verbose, concur_req)
    res_counts = loop.run_until_complete(cor)
    loop.close()
    return res_counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
