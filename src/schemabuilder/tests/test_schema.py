import jsonschema

from .. import schema
from .. import primitives
from . import utils


class TestSchema(utils.TestCase):

    def test_schema(self):
        s = schema.Schema()
        self.assertEqual(
            {
                "$schema": "http://json-schema.org/draft-04/schema#",
                "definitions": {}
            },
            s.to_dict()
        )

    def test_define(self):
        s = schema.Schema()
        s.define("user", primitives.Object())
        self.assertEqual(
            {
                "$schema": "http://json-schema.org/draft-04/schema#",
                "definitions": {
                    "user": {
                        "type": "object"
                    }
                }
            },
            s.to_dict()
        )

    def test_validator(self):
        s = schema.Schema()
        s.define(
            "user",
            primitives.Object(properties={
                "name": primitives.Str(required=True)
            })
        )
        v = s.validator("user")
        v.validate({"name": "bob"})

    def test_validator_fails(self):
        s = schema.Schema()
        s.define(
            "user",
            primitives.Object(properties={
                "name": primitives.Str(required=True)
            })
        )
        v = s.validator("user")
        self.assertRaises(jsonschema.ValidationError, v.validate, {})

    def test_ref(self):
        s = schema.Schema()
        name = s.define("name", primitives.Str())
        s.define(
            "user",
            primitives.Object(properties={
                "name": name(required=True)
            })
        )
        self.assertEqual(
            {
                "name": {"type": "string"},
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"$ref": "#/definitions/name"}
                    },
                    "required": ["name"]

                }
            },
            s.to_dict().get("definitions")
        )

    def test_ref_validate(self):
        s = schema.Schema()
        name = s.define("name", primitives.Str())
        user = s.define(
            "user",
            primitives.Object(properties={
                "name": name(required=True)
            })
        )
        user.validate({"name": "bob"})

    def test_ref_validate_fails(self):
        s = schema.Schema()
        name = s.define("name", primitives.Str())
        user = s.define(
            "user",
            primitives.Object(properties={
                "name": name(required=True)
            })
        )
        self.assertRaises(jsonschema.ValidationError, user.validate, {})
