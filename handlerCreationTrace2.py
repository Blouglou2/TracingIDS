#!/usr/bin/env python
import os
import re
import threading
import time
import subprocess
import sys

from os.path import splitext, expanduser, normpath

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from babeltraceReader import *
from prediction import *


class Handler(FileSystemEventHandler):
    def __init__(self, pattern, exclude, coalesce, command, verbose, notify):
        self.pattern = re.compile(pattern or '.*')
        if exclude:
            self.exclude = normpath(expanduser(exclude))
        else:
            self.exclude = None

        self.coalesce = coalesce
        self.command = command
        self.verbose = verbose
        self.notify = notify
        self.thread = None
        self.q = Queue()

    def start(self):
        self.thread = threading.Thread(target=self._process_q)
        self.thread.daemon = True
        self.thread.start()

    def on_created(self, event):
        global stopped

        if event.is_directory:
            path = event.src_path + "/kernel/"

            # print(path)
            self.q.put(event)

    # def trigger(self, src_path):


    #     if src_path is not None:
    #         path, ext = splitext(src_path)
    #     else:
    #         path, ext = '', ''

    #     cmd = self.command % {'src_path': src_path, 'path': path}
    #     print(cmd)
    #     try:
    #         subprocess.check_call([cmd], shell=True)
    #         subprocess.check_call([
    #             '/usr/bin/osascript',
    #             '-e',
    #             'display notification "Triggered from %s" with title "Watcher"'
    #             % (src_path or '--trigger')
    #         ])
    #     except OSError as exc:
    #         print(exc)
    #         subprocess.check_call([
    #             '/usr/bin/osascript',
    #             '-e',
    #             'display notification "%s from %s" with title "Watcher"'
    #             % (exc, src_path)
    #         ])


    def trigger(self, event):
        num_worker_thread = 4
        threads = []
        for i in range(num_worker_thread):
            t = threading.Thread(target=self.worker(event))
            t.start()
            threads.append(t)
        self.q.join()
        for t in threads:
            t.join()

    def worker(self,event):
        print(event)
        DecisionTreePredict(event+"/kernel")
        self.q.task_done()

    def _process_q(self):
        while True:
            event = self.q.get()

            self.trigger(event.src_path)


@click.command()
@click.option('--verbose', '-v', help='Verbose output.', is_flag=False)
@click.option('--pattern', help='Match filenames.')
@click.option('--exclude', type=click.Path(), help='Exclude directories.')
@click.option('--coalesce', '-c', is_flag=True,
              help='Multiple events trigger one command')
@click.option('--trigger/--no-trigger', '-t/-n', default=False,
              help='Trigger once at startup.')
@click.option('--notify', '-n', is_flag=True, help="Display notification")
@click.argument('command')


def watcher(pattern, exclude, coalesce, trigger, command, verbose, notify):
    args = sys.argv[1:]
    
    observer = Observer()
    handler = Handler(pattern, exclude, coalesce, command, verbose, notify)
    if trigger:
        handler.trigger(None)

    handler.start()

    observer.schedule(handler, path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            print(handler.q.get())
            time.sleep(0.25)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    watcher()
