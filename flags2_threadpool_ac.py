import tqdm
import requests
import collections # collections.Counter() 
from concurrent import futures

from flags2_common import main,HTTPStatus
from flags2_sequential import download_one

DEFAULT_CONCUR_REQ = 30
MAX_CONREQ = 1000

def download_many(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    to_do_map = {}
    with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:
        for cc in cc_list:
            future = executor.submit(download_one, 
                        cc, base_url, verbose)
            to_do_map[future] = cc
        done_iter = futures.as_completed(to_do_map)
        if not verbose:
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list))
        for future in done_iter:
            try:
                res = future.result() 
            except requests.exceptions.HTTPError as exc:
                error_msg = 'HTTP {exc_res.status_code} - {exc_res.reason}'
                error_msg = error_msg.format(exc_res=exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status # res, result namedtuple: Result(status, cc)
            if error_msg:
                status = HTTPStatus.error
            counter[status] += 1
            if verbose and error_msg:
                cc = to_do_map[future] # provide context for error msg
                print('*** Error for {}: {}'.format(cc, error_msg))
            
    return counter

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONREQ)
