#!/usr/bin/env python3


from flashcam.version import __version__
from fire import Fire
from flashcam import config
import os

import mmap
import time
import sys

MMAPFILE = os.path.expanduser("~/.config/flashcam/mmapfile")
MMAPSIZE = 1000


# -------------------------------------------------------------------------

def mmcreate(filename=MMAPFILE):

    with open(filename, "w") as f:
        f.write("-"*MMAPSIZE)


def mmwrite(text, filename = MMAPFILE):
    """
    write text to filename
    """
    if not os.path.exists(filename):
        mmcreate(filename)
    else:
        file_size = os.path.getsize( MMAPFILE )
        print(f"! File Size IS== {file_size}, should be {MMAPSIZE} ")
        if file_size!=MMAPSIZE:
            sys.exit(0)

    with open(filename, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE, offset=0) as mmap_obj:
            #print(" WRITING: ",text)
            mmap_obj.write(str(text).encode("utf8") )  # 2ms
            mmap_obj.flush()





# -------------------------------------------------------------------------

def mmread(filename = MMAPFILE):
    """
TO DEBUG ONLY
    """
    print(filename)
    print(filename)
    print(filename)
    print(filename)
    print(filename)
#    with open(filename, mode="r", encoding="utf8") as file_obj:
#        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
#            text = mmap_obj.read()
#            print("READTEXT =",text)

    with open(filename, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE, offset=0) as mmap_obj:
            text = mmap_obj.read().decode("utf8").strip()
            print(text)
            print(text)
            print(text)
            print(text)
            return text



def mmread_n_clear(  filename = MMAPFILE ):
    """
    read and clear  filename
    """
    if os.path.exists(filename):
        file_size = os.path.getsize( MMAPFILE )
        if int(file_size) != int(MMAPSIZE):
            print(f"! File Size == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size == {file_size}, should be {MMAPSIZE}")
            os.remove( MMAPFILE )
            #sys.exit(0)
            mmcreate(filename)

    if not os.path.exists(filename):
        return  "xxxxxx","1"


    with open(filename, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE, offset=0) as mmap_obj:
            text = mmap_obj.read().decode("utf8").strip()
            # print("READTEXT: ",text)


            # execute(text.decode("utf8"))
            if text[0] == "*":
                response = "xxxxxx","1"
            else:
                response = text.split("*")[0]
                response = f"{response.split()[0].strip()}",f"{response.split()[1].strip()}"
                print("i... mmapread'nclear returning ", response)
                print("i... mmapread'nclear returning ", response)
                print("i... mmapread'nclear returning ", response)

            text = "*"*50
            # print("CLEARING: ",text)



            mmap_obj[:MMAPSIZE] = str(" "*MMAPSIZE).encode("utf8")
            mmap_obj[:len(text)] = str(text).encode("utf8")
            mmap_obj.flush()
            return response
# -------------------------------------------------------------------------

if __name__ == "__main__":
    Fire()
    print("... sleeping 2")
    time.sleep(2)
