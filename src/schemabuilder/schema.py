"""Define helpers to hold, publish and validate against schema
definitions.

"""
import jsonschema

from schemabuilder import utils


class Schema(utils.ToDictMixin):
    """Collects schema definitions

    """

    def __init__(self, id=None, desc=None):
        self.id = id
        self.desc = desc
        self.definitions = {}

    def to_dict(self):
        schema = super(Schema, self).to_dict()
        schema['$schema'] = "http://json-schema.org/draft-04/schema#"
        return schema

    def define(self, id, schema):
        self.definitions[id] = schema
        return _Ref(id, self)

    def ref_resolver(self):
        return jsonschema.RefResolver.from_schema(self.to_dict())

    def validator(self, id):
        return jsonschema.Draft4Validator(
            {'$ref': '#/definitions/%s' % id},
            resolver=self.ref_resolver()
        )


class _Ref(object):

    def __init__(self, id, schema):
        self.id = id
        self.schema = schema

    def validate(self, data):
        validator = self.schema.validator(self.id)
        validator.validate(data)
