from __future__ import with_statement
from __future__ import absolute_import
import sys
import io
import os
import datetime
from io import open

def read(file_thing):
    if isinstance(file_thing, io.TextIOBase):
        return file_thing.readlines()
    if isinstance(file_thing, unicode):
        if file_thing.count(u'\n') > 0:
            return file_thing # list-thing
        else:
            with open(file_thing, u"r", encoding=u'iso-8859-1') as f:
                return f.readlines()
    raise ValueError(u"Cannot read data from " + unicode(type(file_thing)))

def open_read_file(name, mode=u"r", encoding=u'iso-8859-1'):
    return open(name, mode, encoding=encoding)


def print_str(x, f=sys.stdout):    
    f.write(x)
    f.write(u'\n')


tracelevel = 4
log_handle = None

log_output=sys.stdout

def trace(level, *args, **_3to2kwargs):
    if 'file' in _3to2kwargs: file = _3to2kwargs['file']; del _3to2kwargs['file']
    else: file = log_output
    def fix_linendings(s):
        if os.linesep == u'\n':
            return s
        p = 0
        while True:
            p = s.find(u'\n', p+1)
            if p<0: break
            if p>0 and s[p-1] != u'\r':
                s = s[:p] + u'\r' + s[p:]
        return s

    def mystr(thing):
        if isinstance(thing, (list, tuple)):
            msg = []
            prefix = u''

            if len(thing) <= 4:
               separator = u', '
            else:
               separator = (os.linesep+u"   ")
               prefix = separator

            for s in thing:
                msg += [mystr(s)]
            return prefix + separator.join(msg)

        elif isinstance(thing, datetime.datetime):
            return thing.strftime(u"%Y-%m-%d %H:%M:%S")
        elif isinstance(thing, datetime.date):
            return thing.strftime(u"%Y-%m-%d")
        #elif isinstance(thing, bytes):
        #    return bytes.decode('utf-8')
        else:
            try:
                if isinstance(thing, str):
                    s = thing.decode(u'utf-8')
                else:
                    s = unicode(thing)
                s = fix_linendings(s)
                return s
            except UnicodeEncodeError:
                return unicode(thing).encode(u'ascii', u'ignore')
            except Exception, ex:
                return u'Failed to format thing as string caught ' + unicode(ex)

    #if tracelevel < level:
    #    return

    msg = datetime.datetime.now().strftime(u"%H:%M:%S: ")
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


def pretty(value,htchar=u"\t",lfchar=u"\n",indent=0):
  if type(value) in [dict]:
    return u"{%s%s%s}"%(u",".join([u"%s%s%s: %s"%(lfchar,htchar*(indent+1),repr(key),pretty(value[key],htchar,lfchar,indent+1)) for key in value]),lfchar,(htchar*indent))
  elif type(value) in [list,tuple]:
    return (type(value)is list and u"[%s%s%s]" or u"(%s%s%s)")%(u",".join([u"%s%s%s"%(lfchar,htchar*(indent+1),pretty(item,htchar,lfchar,indent+1)) for item in value]),lfchar,(htchar*indent))
  else:
    return repr(value)

def expand_string(s):
    s = os.path.expandvars(s)
    dt = s.find(u'${DATETIME}')
    if dt >= 0:
        s = s[:dt] + datetime.datetime.now().strftime(u"%Y%m%d_%H%M%S") + s[dt+11:]
    dt = s.find(u'${DATE}')
    if dt >= 0:
        s = s[:dt] + datetime.datetime.now().strftime(u"%Y%m%d") + s[dt+7:]
    dt = s.find(u'${TIME}')
    if dt >= 0:
        s = s[:dt] + datetime.datetime.now().strftime(u"%H%M%S") + s[dt+7:]

    return s
    