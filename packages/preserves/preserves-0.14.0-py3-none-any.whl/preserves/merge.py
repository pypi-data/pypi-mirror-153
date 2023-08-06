from .values import ImmutableDict, dict_kvs, Embedded, Record

def merge_embedded_id(a, b):
    return a if a is b else None

def merge(v0, *vs, merge_embedded=None):
    v = v0
    for vN in vs:
        v = merge2(v, vN, merge_embedded=merge_embedded)
    return v

def _die():
    raise ValueError('Cannot merge items')

def merge_seq(aa, bb, merge_embedded=None):
    if len(aa) != len(bb): _die()
    return [merge2(a, b, merge_embedded=merge_embedded) for (a, b) in zip(aa, bb)]

def merge2(a, b, merge_embedded=None):
    if a == b:
        return a
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return merge_seq(a, b)
    if isinstance(a, (set, frozenset)) and isinstance(b, (set, frozenset)):
        _die()
    if isinstance(a, dict) and isinstance(b, dict):
        r = {}
        for (ak, av) in a.items():
            bv = b.get(ak, None)
            r[ak] = av if bv is None else merge2(av, bv, merge_embedded=merge_embedded)
        for (bk, bv) in b.items():
            if bk not in r:
                r[bk] = bv
        return r
    if isinstance(a, Record) and isinstance(b, Record):
        return Record(merge2(a.key, b.key, merge_embedded=merge_embedded),
                      merge_seq(a.fields, b.fields, merge_embedded=merge_embedded))
    if isinstance(a, Embedded) and isinstance(b, Embedded):
        m = (merge_embedded or merge_embedded_id)(a.embeddedValue, b.embeddedValue)
        if m is None: _die()
        return Embedded(m)
    _die()
