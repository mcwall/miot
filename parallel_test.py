from multiprocessing import Pool

def send(code, protocol):
    print(code + protocol)

pool = Pool()
result1 = pool.apply_async(send, ["A", "1"])
result2 = pool.apply_async(send, ["B", "2"])
answer1 = result1.get(timeout=10)
answer2 = result2.get(timeout=10)

