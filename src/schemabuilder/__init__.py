"""JSON schema builder.

:class:`schemabuilder.Str`, :class:`schemabuilder.Bool`,
:class:`schemabuilder.Number`, :class:`schemabuilder.Int`,
:class:`schemabuilder.Object` and :class:`schemabuilder.Array` should
be used to define schema.

:class:`schemabuilder.Schema` should be used to collect schema and
validate against them.

"""
from .primitives import Str
from .primitives import Number
from .primitives import Int
from .primitives import Bool
from .primitives import Object
from .primitives import Array
from .schema import Schema


__all__ = ["Str", "Number", "Int", "Bool", "Object", "Array", "Schema"]
