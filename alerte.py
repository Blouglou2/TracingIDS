#!/usr/bin/env python
# -*- coding : utf-8 -*-
import sys
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format

def RaiseAlert():
    init(strip=not sys.stdout.isatty()) # strip color if stdout is redirected
    cprint(figlet_format("Alerte generale!", font="starwars"),"yellow","on_red")

def main():
    RaiseAlert()

if __name__ == '__main__':
    main()