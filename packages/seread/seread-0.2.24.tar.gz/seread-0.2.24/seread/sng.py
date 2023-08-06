#!/usr/bin/env python3
"""
This code reads serial device. Different ways possible, initial setting
 - arduino (json)
 - ORTEC COUNTER (text)
AND sends to
 - UDP (~/.sng2_udp) 8081 (to work with HTTP server of gregory 9009)
      - gregory thread waits on an open udp port on 8081
 - influx databases defined in ~/.myservice_discover8086
 - writes to files ~/serial....

./sng2.py -l 1-1.3 -c script -b 19200 -t 1,10 --debug -i
./sng2.py -D /dev/ttyUSB0 -c listen -b 19200 -t 1,10 --debug -i false
#
#  PORT-8099 server translates to influxdb
./sng2.py -D /dev/pts/6 -c listen -b 9600 -t 1,10 --debug
#
# problem with /dev/pts/
#
 for ((j=0;j<10;j++)); do for ((i=0;i<10;i++)); do echo 'influxmegeo geo 15.'$j' 49.'$i | nc localhost 8099 ; sleep 2; done; done
#
#------ CONFIG FILES:
~/.seread.calib
~/.myservice_discover8086
~/.myservice_permanent8086
~/.influx_userpassdb
~/.sng2_udp
OUTPUT
~/serial_NG2_udp
~/serial_NG2_jso
"""
# -fire CLI
#
# - with inline sending, 10ms
# - with threadings 5ms
# + with statistical compensation 1ms
#
#
from fire import Fire
from version import __version__

from asyncio import get_event_loop
from serial_asyncio import open_serial_connection
import serial # list devices .... nice tool
import serial.tools.list_ports

import time
import json

# for UDP ======
import socket
import time
import random

#------ create a server - future command+control
import socketserver

import sys

import datetime

#==================== insecure treatment of https is WITHOUT WARNINGS NOW
# verify_ssl   # ssl=True, verify_ssl=False
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


ips=[]
ips2=[]
ipsudp=[]
complained_already = False
complained_already2 = False
complained_already3 = False
# end of UDP =====


#==========influx===========
from influxdb import InfluxDBClient
import os

import datetime as dt

import threading

#===============================
# coding \r\n from file

from codecs import encode


import pprint

import subprocess as sp

#====================================================================
# integration with  raspberry pi  pantilt module
import pantilthat as ptz

#====================================================================
# integration with flashcam !!!!!!!!!!!
import mmap
# IN BIN: MMAPFILE = os.path.expanduser("~/.config/flashcam/mmapfile")


# -------------------------------------------------------------------------
def mmcreate():
    global MMAPFILE
    with open(MMAPFILE, "w") as f:
        f.write("-"*100)

def mmwrite( imgname ):
    """
    write text to filename
    """
    global MMAPFILE
    if imgname is None:
        imgname = "None"
    if not os.path.exists(MMAPFILE):
        mmcreate()
    with open(MMAPFILE, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE, offset=0) as mmap_obj:
            #print(" WRITING: ",text)
            if imgname.find(".jpg")<len(imgname)-5:
                imgname = imgname+".jpg"

            CMD = f'fixed_image "{imgname}"'
            mmap_obj.write( CMD.encode("utf8") )  # 2ms
            mmap_obj.flush()

# -------------------------------------------------------------------------


#====================================================================

def func():
    print("D... function defined in serial2:sng2")
    return True

def test_func():
    print("D... test function ... run pytest")
    assert func()==True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[1;92m'
    WARNING = '\033[93m'
    FADED  = '\033[31m'
    GRAY  = '\033[30m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#=============================== GLOBAL VARIABLES ===========

STARTTAG=dt.datetime.now().strftime("_%Y%m%d_%H%M%S")
creds=[]
ips=[]
myname="x"
calibration={}

AVG_SLEEPVAL=0
dtloo3=1 # interval from the last measurement

lastdiard=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #json shows diffs/tloo2




#================================================================== SERVER TCP/UDP/========start
def str_is_json(myjson):
    # print("D... my local jsontest:",myjson)
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        print("D... not loadable")
        return False
    return True


# echo 'influxme [{"measurement":"geo","fields":{"longitude":15.0,"latitude":50.0}}]' | nc localhost 8099

def translate_net2json( res ):
    """
    translate TCP or UDP call to [json] for influx
    e.g. I use UDP port 8100 to receive rate from HPGe
    """
    global ips,ips2,creds,myname, decimatevac, decimatevacSET


    # D...  influxmevac vac102 09.04.2021 14:26:12 _ P1= 0.00E+0 _ P2= 0.00E+0 ... FL+++
    if res.find("influxmevac ")==0:
        # decimate
        decimatevac-=1
        if not decimatevac==0:
            return False
        decimatevac = decimatevacSET
        #
        fl = None
        r = res.split("influxmevac")[-1].strip()
        r = r.replace("   "," ")
        r = r.replace("  "," ")
        # print(r)
        # print(r.split(" ") )
        if len(r.split()) == 9:
            measu,idat,itim,_,_,p1,_,_,p2 = r.split(" ")
        else:
            # NEW VADIM FLOW
            measu,idat,itim,_,_,p1,_,_,p2,_,_,flow = r.strip().split(" ")
            fl = float(flow)

        p1 = float(p1)
        p2 = float(p2)
        t = datetime.datetime.now().strftime("%H:%M:%S")
        print("D...    ",t,measu,p1,p2,fl)
        res = "influxme "
        if len(r.split()) == 9:
            res = '"fields":{"p1":'+str(p1)+',"p2":'+str(p2)+'}'
        else:
            res =  '"fields":{"p1":'+str(p1)+',"p2":'+str(p2)+',"fl":'+str(fl)+'}'

        res = 'influxme [{"measurement":"'+measu+'",'+res+'}]'
        # string
        res = translate_net2json( res )  #recursive
        return res #<<<<<<<<<<<<<<<<<<<<<<<<<<<<



    # D...  influxmevac vac102 09.04.2021 14:26:12 _ P1= 0.00E+0 _ P2= 0.00E+0 ... FL+++
    if res.find("influxmebeam ")==0:
        # print(res)
        t = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
        with open( os.path.expanduser(OUT_beamon),"a+") as f:
                   f.write( t+" "+res + "\n")
        # decimate # NO DECIMATE FOR BEAM_ON OFF
        # decimatevac-=1
        #if not decimatevac==0:
        #    return False
        #decimatevac = decimatevacSET

        r = res.split("influxmebeam")[-1].strip()
        r = r.replace("   "," ")
        r = r.replace("  "," ")
        # print(r)
        # print(r.split(" ") )


        measu,counter,status,rabbit,position,time = r.strip().split(" ")

        if not(status in ["BEAM_ON_", "BEAM_OFF", "DET_RDY_","DET_NRDY"]):
            print("X... bad unknown status:", status )
            return

        # flashcam !!!
        mmwrite( status )


        value = 100
        if status.find("DET")>=0:
            value = 80
        res = '"fields":{"'+status+'":'+str(value)+'}'

        res = 'influxme [{"measurement":"'+measu+'",'+res+'}]'
        # string


        res = translate_net2json( res )  #recursive
        return res #<<<<<<<<<<<<<<<<<<<<<<<<<<<<



    if res.find("influxmegeo ")==0:
        r = res.split("influxmegeo")[-1].strip()
        measu,lon,lat = r.split(" ")
        res = "influxme "
        res = '"fields":{"longitude":'+str(lon)+',"latitude":'+str(lat)+'}'
        res = 'influxme [{"measurement":"'+measu+'",'+res+'}]'
        # string
        res = translate_net2json( res )  #recursive
        return res #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    res2 = '"fields":{'
    if res.find("gregory")==0:
        r = res.split(":")[-1].strip()
        r = r.replace("  "," ").split(" ")


        measu = "gregory"
        measu = res.split(":")[0]
        #print("MEASUREMENT = ", measu )
        # print("/{}/".format(r))
        # 0 1  b0 ch0
        #print(r)
        for i in range(len(r)):
            if r[i].find("b")==0:
                fldstr=""
                i+=1
                if r[i].find("ch0")==0:
                    chan=r[i][2]
                    rate,pup,reg = r[i+1],r[i+2],r[i+3]
                    #print("D... ", chan,rate,pup,reg )
                    ch=0
                    fldstr=f'"rate{ch}":{rate},"pup{ch}":{pup},"reg{ch}":{reg},'

                if r[i].find("ch1")==0:
                    chan=r[i][2]
                    rate,pup,reg = r[i+1],r[i+2],r[i+3]
                    #print("D... ", chan,rate,pup,reg )
                    ch=1
                    fldstr=f'"rate{ch}":{rate},"pup{ch}":{pup},"reg{ch}":{reg},'

                if r[i].find("ch2")==0:
                    chan=r[i][2]
                    rate,pup,reg = r[i+1],r[i+2],r[i+3]
                    ch=2
                    fldstr=f'"rate{ch}":{rate},"pup{ch}":{pup},"reg{ch}":{reg},'

                if r[i].find("ch3")==0:
                    chan=r[i][2]
                    rate,pup,reg = r[i+1],r[i+2],r[i+3]
                    ch=3
                    fldstr=f'"rate{ch}":{rate},"pup{ch}":{pup},"reg{ch}":{reg},'

                if r[i].find("ch4")==0:
                    chan=r[i][2]
                    rate,pup,reg = r[i+1],r[i+2],r[i+3]
                    ch=4
                    fldstr=f'"rate{ch}":{rate},"pup{ch}":{pup},"reg{ch}":{reg},'

                if r[i].find("ch5")==0:
                    chan=r[i][2]
                    rate,pup,reg = r[i+1],r[i+2],r[i+3]
                    ch=5
                    fldstr=f'"rate{ch}":{rate},"pup{ch}":{pup},"reg{ch}":{reg},'

                if r[i].find("ch6")==0:
                    chan=r[i][2]
                    rate,pup,reg = r[i+1],r[i+2],r[i+3]
                    ch=6
                    fldstr=f'"rate{ch}":{rate},"pup{ch}":{pup},"reg{ch}":{reg},'

                if r[i].find("ch7")==0:
                    chan=r[i][2]
                    rate,pup,reg = r[i+1],r[i+2],r[i+3]
                    ch=7
                    fldstr=f'"rate{ch}":{rate},"pup{ch}":{pup},"reg{ch}":{reg},'

                res2 = res2+fldstr
                # print("INTERMED=",res2)
        #res = '"fields":{"rate0":'+str(rate0)+',"pup0":'+str(pup0)+',"reg0":'+str(reg0)+',"rate1":'+str(rate1)+',"pup1":'+str(pup1)+',"reg1":'+str(reg1)+'}'

        if (res2[-1]==","):
            res2=res2[:-1]
        res2 = res2+"}"

        res2 = 'influxme [{"measurement":"'+measu+'",'+res2+'}]'
        # string
        res2 = translate_net2json( res2 )  #recursive
        return res2 #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    if res.find("influxme ")==0:
        r = res.split("influxme ")[-1].strip()
        print("D... IFM:",r )
        # [ {"measurement":"a", "fields":{} } ]

        # sendme = False
        # print( r )
        # print( r[1:-1] )
        #------ this is the last resort. Everything ends with list of dicts
        if str_is_json( r[1:-1] ): # check if in inner part of [] is json
            # print("D... GOOD , JSON inside")
            json_body=json.loads(r[1:-1])  # string loaded
            json_body=[json_body,]  # made list item
            # return this
            return json_body #<<<<<<<<<<<<<<<<<<
            # sendme=True
        else:
            print("X... influxme MSG NOT JSON: {}".format(res) )
            return False # <<<<<<<<<<<<<<<<<<<



class Handler_UDPServer(socketserver.DatagramRequestHandler):
    def handle(self):
        global ips,ips2,creds,myname
        # Receive a message from a client
        # print("Got an UDP Message from {}".format(self.client_address[0]))
        self.data = self.rfile.readline().strip()
        # print("The Message is {}".format(self.data))
        res = self.data.decode("utf8")
        raw = self.data.decode("utf8")
        #print("UDP...:",res)
        # self.wfile.write("Hello UDP Client! I received a message from you!".encode())

        res = translate_net2json( res )
        if type(res) != bool:
            if (type(res) == list) and (type(res[0]) == dict):  #------------------ FILL INFLUX
                json_body = res
                init_influx_and_name( silent=True )
                #print("D... resending data to influx:")
                for IP in [*ips,*ips2]:
                    print("D... ",bcolors.GRAY, "UDP", IP, json_body, bcolors.ENDC)
                    x = threading.Thread(target=send_influx, args=(IP,json_body,))
                    x.start()
            else:
                print("X...  json not dict", raw)
        #self.request.sendall("influxme ok".encode())
        return


class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    The TCP Server class for demonstration.

    Note: We need to implement the Handle method to exchange data
    with TCP client.
    here are the ideas realized:
    1. transfer commands to serial device (set voltage)
    2. translate other formats and write to influx
       a. VADIM vacuum UDP string
       b. geotest
       c. pantilthat
       d. v4l2

    """
    def handle(self):
        global ips,ips2,creds,myname
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        # print("{} sent:".format(self.client_address[0]))
        # print(self.data)
        # just send back ACK for data arrival confirmation
        res = self.data.decode("utf8")
        # print("D... ",res)

        #================================ ptz part
        if res.find("ptz ")==0:
            r = res.split("ptz ")[-1].strip()
            dig = r.split(" ")[-1]
            dig = int(dig)
            if dig==1:
                dig=2
            if dig==-1:
                dig=-2
            # print("D... dig==:",dig)
            if r.find("pan")==0:
                fin = ptz.get_pan()+ dig
                if (fin>-80) and (fin<80):
                    ptz.pan( fin)
            if r.find("tilt")==0:
                fin = ptz.get_tilt()+ dig
                if (fin>-87) and (fin<87):
                    ptz.tilt( fin )
            MSG = "ACK... p/t: {}/{}".format(ptz.get_pan(),ptz.get_tilt() )
            print(MSG)
            self.request.sendall(MSG.encode())
            return

        #======================================influxme part both TCP or UDP
        # influxme [{...{}}]
        # inlfuxmegeo measurement lon lat .... influxmegeo memame 15 50

        res = translate_net2json( res )
        if type(res) != bool:
            if (type(res) == list) and (type(res[0]) == dict):  #------------------ FILL INFLUX
                json_body = res
                init_influx_and_name( silent=True )
                #print("D... resending data to influx:")
                for IP in [*ips,*ips2]:
                    # print("D... ", IP, json_body)
                    print("D... ",bcolors.GRAY, "TCP", IP, json_body, bcolors.ENDC)
                    x = threading.Thread(target=send_influx, args=(IP,json_body,))
                    x.start()
        self.request.sendall("influxme ok".encode())
        return




def sserver(SHOST, SPORT):
    """
    This is the way how to communicate with the running SEREAD2
    TWO grave Ideas:
    1. transfer commands to serial device (set voltage)
    2. translate other formats and write to influx
       a. VADIM vacuum UDP string
       b. geotest
       c. pantilthat
       d. v4l2
    """

    # Init the TCP server object, bind it to the localhost on 9999 port
    try:
        tcp_server = socketserver.TCPServer((SHOST, SPORT), Handler_TCPServer)
        print("D... TCP server on port:", SPORT )
    except:
        print("XXX ... TCP Server Socket ",SPORT," has a problem to run" )
        print("XXX ... exiting... " )
        print("XXX ... If not killed, kill me please  Ctrl-c" )
        sys.exit(1)
    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()


def sserverudp(SHOST, SPORT):
    """
       a. VADIM vacuum UDP string
    """

    # Init the UDP server object, bind it to the localhost on 9999 port
    try:
        udp_server = socketserver.UDPServer((SHOST, SPORT), Handler_UDPServer)
        print("D... UDP server on port:", SPORT )
    except:
        print("XXX ... UDP Server Socket ",SPORT," has a problem to run" )
        print("XXX ... exiting... " )
        print("XXX ... If not killed, kill me please  Ctrl-c" )
        sys.exit(1)
    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    udp_server.serve_forever()







def kill_tty_pid(tty):
    """
    a trick to KILL others who are on the tty...
    """
    CMD = "fuser "+tty
    print("D... trying to kill all on my tty: ",CMD)
    ok = False
    try:
        res = sp.check_output( CMD.split() ).decode("utf8")
    except:
        ok = True
    if ok:
        print("D ...  no kill ....","_"*60)
        return

    lil = res.split()
    print( lil )

    CMD = "kill "+lil[-1]
    print("_"*60,"\n",CMD,"_"*60)
    sp.check_output( CMD.split() )
    return


def check_one_file(filename, silent=False):
    ok = False
    try:
        with open( os.path.expanduser( filename ) ) as f:
            a=f.readlines()
        ok = True
    except:
        ok = False
    r = ok
    en = bcolors.ENDC
    txt = ""
    if r:
        col = bcolors.OKGREEN
        txt = "[OK]"
    else:
        col = bcolors.FAIL
        txt = "[Not present]"
    if not silent:print( "{:40s} {} {} {}".format(filename, col, txt, en) )
    return ok



def check_the_files():
    global INP_calib,INP_discover,INP_permanent,INP_influx_cred,INP_udp_out,INP_script
    myli = [INP_calib,INP_discover,INP_permanent,INP_influx_cred,INP_udp_out,INP_script]
    # print("D... checking the files:")
    print("_"*20,"INPUT FILE CHECK","_"*42)
    r = True
    for i in myli:
        r = r* check_one_file(i, silent=True)
    if r:
        print("D... ",bcolors.OKGREEN, "all input files present", bcolors.ENDC)
    else:
        for i in myli:
            r = r* check_one_file(i, silent=False)
        # r = check_one_file()
    print("_"*80)


def init_calibration( silent=False ):
    global calibration,  complained_already2
    calibfile = INP_calib
    try:
        with open( os.path.expanduser( calibfile ) ) as f:
            calibration = json.load(f)
        # if silent: print("i... FOUND calibration:   "+calibfile+"  json ")
    except:
        if silent:
            if not complained_already2:
                print("X... NOT FOUND JSON  calibration file: ",calibfile)
                if silent: print(""" USE FOR EXAMPLE:
{
"valuea0":{"a":0.21699,"b":-61.111},
"valuea1":{"a":0.1861328,"b":-40.2}
}
""")
                complained_already2 = True
        return
    if silent:
        if not complained_already2:
            print("D... Calibration JSON ({}):\n".format(calibfile) )
            pprint.pprint(  calibration)
            complained_already2 = True



def init_influx_and_name(silent=False):
    """
    this feeds the global lists of IP
    """
    global ips,ips2,creds,myname, complained_already
    myname=socket.gethostname()


    ips=[]
    creds=[]
    CONFIG = "~/.myservice_discover8086"
    CONFIG2 = "~/.myservice_permanent8086"
    CONFIG3 = "~/.influx_userpassdb"

    CONFIG  = INP_discover
    CONFIG2 = INP_permanent
    CONFIG3 = INP_influx_cred
    Acomplained_already = False


    try:
        with open( os.path.expanduser(CONFIG) ) as f:
            ips=f.readlines()
        ips=[ i.strip() for i in ips]
        if not silent:
            if not complained_already:
                print("i... FOUND      ",CONFIG,ips)
                Acomplained_already = True

    except:
        if not silent:
            if not complained_already:
                print("X... NOT FOUND    ", CONFIG)
                Acomplained_already = True
        # return


    ips2=[]
    try:
        with open( os.path.expanduser(CONFIG2) ) as f:
            ips2=f.readlines()
        ips2=[ i.strip() for i in ips2 ]
        if not silent:
            if not complained_already:
                print("i... FOUND      ",CONFIG2,ips2)
                Acomplained_already = False
    except:
        if not silent:
            if not complained_already:
                print("X... NOT FOUND     ", CONFIG2)
                Acomplained_already = True
        # NOT return


    try:
        with open(os.path.expanduser(CONFIG3) ) as f:
            creds=f.readlines()
        if not silent:
            if not complained_already:
                print("i... Credentials for INFLUX OK", CONFIG3)
                Acomplained_already = True
    except:
        if not silent:
            if not complained_already:
                print("X... NOT FOUND     ", CONFIG3)
                Acomplained_already = True
        # return

    creds=[ i.strip() for i in creds ]


    if Acomplained_already:
        complained_already = True


    #print("#CREDS=", creds)
    #------------------------------- END COMPLAIN


def init_udp_and_name():
    """
    list of IP:udp 1 per line, where to send
    """
    global ipsudp, complained_already3
    myname=socket.gethostname()
    CONFIG = INP_udp_out #"~/.sng2_udp"

    ipsudp=[]
    try:
        with open( os.path.expanduser(CONFIG) ) as f:
            ipsudp=f.readlines()
        ipsudp=[ i.strip() for i in ipsudp]
        if not comlained_already3:
            print("i... FOUND     ",CONFIG,ipsudp)
            print("D...        see with 'nc -lku 8081'")
            complained_already3 = True
    except:
        # print("X... NOT FOUND    ",CONFIG)
        return





def send_influx(IP, json_body):
    global creds
    #print("#==>INFL"+IP)
    if IP[0].isdigit():
        client = InfluxDBClient(IP, 8086,creds[0],creds[1],creds[2],ssl=False, timeout=5)
    else:
        client = InfluxDBClient(IP, 8086,creds[0],creds[1],creds[2],ssl=True, verify_ssl=False, timeout=5)

#    client = InfluxDBClient(IP, 8086,creds[0], creds[1], creds[2] )
#    print("D... json to ",IP,"...", json_body )
    client.write_points(json_body)


def send_udp8081(MESSAGE, UDP_IP, UDP_PORT=8081):
    """
    send something to the UDP socket. Used to FEED ACQ with counter data. take CPORT_UDP
    """
    #print("#==>localUDP8081")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))



def sleep_interval2(timeout, dt, avg_tout):
    global AVG_SLEEPVAL
    if AVG_SLEEPVAL==0:
        AVG_SLEEPVAL=timeout

    dtcorr = (avg_tout - timeout)
    #if (dtcorr>0):dtcorr+=0.0002
    ##if dtcorr<0:dtcorr-=0.00015 # asymetric bias

    AVG_SLEEPVAL = AVG_SLEEPVAL - dtcorr/10 # slow changes
    if AVG_SLEEPVAL<0:
        AVG_SLEEPVAL = 0

    if (timeout>dt) :
        #print(" ... sleep {:.4f} {:.4f}".format( AVG_SLEEPVAL, dtcorr ) )
        time.sleep( AVG_SLEEPVAL )
    return AVG_SLEEPVAL


def sleep_interval( localtimeout , dtcom,  dtcorrstat, baud ):
    # stabilization over larger time 10x
    #print("D... sleeping: ",localtimeout-dtcom -dtcorrstat*0.5)
    # instead of 20s it is long term like 20.010. Bias 5ms
    #    50%+ in dt-comm; bias 5ms...
    #    BUT dtcorrstat will try to compensate that?
    # 20seconds: time.sleep( localtimeout - 1.5*dtcom -dtcorrstat*0.9 - 0.005)
    # 2seconds: works also
    offset=-0.005
    if baud==115200: # arduino
        offset=-0.005
    else: #19200    +0.005   0.008   0.012 #AFTER_CORRECT_ORTEC_2READS: +0.0075
        offset=+0.005
    #time.sleep( localtimeout - 1.5*dtcom -dtcorrstat*0.9 + 0.008)
    sltime= localtimeout - 1.5*dtcom -dtcorrstat*0.9 + offset
    print("\nD... DtDesired={:.3f} DtComm={:.3f} DtCorrStatist={:.3f} offs={:.3f} :=> sleeping={:.3f}".format(
        localtimeout,dtcom,dtcorrstat,offset, sltime)
    )
    if sltime>0:
        print(sltime)
        time.sleep( sltime )
    #




def interpret_json( respo ):
    """
    does also calibration
    """
    global myname, dtloo3
    diard=json.loads(respo) # I know it is dict already
    #print("RES=/{}/DIARD=/{}/".format(respo,diard))
    if not 'measurement' in diard.keys():
        diard['measurement'] = "noname"
    #---myname is global <= gethostname()
    json_body = [ {"measurement":myname+"_"+diard['measurement']} ]

    # --- I PREPARE THE json and UDP form-------------
    json_body[0]["fields"]={ "dt":dtloo3 }

    UDPMESSAGE="{0:.3f}".format( json_body[0]["fields"]["dt"]   )

    #--- I FILL json and UDP-------------------
    for i in diard.keys():
        json_body[0]["fields"][ i ]=diard[ i ]
        try:
            diard[i] = float(diard[i])
            UDPMESSAGE=UDPMESSAGE+" {0:9.2f}".format( diard[ i ] )
        except:
            UDPMESSAGE=UDPMESSAGE+" {}".format( diard[ i ] )
        #====== HERE  INVOLVE CALIBRATION
        #print("D###", calibration.keys() )
        if i in calibration.keys():
            ical = i+"_cal"
            a=calibration[i]['a']
            b=calibration[i]['b']
            rescal = a*diard[ i ]+b
            # print("C... CAL",i,diard[ i ],  "-->", rescal )

            json_body[0]["fields"][ ical ]= rescal
            # i want 0s after deciamal pplaces
            UDPMESSAGE=UDPMESSAGE+" {0:9.2f}".format( round(rescal,2) )
    # print(json_body)
    return json_body,UDPMESSAGE




def interpret_list4( respo ):  # ORTEC
    global myname, dtloo3, lastdiard

    diard,okortec = extrn_decode_list4(respo)
    if not okortec: return None,None

    json_body = [ {"measurement":myname} ]
    json_body[0]["fields"]={"valt":diard[0],
                            "val1":diard[1],
                            "val2":diard[2],
                            "val3":diard[3],
                            "dt":dtloo3,
                            "dvalt_dt":(diard[0]-lastdiard[0])/dtloo3,
                            "dv1_dt":(diard[1]-lastdiard[1])/dtloo3 if (diard[1]>lastdiard[1]) else 0.,
                            "dv2_dt":(diard[2]-lastdiard[2])/dtloo3 if (diard[2]-lastdiard[2]) else 0.,
                            "dv3_dt":(diard[3]-lastdiard[3])/dtloo3 if (diard[3]-lastdiard[3]) else 0.,
    }
    #JSON FOR INFLUX
    #UDP FOR ROOT THTTPSERVER
    UDPMESSAGE="{} {} {} {}".format( int(diard[0]/10),
                                     int(diard[1]) ,
                                     int(diard[2]),
                                     int(diard[3]) )
    for ii in range(len(diard)):
        lastdiard[ii]=diard[ii]

    return json_body,UDPMESSAGE





def extrn_decode_list4(respo):
    # ORTEC?
    diard = [0,0,0,0]
    debuor = False
    if debuor: print("ORTEC?")
    try:
        # - WAIT == % .... I need to remove leading 000000069\n
        # sometimes I catch  (%)000000069\n here....
        #                     i want to be permissible
        if debuor: print("0", respo)
        respo=respo.strip().split("\n")[-1]
        if debuor: print("1", respo )
        # -----then standard way to handle the 4 numbers
        diard=respo.strip().strip(";").split(";")
        if debuor: print("2",diard)
        diard=[  int(i.strip()) for i in diard]
        if debuor: print("3",diard)
        diard[3]  # -------this crashes if not ORTEC 3fields-------
        okortec = True
    except:
        okortec = False

    if debuor: print(okortec)
    return diard, okortec


def extrn_func( respo ):
    """
    this helps to recognise the type of comming data
    """
    respopr=respo
    respopr=respopr.replace("\n","'")
    respopr=respopr.replace("\r","'")

    # print in MAIN
    # print( "... /{}/ {}".format(respopr, ' '*10) , end="\r")

    okj = False     # json
    okj2 = False    # json with value1,2,loop
    okortec = False # ortec counter

    #----------------------JSON TYPE
    try:
        diard=json.loads(respo)
        okj = (type(diard)==dict)
        #print("D... is json")
    except ValueError:
        okj = False
        #print("D... is not json")

    if okj: # it is json
        try:
            diard=json.loads(respo)
            # I dont require anything
            # diard['loop'] # crashes the try if needed
            # diard["valuea0"]
            # diard['valuea1']
            okj2 = True
        except:
            okj2 = False

    #---------------------- ORTEC TYPE
    else:  # -n ot json :
        a, okortec = extrn_decode_list4(respo)

    if okj2:
        return "json"
    if okortec:
        return "list4"

    return None



def extrn_load_scriptlines( fname ):
    # 1.  #EOT:\r  define the ending character on listen
    # 2.  the last line will be repeated undefinitelly
    # 3.  #WAIT: defines waiting character ... % for ortec
    scriptlines=[]
    EOT = b'\r'
    WAIT = '%'
    with open( fname ) as f:
        cmds=f.readlines()
    for cmd in cmds:
        c=cmd.strip()
        print("S... ",c)
        if c.find("#")==0:
            # EOT:\r   .... end of transmission character (Ortec)
            if c.find("#EOT:"):
                EOT=c.split(":")[1] #
                EOT=EOT.replace('\\n','\n').replace('\\r','\r')
            continue # comment possible
        c=c.replace('\\n','\n').replace('\\r','\r')
        scriptlines.append(c)
    return scriptlines, EOT, WAIT



async def run( dev="/dev/ttyS0",
               baud=115200,
               code="word",
               sub_code="quasi;",
               timeout="1",
               influxyes=True,
               debug = False):
#"""
#listen  01 just await readline
## #mirror  02 repeat char
#word    03 read word; and return it
#"""
    global myname, dtloo3, STARTTAG, CPORT_UDP
    #def read_response():
    #    return respo

#     print("code")
#     print("    listen: nothing sent")
# #    print("    mirror: repeats one character")
#     print("    word  : repeats one word delimited by; Can read json arduino. Sends to UDP")
#     print("    script: sends set of lines, last inf., endofline is in #EOT ; ")
    print("="*80)
    print("    device \t  baud    \t  EOL    \t timeout \t influx       ")
    print("-"*80)
    print(" {:10s} \t {:10s} \t {:10s} \t {:10s} \t {}".format(dev,str(baud),
                                                         sub_code,
                                                         str(timeout),
                                                         influxyes) )
    print("-"*80)

    timeoutX = 99999
    if str(timeout).find(",")>0:
        #print("/{}/".format(timeout) )
        timeoutX = timeout[1]
        timeout  = timeout[0]


    dtcom=0.0 # com delay
    dtcorr2nd=0 # one time correction for 2nd passage
    dtcorrstat=0 # correction based onstatistics: from 5ms to <1ms
    dtstat=[ timeout ] # statistics of last 10 DTs
    start=dt.datetime.now()
    startdtc=start
    localtimeout=0.48942 # initial timeout - not to match -t
    reader, writer = await open_serial_connection(url=dev, baudrate=baud, timeout=2)


    scriptmode_passed=False
    scriptlines=[]
    EOT="\r"
    WAIT = '%'
    if code=="script":
        scriptlines,EOT,WAIT = extrn_load_scriptlines("script")

    never_influxed = True # for printout purpose
    last_sleep=0
    timeoutXstart=dt.datetime.now()
    new_serial_exception = True

    while True:

        writeThisTimeX = False # write only on timeoutX

        #print("w")
        dtloop=dt.datetime.now()-start
        dtloo2=dtloop.seconds+dtloop.microseconds/1e6
        # print("dtloo2",dtloo2)

        #may not be here but in  sleepfactory?
        if len(dtstat)>0:
            dtcorrstat=sum(dtstat)/len(dtstat) - timeout
        #print("D... DT={:.5f}      dtcorrstat={:.5f}".format(dtloo2,dtcorrstat) )

        #---------- here there must be sleep
        last_sleep = sleep_interval2( timeout , dtloo2,  sum(dtstat)/len(dtstat) )

        stop = dt.datetime.now()
        dtloop = stop - start

        dtloo3=dtloop.seconds+dtloop.microseconds/1e6
        #print("dtloo3",dtloo3)
        dtstat.append(dtloo3)
        if len(dtstat)>15: dtstat.pop(0) # stabilization over 10 measurements

        start=stop #-----starting new timer
        if (stop-timeoutXstart).total_seconds() > (timeoutX - timeout/2):
            #print() # later
            timeoutXstart = stop
            writeThisTimeX = True


        #======  listen/mirror/word behavior... use====
        #======  listen/mirror/word behavior... use====
        if code=="script":
            if debug: print("===",scriptlines)
            if len(scriptlines)>1:
                print("\nD... writing scriptline:",scriptlines[0].strip()  )
            writer.write(bytes( scriptlines[0], "utf-8"))
            if len(scriptlines)>1:
                scriptlines.pop(0) # remove the top line

        elif code=="word":
            if debug: print("D... writing",sub_code)
            writer.write(bytes(sub_code,'utf8'))

        # elif code=="mirror": # one character only
        #     writer.write(bytes(sub_code[0],'utf8')) # one_letter for mirror test

        else: # only listen
            a=1

        #==== listen by default =============== IN
        #   everytime, even without any command, there is a listen part
        #   both arduino nad ORTEC can work with \r endmark
        #   but I want to extend by EOT
        #    respo contains the mmessage


        print("{0:06.3f} #".format(dtloo3), end="",flush=True)
        line,respo='?',''
        #---------------------- default EOT byte is \r --------------
        empty_bytes=bytes(EOT, "utf8")   # test it before using!!!!
        #empty_bytes=b'\r' # THIS IS EOL FOR ORTEC, works for arduino too
        #-------------------  script can define extra wait byte ---------
        if code == "script":
            empty_bytes = bytes(WAIT, "utf8")
        while True:


            if debug: print("D... waiting for read")
            # this i did to avoid crash when bad tty is input.... (for port 8099 mode)
            try:
                line = await reader.read(1)
            except Exception as e:
                if new_serial_exception:
                    print("D... serial exception",e)
                    new_serial_exception = False
                line=empty_bytes
            if debug: print("D... line is read:", line)

            breakme = False
            if line == empty_bytes: # END OF TRANSMISSION
                break
            try:
                line=line.decode("utf8")
            except Exception as ex:
                print("D... exception= ",ex)
            #    line = ""
            #    print("X... undecoded character",line)
            #    breakme = True
            #if breakme:
            #    break
            # print(line)
            line=line.replace("\r","\n")
            respo=respo+line

            #if debug: print(line, end="", flush=True)

            time.sleep(0.000001) # was 0.0001
        #SAVE TIME TAG OF PC==========
        ftimetag=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f ")
        outtype = extrn_func( respo)
        TAG = "#"
        if outtype is None:
            TAG = "?"
        print(" {} {}".format( ftimetag[:-4], TAG ), end="",flush=True)#=========OUT


        #DDDDDDDDDDDDDDDDDD
        # print(outtype)

        ok2print = False
        if respo.find("measurement")>=0:
            ok2print = True
            respopr=respo.replace("\n","'").replace("\r","'")
            respopr=respopr.replace('"measurement":',"")
            respopr=respopr.replace('"command":',"")
            respopr=respopr.replace('"avg":',"")
            respopr=respopr.replace('"loop":',"")
            respopr=respopr.replace('value',"_")
            respopr=respopr.replace(" ","").replace('"','')

        if outtype=="list4":
            ok2print = True
            respopr=respo.replace("\n","'").replace("\r","'")

        if ok2print: #------------- printing-------------------------------
            reser = 48           # print in terminal width
            size = os.get_terminal_size()
            if len(respopr) + reser >size[0]:
                respopr=".."+respopr[ len(respopr)-(size[0]-reser) :]
            print( " /{}/ ".format(respopr) , end="")


        if outtype==None: ok=False
        if outtype=="json": ok=True

        # if list4: we must read the rest.... PROBABLY A PATCH THAT MAKES NO SENSENOW
        if outtype=="list4":
            ok = True
        # if outtype=="QQQlist4": # 4 fields ";"
        #     try:
        #         ok = False
        #         while True:
        #             empty_bytes=EOT # test it before using!!!!
        #             empty_bytes=b'\r' # THIS IS EOL FOR ORTEC, works for arduino too
        #             #if reader.inWaiting()>0:
        #             #if reader.in_waiting()>0:
        #             line = await reader.read(1)
        #             #print(line)
        #             if line == empty_bytes: break
        #             line=line.decode("utf8")
        #             line=line.replace("\r","\n")
        #             respo=respo+line
        #             #print(line, end="", flush=True)
        #             time.sleep(0.000001) # was 0.0001

        #         if len(diard)==5:
        #             ok=False # skips the error on ORTEC
        #             outtype = None #
        #         else:
        #             ok=True
        #     except:
        #         outtype = None #
        #         ok=False

        #--------------------------- done with output classifications----
        #---- if not ok (error in ortec, None type) : go back
        if not ok:
            print("    - ",end="\r")
            continue #------------------------first stop

        if outtype == "json":
            json_body,UDPMESSAGE = interpret_json( respo )
        if outtype == "list4":
            json_body,UDPMESSAGE = interpret_list4( respo )

        #------- JSON AND UDP READY HERE !
        #===============================>>>>>>>>>>>>>>> Threading SHOTS
        #===============================>>>>>>>>>>>>>>> Threading SHOTS
        #===============================>>>>>>>>>>>>>>> Threading SHOTS
        #===============================>>>>>>>>>>>>>>> Threading SHOTS

        #with open( os.path.expanduser("~/serial_NG2_udp"+STARTTAG+".log"),"a")  as f:
        with open( os.path.expanduser(OUT_udp+STARTTAG+".log"),"a")  as f:
            f.write( ftimetag[:-4]+" "+UDPMESSAGE+"\n" )

        #with open( os.path.expanduser("~/serial_NG2_jso"+STARTTAG+".log"),"a")  as f:
        with open( os.path.expanduser(OUT_json+STARTTAG+".log"),"a")  as f:
            f.write( ftimetag[:-4]+" "+json.dumps(json_body)+"\n" )

        # =======send UDP packet======= start
        if len(ipsudp)!=0:
            for IP in ipsudp:
                ip=IP.split(":")[0]
                port = CPORT_UDP
                try:
                    port=int(IP.split(":")[1])  # overrides the port number CPORT_UDP
                except:
                    port = CPORT_UDP
                x = threading.Thread(target=send_udp8081, args=(UDPMESSAGE,ip,port))
                x.start()
            #print("UDP{} ".format(len(ipsudp)), end="")  #  it breaks the nice lineing
        # ======= UDP thread sent ============ end
        # =======send INFLUX=========== start
        #print( "D...   ",ips,ips2, "... BOTH TOGETHER", [*ips,*ips2] )
        if writeThisTimeX:
            # - init everything, discover may changed
            init_influx_and_name(silent=False)
            init_udp_and_name()
            init_calibration(silent=True)

        if influxyes and writeThisTimeX :
            totinfl = 0
            for IP in [*ips,*ips2]:
                if never_influxed:
                    print("\nD...  influxed to IP: ",IP)
                if len(IP)<7:continue
                totinfl+=1
                x = threading.Thread(target=send_influx, args=(IP,json_body,))
                x.start()
            print("INFL{} ".format(totinfl) ,end="")
            never_influxed=False
        else:
            print("      " ,end="")
            # =======send INFLUX======= end
        if writeThisTimeX:
            print("  ",end="\n")
        else:
            print("  ",end="\r")







#def select_device(dev="/dev/ttyUSB0", loc="1-4", code="ortec"):
# def select_device(DEV="", loc="", code="", SUB_code="", timeout=10, baud=115200,
def select_device(DEV="", loc="", code="",  timeout=10, baud=115200,
                  influxyes=False, filesyes=False, serveryes=False, debug=False):
    ok=False
    devout=""
    devices=serial.tools.list_ports.comports()
    print("="*80)
    print(" ...      \t{:13s} \t{:10s}\t{:4s}:{:4s} \t {}".format("device" , "location", "vendor", "pid", "description" ) )
    print("-"*80)
    #if dev!="" or loc!="":
    #    print("*")
        #print("i... SELECT: \t{:13s} \t{} \t\t  ==>  \t code={}".format(
        #dev, loc, code)  )
        #print("-"*80)

    #====select -D device here
    for i in devices:
        ok=False
        #print("#{}#{}#".format(i.device,dev))
        #print(i, i.device,i.vid,i.pid, i.location, i.description)
        if (i.device == DEV) and  (loc==""):
            ok=True
        if (DEV == "") and  (i.location == loc):
            ok=True
        # print("/{}/{}/{}/".format(loc, i.location, DEV) )
        if not i.location is None:
            print(" ...    {}\t{:13s} \t{:10s}\t{:04x}:{:04x} \t {}".format( "*" if ok else " ", i.device , i.location, i.vid, i.pid, i.description ) )
        if ok: devout=i.device
    print("-"*80)

    SUB_code="empty;"
    if code=="":
        code="listen"
    if code.find("word")==0:
        SUB_code=code[4:]+";"
        code="word"
    #if SUB_code=="":
    #    SUB_code="empty;"

    if len(devout)>1:
        kill_tty_pid( devout )

    # # if no device selected
    # if (devout==""):
    #     print("D... A peculiar situation: your device is not in device's list")
    #     print("D... it is possible to create a virtual serial device (install socket)")
    #     print("D... ")
    #     print("D...  socat PTY,link=/tmp/virtser_connect,raw,echo=0 PTY,link=/tmp/virtser_speak,raw,echo=0")
    #     print("D... echo ahoj > /tmp/virtser_speak")
    #     print("D... and connect to  -D /tmp/virtser_connect")
    #     print("D...")
    #     # devout=DEV

    if (devout=="") and (DEV!=""):
        devout=DEV

    # print("return")
    return devout,code,SUB_code,timeout,baud, influxyes, filesyes, serveryes, debug
#------------ end of select device----------------------------





if __name__=="__main__":
    print("D... version :", __version__ )
    print("X... USE seread PLEASE")
    sys.exit(1)
#     print("D... use :  -D device OR  -l location  -c listen|mirror|word|script -b 19200")
#     print("D... e.g. ./sng2.py -l 2-1.1:1.0 -i false (to send no inlfux)")
#     print("                    -l is enough! , see the location of device")
#     print("-----MODES------")
#     print("    listen")
#     print("          - doesnt write anything")
# #    print("    mirror")
# #    print("          - Writes 'K' and listens")
#     print("    word")
#     print("          - Writes 'Slau;' and listens")
#     print("    script")
#     print("          - reads 'script' file, sends line by line. Last line for oo ")
#     #print("----------------")




#     res,code,sub_code,timeout,baudrate,influxyes,debug=Fire( select_device)   # FIRE HERE




#     print("D... DEVICE SELECTED=/{}/".format(res))
#     print("i... code     =",code)
#     print("i... subcode  =",sub_code)
#     print("i... timeout  =",timeout,"     can be 1,10 for new line every 10sec.")
#     print("i... baudrate =",baudrate)
#     print("i... influxyes=",influxyes)
#     print("i... debug    =",debug)
#     if res=="":quit()
#     if influxyes=="false":influxyes=False
#     #quit()
#     #======================================
#     init_udp_and_name() # prepare UDP server IP  ipsudp

#     if influxyes:
#         init_influx_and_name(silent=False) # prepare credentials
#     #else:
#     #    print("X... influx write False on commandline")
#     init_calibration()

#     #==========sserver
#     print("i... SERVER  RUNS..........")
#     x = threading.Thread(target=sserver, args=(SHOST, SPORT))
#     x.start()
#     #==================================== RUN=============
#     loop = get_event_loop()
#     loop.run_until_complete( run( res, baudrate, code ,sub_code, timeout, influxyes ,debug) )
