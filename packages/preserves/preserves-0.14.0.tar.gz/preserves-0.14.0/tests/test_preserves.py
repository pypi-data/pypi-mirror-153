import numbers
import os
import sys
import unittest

# Make `preserves` available for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preserves import *
from preserves.compat import basestring_, ord_
from preserves.values import _unwrap

if isinstance(chr(123), bytes):
    def _byte(x):
        return chr(x)
    def _hex(x):
        return x.encode('hex')
else:
    def _byte(x):
        return bytes([x])
    def _hex(x):
        return x.hex()

def _buf(*args):
    result = []
    for chunk in args:
        if isinstance(chunk, bytes):
            result.append(chunk)
        elif isinstance(chunk, basestring_):
            result.append(chunk.encode('utf-8'))
        elif isinstance(chunk, numbers.Number):
            result.append(_byte(chunk))
        else:
            raise Exception('Invalid chunk in _buf %r' % (chunk,))
    result = b''.join(result)
    return result

def _varint(v):
    e = Encoder()
    e.varint(v)
    return e.contents()

def _d(bs):
    return decode(bs)

def _e(v):
    return encode(v)

def _R(k, *args):
    return Record(Symbol(k), args)

class BinaryCodecTests(unittest.TestCase):
    def _roundtrip(self, forward, expected, back=None, nondeterministic=False):
        if back is None: back = forward
        self.assertEqual(_d(_e(forward)), back)
        self.assertEqual(_d(_e(back)), back)
        self.assertEqual(_d(expected), back)
        if not nondeterministic:
            actual = _e(forward)
            self.assertEqual(actual, expected, '%s != %s' % (_hex(actual), _hex(expected)))

    def test_decode_varint(self):
        with self.assertRaises(DecodeError):
            Decoder(_buf()).varint()
        self.assertEqual(Decoder(_buf(0)).varint(), 0)
        self.assertEqual(Decoder(_buf(10)).varint(), 10)
        self.assertEqual(Decoder(_buf(100)).varint(), 100)
        self.assertEqual(Decoder(_buf(200, 1)).varint(), 200)
        self.assertEqual(Decoder(_buf(0b10101100, 0b00000010)).varint(), 300)
        self.assertEqual(Decoder(_buf(128, 148, 235, 220, 3)).varint(), 1000000000)

    def test_encode_varint(self):
        self.assertEqual(_varint(0), _buf(0))
        self.assertEqual(_varint(10), _buf(10))
        self.assertEqual(_varint(100), _buf(100))
        self.assertEqual(_varint(200), _buf(200, 1))
        self.assertEqual(_varint(300), _buf(0b10101100, 0b00000010))
        self.assertEqual(_varint(1000000000), _buf(128, 148, 235, 220, 3))

    def test_simple_seq(self):
        self._roundtrip([1,2,3,4], _buf(0xb5, 0x91, 0x92, 0x93, 0x94, 0x84), back=(1,2,3,4))
        self._roundtrip(iter([1,2,3,4]),
                        _buf(0xb5, 0x91, 0x92, 0x93, 0x94, 0x84),
                        back=(1,2,3,4),
                        nondeterministic=True)
        self._roundtrip((-2,-1,0,1), _buf(0xb5, 0x9E, 0x9F, 0x90, 0x91, 0x84))

    def test_str(self):
        self._roundtrip(u'hello', _buf(0xb1, 0x05, 'hello'))

    def test_mixed1(self):
        self._roundtrip((u'hello', Symbol(u'there'), b'world', (), set(), True, False),
                        _buf(0xb5,
                             0xb1, 0x05, 'hello',
                             0xb3, 0x05, 'there',
                             0xb2, 0x05, 'world',
                             0xb5, 0x84,
                             0xb6, 0x84,
                             0x81,
                             0x80,
                             0x84))

    def test_signedinteger(self):
        self._roundtrip(-257, _buf(0xa1, 0xFE, 0xFF))
        self._roundtrip(-256, _buf(0xa1, 0xFF, 0x00))
        self._roundtrip(-255, _buf(0xa1, 0xFF, 0x01))
        self._roundtrip(-254, _buf(0xa1, 0xFF, 0x02))
        self._roundtrip(-129, _buf(0xa1, 0xFF, 0x7F))
        self._roundtrip(-128, _buf(0xa0, 0x80))
        self._roundtrip(-127, _buf(0xa0, 0x81))
        self._roundtrip(-4, _buf(0xa0, 0xFC))
        self._roundtrip(-3, _buf(0x9D))
        self._roundtrip(-2, _buf(0x9E))
        self._roundtrip(-1, _buf(0x9F))
        self._roundtrip(0, _buf(0x90))
        self._roundtrip(1, _buf(0x91))
        self._roundtrip(12, _buf(0x9C))
        self._roundtrip(13, _buf(0xa0, 0x0D))
        self._roundtrip(127, _buf(0xa0, 0x7F))
        self._roundtrip(128, _buf(0xa1, 0x00, 0x80))
        self._roundtrip(255, _buf(0xa1, 0x00, 0xFF))
        self._roundtrip(256, _buf(0xa1, 0x01, 0x00))
        self._roundtrip(32767, _buf(0xa1, 0x7F, 0xFF))
        self._roundtrip(32768, _buf(0xa2, 0x00, 0x80, 0x00))
        self._roundtrip(65535, _buf(0xa2, 0x00, 0xFF, 0xFF))
        self._roundtrip(65536, _buf(0xa2, 0x01, 0x00, 0x00))
        self._roundtrip(131072, _buf(0xa2, 0x02, 0x00, 0x00))

    def test_floats(self):
        self._roundtrip(Float(1.0), _buf(0x82, 0x3f, 0x80, 0, 0))
        self._roundtrip(1.0, _buf(0x83, 0x3f, 0xf0, 0, 0, 0, 0, 0, 0))
        self._roundtrip(-1.202e300, _buf(0x83, 0xfe, 0x3c, 0xb7, 0xb7, 0x59, 0xbf, 0x04, 0x26))

    def test_dict(self):
        self._roundtrip({ Symbol(u'a'): 1,
                          u'b': True,
                          (1, 2, 3): b'c',
                          ImmutableDict({ Symbol(u'first-name'): u'Elizabeth', }):
                            { Symbol(u'surname'): u'Blackwell' } },
                        _buf(0xB7,
                             0xb3, 0x01, "a", 0x91,
                             0xb1, 0x01, "b", 0x81,
                             0xb5, 0x91, 0x92, 0x93, 0x84, 0xb2, 0x01, "c",
                             0xB7, 0xb3, 0x0A, "first-name", 0xb1, 0x09, "Elizabeth", 0x84,
                             0xB7, 0xb3, 0x07, "surname", 0xb1, 0x09, "Blackwell", 0x84,
                             0x84),
                        nondeterministic = True)

    def test_iterator_stream(self):
        d = {u'a': 1, u'b': 2, u'c': 3}
        r = r'b5(b5b1016.9.84){3}84'
        if hasattr(d, 'iteritems'):
            # python 2
            bs = _e(d.iteritems())
            self.assertRegexpMatches(_hex(bs), r)
        else:
            # python 3
            bs = _e(d.items())
            self.assertRegex(_hex(bs), r)
        self.assertEqual(sorted(_d(bs)), [(u'a', 1), (u'b', 2), (u'c', 3)])

    def test_long_sequence(self):
        self._roundtrip((False,) * 14, _buf(0xb5, b'\x80' * 14, 0x84))
        self._roundtrip((False,) * 15, _buf(0xb5, b'\x80' * 15, 0x84))
        self._roundtrip((False,) * 100, _buf(0xb5, b'\x80' * 100, 0x84))
        self._roundtrip((False,) * 200, _buf(0xb5, b'\x80' * 200, 0x84))

    def test_embedded_id(self):
        class A:
            def __init__(self, a):
                self.a = a
        a1 = Embedded(A(1))
        a2 = Embedded(A(1))
        self.assertNotEqual(encode(a1, encode_embedded=id), encode(a2, encode_embedded=id))
        self.assertEqual(encode(a1, encode_embedded=id), encode(a1, encode_embedded=id))
        self.assertEqual(ord_(encode(a1, encode_embedded=id)[0]), 0x86)
        self.assertEqual(ord_(encode(a2, encode_embedded=id)[0]), 0x86)

    def test_decode_embedded_absent(self):
        with self.assertRaises(DecodeError):
            decode(b'\x86\xa0\xff', decode_embedded=None)

    def test_encode_embedded(self):
        objects = []
        def enc(p):
            objects.append(p)
            return len(objects) - 1
        self.assertEqual(encode([Embedded(object()), Embedded(object())], encode_embedded = enc),
                         b'\xb5\x86\x90\x86\x91\x84')

    def test_decode_embedded(self):
        objects = [123, 234]
        def dec(v):
            return objects[v]
        self.assertEqual(decode(b'\xb5\x86\x90\x86\x91\x84', decode_embedded = dec),
                         (Embedded(123), Embedded(234)))

def load_binary_samples():
    with open(os.path.join(os.path.dirname(__file__), 'samples.bin'), 'rb') as f:
        return Decoder(f.read(), include_annotations=True, decode_embedded=lambda x: x).next()

def load_text_samples():
    with open(os.path.join(os.path.dirname(__file__), 'samples.pr'), 'rt') as f:
        return Parser(f.read(), include_annotations=True, parse_embedded=lambda x: x).next()

class TextCodecTests(unittest.TestCase):
    def test_samples_bin_eq_txt(self):
        b = load_binary_samples()
        t = load_text_samples()
        self.assertEqual(b, t)

    def test_txt_roundtrip(self):
        b = load_binary_samples()
        s = stringify(b, format_embedded=lambda x: x)
        self.assertEqual(parse(s, include_annotations=True, parse_embedded=lambda x: x), b)

def add_method(d, tName, fn):
    if hasattr(fn, 'func_name'):
        # python2
        fname = str(fn.func_name + '_' + tName)
        fn.func_name = fname
    else:
        # python3
        fname = str(fn.__name__ + '_' + tName)
        fn.__name__ = fname
    d[fname] = fn

expected_values = {
    "annotation1": { "forward": annotate(9, u"abc"), "back": 9 },
    "annotation2": { "forward": annotate([[], annotate([], u"x")], u"abc", u"def"), "back": ((), ()) },
    "annotation3": { "forward": annotate(5, annotate(2, 1), annotate(4, 3)), "back": 5 },
    "annotation5": { "forward": annotate(_R('R', annotate(Symbol('f'), Symbol('af'))),
                                         Symbol('ar')),
                     "back": _R('R', Symbol('f')) },
    "annotation6": { "forward": Record(annotate(Symbol('R'), Symbol('ar')),
                                       [annotate(Symbol('f'), Symbol('af'))]),
                     "back": _R('R', Symbol('f')) },
    "annotation7": { "forward": annotate([], Symbol('a'), Symbol('b'), Symbol('c')),
                     "back": () },
    "record2": { "value": _R('observe', _R('speak', _R('discard'), _R('capture', _R('discard')))) },
}

def get_expected_values(tName, textForm):
    entry = expected_values.get(tName, {"value": textForm})
    if 'value' in entry:
        return { "forward": entry['value'], "back": entry['value'] }
    elif 'forward' in entry and 'back' in entry:
        return entry
    else:
        raise Exception('Invalid expected_values entry for ' + tName)

def install_test(d, variant, tName, binaryForm, annotatedTextForm):
    textForm = annotatedTextForm.strip()
    entry = get_expected_values(tName, textForm)
    forward = entry['forward']
    back = entry['back']
    def test_match_expected(self): self.assertEqual(textForm, back)
    def test_roundtrip(self): self.assertEqual(self.DS(self.E(textForm)), back)
    def test_forward(self): self.assertEqual(self.DS(self.E(forward)), back)
    def test_back(self): self.assertEqual(self.DS(binaryForm), back)
    def test_back_ann(self): self.assertEqual(self.D(self.E(annotatedTextForm)), annotatedTextForm)
    def test_encode(self): self.assertEqual(self.E(forward), binaryForm)
    def test_encode_canonical(self): self.assertEqual(self.EC(annotatedTextForm), binaryForm)
    def test_encode_ann(self): self.assertEqual(self.E(annotatedTextForm), binaryForm)
    add_method(d, tName, test_match_expected)
    add_method(d, tName, test_roundtrip)
    add_method(d, tName, test_forward)
    add_method(d, tName, test_back)
    add_method(d, tName, test_back_ann)
    if variant in ['normal']:
        add_method(d, tName, test_encode)
    if variant in ['nondeterministic']:
        add_method(d, tName, test_encode_canonical)
    if variant in ['normal', 'nondeterministic']:
        add_method(d, tName, test_encode_ann)

def install_exn_test(d, tName, bs, check_proc):
    def test_exn(self):
        try:
            self.D(bs)
        except:
            check_proc(self, sys.exc_info()[1])
            return
        self.fail('did not fail as expected')
    add_method(d, tName, test_exn)

class CommonTestSuite(unittest.TestCase):
    TestCases = Record.makeConstructor('TestCases', 'cases')

    samples = load_binary_samples()
    tests = TestCases._cases(samples.peel()).peel()
    for (tName0, t0) in tests.items():
        tName = tName0.strip().name
        t = t0.peel()
        if t.key == Symbol('Test'):
            install_test(locals(), 'normal', tName, t[0].strip(), t[1])
        elif t.key == Symbol('NondeterministicTest'):
            install_test(locals(), 'nondeterministic', tName, t[0].strip(), t[1])
        elif t.key == Symbol('DecodeTest'):
            install_test(locals(), 'decode', tName, t[0].strip(), t[1])
        elif t.key == Symbol('DecodeError'):
            def expected_err(self, e):
                self.assertIsInstance(e, DecodeError)
                self.assertNotIsInstance(e, ShortPacket)
            install_exn_test(locals(), tName, t[0].strip(), expected_err)
        elif t.key in [Symbol('DecodeShort'), Symbol('DecodeEOF')]:
            def expected_short(self, e):
                self.assertIsInstance(e, ShortPacket)
            install_exn_test(locals(), tName, t[0].strip(), expected_short)
        elif t.key in [Symbol('ParseError'), Symbol('ParseShort'), Symbol('ParseEOF')]:
            # Skipped for now, until we have an implementation of text syntax
            pass
        else:
            raise Exception('Unsupported test kind', t.key)

    def DS(self, bs):
        return decode(bs, decode_embedded=lambda x: x)

    def D(self, bs):
        return decode_with_annotations(bs, decode_embedded=lambda x: x)

    def E(self, v):
        return encode(v, encode_embedded=lambda x: x)

    def EC(self, v):
        return encode(v, encode_embedded=lambda x: x, canonicalize=True)

class RecordTests(unittest.TestCase):
    def test_getters(self):
        T = Record.makeConstructor('t', 'x y z')
        T2 = Record.makeConstructor('t', 'x y z')
        U = Record.makeConstructor('u', 'x y z')
        t = T(1, 2, 3)
        self.assertTrue(T.isClassOf(t))
        self.assertTrue(T2.isClassOf(t))
        self.assertFalse(U.isClassOf(t))
        self.assertEqual(T._x(t), 1)
        self.assertEqual(T2._y(t), 2)
        self.assertEqual(T._z(t), 3)
        with self.assertRaises(TypeError):
            U._x(t)
