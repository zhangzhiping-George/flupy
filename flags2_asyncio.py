'''
save_flag is NOT asyncIO process,
flags3_asyncio.py make save_flag work with run_in_executor
as asyncio saving
'''
import asyncio
import collections 

import aiohttp
from aiohttp import web
import tqdm

from flags2_common import main, Result, HTTPStatus, save_flag#, BASE_URL

# coroutine with threads num controlling
# add error handling: where to handle

DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

class FetchError(Exception):
    def __init__(self, cc):
        self.cc = cc

@asyncio.coroutine
def get_flag(cc, base_url):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = yield from aiohttp.ClientSession().get(url)
    #resp = yield from aiohttp.request('GET', url)
    if resp.status == 200:
        image = yield from resp.read()
        return image
    elif resp.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.HttpProcessingError(
        code=resp.status,message=resp.reason,
        headers=reps.headers)

@asyncio.coroutine
def download_one(cc, base_url, verbose, concur_req):
    try:
        with (yield from asyncio.Semaphore(value=concur_req)):
            image = yield from get_flag(cc, base_url)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
    except Exception as exc: 
        raise FetchError(cc) from exc
    else:
        save_flag(image, cc.lower()+'.gif')
        status = HTTPStatus.ok
        msg = 'ok'
    if verbose and msg:
        print(cc, msg)
    return Result(status, cc)

@asyncio.coroutine
def downloader_cor(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    to_do_iter = [download_one(cc, base_url, verbose, concur_req) for cc in cc_list]
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
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__
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
