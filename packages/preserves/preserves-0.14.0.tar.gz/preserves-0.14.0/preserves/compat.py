try:
    basestring_ = basestring
except NameError:
    basestring_ = str

if isinstance(chr(123), bytes):
    ord_ = ord
else:
    ord_ = lambda x: x

try:
    unichr_ = unichr
except NameError:
    unichr_ = chr
