import sys
import io
import os
import datetime

def read(file_thing) -> [str]:
    if isinstance(file_thing, io.TextIOBase):
        return file_thing.readlines()
    if isinstance(file_thing, str):
        if file_thing.count('\n') > 0:
            return file_thing # list-thing
        else:
            with open(file_thing, "r", encoding='iso-8859-1') as f:
                return f.readlines()
    raise ValueError("Cannot read data from " + str(type(file_thing)))

def open_read_file(name, mode:str="r", encoding='iso-8859-1') -> io.TextIOBase:
    return open(name, mode, encoding=encoding)


def print_str(x, f=sys.stdout):    
    f.write(x)
    f.write('\n')


tracelevel = 4
log_handle = None

file=sys.stdout

def trace(level:int, *args):
    def fix_linendings(s: str) -> str:
        if os.linesep == '\n':
            return s
        p = 0
        while True:
            p = s.find('\n', p+1)
            if p<0: break
            if p>0 and s[p-1] != '\r':
                s = s[:p] + '\r' + s[p:]
        return s

    def mystr(thing):
        if isinstance(thing, (list, tuple)):
            msg = []
            prefix = ''

            if len(thing) <= 4:
               separator = ', '
            else:
               separator = (os.linesep+"   ")
               prefix = separator

            for s in thing:
                msg += [mystr(s)]
            return prefix + separator.join(msg)

        elif isinstance(thing, datetime.datetime):
            return thing.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(thing, datetime.date):
            return thing.strftime("%Y-%m-%d")
        #elif isinstance(thing, bytes):
        #    return bytes.decode('utf-8')
        else:
            try:
                if isinstance(thing, bytes):
                    s = thing.decode('utf-8')
                else:
                    s = str(thing)
                s = fix_linendings(s)
                return s
            except UnicodeEncodeError:
                return str(thing).encode('ascii', 'ignore')
            except Exception as ex:
                return 'Failed to format thing as string caught ' + str(ex)

    #if tracelevel < level:
    #    return

    msg = datetime.datetime.now().strftime("%H:%M:%S: ")
    for thing in args:
        msg += mystr(thing)

    msg = msg.rstrip()

    file.write( msg )

    # handle = file if not file is None else ( sys.stderr if log_handle is None  else log_handle )
    # try:
    #     print(msg, file=handle)
    # except TypeError:
    #     file.write( handle, msg )
    # except UnicodeEncodeError:
    #     os.write( handle, msg.encode('cp850', errors='replace'))


def pretty(value,htchar="\t",lfchar="\n",indent=0):
  if type(value) in [dict]:
    return "{%s%s%s}"%(",".join(["%s%s%s: %s"%(lfchar,htchar*(indent+1),repr(key),pretty(value[key],htchar,lfchar,indent+1)) for key in value]),lfchar,(htchar*indent))
  elif type(value) in [list,tuple]:
    return (type(value)is list and "[%s%s%s]" or "(%s%s%s)")%(",".join(["%s%s%s"%(lfchar,htchar*(indent+1),pretty(item,htchar,lfchar,indent+1)) for item in value]),lfchar,(htchar*indent))
  else:
    return repr(value)

def expand_string(s:[str]) -> str:
    s = os.path.expandvars(s)
    dt = s.find('${DATETIME}')
    if dt >= 0:
        s = s[:dt] + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + s[dt+11:]
    dt = s.find('${DATE}')
    if dt >= 0:
        s = s[:dt] + datetime.datetime.now().strftime("%Y%m%d") + s[dt+7:]
    dt = s.find('${TIME}')
    if dt >= 0:
        s = s[:dt] + datetime.datetime.now().strftime("%H%M%S") + s[dt+7:]

    return s
    