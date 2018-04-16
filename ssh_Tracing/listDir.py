import os
import glob
from stat import ST_CTIME

def dateSort(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

def main():
    directory = "/home/robin/Bureau/TestMachineLearning/HomeAssistant/hassbian"
    print(os.getenv('PATH'))
    print("\n")
    dateSort(directory)

if __name__ == "__main__":
    main()