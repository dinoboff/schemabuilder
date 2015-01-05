"""Define helpers to hold, publish and validate against schema
definitions.

"""
import weakref
import jsonschema

from . import primitives
from . import utils


class Schema(utils.ToDictMixin):
    """Collects schema definitions

    """

    def __init__(self, id=None, desc=None):
        self._id = id
        self._desc = desc
        self._schema = None
        self.definitions = {}

    def to_dict(self):
        """Return the schema as a dict ready to be serialized.

        """
        schema = super(Schema, self).to_dict()
        schema['$schema'] = "http://json-schema.org/draft-04/schema#"
        if self._id:
            schema['id'] = self._id
        if self._desc:
            schema['description'] = self._desc
        return schema

    def define(self, id, schema):
        """Add a schema to the list of definition

        :param id: id of the schema.
        :param schema: the schema as a dict or a
                       :class:schemabuilder.primitives.Generic
        :return: reference to schema.
        :rtype: :class:`schemabuilder.schema.Ref`

        """
        self.definitions[id] = schema
        self._schema = None
        return self.ref(id)

    def ref(self, id):
        return Ref(id, self)

    def ref_resolver(self):
        if self._schema is None:
            self._schema = self.to_dict()
        return jsonschema.RefResolver.from_schema(self._schema)

    def validator(self, id):
        """Create a validator for the current state of the schema.

        Note: a validator (the resolver it's using) is not thread safe.

        :param id: id of the schema in the list of definition.
        :return: a validator.
        :rtype: :class:`jsonschema.Draft4Validator`
        """
        return jsonschema.Draft4Validator(
            {'$ref': '#/definitions/%s' % id},
            resolver=self.ref_resolver()
        )


class Ref(primitives.Generic):
    """Reference to a schema inside a schema collection.

    Can be used to reference that schema in an other schema of the some
    collection.

    :param id: name of the schema
    :param schema: schema collection the schema resides.

    .. warning::
        The schema is saved as a weak reference. It will only be  able to
        validate data while a reference of that schema live somewhere
        else.

    """

    def __init__(self, id, schema, **kw):
        super(Ref, self).__init__(**kw)
        self._id = id
        self._schema = weakref.proxy(schema)

    def validate(self, data):
        """Validate the data against the schema.

        """
        validator = self._schema.validator(self._id)
        validator.validate(data)

    def to_dict(self):
        schema = super(Ref, self).to_dict()
        schema['$ref'] = '#/definitions/%s' % self._id
        return schema
