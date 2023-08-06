import numbers
import struct

from .values import *
from .error import *
from .compat import basestring_, ord_

class BinaryCodec(object): pass

class Decoder(BinaryCodec):
    def __init__(self, packet=b'', include_annotations=False, decode_embedded=lambda x: x):
        super(Decoder, self).__init__()
        self.packet = packet
        self.index = 0
        self.include_annotations = include_annotations
        self.decode_embedded = decode_embedded

    def extend(self, data):
        self.packet = self.packet[self.index:] + data
        self.index = 0

    def nextbyte(self):
        if self.index >= len(self.packet):
            raise ShortPacket('Short packet')
        self.index = self.index + 1
        return ord_(self.packet[self.index - 1])

    def nextbytes(self, n):
        start = self.index
        end = start + n
        if end > len(self.packet):
            raise ShortPacket('Short packet')
        self.index = end
        return self.packet[start : end]

    def varint(self):
        v = self.nextbyte()
        if v < 128:
            return v
        else:
            return self.varint() * 128 + (v - 128)

    def peekend(self):
        matched = (self.nextbyte() == 0x84)
        if not matched:
            self.index = self.index - 1
        return matched

    def nextvalues(self):
        result = []
        while not self.peekend():
            result.append(self.next())
        return result

    def nextint(self, n):
        if n == 0: return 0
        acc = self.nextbyte()
        if acc & 0x80: acc = acc - 256
        for _i in range(n - 1):
            acc = (acc << 8) | self.nextbyte()
        return acc

    def wrap(self, v):
        return Annotated(v) if self.include_annotations else v

    def unshift_annotation(self, a, v):
        if self.include_annotations:
            v.annotations.insert(0, a)
        return v

    def next(self):
        tag = self.nextbyte()
        if tag == 0x80: return self.wrap(False)
        if tag == 0x81: return self.wrap(True)
        if tag == 0x82: return self.wrap(Float(struct.unpack('>f', self.nextbytes(4))[0]))
        if tag == 0x83: return self.wrap(struct.unpack('>d', self.nextbytes(8))[0])
        if tag == 0x84: raise DecodeError('Unexpected end-of-stream marker')
        if tag == 0x85:
            a = self.next()
            v = self.next()
            return self.unshift_annotation(a, v)
        if tag == 0x86:
            if self.decode_embedded is None:
                raise DecodeError('No decode_embedded function supplied')
            return self.wrap(Embedded(self.decode_embedded(self.next())))
        if tag >= 0x90 and tag <= 0x9f: return self.wrap(tag - (0xa0 if tag > 0x9c else 0x90))
        if tag >= 0xa0 and tag <= 0xaf: return self.wrap(self.nextint(tag - 0xa0 + 1))
        if tag == 0xb0: return self.wrap(self.nextint(self.varint()))
        if tag == 0xb1: return self.wrap(self.nextbytes(self.varint()).decode('utf-8'))
        if tag == 0xb2: return self.wrap(self.nextbytes(self.varint()))
        if tag == 0xb3: return self.wrap(Symbol(self.nextbytes(self.varint()).decode('utf-8')))
        if tag == 0xb4:
            vs = self.nextvalues()
            if not vs: raise DecodeError('Too few elements in encoded record')
            return self.wrap(Record(vs[0], vs[1:]))
        if tag == 0xb5: return self.wrap(tuple(self.nextvalues()))
        if tag == 0xb6: return self.wrap(frozenset(self.nextvalues()))
        if tag == 0xb7: return self.wrap(ImmutableDict.from_kvs(self.nextvalues()))
        raise DecodeError('Invalid tag: ' + hex(tag))

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

def decode(bs, **kwargs):
    return Decoder(packet=bs, **kwargs).next()

def decode_with_annotations(bs, **kwargs):
    return Decoder(packet=bs, include_annotations=True, **kwargs).next()

class Encoder(BinaryCodec):
    def __init__(self, encode_embedded=lambda x: x, canonicalize=False):
        super(Encoder, self).__init__()
        self.buffer = bytearray()
        self._encode_embedded = encode_embedded
        self._canonicalize = canonicalize

    def reset(self):
        self.buffer = bytearray()

    def encode_embedded(self, v):
        if self._encode_embedded is None:
            raise EncodeError('No encode_embedded function supplied')
        return self._encode_embedded(v)

    def contents(self):
        return bytes(self.buffer)

    def varint(self, v):
        if v < 128:
            self.buffer.append(v)
        else:
            self.buffer.append((v % 128) + 128)
            self.varint(v // 128)

    def encodeint(self, v):
        bitcount = (~v if v < 0 else v).bit_length() + 1
        bytecount = (bitcount + 7) // 8
        if bytecount <= 16:
            self.buffer.append(0xa0 + bytecount - 1)
        else:
            self.buffer.append(0xb0)
            self.varint(bytecount)
        def enc(n,x):
            if n > 0:
                enc(n-1, x >> 8)
                self.buffer.append(x & 255)
        enc(bytecount, v)

    def encodevalues(self, tag, items):
        self.buffer.append(0xb0 + tag)
        for i in items: self.append(i)
        self.buffer.append(0x84)

    def encodebytes(self, tag, bs):
        self.buffer.append(0xb0 + tag)
        self.varint(len(bs))
        self.buffer.extend(bs)

    def encodeset(self, v):
        if not self._canonicalize:
            self.encodevalues(6, v)
        else:
            c = Canonicalizer(self._encode_embedded)
            for i in v: c.entry([i])
            c.emit_entries(self, 6)

    def encodedict(self, v):
        if not self._canonicalize:
            self.encodevalues(7, list(dict_kvs(v)))
        else:
            c = Canonicalizer(self._encode_embedded)
            for (kk, vv) in v.items(): c.entry([kk, vv])
            c.emit_entries(self, 7)

    def append(self, v):
        v = preserve(v)
        if hasattr(v, '__preserve_write_binary__'):
            v.__preserve_write_binary__(self)
        elif v is False:
            self.buffer.append(0x80)
        elif v is True:
            self.buffer.append(0x81)
        elif isinstance(v, float):
            self.buffer.append(0x83)
            self.buffer.extend(struct.pack('>d', v))
        elif isinstance(v, numbers.Number):
            if v >= -3 and v <= 12:
                self.buffer.append(0x90 + (v if v >= 0 else v + 16))
            else:
                self.encodeint(v)
        elif isinstance(v, bytes):
            self.encodebytes(2, v)
        elif isinstance(v, basestring_):
            self.encodebytes(1, v.encode('utf-8'))
        elif isinstance(v, list):
            self.encodevalues(5, v)
        elif isinstance(v, tuple):
            self.encodevalues(5, v)
        elif isinstance(v, set):
            self.encodeset(v)
        elif isinstance(v, frozenset):
            self.encodeset(v)
        elif isinstance(v, dict):
            self.encodedict(v)
        else:
            try:
                i = iter(v)
            except TypeError:
                i = None
            if i is None:
                self.cannot_encode(v)
            else:
                self.encodevalues(5, i)

    def cannot_encode(self, v):
        raise TypeError('Cannot preserves-encode: ' + repr(v))

class Canonicalizer:
    def __init__(self, encode_embedded):
        self.encoder = Encoder(encode_embedded, canonicalize=True)
        self.entries = []

    def entry(self, pieces):
        for piece in pieces: self.encoder.append(piece)
        entry = self.encoder.contents()
        self.encoder.reset()
        self.entries.append(entry)

    def emit_entries(self, outer_encoder, tag):
        outer_encoder.buffer.append(0xb0 + tag)
        for e in sorted(self.entries): outer_encoder.buffer.extend(e)
        outer_encoder.buffer.append(0x84)

def encode(v, **kwargs):
    e = Encoder(**kwargs)
    e.append(v)
    return e.contents()

def canonicalize(v, **kwargs):
    return encode(v, canonicalize=True, **kwargs)
