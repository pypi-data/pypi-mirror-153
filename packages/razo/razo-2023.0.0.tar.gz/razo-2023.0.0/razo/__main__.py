# coding=utf-8

import datetime
import os
import sys
import time as tm
import numpy as np
import password as pw

try:
    env = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + '\\.razo_nt\\'
except KeyError as fru:
    env = os.environ['HOME'] + '/.razo_nt/'

try:
    from razo_langpack import pack
except ModuleNotFoundError as aheddew:
    from razo_langpack_d import pack
vers = ['2023.0.0', 'time-1']

class Memory:
    def __init__(self,name):
        self.name=name
        self.__data={}
    def add(self,datas):
        for i,j in datas.items():
            self.__data[i]=j
    def remove(self,*key):
        for i in key:
            self.__data.pop(i)
    def get(self):
        return self.__data
    def clear(self):
        self.__data={}
class razo_p:
    password = pw.Password(method='sha512', hash_encoding='base64')

read1='';read2=''
rooting = False;sudoroot = False;nowsudo = False;nowuser='None'

try:
    if sys.argv[1] == '-root':
        rooting = True
except IndexError as inddde:
    rooting = False
liense = pack[0]


def __etting__():
    ld = {}
    print(pack[1])
    print(liense)
    a = input(pack[2])
    if a == 'n':
        print(pack[3])
        tm.sleep(5)
        sys.exit(0)
    a=input(pack[27])
    ld['machine']=a
    print(pack[4])
    while True:
        a = input('\033[0;30;40m')
        print('\033[0;37;40m')
        d = input(pack[25] + '\033[0;30;40m')
        print('\033[0;37;40m')
        if a!=d:
            print(pack[24])
        else:
            break
    c = razo_p()
    c.password = a
    ld['users']={}
    ld['users']['root']=c
    print(pack[26])
    while True:
        while True:
            b=input(pack[22])
            c=input(pack[23]+'\033[0;30;40m')
            print('\033[0;37;40m')
            d=input(pack[25]+'\033[0;30;40m')
            print('\033[0;37;40m')
            if c==d:
                break
            else:
                print(pack[24])
        f=razo_p()
        f.password=c
        ld['users'][b]=f
        e=input(pack[21])
        if e=='y':
            continue
        else:
            break

    a=Memory('razo_datas')

    a.add(ld)
    np.save(env + 'settings.npy', a)


def showinfo():
    listget = pack[13]
    timer = datetime.datetime.now()
    weekday = listget[timer.weekday()]
    print(timer.strftime(pack[14]) + ' {}'.format(weekday))
    print('Razo {0}({1}) @{2}'.format(vers[0], vers[1],read1))



h = pack[8]




def help():
    print(h)


def su():
    global rooting
    if rooting or nowsudo:
        return 0
    a = input(pack[9] + '\033[8;37;40m')
    print('\033[0;37;40m')
    if read2['root'].password == a:
        rooting = True
        return 0
    else:
        tm.sleep(2)
        print(pack[10])


def shutdown():
    if rooting:
        yes = input(pack[11])
        if yes == 'y':
            print(pack[12])
            tm.sleep(5)
            sys.exit(0)
    else:
        print(pack[15])


def setting():
    global rooting
    if rooting:
        __etting__()
        rooting = False
    else:
        print(pack[15])


def time():
    listget = pack[13]
    timer = datetime.datetime.now()
    weekday = listget[timer.weekday()]
    print(timer.strftime(pack[14]) + ' {}'.format(weekday))


def info():
    showinfo()


def __wai__(b):
    b_list = ['__etting__', '__wai__', '__main_p__', '__out_and_in__', '__getin__']
    c=b.split(';')
    global nowsudo
    for a in c:
        if a in b_list:
            os.system(a)
            return 0
        elif a == 'exit':
            print('No way!')
            return 0
        elif a=='logoff':
            return 50
        try:
            exec(a + '()')
        except (SyntaxError, NameError) as abcddd:
            try:
                dc = os.system(a)
                tm.sleep(0.5)
                print(pack[20].format(dc))
            except SystemExit as fhuuuifr:
                pass

def __main_p__():
    global rooting
    global nowuser
    while True:
        nowuser=input(pack[22])
        if nowuser in read2:
            b=input(pack[23]+'\033[8;37;40m')
            print('\033[0;37;40m')
            if read2[nowuser].password==b:
                if nowuser=='root':
                    rooting=True
                break
            else:
                print(pack[24])
                continue
        else:
            print(pack[24])
            continue
    print(pack[6])

    while True:
        if not rooting:
            a=input('[{0}@{1}]>>> '.format(nowuser,read1))
        else:
            a = input('[{0}@{1}]>>> '.format('root', read1))

        getds=__wai__(a)
        if getds==50:
            __out_and_in__()

def __out_and_in__():
    global nowuser
    nowuser=None
    showinfo()
    __main_p__()

def __getin__():
    global read1
    global read2
    if not os.path.exists(env):
        os.mkdir(env)
        __etting__()
    try:
        read1=np.load(env + 'settings.npy', allow_pickle=True).item().get()['machine']
        read2 = np.load(env + 'settings.npy', allow_pickle=True).item().get()['users']
    except (FileNotFoundError,KeyError) as nots:
        __etting__()
        read1 = np.load(env + 'settings.npy', allow_pickle=True).item().get()['machine']
        read2 = np.load(env + 'settings.npy', allow_pickle=True).item().get()['users']
    showinfo()
    __main_p__()


if __name__ == '__main__':
    __getin__()
