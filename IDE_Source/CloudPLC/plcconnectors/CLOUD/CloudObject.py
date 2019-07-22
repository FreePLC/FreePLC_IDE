#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Cloud connector, based on LPCObject.py and LPCAppObjet.py
# from PLCManager


import os
import sys
import struct

if __name__ == "__main__":
    __builtins__.BMZ_DBG = True
    append_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    sys.path.append(append_path)

from threading import Lock
import ctypes
from CloudProto import *
from targets.typemapping import LogLevelsCount, TypeTranslator, UnpackDebugBuffer
from util.ProcessLogger import ProcessLogger

import pdb


class CloudObject():
    def __init__(self, libfile, confnodesroot, comportstr):

        self.TransactionLock = Lock()
        self.PLCStatus = "Disconnected"
        self.libfile = libfile
        self.confnodesroot = confnodesroot
        self.PLCprint = confnodesroot.logger.writeyield
        self._Idxs = []

        self.TransactionLock.acquire()
        try:
            self.connect(libfile, comportstr, 115200, 20)
        except Exception, e:
            self.confnodesroot.logger.write_error(str(e) + "\n")
            self.SerialConnection = None
            self.PLCStatus = None  # ProjectController is responsible to set "Disconnected" status
        self.TransactionLock.release()

    def connect(self, libfile, comportstr, baud, timeout):
        self.SerialConnection = CloudProto(libfile, comportstr, baud, timeout)

    def read_project(self, data_dir):
        return open(os.path.join(data_dir)).read()

    def _HandleSerialTransaction(self, transaction, must_do_lock):
        res = None
        failure = None
        # Must acquire the lock
        if must_do_lock:
            self.TransactionLock.acquire()
        if self.SerialConnection is not None:
            # Do the job
            try:
                self.PLCStatus, res = \
                    self.SerialConnection.HandleTransaction(transaction)
            except CloudProtoError, e:
                if self.SerialConnection is not None:
                    self.SerialConnection.Close()
                    self.SerialConnection = None
                failure = str(transaction) + str(e)
                self.PLCStatus = None  # ProjectController is responsible to set "Disconnected" status
            except Exception, e:
                failure = str(transaction) + str(e)
        # Must release the lock
        if must_do_lock:
            self.TransactionLock.release()
        return res, failure

    def HandleSerialTransaction(self, transaction):
        res = None;
        failure = None;
        res, failure = self._HandleSerialTransaction(transaction, True)
        if failure is not None:
            print(failure + "\n")
            self.confnodesroot.logger.write_warning(failure + "\n")
        return res

    def StartPLC(self):
        self.HandleSerialTransaction(STARTTransaction())

    def StopPLC(self):
        self.HandleSerialTransaction(STOPTransaction())
        return True

    def NewPLC(self, md5sum, data, extrafiles):
        if self.MatchMD5(md5sum) == False:
            res = None;
            status = None;
            self.TransactionLock.acquire()
            projectbin = self.read_project(data[0])
            #cmd = [token % {"serial_port": self.SerialConnection.port} for token in data]
            self._HandleSerialTransaction(STOPTransaction(), False)
            self._HandleSerialTransaction(SETRTCTransaction(), False)

            length = os.path.getsize(data[0])
            remainder = length % 8

            with open(data[0], 'ab+') as f:
                if remainder == 1:
                    f.write('\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
                    length = ((length/8)+1)*8
                elif remainder == 2:
                    f.write('\xFF\xFF\xFF\xFF\xFF\xFF')
                    length = ((length/8)+1)*8
                elif remainder == 3:
                    f.write('\xFF\xFF\xFF\xFF\xFF')
                    length = ((length/8)+1)*8
                elif remainder == 4:
                    f.write('\xFF\xFF\xFF\xFF')
                    length = ((length/8)+1)*8
                elif remainder == 5:
                    f.write('\xFF\xFF\xFF')
                    length = ((length/8)+1)*8
                elif remainder == 6:
                    f.write('\xFF\xFF')
                    length = ((length/8)+1)*8
                elif remainder == 7:
                    f.write('\xFF')
                    length = ((length/8)+1)*8
                else:
                    length = ((length/8))*8
                f.seek(0,0)
                checksum = 0
                i = 0
                loop = length/8
                status, res = self._HandleSerialTransaction(SET_ProjectBlockTransaction(loop), False)
                time.sleep(1)
                while loop:
                    temp_data = f.read(8)
                    status, res = self._HandleSerialTransaction(SET_ProjectBinTransaction(i, temp_data), False)
                    buffer_data, = struct.unpack('Q', temp_data)
                    checksum += buffer_data
                    loop -= 1
                    i= i + 1
                    #if (i%100) == 0:
                        #print('.')
                    #time.sleep(0.001)
                checksum &= ((1 << 64 ) - 1)
                #temp_data = struct.pack('Q', checksum)
                status, res = self._HandleSerialTransaction(SET_ProjectChecksumTransaction(checksum), False)
                time.sleep(0.01)
                status, res = self._HandleSerialTransaction(GET_DOWNLOADSTATUSTransaction(), False)
                if res is not None and len(res) >= 4:
                    res = res
                f.close()
            self.TransactionLock.release()
        else:
            self.StopPLC();
            return self.PLCStatus == "Stopped"
        return self.PLCStatus

    def GetPLCstatus(self):
        strcounts = self.HandleSerialTransaction(GET_LOGCOUNTSTransaction())
        if strcounts is not None and len(strcounts) == LogLevelsCount * 4:
            cstrcounts = ctypes.create_string_buffer(strcounts)
            ccounts = ctypes.cast(cstrcounts, ctypes.POINTER(ctypes.c_uint32))
            counts = [int(ccounts[idx]) for idx in xrange(LogLevelsCount)]
        else:
            counts = [0] * LogLevelsCount
        return self.PLCStatus, counts

    def MatchMD5(self, MD5):
        self.MatchSwitch = False
        data = self.HandleSerialTransaction(GET_PLCIDTransaction())
        self.MatchSwitch = True
        if data is not None:
            return data[:32] == MD5[:32]
        return False

    def SetTraceVariablesList(self, idxs):
        """
        Call ctype imported function to append
        these indexes to registred variables in PLC debugger
        """
        if idxs:
            buff = ""
            # keep a copy of requested idx
            self._Idxs = idxs[:]
            for idx, iectype, force in idxs:
                idxstr = ctypes.string_at(
                    ctypes.pointer(
                        ctypes.c_uint32(idx)), 4)
                if force != None:
                    c_type, unpack_func, pack_func = TypeTranslator.get(iectype, (None, None, None))
                    forced_type_size = ctypes.sizeof(c_type) \
                        if iectype != "STRING" else len(force) + 1
                    forced_type_size_str = chr(forced_type_size)
                    forcestr = ctypes.string_at(
                        ctypes.pointer(
                            pack_func(c_type, force)),
                        forced_type_size)
                    buff += idxstr + forced_type_size_str + forcestr
                else:
                    buff += idxstr + chr(0)
        else:
            buff = ""
            self._Idxs = []
        self.HandleSerialTransaction(SET_TRACE_VARIABLETransaction(buff))

    def GetTraceVariables(self):
        """
        Return a list of variables, corresponding to the list of required idx
        """
        strbuf = self.HandleSerialTransaction(GET_TRACE_VARIABLETransaction())
        TraceVariables = []
        if strbuf is not None and len(strbuf) >= 4 and self.PLCStatus == "Started":
            size = len(strbuf) - 4
            ctick = ctypes.create_string_buffer(strbuf[:4])
            tick = ctypes.cast(ctick, ctypes.POINTER(ctypes.c_uint32)).contents
            if size > 0:
                cbuff = ctypes.create_string_buffer(strbuf[4:])
                buff = ctypes.cast(cbuff, ctypes.c_void_p)
                TraceBuffer = ctypes.string_at(buff.value, size)
                # Add traces
                TraceVariables.append((tick.value, TraceBuffer))
        return self.PLCStatus, TraceVariables

    def ResetLogCount(self):
        self.HandleSerialTransaction(RESET_LOGCOUNTSTransaction())


    def GetLogMessage(self, level, msgid):
        strbuf = self.HandleSerialTransaction(GET_LOGMSGTransaction(level, msgid))
        if strbuf is not None and len(strbuf) > 12:
            cbuf = ctypes.cast(
                ctypes.c_char_p(strbuf[:12]),
                ctypes.POINTER(ctypes.c_uint32))
            return (strbuf[12:],) + tuple(int(cbuf[idx]) for idx in range(3))
        return None

    def ForceReload(self):
        raise CloudProtoError("Not implemented")

    def RemoteExec(self, script, **kwargs):
        return (-1, "RemoteExec is not supported by Cloud target!")


if __name__ == "__main__":
    """
    "C:\Program Files\Beremiz\python\python.exe" CloudObject.py
    """


    class TestLogger():
        def __init__(self):
            self.lock = Lock()

        def write(self, v):
            self.lock.acquire()
            print(v)
            self.lock.release()

        def writeyield(self, v):
            self.lock.acquire()
            print(v)
            self.lock.release()

        def write_warning(self, v):
            if v is not None:
                self.lock.acquire()
                msg = "Warning: " + v
                print(msg)
                self.lock.release()

        def write_error(self, v):
            if v is not None:
                self.lock.acquire()
                msg = "Warning: " + v
                print(msg)
                self.lock.release()


    class TestRoot:
        def __init__(self):
            self.logger = TestLogger()


    if os.name in ("nt", "ce"):
        lib_ext = ".dll"
    else:
        lib_ext = ".so"

    TstLib = os.path.dirname(os.path.realpath(__file__)) + "/../../../YaPySerial/bin/libYaPySerial" + lib_ext
    if (os.name == 'posix' and not os.path.isfile(TstLib)):
        TstLib = "libYaPySerial" + lib_ext

    TstRoot = TestRoot()
    print "Construct PLC..."
    TstPLC = CloudObject(TstLib, TstRoot, "COM10")

    print "Start PLC..."
    res = TstPLC.StartPLC()
    print(res)

    print "Get PLC status..."
    res = TstPLC.GetPLCstatus();
    print(res)

    print "MatchMD5..."
    res = TstPLC.MatchMD5("aaabbb")
    print(res)

    print "MatchMD5..."
    res = TstPLC.MatchMD5("2c2700c2c543f64e93747d21277de8fdUnknown#Uncnown#Uncnown")
    print(res)

    print "SetTraceVariablesList..."
    idxs = []
    idxs.append((0, "BOOL", 1))
    idxs.append((1, "BOOL", 1))
    res = TstPLC.SetTraceVariablesList(idxs)
    print(res)

    print "GetTraceVariables..."
    res = TstPLC.GetTraceVariables()
    print(res)

    print "GetLogMessage..."
    res = TstPLC.GetLogMessage(0, 0)
    print(res)

    print "ResetLogCount..."
    TstPLC.ResetLogCount()

    TstPLC.StopPLC()

    time.sleep(3)
