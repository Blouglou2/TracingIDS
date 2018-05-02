#!/usr/bin/env python
# -*- coding :ascii -*-

import babeltraceReader as babelRead
from transitions import Machine
import sys
import re
import testFeatureExtraction
import itertools
import babeltrace

class synthetic_entry_exit_syscall(object):
    states = ['entry', 'exit']
    fields = {}

    def __init__(self, name):

        # Name of the syscall
        self.name = name
        # Initialize the state machine
        self.machine = Machine(model=self, states=synthetic_entry_exit_syscall.states, initial='entry')
        # Add transitions
        self.machine.add_transition('lectureExit', 'entry', 'exit')

    # def __del__(self):
    #     print("deleted")

    def addFieldsEntry(self,dictEvent):
        self.fields = dictEvent.copy()

    def addFieldsExit(self,dictEvent):
        # self.fields["ret"] = dictEvent["ret"]
        self.fields["a_nomEvent"] = self.name
        for key in dictEvent:
            if key not in self.fields:
                self.fields[key] = dictEvent[key]
        self.fields["d_timestamp"] += dictEvent["d_timestamp"]


    # TODO comment vérifier que le syscall exit correspond bien au syscall_entry? Le exit n'a pas de filename
    def eventMatch(self,dictEvent):
        if (self.fields["cpu_id"] == dictEvent["cpu_id"]) and (self.name.split("syscall_")[1] == dictEvent["a_nomEvent"].split("syscall_exit_")[1]):
            return 1
        else :
            return 0





def synthetic_EntryExit(trace_path, listeMachines):

    for event,output in babelRead.getEventsSynthetic(trace_path):

        # print(event)
        if re.search("syscall_entry",event["a_nomEvent"]):
            synteticSyscall = synthetic_entry_exit_syscall(event["a_nomEvent"].split("syscall_entry_")[1])
            synteticSyscall.addFieldsEntry(event)
            listeMachines.append(synteticSyscall)
        if re.search("syscall_exit",event["a_nomEvent"]):
            for machine in listeMachines:
                # print("\n\n------------")
                # print(machine.fields)
                # print(event)
                # print("------------\n\n")
                try:
                    if machine.eventMatch(event):
                        machine.lectureExit()
                        machine.addFieldsExit(event)
                        print("Fields de machine :")
                        print(machine.fields)
                        listeMachines.remove(machine)
                        yield machine.fields
                    else:
                        pass
                except:
                    pass
        else:
            yield event
        # print(len(listeMachines))
        # print(synteticSyscall.state)


def synthetic_EntryExitFromEvent(event,listeMachines):
    # if re.search("syscall_entry",event["a_nomEvent"]):
    if "syscall_entry" in event["a_nomEvent"]:
            synteticSyscall = synthetic_entry_exit_syscall("syscall_"+event["a_nomEvent"].split("syscall_entry_")[1])
            synteticSyscall.addFieldsEntry(event)
            listeMachines.append(synteticSyscall)
            return
    # if re.search("syscall_exit",event["a_nomEvent"]):
    if "syscall_exit" in event["a_nomEvent"]:
        for machine in listeMachines:
            # print("\n\n------------")
            # print(machine.fields)
            # print(event)
            # print("------------\n\n")
            try:
                if machine.eventMatch(event):
                    machine.lectureExit()
                    machine.addFieldsExit(event)
                    # print("Fields de machine :")
                    # print(machine.fields)
                    listeMachines.remove(machine)
                    return machine.fields
                else:
                    pass
            except:
                pass
    else:
        return event
    return event


def synthetic_EntryExitFromCSV():

    # dictDataset = itertools.chain.from_iterable(testFeatureExtraction.readCSV_data("./data/dataset/"))
    dictDataset = next(testFeatureExtraction.readCSV_data("./data/dataset/"))
    # print(next(dictDataset))
    listeMachines = []
    # for i in range(0,100):
    #     event = next(dictDataset)
    #     if re.search("syscall",event["a_nomEvent"]):
    #         print(event)
    #         synthetic_EntryExitFromEvent(event,listeMachines)
    #         print("\n\n------------------")

    # print(next(dictDataset))
    # print(next(dictDataset))

    listedict = []
    for event in dictDataset:
        print(event)
        listedict.append(synthetic_EntryExitFromEvent(event,listeMachines))
    # print(next(listedict))

    for event in listedict:
        print("\n------------")
        print(event)

    # return synthetic_EntryExitFromEvent(event, listeMachines) # TODO vérifier que c'est la bonne sortie pour feed DecisionTree


def main():
    # trace_path = sys.argv[1]

    # sateMachines = []

    # synthetic_EntryExit(trace_path,sateMachines)

    synthetic_EntryExitFromCSV()


if __name__ == '__main__':
    main()