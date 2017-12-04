from copy import deepcopy

class job:
    def __init__(self,id,a,d):
        self.id = id
        self.ar = a
        self.dur = d
        self.rem = d
        self.end_time =0
        self.complete = False
        self.rt = 0
        self.ta = 0
        self.wt = 0
        self.started = False
        self.st = 0

    def dec(self):
        if self.rem > 0:
            self.rem -=1

    def end(self, timer):
        self.end_time = timer

    def __str__(self):
        return("id: %s\narrival: %s\nduration: %s\nremainder: %s\nstart time: %s\nend time: %s\nresponse: %s\nturn around: %s\nwait: %s\n"%(self.id, self.ar,self.dur,self.rem,self.st,self.end_time,self.rt, self.ta,self.wt))


class scheduling:
    def __init__(self, tups):
        self.jobs = [job(*x) for x in tups]
        self.sjf_table = []
        self.fcfs_table = []
        self.srf_table = []
        self.rr_table = []


    def fcfs_t(self):
        self.process_print_log(self.fcfs_table,"First Come First Serve")
    def sjf_t(self):
        self.process_print_log(self.sjf_table,"Shortest Job First")
    def srf_t(self):
        self.process_print_log(self.srf_table, "Shortest Remaining Time First")
    def rr_t(self):
        self.process_print_log(self.rr_table, "Round Robin")

    @staticmethod
    def process_print_log(table, name):
        header = [("Response", "Wait", "Turn Around")]
        fcfs_log = ""
        special = ""
        count = 0
        for x in header + table:

            job_log = ""
            for y in x:
                job = str(y).ljust(20)
                job_log+=job
                if count == 0:
                    special = job_log

            if count == len(table):
                fcfs_log+="\nTOTALS\n" + special + "\n"
            fcfs_log+=job_log+"\n"
            count+=1

        print(name)
        print(fcfs_log)


    def sjf(self):

        sjobs = deepcopy(self.jobs)
        complete = 0
        time = 0
        while complete < len(sjobs):
            ready = []
            job_ready = False
            for job in sjobs:
                if job.ar <= time and not job.complete:
                    ready.append(job)
                    job_ready = True
            if job_ready:
                small = min(ready, key=lambda x: x.dur)
                while small.rem > 0:
                    small.dec()
                    time += 1
                if small.rem == 0:
                    small.complete = True
                    small.end_time = time
                    small.rt = small.end_time - small.ar - small.dur
                    small.wt = small.end_time - small.ar - small.dur
                    small.ta = small.wt + small.dur
                    complete += 1
            else:
                time += 1
        tt = [x.ta for x in sjobs]
        wt = [x.wt for x in sjobs]
        rt = [x.rt for x in sjobs]
        self.sjf_table = list(zip(rt,wt,tt))
        n= len(sjobs)
        ar= sum(rt)/n
        aw = sum(wt)/n
        at = sum(tt)/n
        self.sjf_table.append((ar, aw, at))
        return ar, aw, at

    def fcfs(self):
        time = 0
        sjobs = deepcopy(self.jobs)
        for curr in sjobs:
            while not curr.complete:
                if curr.ar <= time:
                    if not curr.complete:
                        curr.dec()
                        time+=1
                        if curr.rem == 0:
                            curr.end_time = time
                            curr.ta = curr.end_time - curr.ar
                            curr.wt = curr.ta - curr.dur
                            curr.rt = curr.end_time - (curr.dur +curr.ar)
                            curr.complete = True
                else:
                    time+=1

        tt = [x.ta for x in sjobs]
        wt = [x.wt for x in sjobs]
        rt = [x.rt for x in sjobs]

        self.fcfs_table = list(zip(rt,wt,tt))

        n= len(sjobs)
        ar= sum(rt)/n
        aw = sum(wt)/n
        at = sum(tt)/n

        self.fcfs_table.append((ar,aw,at))

        return ar, aw, at

    def srf(self):
        time = 0
        complete = 0
        sjobs = deepcopy(self.jobs)
        while complete < len(sjobs):
            ready = []
            check = False
            for job in sjobs:
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
                    complete += 1
                    small.end_time = time + 1
                    small.complete = True

            time += 1
        for job in sjobs:
            if job.complete:
                job.wt = job.end_time - job.ar - job.dur
                job.ta = job.end_time - job.ar
                job.rt = (job.st - job.ar)
        tt = [x.ta for x in sjobs]
        wt = [x.wt for x in sjobs]
        rt = [x.rt for x in sjobs]

        self.srf_table = list(zip(rt,wt,tt))
        n= len(self.jobs)
        ar= sum(rt)/n
        aw = sum(wt)/n
        at = sum(tt)/n
        self.srf_table.append((ar,aw,at))

        return ar,aw,at

    def rr(self):
        wait = 0
        complete = 0
        time = 0
        ready = []
        q = 100
        sjobs = deepcopy(self.jobs)
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
                    if job.complete:
                        pass
                    elif job.rem > q and not job.complete:
                        time += q
                        job.rem -= q
                        # print(time, job.id, job.rt, job.wt)

                    else:
                        if not job.complete:
                            time += job.rem
                            job.ta = time - job.ar
                            job.wt = job.ta - job.dur
                            job.rt = job.st - job.ar
                            if job.rt < 0:
                                job.rt = 0
                            # print('wt:%s' %(job.wt))
                            job.end_time = time
                            job.rem = 0
                            job.complete = True
                            ready.remove(job)
                            complete += 1
                            # print(time, job.id, job.rt, job.wt)

        tt = [x.ta for x in sjobs]
        wt = [x.wt for x in sjobs]
        rt = [x.rt for x in sjobs]

        self.rr_table = list(zip(rt,wt,tt))
        n= len(self.jobs)
        ar= sum(rt)/n
        aw = sum(wt)/n
        at = sum(tt)/n
        self.rr_table.append((ar,aw,at))

        return ar, aw, at


def getnums():
    with open('list.txt', 'r+') as file:
        a = []
        b = []
        c=[]
        all_tups = []
        counter = 0
        for z in file:
            counter +=1
            x, y = z.split()
            a.append(int(x))
            b.append(int(y))
            c.append(counter)
        tups = zip(c,a,b)
        for x in tups:
            all_tups.append(x)
    return all_tups

def print_total(table):
    header = [("Response", "Wait", "Turn Around")]
    fcfs_log = ""
    for x in header + [table]:
        job_log = ""
        for y in x:
            job = str(y).ljust(20)
            job_log+=job
        fcfs_log+=job_log+"\n"
    print(fcfs_log)


def main():
    tups = getnums()
    sch = scheduling(tups)
    sjf = sch.sjf()
    fcfs = sch.fcfs()
    srf = sch.srf()
    rr = sch.rr()
    print("First Come First Serve:")
    print_total(fcfs)
    sch.fcfs_t()
    print("Shortest Job First")
    print_total(sjf)
    sch.sjf_t()
    print("Shortest Remaining Time First")
    print_total(srf)
    sch.srf_t()

    print("Round Robin")
    print_total(rr)
    sch.rr_t()




if __name__ == "__main__":
    main()