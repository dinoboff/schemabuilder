"""Defines building blocks for a json-schema document


"""
import copy

from . import utils


class Generic(utils.ToDictMixin):
    """Base schema class

    Defines generic object with the default attribute most other json
    object accept, including description, title, default or enum.

    :param id: schema id.
    :param desc: schema description.
    :param title: schema title.
    :param default: default value (ignored by most validator).
    :param enum: list of valid value.
    :param required: marks the schema as required.
    :param format: value format (like `uri` or `email`).
    :param type: schema type.
    :param one_of: list of schema. The value must validate against one
                   of them.
    :param any_of: list of schema. The value must validate against one
                   or many of the schema.
    :param all_of: list of schema. The value must validate against all
                   of them.

    """

    def __init__(self, **kw):
        self._update(**kw)

    def _update(
        self,
        id=None,
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
        self.id = id
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

    def __call__(self, **kw):
        generic = copy.copy(self)
        generic._update(**kw)
        return generic


class Str(Generic):
    """a String type with its optional min/max length and pattern
    attributes.

    :param min: minimum length of the string.
    :param max: maximum length of the string.
    :param pattern: regex pattern the string should validate against.

    """

    def _update(self, min=None, max=None, pattern=None, **kw):
        kw.setdefault("type", "string")
        super(Str, self)._update(**kw)
        self.pattern = pattern
        if min is not None:
            self.min_length = int(min)
        if max is not None:
            self.max_length = int(max)


class Number(Generic):
    """A number type with its multipleOf and range attributes.

    :param min: minimum valid value.
    :param max: maximum valid value.
    :param exclusive_min: should the minimum valid be exclusive.
    :param exclusive_max: should the maximum valid be exclusive.
    :param multiple_of: a value the number should be a multiple of.

    """
    _base_type = float

    def _update(
        self,
        min=None,
        max=None,
        exclusive_min=None,
        exclusive_max=None,
        multiple_of=None,
        **kw
    ):
        kw.setdefault("type", "number")
        super(Number, self)._update(**kw)
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

    def _update(self, **kw):
        kw.setdefault("type", "integer")
        super(Int, self)._update(**kw)


class Bool(Generic):
    """Boolean type

    """
    def _update(self, **kw):
        kw.setdefault("type", "boolean")
        super(Bool, self)._update(**kw)


class Object(Generic):
    """An object type.

    :param properties: dict of properties, key -> property type.
    :param pattern_properties: like properties, but the keys are defines
                               by a regex pattern.

    :param additional_properties: should there be any additional
                                  properties?

    :param min: minimum number of properties.
    :param max: maximum number of properties.
    :param required: list of properties names that are required.


    """

    def _update(
        self,
        properties=None,
        pattern_properties=None,
        additional_properties=None,
        min=None,
        max=None,
        required=(),
        **kw
    ):
        kw.setdefault("type", "object")
        super(Object, self)._update(**kw)

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
    def _update(
        self,
        items=None,
        additional_items=None,
        min=None,
        max=None,
        is_set=None,
        **kw
    ):
        kw.setdefault("type", "array")
        super(Array, self)._update(**kw)
        self.type = "array"
        self.items = items
        self.min_items = min
        self.max_items = max
        if additional_items is not None:
            self.additional_items = bool(additional_items)
        if is_set is not None:
            self.unique_items = is_set
