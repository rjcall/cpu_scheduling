from rsjf import getnums, job
from copy import deepcopy

def rr(jobs):
    wait = 0
    complete = 0
    time = 0
    ready = []
    q = 100
    sjobs = deepcopy(jobs)
    while complete < len(sjobs):
        r = True
        for job in sjobs:
            if not job.complete and job.ar <= time:
                if job not in ready:
                    ready.insert(0, job)
                r = False
        if r:
            time += 1
        else:
            for job in ready:
                if job.started == False:
                    job.st = time
                    job.started = True
                if job.complete:
                    pass
                elif job.rem > q and not job.complete:
                    time += q
                    job.rem -= q
                    print(time - job.rem)
                    # print(time, job.id, job.rt, job.wt)

                else:
                    if not job.complete:
                        job.end_time = time
                        time += job.rem
                        job.ta = time - job.ar
                        job.wt = job.ta - job.dur
                        job.rt = job.end_time - job.st
                        if job.rt < 0:
                            job.rt = 0
                        # print('wt:%s' %(job.wt))


                        job.rem = 0
                        job.complete = True
                        ready.remove(job)
                        complete += 1
                        # print(time, job.id, job.rt, job.wt)

    tt = [x.ta for x in sjobs]
    wt = [x.wt for x in sjobs]
    rt = [x.rt for x in sjobs]

    rr_table = list(zip(rt, wt, tt))
    n = len(jobs)
    ar = sum(rt) / n
    aw = sum(wt) / n
    at = sum(tt) / n
    rr_table.append((ar, aw, at))

    return ar, aw, at

tups = getnums()

# tups = list(zip((1,2,3),(1,2,3),(10,5,8)))



jobs = [job(*x) for x in tups]
a,b,c = rr(jobs)
print(a,b,c)
# # print(len(jobs
# for job in jobs:
#     print(job)






