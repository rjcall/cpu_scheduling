from rsjf import getnums, job

def sjf(jobs):
    time = 0
    complete = 0

    while complete < len(jobs):
        ready = []
        check = False
        for job in jobs:
            if job.ar <= time and not job.complete:
                ready.append(job)
                check = True
        if check:
            small = min(ready, key=lambda x: x.rem)
            if small.started == False:
                small.st = time
                small.started = True

            small.dec()
            if small.rem == 0:
                complete +=1
                small.end_time = time +1
                small.complete = True

        time+=1
    for job in jobs:
        if job.complete:
            job.wt = job.end_time - job.ar - job.dur
            job.ta = job.end_time - job.ar
            job.rt = (job.st - job.ar)
    avwt = sum([x.wt for x in jobs])/len(jobs)
    avtt = sum([x.ta for x in jobs]) / len(jobs)
    avrt = sum([x.rt for x in jobs]) / len(jobs)

    return avrt, avtt, avwt


tups = getnums()
jobs = [job(*x) for x in tups]
sjf(jobs)
for job in jobs:
    print(job)
