from .values import ImmutableDict, dict_kvs, Embedded, Record

def map_embeddeds(f, v):
    def walk(v):
        if isinstance(v, Embedded):
            return f(v.embeddedValue)
        elif isinstance(v, (list, tuple)):
            return tuple(walk(w) for w in v)
        elif isinstance(v, (set, frozenset)):
            return frozenset(walk(w) for w in v)
        elif isinstance(v, dict):
            return ImmutableDict.from_kvs(walk(w) for w in dict_kvs(v))
        elif isinstance(v, Record):
            return Record(walk(v.key), walk(v.fields))
        else:
            return v
    return walk(v)
