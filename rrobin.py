from rsjf import getnums, job


def check_q(jobs, done,time_inc, time, ready):
    for job in jobs:
        if job.rem > 0:
            done = False
            if job.ar <= time and not job.complete:
                time_inc = False
                if job not in ready:
                    ready.append(job)
    return ready

def waiting_time(jobs):
    time = 0
    ready = []
    complete = 0
    while complete < len(jobs):
        done = True
        q = 100
        time_inc = True


        if len(ready) > 0:
            for job in range(ready:
                if not job.started:
                    job.st = time
                    job.started = True



    avwt = sum([x.wt for x in jobs]) / len(jobs)
    avtt = sum([x.ta for x in jobs]) / len(jobs)
    avrt = sumw([x.rt for x in jobs]) / len(jobs)

    return avrt, avtt, avwt


tups = getnums()
# tups = list(zip((1,2,3),(1,2,3),(10,5,8)))



jobs = [job(*x) for x in tups]
a,b,c = waiting_time(jobs)
# print(len(jobs))
print(c)
for job in jobs:
    print(job.id,job.st, job.wt)

