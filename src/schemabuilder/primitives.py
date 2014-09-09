"""Defines building blocks for a json-schema document


"""
import collections


def _to_camel_case(s):
    """Convert a property attribute name to camel case.

    """
    return s[0] + s.title().replace("_", "")[1:]


class Generic(object):
    """Base class

    Defines generic object with the default attribute most other json
    object accept: description, title, default and enum.

    """

    def __init__(
        self,
        desc=None,
        title=None,
        default=None,
        enum=None,
        required=False,
        dependencies=None,
        type=None,
        format=None,
        one_of=None,
        all_of=None,
        any_of=None,
        null_allowed=False,
    ):
        self.description = desc
        self.title = title
        self.default = default
        self.enum = enum
        self.type = type
        self.format = format
        self.one_of = one_of
        self.all_of = all_of
        self.any_of = any_of
        self._required = required
        self._dependencies = dependencies
        if null_allowed and self.type:
            if isinstance(self.type, (list, tuple,)):
                types = set(self.type)
                types.add("null")
                self.type = list(types)
            else:
                self.type = [self.type, "null"]

    def to_dict(self):
        result = {}
        stack = collections.deque()
        stack.append((result, self.__dict__))
        while stack:
            dest, source = stack.pop()
            if isinstance(dest, dict):
                self._process_dict(dest, source, stack)
            else:
                self._process_list(dest, source, stack)
        return result

    @staticmethod
    def _process_dict(dest, source, stack):
        for k, v in source.iteritems():
            if v is None or k[0] == "_":
                continue
            cck = _to_camel_case(k)
            if isinstance(v, dict):
                dest[cck] = {}
                stack.append((dest[cck], v,))
            elif isinstance(v, (list, tuple,)):
                dest[cck] = []
                stack.append((dest[cck], v,))
            elif hasattr(v, "to_dict"):
                dest[cck] = v.to_dict()
            else:
                dest[cck] = v

    @staticmethod
    def _process_list(dest, source, stack):
        for v in source:
            if v is None:
                continue

            if isinstance(v, dict):
                dest.append({})
                stack.append((dest[-1], v,))
            if isinstance(v, (list, tuple,)):
                dest.append([])
                stack.append((dest[-1], v,))
            elif hasattr(v, "to_dict"):
                dest.append(v.to_dict())
            else:
                dest.append(v)


class Str(Generic):
    """a String type with its optional min/max length and pattern
    attributes.

    """

    def __init__(self, min=None, max=None, pattern=None, **kw):
        kw.setdefault("type", "string")
        super(Str, self).__init__(**kw)
        self.pattern = pattern
        if min is not None:
            self.min_length = int(min)
        if max is not None:
            self.max_length = int(max)


class Number(Generic):
    """A number type with its multipleOf and range attributes.

    """
    _base_type = float

    def __init__(
        self,
        min=None,
        max=None,
        exclusive_min=None,
        exclusive_max=None,
        multiple_of=None,
        **kw
    ):
        kw.setdefault("type", "number")
        super(Number, self).__init__(**kw)
        if multiple_of is not None:
            self.multiple_of = self._base_type(multiple_of)
        if min is not None:
            self.minimum = self._base_type(min)
        if max is not None:
            self.maximum = self._base_type(max)
        if exclusive_min is not None:
            self.exclusive_minimum = bool(exclusive_min)
        if exclusive_max is not None:
            self.exclusive_maximum = bool(exclusive_max)


class Int(Number):
    """An integer type with the same attributes than Number.

    """
    _base_type = int

    def __init__(self, **kw):
        kw.setdefault("type", "integer")
        super(Int, self).__init__(**kw)


class Bool(Generic):
    """Boolean type

    """
    def __init__(self, **kw):
        kw.setdefault("type", "boolean")
        super(Bool, self).__init__(**kw)


class Object(Generic):
    """An object type.

    """

    def __init__(self,
        properties=None,
        pattern_properties=None,
        additional_properties=None,
        min=None,
        max=None,
        required=(),
        **kw
    ):
        kw.setdefault("type", "object")
        super(Object, self).__init__(**kw)

        self.properties = properties
        self.pattern_properties = pattern_properties
        self.additional_properties = additional_properties
        self.min_properties = min
        self.max_properties = max
        self._required = required

    def to_dict(self):
        d = super(Object, self).to_dict()
        required, deps = self._requirements()
        if required:
            d["required"] = required
        if deps:
            d["dependencies"] = deps
        return d

    def _requirements(self):
        required = set(self._required)
        deps = {}
        if self.properties is None:
            return list(required), deps

        for k, v in self.properties.iteritems():
            if v._required:
                required.add(k)
            if v._dependencies:
                deps[k] = v._dependencies

        return list(required), deps


class Array(Generic):
    """Array type.

    """
    def __init__(
        self,
        items=None,
        additional_items=None,
        min=None,
        max=None,
        is_set=None,
        **kw
    ):
        kw.setdefault("type", "array")
        super(Array, self).__init__(**kw)
        self.type = "array"
        self.items = items
        self.min_items = min
        self.max_items = max
        if additional_items is not None:
            self.additional_items = bool(additional_items)
        if is_set is not None:
            self.unique_items = is_set

