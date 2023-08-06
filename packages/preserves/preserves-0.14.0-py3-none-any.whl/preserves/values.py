import re
import sys
import struct

from .error import DecodeError

def preserve(v):
    while hasattr(v, '__preserve__'):
        v = v.__preserve__()
    return v

class Float(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        other = _unwrap(other)
        if other.__class__ is self.__class__:
            return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return 'Float(' + repr(self.value) + ')'

    def __preserve_write_binary__(self, encoder):
        encoder.buffer.append(0x82)
        encoder.buffer.extend(struct.pack('>f', self.value))

    def __preserve_write_text__(self, formatter):
        formatter.chunks.append(repr(self.value) + 'f')

# FIXME: This regular expression is conservatively correct, but Anglo-chauvinistic.
RAW_SYMBOL_RE = re.compile(r'^[a-zA-Z~!$%^&*?_=+/.][-a-zA-Z~!$%^&*?_=+/.0-9]*$')

class Symbol(object):
    def __init__(self, name):
        self.name = name.name if isinstance(name, Symbol) else name

    def __eq__(self, other):
        other = _unwrap(other)
        return isinstance(other, Symbol) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '#' + self.name

    def __preserve_write_binary__(self, encoder):
        bs = self.name.encode('utf-8')
        encoder.buffer.append(0xb3)
        encoder.varint(len(bs))
        encoder.buffer.extend(bs)

    def __preserve_write_text__(self, formatter):
        if RAW_SYMBOL_RE.match(self.name):
            formatter.chunks.append(self.name)
        else:
            formatter.chunks.append('|')
            for c in self.name:
                if c == '|': formatter.chunks.append('\\|')
                else: formatter.write_stringlike_char(c)
            formatter.chunks.append('|')

class Record(object):
    def __init__(self, key, fields):
        self.key = key
        self.fields = tuple(fields)
        self.__hash = None

    def __eq__(self, other):
        other = _unwrap(other)
        return isinstance(other, Record) and (self.key, self.fields) == (other.key, other.fields)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self.__hash is None:
            self.__hash = hash((self.key, self.fields))
        return self.__hash

    def __repr__(self):
        return str(self.key) + '(' + ', '.join((repr(f) for f in self.fields)) + ')'

    def __preserve_write_binary__(self, encoder):
        encoder.buffer.append(0xb4)
        encoder.append(self.key)
        for f in self.fields:
            encoder.append(f)
        encoder.buffer.append(0x84)

    def __preserve_write_text__(self, formatter):
        formatter.chunks.append('<')
        formatter.append(self.key)
        for f in self.fields:
            formatter.chunks.append(' ')
            formatter.append(f)
        formatter.chunks.append('>')

    def __getitem__(self, index):
        return self.fields[index]

    @staticmethod
    def makeConstructor(labelSymbolText, fieldNames):
        return Record.makeBasicConstructor(Symbol(labelSymbolText), fieldNames)

    @staticmethod
    def makeBasicConstructor(label, fieldNames):
        if type(fieldNames) == str:
            fieldNames = fieldNames.split()
        arity = len(fieldNames)
        def ctor(*fields):
            if len(fields) != arity:
                raise Exception("Record: cannot instantiate %r expecting %d fields with %d fields"%(
                    label,
                    arity,
                    len(fields)))
            return Record(label, fields)
        ctor.constructorInfo = RecordConstructorInfo(label, arity)
        ctor.isClassOf = lambda v: \
                         isinstance(v, Record) and v.key == label and len(v.fields) == arity
        def ensureClassOf(v):
            if not ctor.isClassOf(v):
                raise TypeError("Record: expected %r/%d, got %r" % (label, arity, v))
            return v
        ctor.ensureClassOf = ensureClassOf
        for fieldIndex in range(len(fieldNames)):
            fieldName = fieldNames[fieldIndex]
            # Stupid python scoping bites again
            def getter(fieldIndex):
                return lambda v: ensureClassOf(v)[fieldIndex]
            setattr(ctor, '_' + fieldName, getter(fieldIndex))
        return ctor

class RecordConstructorInfo(object):
    def __init__(self, key, arity):
        self.key = key
        self.arity = arity

    def __eq__(self, other):
        other = _unwrap(other)
        return isinstance(other, RecordConstructorInfo) and \
            (self.key, self.arity) == (other.key, other.arity)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self.__hash is None:
            self.__hash = hash((self.key, self.arity))
        return self.__hash

    def __repr__(self):
        return str(self.key) + '/' + str(self.arity)

# Blub blub blub
class ImmutableDict(dict):
    def __init__(self, *args, **kwargs):
        if hasattr(self, '__hash'): raise TypeError('Immutable')
        super(ImmutableDict, self).__init__(*args, **kwargs)
        self.__hash = None

    def __delitem__(self, key): raise TypeError('Immutable')
    def __setitem__(self, key, val): raise TypeError('Immutable')
    def clear(self): raise TypeError('Immutable')
    def pop(self, k, d=None): raise TypeError('Immutable')
    def popitem(self): raise TypeError('Immutable')
    def setdefault(self, k, d=None): raise TypeError('Immutable')
    def update(self, e, **f): raise TypeError('Immutable')

    def __hash__(self):
        if self.__hash is None:
            h = 0
            for k in self:
                h = ((h << 5) ^ (hash(k) << 2) ^ hash(self[k])) & sys.maxsize
            self.__hash = h
        return self.__hash

    @staticmethod
    def from_kvs(kvs):
        i = iter(kvs)
        result = ImmutableDict()
        result_proxy = super(ImmutableDict, result)
        try:
            while True:
                k = next(i)
                try:
                    v = next(i)
                except StopIteration:
                    raise DecodeError("Missing dictionary value")
                result_proxy.__setitem__(k, v)
        except StopIteration:
            pass
        return result

def dict_kvs(d):
    for k in d:
        yield k
        yield d[k]

inf = float('inf')

class Annotated(object):
    def __init__(self, item):
        self.annotations = []
        self.item = item

    def __preserve_write_binary__(self, encoder):
        for a in self.annotations:
            encoder.buffer.append(0x85)
            encoder.append(a)
        encoder.append(self.item)

    def __preserve_write_text__(self, formatter):
        for a in self.annotations:
            formatter.chunks.append('@')
            formatter.append(a)
            formatter.chunks.append(' ')
        formatter.append(self.item)

    def strip(self, depth=inf):
        return strip_annotations(self, depth)

    def peel(self):
        return strip_annotations(self, 1)

    def __eq__(self, other):
        return self.item == _unwrap(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.item)

    def __repr__(self):
        return ' '.join(list('@' + repr(a) for a in self.annotations) + [repr(self.item)])

def is_annotated(v):
    return isinstance(v, Annotated)

def strip_annotations(v, depth=inf):
    if depth == 0: return v
    if not is_annotated(v): return v

    next_depth = depth - 1
    def walk(v):
        return strip_annotations(v, next_depth)

    v = v.item
    if isinstance(v, Record):
        return Record(strip_annotations(v.key, depth), tuple(walk(f) for f in v.fields))
    elif isinstance(v, list):
        return tuple(walk(f) for f in v)
    elif isinstance(v, tuple):
        return tuple(walk(f) for f in v)
    elif isinstance(v, set):
        return frozenset(walk(f) for f in v)
    elif isinstance(v, frozenset):
        return frozenset(walk(f) for f in v)
    elif isinstance(v, dict):
        return ImmutableDict.from_kvs(walk(f) for f in dict_kvs(v))
    elif is_annotated(v):
        raise ValueError('Improper annotation structure')
    else:
        return v

def annotate(v, *anns):
    if not is_annotated(v):
        v = Annotated(v)
    for a in anns:
        v.annotations.append(a)
    return v

def _unwrap(x):
    if is_annotated(x):
        return x.item
    else:
        return x

class Embedded:
    def __init__(self, value):
        self.embeddedValue = value

    def __eq__(self, other):
        other = _unwrap(other)
        if other.__class__ is self.__class__:
            return self.embeddedValue == other.embeddedValue

    def __hash__(self):
        return hash(self.embeddedValue)

    def __repr__(self):
        return '#!%r' % (self.embeddedValue,)

    def __preserve_write_binary__(self, encoder):
        encoder.buffer.append(0x86)
        encoder.append(encoder.encode_embedded(self.embeddedValue))

    def __preserve_write_text__(self, formatter):
        formatter.chunks.append('#!')
        formatter.append(formatter.format_embedded(self.embeddedValue))
