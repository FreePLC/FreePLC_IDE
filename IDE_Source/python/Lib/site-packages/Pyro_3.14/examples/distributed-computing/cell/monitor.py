from Pyro.EventService.Clients import Subscriber

import os

#
# The monitor application that shows a table of running
# tasks and the progress of each task.
#
class CellSubscriber(Subscriber):
    def __init__(self):
        Subscriber.__init__(self)
        self.subscribeMatch(r'^Distributed\.cell\..*$')    
        self.tasks={}
        self.counter=0
    def event(self, event):
        task=event.subject.split("Distributed.cell.")[1]
        if event.msg=="START":
            self.tasks[task]=0.0
        elif event.msg=="FINISHED":
            self.tasks[task]=1.0
        else:
            self.tasks[task]=event.msg
        self.counter+=1
        self.screen()
        
    def screen(self):
        if os.name=='nt' or 'win' in os.name:
            os.system("cls")
        else:
            os.system("clear")
        print "------Distributed Computing Monitor is listening (%d)-------" % self.counter
        print "TASK                 PROGRESS"
        for task,progress in self.tasks.items():
            if progress>=1.0:
                progressstr="[done]"
            else:
                progressstr="[%s]" % (('*'*int(progress*30.0+0.5)).ljust(30))
            print task.ljust(20), progressstr


sub = CellSubscriber()
sub.screen()
sub.listen()
