class DecodeError(ValueError): pass
class EncodeError(ValueError): pass
class ShortPacket(DecodeError): pass
