#
# PyDBG
# Copyright (C) 2006 Pedram Amini <pedram.amini@gmail.com>
#
# $Id: defines.py 224 2007-10-12 19:51:45Z aportnoy $
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
#
# windows_h.py was generated with:
#
#    c:\Python\Lib\site-packages\ctypes\wrap
#    c:\python\python h2xml.py windows.h -o windows.xml -q -c
#    c:\python\python xml2py.py windows.xml -s DEBUG_EVENT -s CONTEXT -s MEMORY_BASIC_INFORMATION -s LDT_ENTRY \
#        -s PROCESS_INFORMATION -s STARTUPINFO -s SYSTEM_INFO -o windows_h.py
#
# Then the import of ctypes was changed at the top of the file to utilize my_ctypes, which adds the necessary changes
# to support the pickle-ing of our defined data structures and ctype primitives.
#

from ctypes import *

HANDLE = c_void_p
LPVOID = c_void_p
DWORD = c_ulong
WORD = c_ushort
CHAR = c_char
ULONG = c_ulong 
LPSTR = POINTER(CHAR)
BYTE = c_char 
LPBYTE = POINTER(BYTE)

LPTHREAD_START_ROUTINE = WINFUNCTYPE(DWORD, LPVOID)


#http://msdn.microsoft.com/en-us/library/windows/desktop/ms684873(v=vs.85).aspx
class ProcessInfo(Structure):
    _fields_ = [('hProcess', HANDLE),
                ('hThread', HANDLE),
                ('dwProcessId', DWORD),
                ('dwThreadId', DWORD),
               ]

#http://msdn.microsoft.com/en-us/library/windows/desktop/ms686331(v=vs.85).aspx
class StartupInfo(Structure):
    _fields_ = [ ('cb', DWORD),
            ('lpReserved', LPSTR),
            ('lpDesktop', LPSTR),
            ('lpTitle', LPSTR),
            ('dwX', DWORD),
            ('dwY', DWORD),
            ('dwXSize', DWORD),
            ('dwYSize', DWORD),
            ('dwXCountChars', DWORD),
            ('dwYCountChars', DWORD),
            ('dwFillAttribute', DWORD),
            ('dwFlags', DWORD),
            ('wShowWindow', WORD),
            ('cbReserved2', WORD),
            ('lpReserved2', LPBYTE),
            ('hStdInput', HANDLE),
            ('hStdOutput', HANDLE),
            ('hStdError', HANDLE),
            ]     

#http://msdn.microsoft.com/en-us/library/windows/desktop/aa363082(v=vs.85).aspx
class EXCEPTION_RECORD(Structure):
    pass

EXCEPTION_RECORD._fields_ =  [('ExceptionCode', DWORD),
                              ('ExceptionFlags', DWORD),
                              ('ExceptionRecord', POINTER(EXCEPTION_RECORD)),
                              ('ExceptionAddress', LPVOID),
                              ('NumberParameters', DWORD),
                              ('ExceptionInformation', POINTER(ULONG) * 15),
                             ]


#http://msdn.microsoft.com/en-us/library/windows/desktop/ms679326(v=vs.85).aspx
class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [('ExceptionRecord', EXCEPTION_RECORD),
                ('dwFirstChance', DWORD),
               ]

#http://msdn.microsoft.com/en-us/library/windows/desktop/ms679287(v=vs.85).aspx
class CREATE_THREAD_DEBUG_INFO(Structure):
    _fields_ = [ ('hThread', HANDLE),
                 ('lpThreadLocalBase', LPVOID),
                 ('lpStartAddress', LPTHREAD_START_ROUTINE),
               ]

#
class POSIBLE_DEBUG_EVENT(Union):
    _fields_ = [('Exception', EXCEPTION_DEBUG_INFO),
                ]
#http://msdn.microsoft.com/en-us/library/windows/desktop/ms679308(v=vs.85).aspx
class DEBUG_EVENT(Structure):
    _fields_ = [('dwDebugEventCode', DWORD),
                ('dwProcessId', DWORD),
                ('dwThreadId', DWORD),
                ('u', POSIBLE_DEBUG_EVENT)
               ]


###
### manually declare various #define's as needed.
###

# debug event codes.
EXCEPTION_DEBUG_EVENT          = 0x00000001
CREATE_THREAD_DEBUG_EVENT      = 0x00000002
CREATE_PROCESS_DEBUG_EVENT     = 0x00000003
EXIT_THREAD_DEBUG_EVENT        = 0x00000004
EXIT_PROCESS_DEBUG_EVENT       = 0x00000005
LOAD_DLL_DEBUG_EVENT           = 0x00000006
UNLOAD_DLL_DEBUG_EVENT         = 0x00000007
OUTPUT_DEBUG_STRING_EVENT      = 0x00000008
RIP_EVENT                      = 0x00000009
USER_CALLBACK_DEBUG_EVENT      = 0xDEADBEEF     # added for callback support in debug event loop.

# debug exception codes.
#http://msdn.microsoft.com/en-us/library/windows/desktop/aa363082(v=vs.85).aspx
#codes number in http://svn.netlabs.org/repos/odin32/trunk/include/exceptions.h 
EXCEPTION_ACCESS_VIOLATION      = 0xC0000005
EXCEPTION_ARRAY_BOUNDS_EXCEEDED = 0xC000008C
EXCEPTION_BREAKPOINT            = 0x80000003
EXCEPTION_DATATYPE_MISALIGNMENT = 0x80000002
#EXCEPTION_FLT_DIVIDE_BY_ZERO   = 0xC000008e
#EXCEPTION_FLT_INVALID_OPERATION= 0xC0000090
#EXCEPTION_FLT_OVERFLOW         = 0xC0000091
#EXCEPTION_FLT_STACK_CHECK      = 0xC0000092
EXCEPTION_ILLEGAL_INSTRUCTION   = 0xC000001d
EXCEPTION_IN_PAGE_ERROR         = 0xC0000006
#EXCEPTION_INT_DIVIDE_BY_ZERO   = 0xC0000094                 
#EXCEPTION_INT_OVERFLOW         = 0xC0000095
EXCEPTION_NONCONTINUABLE_EXCEPTION = 0xC0000025
EXCEPTION_PRIV_INSTRUCTION     = 0xC0000096
#EXCEPTION_SINGLE_STEP          = 0x80000004
EXCEPTION_STACK_OVERFLOW       = 0xC00000FD

# hw breakpoint conditions
HW_ACCESS                      = 0x00000003
HW_EXECUTE                     = 0x00000000
HW_WRITE                       = 0x00000001

CONTEXT_CONTROL                = 0x00010001
CONTEXT_FULL                   = 0x00010007
CONTEXT_DEBUG_REGISTERS        = 0x00010010
CREATE_NEW_CONSOLE             = 0x00000010
DBG_CONTINUE                   = 0x00010002
DBG_EXCEPTION_NOT_HANDLED      = 0x80010001
DBG_EXCEPTION_HANDLED          = 0x00010001
DEBUG_PROCESS                  = 0x00000001
DEBUG_ONLY_THIS_PROCESS        = 0x00000002
EFLAGS_RF                      = 0x00010000
EFLAGS_TRAP                    = 0x00000100
ERROR_NO_MORE_FILES            = 0x00000012
FILE_MAP_READ                  = 0x00000004
FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
FORMAT_MESSAGE_FROM_SYSTEM     = 0x00001000
INVALID_HANDLE_VALUE           = 0xFFFFFFFF
MEM_COMMIT                     = 0x00001000
MEM_DECOMMIT                   = 0x00004000
MEM_IMAGE                      = 0x01000000
MEM_RELEASE                    = 0x00008000
PAGE_NOACCESS                  = 0x00000001
PAGE_READONLY                  = 0x00000002
PAGE_READWRITE                 = 0x00000004
PAGE_WRITECOPY                 = 0x00000008
PAGE_EXECUTE                   = 0x00000010
PAGE_EXECUTE_READ              = 0x00000020
PAGE_EXECUTE_READWRITE         = 0x00000040
PAGE_EXECUTE_WRITECOPY         = 0x00000080
PAGE_GUARD                     = 0x00000100
PAGE_NOCACHE                   = 0x00000200
PAGE_WRITECOMBINE              = 0x00000400
PROCESS_ALL_ACCESS             = 0x001F0FFF
SE_PRIVILEGE_ENABLED           = 0x00000002
SW_SHOW                        = 0x00000005
THREAD_ALL_ACCESS              = 0x001F03FF
TOKEN_ADJUST_PRIVILEGES        = 0x00000020
UDP_TABLE_OWNER_PID            = 0x00000001
VIRTUAL_MEM                    = 0x00003000

