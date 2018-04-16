#!/bin/bash

if [$# -eq 1]
	then
		echo 'No arguments supplied'
fi
# Le RANDOM est utile afin que deux sessions crées à la suite n'aient pas le même nom, sinon les temps de snapshot ne sont pas réinitialisés
sudo lttng create tracingSSH$(( (RANDOM % 1000) +1)) --set-url=net://132.207.72.19 --snapshot
sudo lttng enable-event --kernel --syscall access,chdir,chmod,chown,chroot,clone,close,connect,copy_file_range,creat,delete_module,execve,execveat,exit,exit_group,faccessat,fallocate,fchdir,fchmod,fchmodat,fchown,fchownat,finit_module,fork,getcpu,getcwd,getdents,getdents64,getegid,geteuid,getgid,getpgid,getpgrp,getpid,getppid,gettid,getuid,kexec_file_load,kexec_load,kill,lchown,link,linkat,listen,migrate_pages,mkdir,mkdirat,mount,mq_unlink,open,openat,open_by_handle_at,newstat,pipe,pipe2,pivot_root,read,readahead,readlink,readlinkat,readv,reboot,remap_file_pages,rename,renameat,renameat2,restart_syscall,rmdir,sched_getparam,setdomainname,setfsgid,setfsuid,setgid,setgroups,sethostname,setitimer,set_mempolicy,setns,setpgid,setpriority,setregid,setresgid,setresuid,setreuid,setrlimit,set_robust_list,setsid,setsockopt,set_tid_address,settimeofday,setuid,setxattr,shutdown,socket,symlink,symlinkat,sysctl,sysfs,sysinfo,syslog,tgkill,tkill,umount,unlink,unlinkat,unshare,vfork,write,writev
sudo lttng enable-event --kernel sched_switch,sched_process_fork,sched_process_exec,net_dev_queue,module_load,module_free,power_cpu_frequency,sched_process_exit,writeback_queue,writeback_exec,writeback_start
sleep .5 
sudo lttng start 
sleep 1

trap 'exit' INT  # Pour sortir de la boucle infinie
while true
do
	sleep $1
	sudo lttng regenerate statedump
	sudo lttng snapshot record
done
