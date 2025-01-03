import heapq

def file_to_dict(path : str)-> dict:
    freq:dict = {}
    with open(path) as f:
        while True:
            c = f.read(1)
            if not c:
                print("end of file")
                break
            # add 1 to corresponding
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1
    return freq


def dic_to_heap(freq:dict)->list:
    heap = []
    for char in freq:
        heapq.heappush(heap, (freq[char], char))
    return heap


