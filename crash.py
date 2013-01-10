'''
A simple debugging loop using ctypes.
This detects if the debugee crashes, timeouts or is closed normally.

Described in detail in this blog post:
http://blog.binamuse.com/2013/01/a-micro-windows-crash-catcher-in-python.html
Author: Joshep C.S. 

Defines stolen from pydbg.
'''
from ctypes import *
from defines import *
from time import time, sleep
import sys

kernel32 = windll.kernel32

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python deburger.py "command_line" '

    cmd = sys.argv[1]
    timeout = 10

    pi = ProcessInfo()
    si = StartupInfo()
    #Running cmd in a new process 
    #http://msdn.microsoft.com/en-us/library/windows/desktop/ms682425(v=vs.85).aspx
    success = kernel32.CreateProcessA(c_char_p(0),  #cmd must not be None
                                      c_char_p(cmd),
                                      0,
                                      0,
                                      0,
                                      1,            #follow forks 
                                      0,
                                      0,
                                      byref(si),
                                      byref(pi))

    if not success:
        print "[*] Process \"%s\" failed  " % cmd
        print kernel32.GetLastError()
        exit(-1)

    pids = None
    closed = "Normal"
    maxTime = time() + timeout

    dwContinueStatus = DBG_CONTINUE
    debug = DEBUG_EVENT()

    while pids is None or pids:
        #Wait for a debugging event to occur. The second parameter indicates
        #that the function does not return until a debugging event occurs. 
        if kernel32.WaitForDebugEvent(byref(debug), 100):
            #Process the debugging event code.
            if debug.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                #Process the exception code. When handling 
                #exceptions, remember to set the continuation 
                #status parameter (dwContinueStatus). This value 
                #is used by the ContinueDebugEvent function. 
                if debug.u.Exception.ExceptionRecord.ExceptionCode in \
                                              [ EXCEPTION_ACCESS_VIOLATION, 
                                                EXCEPTION_ARRAY_BOUNDS_EXCEEDED,
                                                EXCEPTION_DATATYPE_MISALIGNMENT,
                                                EXCEPTION_ILLEGAL_INSTRUCTION,
                                                EXCEPTION_IN_PAGE_ERROR,
                                                EXCEPTION_PRIV_INSTRUCTION,
                                                EXCEPTION_STACK_OVERFLOW ]:
                    print 'EXCEPTION CODE:', hex(debug.u.Exception.ExceptionRecord.ExceptionCode)
                    closed  = 'Crashed'
                else:
                    dwContinueStatus = DBG_EXCEPTION_NOT_HANDLED
                             
            elif debug.dwDebugEventCode == CREATE_PROCESS_DEBUG_EVENT:
                if pids is None:
                    pids = []
                pids.append(debug.dwProcessId)               
            elif debug.dwDebugEventCode == EXIT_PROCESS_DEBUG_EVENT:
                pids.remove(debug.dwProcessId)
              
        #If crashed or the timeout was reached
        #Close all processes in the debugge loop.    
        if maxTime < time() or closed == 'Crashed':
            if closed != 'Crashed':
                closed = 'Timeout'
            #http://msdn.microsoft.com/en-us/library/windows/desktop/ms686714(v=vs.85).aspx
            for pid in reversed(pids):
                handle = kernel32.OpenProcess(1, 0, pid)
                kernel32.TerminateProcess(handle,0)
                kernel32.CloseHandle(handle)

        #http://msdn.microsoft.com/en-us/library/windows/desktop/ms679285(v=vs.85).aspx 
        kernel32.ContinueDebugEvent(debug.dwProcessId, debug.dwThreadId, dwContinueStatus)

    print 'Exit Process:' , closed

##################################################################################################
