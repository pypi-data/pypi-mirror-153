import numbers
import struct
import base64

from .values import *
from .error import *
from .compat import basestring_, unichr_
from .binary import Decoder

class TextCodec(object): pass

class Parser(TextCodec):
    def __init__(self, input_buffer=u'', include_annotations=False, parse_embedded=lambda x: x):
        super(Parser, self).__init__()
        self.input_buffer = input_buffer
        self.index = 0
        self.include_annotations = include_annotations
        self.parse_embedded = parse_embedded

    def extend(self, text):
        self.input_buffer = self.input_buffer[self.index:] + text
        self.index = 0

    def _atend(self):
        return self.index >= len(self.input_buffer)

    def peek(self):
        if self._atend():
            raise ShortPacket('Short input buffer')
        return self.input_buffer[self.index]

    def skip(self):
        self.index = self.index + 1

    def nextchar(self):
        c = self.peek()
        self.skip()
        return c

    def skip_whitespace(self):
        while not self._atend():
            c = self.peek()
            if not (c.isspace() or c == ','):
                break
            self.skip()

    def gather_annotations(self):
        vs = []
        while True:
            self.skip_whitespace()
            c = self.peek()
            if c == ';':
                self.skip()
                vs.append(self.comment_line())
            elif c == '@':
                self.skip()
                vs.append(self.next())
            else:
                return vs

    def comment_line(self):
        s = []
        while True:
            c = self.nextchar()
            if c == '\r' or c == '\n':
                return self.wrap(u''.join(s))
            s.append(c)

    def read_intpart(self, acc, c):
        if c == '0':
            acc.append(c)
        else:
            self.read_digit1(acc, c)
        return self.read_fracexp(acc)

    def read_fracexp(self, acc):
        is_float = False
        if self.peek() == '.':
            is_float = True
            acc.append(self.nextchar())
            self.read_digit1(acc, self.nextchar())
        if self.peek() in 'eE':
            acc.append(self.nextchar())
            return self.read_sign_and_exp(acc)
        else:
            return self.finish_number(acc, is_float)

    def read_sign_and_exp(self, acc):
        if self.peek() in '+-':
            acc.append(self.nextchar())
        self.read_digit1(acc, self.nextchar())
        return self.finish_number(acc, True)

    def finish_number(self, acc, is_float):
        if is_float:
            if self.peek() in 'fF':
                self.skip()
                return Float(float(u''.join(acc)))
            else:
                return float(u''.join(acc))
        else:
            return int(u''.join(acc))

    def read_digit1(self, acc, c):
        if not c.isdigit():
            raise DecodeError('Incomplete number')
        acc.append(c)
        while not self._atend():
            if not self.peek().isdigit():
                break
            acc.append(self.nextchar())

    def read_stringlike(self, terminator, hexescape, hexescaper):
        acc = []
        while True:
            c = self.nextchar()
            if c == terminator:
                return u''.join(acc)
            if c == '\\':
                c = self.nextchar()
                if c == hexescape: hexescaper(acc)
                elif c == terminator or c == '\\' or c == '/': acc.append(c)
                elif c == 'b': acc.append(u'\x08')
                elif c == 'f': acc.append(u'\x0c')
                elif c == 'n': acc.append(u'\x0a')
                elif c == 'r': acc.append(u'\x0d')
                elif c == 't': acc.append(u'\x09')
                else: raise DecodeError('Invalid escape code')
            else:
                acc.append(c)

    def hexnum(self, count):
        v = 0
        for i in range(count):
            c = self.nextchar().lower()
            if c >= '0' and c <= '9':
                v = v << 4 | (ord(c) - ord('0'))
            elif c >= 'a' and c <= 'f':
                v = v << 4 | (ord(c) - ord('a') + 10)
            else:
                raise DecodeError('Bad hex escape')
        return v

    def read_string(self, delimiter):
        def u16_escape(acc):
            n1 = self.hexnum(4)
            if n1 >= 0xd800 and n1 <= 0xdbff:
                ok = True
                ok = ok and self.nextchar() == '\\'
                ok = ok and self.nextchar() == 'u'
                if not ok:
                    raise DecodeError('Missing second half of surrogate pair')
                n2 = self.hexnum(4)
                if n2 >= 0xdc00 and n2 <= 0xdfff:
                    n = ((n1 - 0xd800) << 10) + (n2 - 0xdc00) + 0x10000
                    acc.append(unichr_(n))
                else:
                    raise DecodeError('Bad second half of surrogate pair')
            else:
                acc.append(unichr_(n1))
        return self.read_stringlike(delimiter, 'u', u16_escape)

    def read_literal_binary(self):
        s = self.read_stringlike('"', 'x', lambda acc: acc.append(unichr_(self.hexnum(2))))
        return s.encode('latin-1')

    def read_hex_binary(self):
        acc = bytearray()
        while True:
            self.skip_whitespace()
            if self.peek() == '"':
                self.skip()
                return bytes(acc)
            acc.append(self.hexnum(2))

    def read_base64_binary(self):
        acc = []
        while True:
            self.skip_whitespace()
            c = self.nextchar()
            if c == ']':
                acc.append(u'====')
                return base64.b64decode(u''.join(acc))
            if c == '-': c = '+'
            if c == '_': c = '/'
            if c == '=': continue
            acc.append(c)

    def upto(self, delimiter):
        vs = []
        while True:
            self.skip_whitespace()
            if self.peek() == delimiter:
                self.skip()
                return tuple(vs)
            vs.append(self.next())

    def read_dictionary(self):
        acc = []
        while True:
            self.skip_whitespace()
            if self.peek() == '}':
                self.skip()
                return ImmutableDict.from_kvs(acc)
            acc.append(self.next())
            self.skip_whitespace()
            if self.nextchar() != ':':
                raise DecodeError('Missing expected key/value separator')
            acc.append(self.next())

    def read_raw_symbol(self, acc):
        while not self._atend():
            c = self.peek()
            if c.isspace() or c in '(){}[]<>";,@#:|':
                break
            self.skip()
            acc.append(c)
        return Symbol(u''.join(acc))

    def wrap(self, v):
        return Annotated(v) if self.include_annotations else v

    def next(self):
        self.skip_whitespace()
        c = self.peek()
        if c == '-':
            self.skip()
            return self.wrap(self.read_intpart(['-'], self.nextchar()))
        if c.isdigit():
            self.skip()
            return self.wrap(self.read_intpart([], c))
        if c == '"':
            self.skip()
            return self.wrap(self.read_string('"'))
        if c == '|':
            self.skip()
            return self.wrap(Symbol(self.read_string('|')))
        if c in ';@':
            annotations = self.gather_annotations()
            v = self.next()
            if self.include_annotations:
                v.annotations = annotations + v.annotations
            return v
        if c == ':':
            raise DecodeError('Unexpected key/value separator between items')
        if c == '#':
            self.skip()
            c = self.nextchar()
            if c == 'f': return self.wrap(False)
            if c == 't': return self.wrap(True)
            if c == '{': return self.wrap(frozenset(self.upto('}')))
            if c == '"': return self.wrap(self.read_literal_binary())
            if c == 'x':
                if self.nextchar() != '"':
                    raise DecodeError('Expected open-quote at start of hex ByteString')
                return self.wrap(self.read_hex_binary())
            if c == '[': return self.wrap(self.read_base64_binary())
            if c == '=':
                old_ann = self.include_annotations
                self.include_annotations = True
                bs_val = self.next()
                self.include_annotations = old_ann
                if len(bs_val.annotations) > 0:
                    raise DecodeError('Annotations not permitted after #=')
                bs_val = bs_val.item
                if not isinstance(bs_val, bytes):
                    raise DecodeError('ByteString must follow #=')
                return self.wrap(Decoder(bs_val, include_annotations = self.include_annotations).next())
            if c == '!':
                if self.parse_embedded is None:
                    raise DecodeError('No parse_embedded function supplied')
                return self.wrap(Embedded(self.parse_embedded(self.next())))
            raise DecodeError('Invalid # syntax')
        if c == '<':
            self.skip()
            vs = self.upto('>')
            if len(vs) == 0:
                raise DecodeError('Missing record label')
            return self.wrap(Record(vs[0], vs[1:]))
        if c == '[':
            self.skip()
            return self.wrap(self.upto(']'))
        if c == '{':
            self.skip()
            return self.wrap(self.read_dictionary())
        if c in '>]}':
            raise DecodeError('Unexpected ' + c)
        self.skip()
        return self.wrap(self.read_raw_symbol([c]))

    def try_next(self):
        start = self.index
        try:
            return self.next()
        except ShortPacket:
            self.index = start
            return None

    def __iter__(self):
        return self

    def __next__(self):
        v = self.try_next()
        if v is None:
            raise StopIteration
        return v

def parse(bs, **kwargs):
    return Parser(input_buffer=bs, **kwargs).next()

def parse_with_annotations(bs, **kwargs):
    return Parser(input_buffer=bs, include_annotations=True, **kwargs).next()

class Formatter(TextCodec):
    def __init__(self,
                 format_embedded=lambda x: x,
                 indent=None,
                 with_commas=False,
                 trailing_comma=False):
        super(Formatter, self).__init__()
        self.indent_delta = 0 if indent is None else indent
        self.indent_distance = 0
        self.with_commas = with_commas
        self.trailing_comma = trailing_comma
        self.chunks = []
        self._format_embedded = format_embedded

    def format_embedded(self, v):
        if self._format_embedded is None:
            raise EncodeError('No format_embedded function supplied')
        return self._format_embedded(v)

    def contents(self):
        return u''.join(self.chunks)

    def is_indenting(self):
        return self.indent_delta > 0

    def write_indent(self):
        if self.is_indenting():
            self.chunks.append('\n' + ' ' * self.indent_distance)

    def write_indent_space(self):
        if self.is_indenting():
            self.write_indent()
        else:
            self.chunks.append(' ')

    def write_stringlike_char(self, c):
        if c == '\\': self.chunks.append('\\\\')
        elif c == '\x08': self.chunks.append('\\b')
        elif c == '\x0c': self.chunks.append('\\f')
        elif c == '\x0a': self.chunks.append('\\n')
        elif c == '\x0d': self.chunks.append('\\r')
        elif c == '\x09': self.chunks.append('\\t')
        else: self.chunks.append(c)

    def write_seq(self, opener, closer, vs, appender):
        vs = list(vs)
        itemcount = len(vs)
        self.chunks.append(opener)
        if itemcount == 0:
            pass
        elif itemcount == 1:
            appender(vs[0])
        else:
            self.indent_distance = self.indent_distance + self.indent_delta
            self.write_indent()
            appender(vs[0])
            for v in vs[1:]:
                if self.with_commas: self.chunks.append(',')
                self.write_indent_space()
                appender(v)
            self.indent_distance = self.indent_distance - self.indent_delta
            if self.trailing_comma: self.chunks.append(',')
            self.write_indent()
        self.chunks.append(closer)

    def append(self, v):
        v = preserve(v)
        if hasattr(v, '__preserve_write_text__'):
            v.__preserve_write_text__(self)
        elif v is False:
            self.chunks.append('#f')
        elif v is True:
            self.chunks.append('#t')
        elif isinstance(v, float):
            self.chunks.append(repr(v))
        elif isinstance(v, numbers.Number):
            self.chunks.append('%d' % (v,))
        elif isinstance(v, bytes):
            self.chunks.append('#[%s]' % (base64.b64encode(v).decode('ascii'),))
        elif isinstance(v, basestring_):
            self.chunks.append('"')
            for c in v:
                if c == '"': self.chunks.append('\\"')
                else: self.write_stringlike_char(c)
            self.chunks.append('"')
        elif isinstance(v, list):
            self.write_seq('[', ']', v, self.append)
        elif isinstance(v, tuple):
            self.write_seq('[', ']', v, self.append)
        elif isinstance(v, set):
            self.write_seq('#{', '}', v, self.append)
        elif isinstance(v, frozenset):
            self.write_seq('#{', '}', v, self.append)
        elif isinstance(v, dict):
            def append_kv(kv):
                self.append(kv[0])
                self.chunks.append(': ')
                self.append(kv[1])
            self.write_seq('{', '}', v.items(), append_kv)
        else:
            try:
                i = iter(v)
            except TypeError:
                i = None
            if i is None:
                self.cannot_format(v)
            else:
                self.write_seq('[', ']', i, self.append)

    def cannot_format(self, v):
        raise TypeError('Cannot preserves-format: ' + repr(v))

def stringify(v, **kwargs):
    e = Formatter(**kwargs)
    e.append(v)
    return e.contents()
