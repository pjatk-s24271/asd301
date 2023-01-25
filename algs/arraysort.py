import time
def arraysort(arr: list[int]):
    m = abs(min(min(arr), 0))

    r = []
    for i in range(max(arr) + m + 1): r.append([])

    for e in arr:
        r[e].append(e)
    
    rr = []

    for e in r[-m:]:
        for ee in e:
            rr.append(ee)

    for e in r[:-m]:
        for ee in e:
            rr.append(ee)
        
    return rr