from concurrent import futures

from flags import get_flag, show_flag, main

MAX_WORKERS = 20
def download_one(cc):
    get_flag(cc)
    show_flag(cc)
    return cc

'''
def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))
'''
def download_many(cc_list):
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
    #with futures.ProcessPoolExecutor() as executor:
        to_do = []
        for cc in cc_list:
            future = executor.submit(download_one, cc)
            to_do.append(future)
            print('Scheduled for {}: {!r}'.format(download_one, cc))

        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            print('{} result: {!r}'.format(future, res))
            results.append(res)
    return len(results)

if __name__ == '__main__':
    main(download_many)
