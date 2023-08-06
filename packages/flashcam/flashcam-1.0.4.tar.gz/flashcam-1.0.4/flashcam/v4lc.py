
#!/usr/bin/env python3
'''
 on https://github.com/TheStaticTurtle/RemoteV4L2-CTL/blob/master/remote_v4l2ctl/utils.py
'''
from flashcam.version import __version__
from fire import Fire
from flashcam import config

#import v4l2py
#from v4l2py import Device

import subprocess as sp

import cv2

import matplotlib.pyplot as plt
import numpy as np
import json

import itertools # duplicite list removeal

import sys


import time # tuning has a delay from camera chip.... oscilates...

import random # i need to skip some tune frames


class V4L2_Control:
    """docstring for V4L2_CTL"""

    def __init__(self, control_group, name, addr, type, min=-99, max=-99, step=-99, default=-99, value=-99, flags="none", access="local", device="/dev/video0", callback=None):
        super(V4L2_Control, self).__init__()
        self.control_group = control_group

        self.name = name
        self.addr = addr
        self.type = type
        self.min = min
        self.max = max
        self.step = step
        self.default = default
        self.value = value
        self.flags = flags

        self.access = access
        self.device = device
        self.callback = callback

        self.server = None


    def setServer(self, server):
        self.server = server

    def get_value(self):
        return self.value

    def getmin_value(self):
        return self.min

    def getmax_value(self):
        return self.max

    def setdef_value(self):
        return self.change_value(self.default)

    # uuuuuiiiiiiiiii ---works
    def getdef_value(self):
        return self.default

    def change_value(self, value):
        if value> self.max:
            value = self.max
        if value< self.min:
            value = self.min
        try:
            value = int(value)
        except Exception as e:
            print("change_value: Invalid input -> " + str(e))
            return -1

        if self.step != -99 and value < self.min:
            print("change_value: Value too little", value," x ",self.min)
            return -1

        if self.step != -99 and value > self.max:
            print("change_value: Value too big", value," x ",self.max)
            return -1

        if self.step != -99 and value % self.step != 0:
            print("change_value: Invalid step number (Steps per " + str(self.step) + ")")
            return -1

        if self.type == "custom":
            if self.callback is not None:
                return self.callback(value)

        if self.access == "local":
            #print("Executing: " + ' '.join(['v4l2-ctl', '-d', self.device, '--set-ctrl=' + self.name + '=' + str(value)]))
            try:
                sp.check_output(['v4l2-ctl', '-d', self.device, '--set-ctrl=' + self.name + '=' + str(value)]).decode("utf-8")
                self.value = value
                time.sleep(0.1) # i want to see a blink ??
                return 0
            except sp.CalledProcessError as e:
                print(
                    "Failed to execute command" +
                    ' '.join(['v4l2-ctl', '-d', self.device, '--set-ctrl=' + self.name + '=' + str(value)]) +
                    " -> "+str(e)
                )
                return -1
        elif self.access == "remote" and self.server is not None:
            print("Sending remote command: " + self.name + '=' + str(value))
            r = self.server.send_value_set(self.name, value)
            self.value = value
            return r

    def asdict(self):
        return {
            "control_group": self.control_group,
            "name": self.name,
            "addr": self.addr,
            "type": self.type,
            "min": self.min,
            "max": self.max,
            "step": self.step,
            "default": self.default,
            "value": self.value,
            "flags": self.flags
        }
    def __repr__(self):
        return str(self)
    def __str__(self):
        out = "V4L2_Control() -> " + self.name + " " + self.addr + " (" + self.type + ")  :  "
        out += "min=" + str(self.min) + " " if self.min != -99 else ""
        out += "max=" + str(self.max) + " " if self.max != -99 else ""
        out += "step=" + str(self.step) + " " if self.step != -99 else ""
        out += "default=" + str(self.default) + " " if self.default != -99 else ""
        out += "value=" + str(self.value) + " " if self.value != -99 else ""
        out += "flags=" + self.flags + " " if self.flags != "none" else ""
        return out



class V4L2_CTL():
    """docstring for V4L2_CTL"""

    def __init__(self, device="/dev/video0"):
        super(V4L2_CTL, self).__init__()
        self.device = device
        self.controls = self._list_controls()
        self.capabilities = []
        self.update_capabilities()

        for control in self.controls:
            #print(control.name)
            setattr(self, "set_" + control.name, control.change_value)
            setattr(self, "getmin_" + control.name, control.getmin_value)
            setattr(self, "getmax_" + control.name, control.getmax_value)
            setattr(self, "setdef_" + control.name, control.setdef_value)
            setattr(self, "get_" + control.name, control.get_value)
            setattr(self, "getdef_" + control.name, control.getdef_value)

    def get_capbilities_as_json(self):
        return json.dumps([x.asdict() for x in self.controls])

    def get_capbilities(self):
        li = [x.asdict() for x in self.controls]
        ca = []
        for i in li:
            ca.append( i["name"] )
        return ca


    # def refresh(self):
    #     super(V4L2_CTL, self).__init__()
    #     self.controls = self._list_controls()
    #     self.capabilities = []
    #     self.update_capabilities()
    #     for control in self.controls:
    #         #print(control.name)
    #         setattr(self, "set_" + control.name, control.change_value)
    #         setattr(self, "getmin_" + control.name, control.getmin_value)
    #         setattr(self, "getmax_" + control.name, control.getmax_value)
    #         setattr(self, "setdef_" + control.name, control.setdef_value)
    #         setattr(self, "get_" + control.name, control.get_value)
    #         setattr(self, "getdef_" + control.name, control.getdef_value)


    def update_capabilities(self):
        self.capabilities = [x.name for x in self.controls]

    def has_capability(self,what):
        return what in self.capabilities

    def _list_controls(self):
        controls = []
        #print("Executing: " + ' '.join(['v4l2-ctl', '-d', self.device, '-l']))
        CMD = ['which','v4l2-ctl']
        child = sp.Popen( CMD, stdout = sp.PIPE )
        returncode = child.returncode
        # print(f"i... v4l2-ctl:", returncode, 'str=',child.communicate()[0] )
        if not(returncode is None):
            print("X... install v4l2-ctl:  apt install v4l-utils")
            sys.exit(1)

        CMDL = ['v4l2-ctl', '-d', self.device, '-l']
        #print("i... ", CMDL )
        output = ""
        try:
            output = sp.check_output( CMDL ).decode("utf-8")  # TODO: Check if the output is valid
        except Exception as e:
            print("!... Exception when", CMDL)
    #print(f"i... output = /{output}/")
        if len(output) <2:
            #print("D... no output, returning")
            return []

        raw_ctrls = [x for x in output.split('\n') if x]  # TODO: Same

        last_control_group = "unknown"
        for raw_ctrl in raw_ctrls:
            if raw_ctrl[0] != ' ':
                last_control_group = ('_'.join(raw_ctrl.split(" ")[:-1])).lower()
                print("Found new control group: " + last_control_group)
            else:
                # Remove double white spaces
                while "  " in raw_ctrl:
                    raw_ctrl = raw_ctrl.replace("  ", " ")

                raw_ctrl_what, raw_ctrl_values = raw_ctrl.split(":")
                raw_ctrl_what = [x for x in raw_ctrl_what.split(' ') if x and x != ' ']

                values = {
                    "min": -99,
                    "max": -99,
                    "step": -99,
                    "default": -99,
                    "value": -99,
                    "flags": "none"
                }

                for name, value in [name_value_combo.split("=") for name_value_combo in raw_ctrl_values.split(" ") if
                                    "=" in name_value_combo]:
                    values[name] = value

                ctrlr = V4L2_Control(
                    last_control_group,
                    raw_ctrl_what[0],
                    raw_ctrl_what[1],
                    raw_ctrl_what[2].replace("(", "").replace(")", ""),
                    min=int(values["min"]),
                    max=int(values["max"]),
                    step=int(values["step"]),
                    default=int(values["default"]),
                    value=int(values["value"]),
                    flags=values["flags"],
                    device=self.device
                )

                #print("N..." + str(ctrlr))
                controls.append(ctrlr)


        return controls


#------------------------------------------------------------------------------------------------

# print("v... unit 'unitname' loaded, version:",__version__)




def get_gem( cc, capa ):
    # capa = cc.get_capbilities()

    agm = None
    aex = None
    aea = None
    aga = None

    if "gamma" in capa:
        gm = cc.get_gamma()
        gmd = cc.getdef_gamma()
        minm = cc.getmin_gamma()
        maxm = cc.getmax_gamma()
        gm10 = (gm-minm)/(maxm-minm)
        agm = (gm,gmd,minm,maxm,gm10)
        print(f"I... gamma             {gm:5d};  range({minm:4d},{maxm:5d}) def: {gmd} {gm10:.5f}")

    if "exposure_absolute" in capa:
        ex = cc.get_exposure_absolute()
        exd=  cc.getdef_exposure_absolute()
        mine = cc.getmin_exposure_absolute()
        maxe = cc.getmax_exposure_absolute()
        ex10 = (ex-mine)/(maxe-mine)
        aex = (ex,exd,mine,maxe,ex10)
        print(f"I... exposure_absolute {ex:5d};  range({mine:4d},{maxe:5d}) def: {exd} {ex10:.5f}")

    if "exposure_auto" in capa:
        ea = cc.get_exposure_auto()
        ead=  cc.getdef_exposure_auto()
        minea = cc.getmin_exposure_auto()
        maxea = cc.getmax_exposure_auto()
        aea = (ea,ead,minea,maxea)
        print(f"I... exposure auto     {ea:5d};  range({minea:4d},{maxea:5d}) def: {ead}")

    # A STRANGE CAMERA
    if "exposure" in capa:
        ex = cc.get_exposure()
        exd=  cc.getdef_exposure_absolute()
        mine = cc.getmin_exposure()
        maxe = cc.getmax_exposure()
        gm10 = (ex-mine)/(maxe-mine)
        aex = (ex,exd,mine,maxe,ex10)
        print(f"I...  exposure         {ex:4d};  range({mine:4d},{maxe:5d}) def: {exd} {ex10:.5f}")

    if "gain" in capa:
        ga = cc.get_gain()
        gad = cc.getdef_gain()
        ming = cc.getmin_gain()
        maxg = cc.getmax_gain()
        ga10 = (ga-ming)/(maxg-ming)
        aga = (ga,gad,ming,maxg,ga10)

        print(f"I...  gain             {ga:4d};  range({ming:4d},{maxg:5d}) def: {gad} {ga10:.5f}")


    return aea,aex,aga,agm








def set_gem(cc, gain=None, expo=None, mmaga=None):

    capa = cc.get_capbilities()
    aea,aex,aga,agm = get_gem(cc, capa)
    if aex!=None: ex,exd,mine,maxe,ex10 = aex
    if agm!=None: gm,gmd,minm,maxm,gm10 = agm
    if aga!=None: ga,gad,ming,maxg,ga10 = aga



    print(f"i1... in set_gem: ex={ex}")
    if not expo is None:
        print(f"ix... expo demand {expo}")
        if (expo == "auto"):
            if "exposure_absolute" in capa:
                print("D... AUTO EXPOSURE ON")
                cc.setdef_exposure_auto()  # i thik he knows what is auto
        elif expo !=-1:
            if "exposure_absolute" in capa:
                if "exposure_auto" in capa:
                    print("D... AUTO EXPOSURE OFF")
                    cc.setdef_exposure_auto() # doesnt do default 3
                    #print("ex def",cc.get_exposure_auto())
                    cc.set_exposure_auto(1)  # I just a guess, 1 may be manual, 3


                    ex = cc.get_exposure_absolute()
                    mine = cc.getmin_exposure_absolute()
                    maxe = cc.getmax_exposure_absolute()
                    print(f"i... current exposure {ex}   range {mine}, {maxe}")

                    if (expo == "def"):
                        cc.setdef_exposure_absolute()
                        print("i... new ex= default")
                    else:
                        ex = int( expo * (maxe-mine)+mine)
                        if expo>1: ex+=1
                        if expo<1: ex-=1
                        if ex>maxe: ex=maxe
                        if ex<mine: ex=mine
                        print(f"i... new ex1= {ex};   {expo}")

                    cc.set_exposure_absolute(ex)
            # very stupid wabcam
            elif "exposure" in capa:
                ex = cc.get_exposure()
                mine = cc.getmin_exposure()
                maxe = cc.getmax_exposure()
                print(f"i... current exposure {ex}   range {mine}, {maxe}")

                ex = int( expo * (maxe-mine)+mine)
                if expo>1: ex+=1
                if expo<1: ex-=1
                if ex>maxe: ex=maxe
                if ex<mine: ex=mine
                print("i... new ex2= ",ex)

                cc.set_exposure(ex)
            else:
                print("X... exposure_absolute NOR exposure not in capacities")

    print(f"i2... in set_gem: ex={ex}")

    if not gain is None:
        if gain == "def":
            if "gain" in capa:
                cc.setdef_gain()
        elif gain !=-1:
            if "gain" in capa:
                ga = cc.get_gain()
                ming = cc.getmin_gain()
                maxg = cc.getmax_gain()
                print(f"i... current gain {ga}   range {ming}, {maxg}")

                ga = int( gain * (maxg-ming)+ming)
                if gain>1: ga+=1
                if gain<1: ga-=1
                if ga>maxg: ga=maxg
                if ga<ming: ga=ming
                print("i... new ga = ",ga)
                cc.set_gain(ga)
            else:
                print("X... gain noit in capacities")

    if not mmaga is None:
        if mmaga == "def":
            if "gamma" in capa:
                cc.setdef_gamma()
        elif mmaga !=-1:
            if "gamma" in capa:
                gm = cc.get_gamma()
                minm = cc.getmin_gamma()
                maxm = cc.getmax_gamma()
                print(f"i... current gamma {gm}   range {minm}, {maxm}")

                gm = int( mmaga * (maxm-minm)+minm)
                if gm>maxm: gm=maxm
                if gm<minm: gm=minm
                print("i... new gm= ",gm)

                cc.set_gamma(gm)
            else:
                print("X... gamma not in capacities")

    #------------------------------------------end of function--- SET_GEM








def func(debug = False):

    print("D... in unit unitname function func DEBUG may be filtered")
    print("i... in unit unitname function func - info")
    print("X... in unit unitname function func - ALERT")
    return True

# def test_config_save():
#     config.CONFIG['filename'] = "~/.config/flashcam/cfg.json"
#     config.show_config()
#     print( config.get_config_file() )
#     return config.save_config()

# def test_config_read():
#     config.CONFIG['filename'] = "~/.config/flashcam/cfg.json"
#     config.load_config()
#     config.show_config()
#     print( config.get_config_file() )
#     assert config.save_config() == True

def test_func():
    print("i... TESTING function func")
    assert func() == True








#------------------------------------------------------------------------------------------------

def get_resolutions(vidnum):
    CMD = ['v4l2-ctl', '-d', "/dev/video"+str(vidnum),  "--list-formats-ext"]
    #print("i... cmd = {CMD}")
    output = sp.check_output(CMD).decode(
            "utf-8")  # TODO: Check if the output is valid
    output = output.split("\n")
    output = sorted( [ x.split("Discrete ")[-1] for x in output if x.find("Size: Discrete")>0 ])

    output = [tupl for tupl in {item for item in output }]
    output = sorted( output, key = lambda x: int(x.split("x")[0]) * int(x.split("x")[1]) )
    #o = [ float(o.split("x")[0]+"."+o.split("x")[1]) for o in output]
    # print(output)
    return output






#==================================== WORKS

def tune_histo(cc, h_avg, limitgamma=150):

    glow,ghigh = 16,28

    dg= (ghigh-glow)/2
    med = (ghigh+glow)/2

    if (h_avg>=glow) and (h_avg<=ghigh):
        return
    h_avg= int(h_avg)

    dist = (h_avg- med)/dg # distance in #of sigma
    if abs(dist)<=1:
        return

    capa = cc.get_capbilities()
    aea,aex,aga,agm = get_gem(cc, capa)
    if aex!=None: ex,exd,mine,maxe,ex10 = aex
    if agm!=None: gm,gmd,minm,maxm,gm10 = agm
    if aga!=None: ga,gad,ming,maxg,ga10 = aga


    ok = False
    if dist<-1:
        if (ex<0.2) and(random.randint(0,10)<7): # I skip   frames to stop oscilation
            return
        if aex!=None:
            if ex10<1:
                set_gem(cc, expo=ex10*1.01+0.001)
                ok = True
        if not ok:
            if aga!=None:
                if ga10<1:
                    set_gem(cc, gain=ga10*1.01+0.001)
                    ok = True

    if dist>1:
        if (ex10<0.2) and (random.randint(0,10)<2): # I skip   frames to stop oscilation
            return
        if aex!=None:
            if ex10>0:
                set_gem(cc, expo=ex10*0.99-0.001)
                ok = True
        if not ok:
            if aga!=None:
                if ga10>0:
                    set_gem(cc, gain=ga10*0.99-0.001)
                    ok = True


    # time.sleep(0.2)
    return

    # 48 - 20 = 28;  28/4 ... 6x
    maxg,gg,ming = 2,1,0
    gg,mg,ex = 0,0,0
    defg,defm = 0,0
    maxe,ex,mine = 500,100,100
    maxg,ex,minm = 500,100,100
    maxm,ex,minm = 500,100,100

    if "gain" in capa:
        gg = cc.get_gain()
        maxg = cc.getmax_gain()
        ming = cc.getmin_gain()

    if "gamma" in capa:
        mg = cc.get_gamma()
        maxm = cc.getmax_gamma()
        minm = cc.getmin_gamma()
        defm = cc.getdef_gamma()
        maxm = limitgamma # terrible result if too much


    if "exposure_absolute" in capa:
        ex = cc.get_exposure_absolute()
        mine = cc.getmin_exposure_absolute()
        maxe = cc.getmax_exposure_absolute()


    if dist<-1:
        if "exposure_auto" in capa:
            exposure_auto = cc.get_exposure_auto()
            #if exposure_auto!=1:
            cc.set_exposure_auto(3)
        else:
            print("X... cannot tune the exposure (no auto)")
            return
        return

    elif dist>4:
        FAC = 0.5
    elif dist>3:
        FAC = 0.7
    elif dist>2:
        FAC = 0.9
    elif dist>1:
        FAC = 0.98
    #print(FAC)
    #print(FAC)
    # no caf     CAF = 1/FAC

    # CAF = 1/FAC_BASE # I override the speed from bottom to up

    print(f"i...  {med} +- {dg}  <{h_avg}>  {dist:4.1f}sigma  {FAC:5.2f}x")


    if "exposure_absolute" in capa:
        exposure_absolute = cc.get_exposure_absolute()
        if exposure_absolute!=1:
            cc.set_exposure_auto(1)
    else:
        print("X... cannot tune the exposure (no auto)")
        return


    gg2,ex2,mg2 = gg,ex,mg

    #print(f"                   {ming} - {gg} - {maxg} ; {mine}-{ex}-{maxe} ")
    if h_avg<glow: #------------------ increase
        ex2 = int(FAC*ex)
        gg2 = int(FAC*gg)
        mg2=mg # tune separate
        #mg2 = int(1.1*mg)
        #print(f"increasing {ex} to {ex2}")
        if gg2==gg:
            gg2+=1
        #if mg2==mg:
        #    mg2+=1
        if ex2==ex:
            ex2+=1
        #print(f"increasing {ex} to {ex2}")
    elif h_avg>ghigh:
        ex2 = int(FAC*ex)
        gg2 = int(FAC*gg)
        mg2 = defm # int(0.9*mg)
        if gg2==gg:
            gg2-=1
        #if mg2==mg:
        #    mg2-=1
        if ex2==ex:
            ex2-=1

    gg,ex,mg = gg2,ex2,mg2


    if gg>maxg: gg=maxg
    if gg<ming: gg=ming

    if ex>maxe: ex=maxe
    if ex<mine: ex=mine

    if (ex==maxe) and (gg==maxg):
        print("!... on max")
        mg2=mg
        if h_avg<glow: #------------------ increase
            print("inc gamma now")
            mg2 = int(1.1*mg)
            #print(f"increasing {mg} to {mg2}")
            if mg2==mg:
                mg2+=1
            if mg2>maxm: mg2=maxm
            if mg2<minm: mg2=minm
    else:
        mg2=defm





    #print(f"                   gain {gg}  expo {ex} gamma {mg} ")
    #print(f"                   gain {gg}  expo {ex} gamma {mg} ")
    print(f"        gain {gg} ({ming}/{maxg})  expo {ex} ({mine}/{maxe}) gamma {mg} ({minm}/{maxm}) ")
    time.sleep(0.6)

    if "exposure_absolute" in capa: cc.set_exposure_absolute(ex)
    if "gain" in capa: cc.set_gain(gg)
    if "gamma" in capa: cc.set_gamma(mg2)

    # if gg>maxg:
    #     if h_avg<glow:
    #         ex+=2
    #         cc.set_exposure_absolute(ex)
    #     elif h_avg>ghigh:
    #        gg-=2
    #        if "gain" in capa: cc.set_gain(gg)
    # elif gg<ming:
    #     if h_avg>ghigh:
    #        ex-=2
    #        cc.set_exposure_absolute(ex)
    #     if h_avg<glow:
    #        gg+=2
    #        if "gain" in capa: cc.set_gain(gg)
    # else:
    #     if h_avg<glow:
    #         gg+=2
    #         if "gain" in capa: cc.set_gain(gg)
    #     elif h_avg>ghigh:
    #         gg-=2
    #         if "gain" in capa: cc.set_gain(gg)
    #res = cc.set_exposure_absolute(ex)
    return gg,ex


def main( devid ):
    """
    Here it is a test to set exposure and gain by histogram
    """
    #cam = Device.from_id(0)
    #print( cam.info)
    #print()
    #print(cam.video_capture.get_format())
    cc = V4L2_CTL("/dev/video"+str(devid))
    vid = cv2.VideoCapture(devid)


    lw=1
    bins=256

    initme = True
    gain = 100
    capa = cc.get_capbilities()

    if "exposure_auto" in capa:
        print("D... AUTO EXPOSURE OFF")
        cc.setdef_exposure_auto() # doesnt do default 3
        print("ex def",cc.get_exposure_auto())
        cc.set_exposure_auto(1)

    #print("ex 3",cc.get_exposure_auto())
    if "gain" in capa:
        cc.setdef_gain()
        gg = cc.get_gain()
        print("defgain ",gg)

    if "exposure_absolute" in capa:
        ex = cc.get_exposure_absolute()
        cc.setdef_exposure_absolute()

    gain= 0

    #create two subplots
    ax1 = plt.subplot(1,2,1)
    ax2 = plt.subplot(1,2,2)
    lineGray, = ax2.plot(np.arange(bins), np.zeros((bins,1)), c='r', lw=lw)
    ax2.set_xlim(-10, bins + 10)

    while(True):# https://github.com/nrsyed/computer-vision/blob/master/real_time_histogram/real_time_histogram.py
        #print(" ... gain,  exposure   ",cc.get_gain(), cc.get_exposure_absolute() )

        ret, frame = vid.read()
        # if initme:

        #     #ax2.set_ylim(0, 1)
        #     ax1.set_axis_off()
        #     ax2.spines['right'].set_visible(False)
        #     #ax.spines['bottom'].set_visible(False)
        #     ax2.spines['left'].set_visible(False)
        #     #ax2.set_axis_off()

        #     #create two image plots
        #     im1 = ax1.imshow(frame)

        #     #im2 = ax2.imshow(frame)
        #     #plt.autoscale(enable=True, axis='x', tight=True)
        #     #ax1 = plt.gca()  # only to illustrate what `ax` is
        #     #ax1.autoscale(enable=True, axis='both', tight=True)
        #     #ax2.autoscale(enable=True, axis='both', tight=True)
        #     plt.rcParams['axes.xmargin'] = 0
        #     plt.rcParams['axes.ymargin'] = 0
        #     plt.ion()
        #     ####print("i... plt show")
        #     #plt.show()
        #     #plt.pause(0.01)
        #     initme = False

        framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([framegray], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        hist /= hist.sum()

        #h_avg = (hist*np.arange(bins)).sum()
        #h_std = ((hist*np.arange(bins)*np.arange(bins)).sum())**0.5


        #------------------ https://stackoverflow.com/questions/9390592/drawing-histogram-in-opencv-python
        #h = np.zeros((300,256,3))
        h = np.zeros((480,640,3))
        h = frame.copy()
        #h = np.flipud(h)

        BINS = 64
        bins = np.arange(BINS).reshape(BINS,1)
        color = [ (255,0,0),(0,255,0),(0,0,255) ]

        for ch, col in enumerate(color):
            hist_item = cv2.calcHist([frame],[ch],None,[BINS],[0,255])
            cv2.normalize(hist_item,hist_item, 0, 255, cv2.NORM_MINMAX)
            hist=np.int32(np.around(hist_item))
            pts = np.column_stack((bins*int(640/BINS),480-(hist*480/255).astype(int)))
            cv2.polylines(h,[pts],False,col)

        framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist_gray = cv2.calcHist([framegray], [0], None, [BINS], [0, 255])
        cv2.normalize(hist_gray,hist_gray,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_gray))
        pts = np.column_stack((bins*int(640/BINS),480-(hist*480/255).astype(int)))
        cv2.polylines(h,[pts], False,  [255,255,255], thickness= 2 )


        #h=np.flipud(h)

        cv2.imshow('colorhist',h)
        #cv2.waitKey(1)


        #gg,ex = tune_histo(cc, h_avg)
        #print(f" g={gg} e={ex}   {h_avg:.1f} ({h_std:.1f}) ", end = "\r" )


        #im1.set_data(frame)
        #lineGray.set_ydata(hist)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("i... in the __main__ of unitname of flashcam")
    Fire(main)
