import time
def test(n):
    lst = []
    print time.strftime('%H:%M:%S')
    #for i in range(10000*n):
    #    lst = lst + [i]
    #    # lst.append(i)
    lst = list(range(10000*n))
    # lst = [i for i in range(10000*n)]
    print time.strftime('%H:%M:%S')
    print lst[:30]
    # return lst 
    # return list(rannge(10000*n)
test(10)    
    

