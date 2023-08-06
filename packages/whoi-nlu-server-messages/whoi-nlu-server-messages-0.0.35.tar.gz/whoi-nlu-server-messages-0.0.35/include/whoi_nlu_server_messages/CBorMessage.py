from dataclasses import fields

from cbor2 import dumps, loads


class CBorMessage:

    def as_dict(self) -> dict:
        return {
            k: (
                v.as_dict() if isinstance(v, CBorMessage) else v
            ) for k, v in self.__dict__.items()
        }

    def to_bytes(self) -> bytes:
        return dumps(self.as_dict())

    def _ensure_types(self):
        for field in fields(self):
            if issubclass(field.type, CBorMessage):
                field_val = field.type(**getattr(self, field.name))
                field_val._ensure_types()
                setattr(self, field.name, field_val)

    @classmethod
    def from_bytes(cls, data: bytes) -> 'CBorMessage':
        d = loads(data)
        d.pop("_t", None)
        v = cls(**d)
        v._ensure_types()
        return v
