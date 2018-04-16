import babeltrace.reader
import re
import sys
import datetime




def processTraces(trace_path) :

    trace_collection = babeltrace.reader.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        print(event.name+" :")
        for field in event:
            print("\t"+str(field)+" : "+str(event[field]))

        # if re.search("chmod",event.name) :
        #     if ('filename' in event.keys()):
        #         print("Tentative de chmod sur "+event['filename'])
        #         print(datetime.datetime.now())
        #     else:
        #         print("Tentative de chmod")
        #         print(datetime.datetime.now())
        
        # if re.search("faccessat",event.name) :
        #     if ('filename' in event.keys()):
        #         if not ( re.search("/etc/ld.so.preload",event['filename']) or re.search("lttng",event['filename'])) :
        #             print("Acces à " + event['filename'])
        #             if (re.search("chmod",event['filename'])):
        #                 print(datetime.datetime.now())
                
        # if re.search("execve",event.name) :
        #     if ('filename' in event.keys()):
        #         if not ( re.search("/bin/sleep",event['filename']) or re.search("lttng",event['filename'])) :
        #             print("Execution de " + event['filename'])
        #         if (re.search("chmod",event['filename'])):
        #             print(datetime.datetime.now())

    # print("Fin de l'analyse")




def readAllEvents(trace_path) :

    trace_collection = babeltrace.reader.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:

        if re.search("syscall",event.name) :
                print(event.name)
        for key in event.keys() :
            print("\t",key," : ",event[key])
           

    print("Fin de l'analyse")

def readSyscalls(trace_path) :

    trace_collection = babeltrace.reader.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        # print(event.name)

        if re.search("syscall",event.name) :
                print(event.name)
    print("Fin de l'analyse")


def printKeys(trace_path) :

    cont = 0
    trace_collection = babeltrace.reader.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        # print(event.name, " : ",event.keys(),"\n")

        if re.search("net",event.name) :
            print("\n", event.name, " : ")
            if 'network_header' in event.keys() :
                print(event['network_header'])
            if 'magic' in event.keys() :
                print(event['magic'])
            if 'packet_size' in event.keys() :
                print(event['packet_size'])
            if 'skbaddr' in event.keys() :
                print(event['skbaddr'])
            if 'events_discarded' in event.keys() :
                print(event['events_discarded'])
            print(event['content_size'])
            print(event['v'])

            cont +=1
            if cont>3 :
                break

    print("Fin de l'analyse")


def main():

    trace_path = sys.argv[1]

    print(trace_path)

    trace_collection = babeltrace.reader.TraceCollection()

    trace_handle = trace_collection.add_trace(trace_path, 'ctf')

    for event in trace_collection.events:
        # re.search("ioctl",event.name) or re.search("kmem",event.name) or re.search("irq",event.name)  or re.search("sched",event.name) or re.search("rcu_",event.name)
        if (1 ) :
            
            print("\n", event.name, " : ")
            for key in event.keys() :
                    print("\t",key," : ",event[key])
        
            

if __name__ == '__main__':
    main()