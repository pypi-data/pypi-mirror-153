from . import *
from .schema import load_schema_file, extend
from .values import _unwrap
from .compat import basestring_
import pathlib
import re

syntax = load_schema_file(pathlib.Path(__file__).parent / 'path.prb').path

Selector = syntax.Selector
Predicate = syntax.Predicate

def parse(s):
    return parse_selector(Parser(s))

def parse_selector(tokens):
    steps = []
    tokens = iter(tokens)
    while True:
        try:
            steps.append(parse_step(tokens))
        except StopIteration:
            return syntax.Selector(steps)

AXIS_VALUES = Symbol('/')
AXIS_DESCENDANTS = Symbol('//')
AXIS_MEMBER = Symbol('.')
AXIS_LABEL = Symbol('.^')
AXIS_KEYS = Symbol('.keys')
AXIS_LENGTH = Symbol('.length')
AXIS_ANNOTATIONS = Symbol('.annotations')
AXIS_EMBEDDED = Symbol('.embedded')

FILTER_NOP = Symbol('*')
FILTER_EQ1 = Symbol('eq')
FILTER_EQ2 = Symbol('=')
FILTER_NE1 = Symbol('ne')
FILTER_NE2 = Symbol('!=')
FILTER_LT = Symbol('lt')
FILTER_LE = Symbol('le')
FILTER_GT = Symbol('gt')
FILTER_GE = Symbol('ge')
FILTER_RE1 = Symbol('re')
FILTER_RE2 = Symbol('=r')
FILTER_LABEL = Symbol('^')

FILTER_BOOL = Symbol('bool')
FILTER_FLOAT = Symbol('float')
FILTER_DOUBLE = Symbol('double')
FILTER_INT = Symbol('int')
FILTER_STRING = Symbol('string')
FILTER_BYTES = Symbol('bytes')
FILTER_SYMBOL = Symbol('symbol')
FILTER_REC = Symbol('rec')
FILTER_SEQ = Symbol('seq')
FILTER_SET = Symbol('set')
FILTER_DICT = Symbol('dict')
FILTER_EMBEDDED = Symbol('embedded')

TRANSFORM_REAL = Symbol('~real')
TRANSFORM_INT = Symbol('~int')

def parse_step(tokens):
    t = next(tokens)
    if isinstance(t, tuple): return syntax.Step.Filter(syntax.Filter.test(parse_predicate(iter(t))))
    if t == AXIS_VALUES: return syntax.Step.Axis(syntax.Axis.values())
    if t == AXIS_DESCENDANTS: return syntax.Step.Axis(syntax.Axis.descendants())
    if t == AXIS_MEMBER: return syntax.Step.Axis(syntax.Axis.at(next(tokens)))
    if t == AXIS_LABEL: return syntax.Step.Axis(syntax.Axis.label())
    if t == AXIS_KEYS: return syntax.Step.Axis(syntax.Axis.keys())
    if t == AXIS_LENGTH: return syntax.Step.Axis(syntax.Axis.length())
    if t == AXIS_ANNOTATIONS: return syntax.Step.Axis(syntax.Axis.annotations())
    if t == AXIS_EMBEDDED: return syntax.Step.Axis(syntax.Axis.embedded())
    if t == FILTER_NOP: return syntax.Step.Filter(syntax.Filter.nop())
    if t == FILTER_EQ1 or t == FILTER_EQ2: return parse_comparison(tokens, syntax.Comparison.eq())
    if t == FILTER_NE1 or t == FILTER_NE2: return parse_comparison(tokens, syntax.Comparison.ne())
    if t == FILTER_LT: return parse_comparison(tokens, syntax.Comparison.lt())
    if t == FILTER_GT: return parse_comparison(tokens, syntax.Comparison.gt())
    if t == FILTER_LE: return parse_comparison(tokens, syntax.Comparison.le())
    if t == FILTER_GE: return parse_comparison(tokens, syntax.Comparison.ge())
    if t == FILTER_RE1 or t == FILTER_RE2:
        re_val = next(tokens)
        if not isinstance(re_val, str): raise ValueError('Expected string argument to re/=r')
        try:
            re.compile(re_val)
        except:
            raise ValueError('Invalid regular expression')
        return syntax.Step.Filter(syntax.Filter.regex(re_val))
    if t == FILTER_LABEL:
        label_lit = next(tokens)
        return syntax.Step.Test(syntax.Predicate.Selector(syntax.Selector([
            syntax.Step.Axis(syntax.Axis.label()),
            syntax.Step.Filter(syntax.Filter.compare(
                syntax.Comparison.eq(),
                label_lit))])))
    if t == TRANSFORM_REAL: return syntax.Step.Filter(syntax.Filter.real)
    if t == TRANSFORM_INT: return syntax.Step.Filter(syntax.Filter.int)
    if t == FILTER_BOOL: return kind_filter(syntax.ValueKind.Boolean())
    if t == FILTER_FLOAT: return kind_filter(syntax.ValueKind.Float())
    if t == FILTER_DOUBLE: return kind_filter(syntax.ValueKind.Double())
    if t == FILTER_INT: return kind_filter(syntax.ValueKind.SignedInteger())
    if t == FILTER_STRING: return kind_filter(syntax.ValueKind.String())
    if t == FILTER_BYTES: return kind_filter(syntax.ValueKind.ByteString())
    if t == FILTER_SYMBOL: return kind_filter(syntax.ValueKind.Symbol())
    if t == FILTER_REC: return kind_filter(syntax.ValueKind.Record())
    if t == FILTER_SEQ: return kind_filter(syntax.ValueKind.Sequence())
    if t == FILTER_SET: return kind_filter(syntax.ValueKind.Seq())
    if t == FILTER_DICT: return kind_filter(syntax.ValueKind.Dictionary())
    if t == FILTER_EMBEDDED: return kind_filter(syntax.ValueKind.Embedded())
    raise ValueError('Invalid Preserves path step: ' + repr(t))

def kind_filter(value_kind):
    return syntax.Step.Filter(syntax.Filter.kind(value_kind))

def parse_comparison(tokens, op):
    return syntax.Step.Filter(syntax.Filter.compare(op, next(tokens)))

OP_NOT = Symbol('!')
OP_PLUS = Symbol('+')
OP_AND = Symbol('&')

def split_by(tokens, delimiter):
    groups = []
    group = []
    def finish():
        groups.append(group[:])
        group.clear()
    for t in tokens:
        if t == delimiter:
            finish()
        else:
            group.append(t)
    finish()
    return groups

def parse_predicate(tokens):
    tokens = list(tokens)
    union_pieces = split_by(tokens, OP_PLUS)
    intersection_pieces = split_by(tokens, OP_AND)
    if len(union_pieces) > 1 and len(intersection_pieces) > 1:
        raise ValueError('Ambiguous parse: mixed "+" and "&" operators')
    if len(union_pieces) > 1:
        return syntax.Predicate.or_([parse_non_binop(ts) for ts in union_pieces])
    if len(intersection_pieces) > 1:
        return syntax.Predicate.and_([parse_non_binop(ts) for ts in intersection_pieces])
    return parse_non_binop(union_pieces[0])

def parse_non_binop(tokens):
    if tokens[:1] == [OP_NOT]:
        return syntax.Predicate.not_(parse_non_binop(tokens[1:]))
    else:
        return syntax.Predicate.Selector(parse_selector(tokens))

@extend(syntax.Predicate.Selector)
def exec(self, v):
    result = self.value.exec(v)
    return len(tuple(result)) > 0

@extend(syntax.Predicate.not_)
def exec(self, v):
    return not self.pred.exec(v)

@extend(Predicate.or_)
def exec(self, v):
    for p in self.preds:
        if p.exec(v): return True
    return False

@extend(Predicate.and_)
def exec(self, v):
    for p in self.preds:
        if not p.exec(v): return False
    return True

@extend(Selector)
def exec(self, v):
    vs = (v,)
    for step in self.value:
        vs = tuple(w for v in vs for w in step.exec(v))
    return vs

@extend(syntax.Step.Axis)
@extend(syntax.Step.Filter)
def exec(self, v):
    return self.value.exec(v)

def children(value):
    value = _unwrap(preserve(_unwrap(value)))
    if isinstance(value, Record):
        return value.fields
    if isinstance(value, list) or isinstance(value, tuple):
        return tuple(value)
    if isinstance(value, set) or isinstance(value, frozenset):
        return tuple(value)
    if isinstance(value, dict):
        return tuple(value.values())
    return ()

def descendants(value):
    acc = [value]
    i = 0
    while i < len(acc):
        acc.extend(children(acc[i]))
        i = i + 1
    return tuple(acc)

@extend(syntax.Axis.values)
def exec(self, v):
    return children(v)

@extend(syntax.Axis.descendants)
def exec(self, v):
    return descendants(v)

@extend(syntax.Axis.at)
def exec(self, v):
    v = preserve(_unwrap(v))
    if isinstance(v, Symbol):
        v = v.name
    try:
        return (v[self.key],)
    except:
        return ()

@extend(syntax.Axis.label)
def exec(self, v):
    v = preserve(_unwrap(v))
    return (v.label,) if isinstance(v, Record) else ()

@extend(syntax.Axis.keys)
def exec(self, v):
    v = preserve(_unwrap(v))
    if isinstance(v, Symbol):
        return tuple(range(len(v.name)))
    if isinstance(v, basestring_) or \
       isinstance(v, list) or \
       isinstance(v, tuple) or \
       isinstance(v, bytes):
        return tuple(range(len(v)))
    if isinstance(v, Record):
        return tuple(range(len(v.fields)))
    if isinstance(v, dict):
        return tuple(v.keys())
    return ()

@extend(syntax.Axis.length)
def exec(self, v):
    v = preserve(_unwrap(v))
    if isinstance(v, Symbol):
        return (len(v.name),)
    if isinstance(v, basestring_) or \
       isinstance(v, list) or \
       isinstance(v, tuple) or \
       isinstance(v, bytes) or \
       isinstance(v, dict):
        return (len(v),)
    if isinstance(v, Record):
        return (len(v.fields),)
    return (0,)

@extend(syntax.Axis.annotations)
def exec(self, v):
    return tuple(v.annotations) if is_annotated(v) else ()

@extend(syntax.Axis.embedded)
def exec(self, v):
    return (v.embeddedValue,) if isinstance(v, Embedded) else ()

@extend(syntax.Filter.nop)
def exec(self, v):
    return (v,)

@extend(syntax.Filter.compare)
def exec(self, v):
    return (v,) if self.op.compare(v, self.literal) else ()

@extend(syntax.Comparison.eq)
def compare(self, lhs, rhs):
    return lhs == rhs

@extend(syntax.Comparison.ne)
def compare(self, lhs, rhs):
    return lhs != rhs

@extend(syntax.Comparison.lt)
def compare(self, lhs, rhs):
    return lhs < rhs

@extend(syntax.Comparison.ge)
def compare(self, lhs, rhs):
    return lhs >= rhs

@extend(syntax.Comparison.gt)
def compare(self, lhs, rhs):
    return lhs > rhs

@extend(syntax.Comparison.le)
def compare(self, lhs, rhs):
    return lhs <= rhs

@extend(syntax.Filter.regex)
def exec(self, v):
    r = re.compile(self.regex)
    if isinstance(v, Symbol):
        return (v,) if r.match(v.name) else ()
    if isinstance(v, basestring_):
        return (v,) if r.match(v) else ()
    return ()

@extend(syntax.Filter.test)
def exec(self, v):
    return (v,) if self.pred.exec(v) else ()

@extend(syntax.Filter.real)
def exec(self, v):
    if isinstance(v, Float):
        return (v.value,)
    if type(v) == float:
        return (v,)
    if type(v) == int:
        return (float(v),)
    return ()

@extend(syntax.Filter.int)
def exec(self, v):
    if isinstance(v, Float):
        return (int(v.value()),)
    if type(v) == float:
        return (int(v),)
    if type(v) == int:
        return (v,)
    return ()

@extend(syntax.Filter.kind)
def exec(self, v):
    return self.kind.exec(v)

@extend(syntax.ValueKind.Boolean)
def exec(self, v):
    return (v,) if type(v) == bool else ()

@extend(syntax.ValueKind.Float)
def exec(self, v):
    return (v,) if isinstance(v, Float) else ()

@extend(syntax.ValueKind.Double)
def exec(self, v):
    return (v,) if type(v) == float else ()

@extend(syntax.ValueKind.SignedInteger)
def exec(self, v):
    return (v,) if type(v) == int else ()

@extend(syntax.ValueKind.String)
def exec(self, v):
    return (v,) if isinstance(v, basestring_) else ()

@extend(syntax.ValueKind.ByteString)
def exec(self, v):
    return (v,) if isinstance(v, bytes) else ()

@extend(syntax.ValueKind.Symbol)
def exec(self, v):
    return (v,) if isinstance(v, Symbol) else ()

@extend(syntax.ValueKind.Record)
def exec(self, v):
    return (v,) if isinstance(v, Record) else ()

@extend(syntax.ValueKind.Sequence)
def exec(self, v):
    return (v,) if type(v) in [list, tuple] else ()

@extend(syntax.ValueKind.Set)
def exec(self, v):
    return (v,) if type(v) in [set, frozenset] else ()

@extend(syntax.ValueKind.Dictionary)
def exec(self, v):
    return (v,) if isinstance(v, dict) else ()

@extend(syntax.ValueKind.Embedded)
def exec(self, v):
    return (v,) if isinstance(v, Embedded) else ()

if __name__ == '__main__':
    import sys
    sel = parse(sys.argv[1])
    d = Parser()
    while True:
        chunk = sys.stdin.readline()
        if chunk == '': break
        d.extend(chunk)
        for v in d:
            for w in sel.exec(v):
                print(stringify(w))
