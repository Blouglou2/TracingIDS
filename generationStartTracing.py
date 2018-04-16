import re
import yaml

def listeEventsToKeep():
    fichier= "eventsAGarder.yaml"
    listeEvents = parse(fichier)
    return listeEvents

def parse(fichier):
    with open(fichier,'r') as f:
        try:
            dictParser = yaml.load(f)
        except yaml.YAMLError as exc:
            print(exc)
    return dictParser["syscall"].split(" "),dictParser["AutresEvents"].split(" ")

def main():
    url = "132.207.72.19"
    listeSyscall, listeEvents = listeEventsToKeep()

    with open('./ssh_Tracing/scriptTracageRpi/startTracing.sh','w') as fichier:
        fichier.writelines(["#!/bin/bash\n" , "\n" ,"if [$# -eq 1]\n", "\tthen\n", "\t\techo 'No arguments supplied'\n", "fi\n", "# Le RANDOM est utile afin que deux sessions crées à la suite n'aient pas le même nom, sinon les temps de snapshot ne sont pas réinitialisés\n" \
        ,"sudo lttng create tracingSSH$(( (RANDOM % 1000) +1)) --set-url=net://"+url+" --snapshot\n","sudo lttng enable-event --kernel --syscall "+",".join(item for item in listeSyscall)+"\n" \
        , "sudo lttng enable-event --kernel "+",".join(item for item in listeEvents)+"\n" , "sleep .5 \n" , "sudo lttng start \n" , "sleep 1\n" , "\n",\
        "trap 'exit' INT  # Pour sortir de la boucle infinie\n" , "while true\n" , "do\n" , "\tsleep $1\n" ,"\tsudo lttng regenerate statedump\n" , "\tsudo lttng snapshot record\n" , "done\n"])
    fichier.close()
    print("Ecriture terminee")

    # print(listeEvents)


if __name__ == "__main__":
    main()