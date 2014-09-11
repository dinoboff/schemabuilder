from .. import primitives
from . import utils


class TestGeneric(utils.TestCase):

    def test_to_dict(self):
        generic = primitives.Generic()
        self.assertEqual({}, generic.to_dict())

    def test_id(self):
        generic = primitives.Generic(id="#user")
        self.assertEqual({"id": "#user"}, generic.to_dict())

    def test_desc(self):
        generic = primitives.Generic(desc="some schema definition")
        self.assertEqual({
                "description": "some schema definition"
            },
            generic.to_dict()
        )

    def test_title(self):
        generic = primitives.Generic(title="Definition")
        self.assertEqual({
                "title": "Definition"
            },
            generic.to_dict()
        )

    def test_default(self):
        generic = primitives.Generic(default="foo")
        self.assertEqual({
                "default": "foo"
            },
            generic.to_dict()
        )

    def test_enum(self):
        generic = primitives.Generic(enum=[1,2,])
        self.assertEqual({
                "enum":[1,2]
            },
            generic.to_dict()
        )

    def test_null_allowed(self):
        generic = primitives.Generic(type="string", null_allowed=True)
        self.assertEqual({
                "type": ["string", "null"]
            },
            generic.to_dict()
        )

    def test_null_allowed_with_array(self):
        generic = primitives.Generic(type=["string"], null_allowed=True)
        self.assertEqual({
                "type": ["null", "string"]
            },
            generic.to_dict()
        )

    def test_copy(self):
        generic_1 = primitives.Generic()
        generic_2 = generic_1(default="Guest")
        self.assertIsNot(generic_1, generic_2)
        self.assertIsNone(generic_1.default)
        self.assertEqual("Guest", generic_2.default)


class TestStr(utils.TestCase):

    def test_to_dict(self):
        s = primitives.Str()
        self.assertEqual({"type": "string"}, s.to_dict())

    def test_min(self):
        s = primitives.Str(min=3)
        self.assertEqual(
            {"type": "string", "minLength": 3},
            s.to_dict()
        )

    def test_max(self):
        s = primitives.Str(max=20)
        self.assertEqual(
            {"type": "string", "maxLength": 20},
            s.to_dict()
        )

    def test_pattern(self):
        s = primitives.Str(pattern=r"^[a-z]+$")
        self.assertEqual(
            {"type": "string", "pattern": "^[a-z]+$"},
            s.to_dict()
        )

    def test_format(self):
        s = primitives.Str(format="email")
        self.assertEqual(
            {"type": "string", "format": "email"},
            s.to_dict()
        )


class TestNumber(utils.TestCase):

    def test_to_dict(self):
        n = primitives.Number()
        self.assertEqual({"type": 'number'}, n.to_dict())

    def test_multiplicity(self):
        n = primitives.Number(multiple_of=1.0)
        self.assertEqual(
            {"type": 'number', "multipleOf": 1.0},
            n.to_dict()
        )

    def test_min(self):
        n = primitives.Number(min=1.0)
        self.assertEqual(
            {"type": 'number', "minimum": 1.0},
            n.to_dict()
        )

    def test_max(self):
        n = primitives.Number(max=1.0)
        self.assertEqual(
            {"type": 'number', "maximum": 1.0},
            n.to_dict()
        )

    def test_exclusive_min(self):
        n = primitives.Number(min=1.0, exclusive_min=True)
        self.assertEqual(
            {"type": 'number', "minimum": 1.0, "exclusiveMinimum": True},
            n.to_dict()
        )

    def test_exclusive_max(self):
        n = primitives.Number(max=1.0, exclusive_max=True)
        self.assertEqual(
            {"type": 'number', "maximum": 1.0, "exclusiveMaximum": True},
            n.to_dict()
        )


class TestInt(utils.TestCase):

    def test_to_dict(self):
        i = primitives.Int()
        self.assertEqual({"type": 'integer'}, i.to_dict())

    def test_base_type(self):
        i = primitives.Int(multiple_of=1.0)
        self.assertTrue(isinstance(i.multiple_of, int))


class TestObject(utils.TestCase):

    def test_to_dict(self):
        o = primitives.Object()
        self.assertEqual({"type": "object"}, o.to_dict())

    def test_properties(self):
        o = primitives.Object(properties={'name': primitives.Str()})
        self.assertEqual(
            {"type": "object", "properties": {"name": {"type": "string"}}},
            o.to_dict()
        )

    def test_additional_properties(self):
        o = primitives.Object(additional_properties=False)
        self.assertEqual(
            {"type": "object", "additionalProperties": False},
            o.to_dict()
        )

    def test_pattern_properties(self):
        o = primitives.Object(pattern_properties={'^[0-9]$': primitives.Str()})
        self.assertEqual(
            {"type": "object", "patternProperties": {"^[0-9]$": {"type": "string"}}},
            o.to_dict()
        )

    def test_required(self):
        o = primitives.Object(properties={'name': primitives.Str(required=True)})
        self.assertEqual(
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name",]
            },
            o.to_dict()
        )

    def test_extra_required(self):
        o = primitives.Object(
            required=('email',),
            properties={'name': primitives.Str(required=True)}
        )
        self.assertEqual(
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["email", "name"]
            },
            o.to_dict()
        )

    def test_size(self):
        o = primitives.Object(min=2, max=3)
        self.assertEqual(
            {"type": "object", "minProperties": 2, "maxProperties": 3},
            o.to_dict()
        )

    def test_dependencies(self):
        o = primitives.Object(
            properties={
                'name': primitives.Str(dependencies=['email'])
            }
        )
        self.assertEqual(
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "dependencies": {
                    "name": ["email"]
                }
            },
            o.to_dict()
        )

    def test_one_off(self):
        with_name = primitives.Object(
            properties={"name": primitives.Str(required=True)}
        )
        with_email = primitives.Object(
            properties={"email": primitives.Str(required=True)}
        )
        o = primitives.Object(one_of=(with_name, with_email,))
        self.assertEqual(
            {
                "type": "object",
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"}
                        },
                        "required": ["name"]
                    },
                    {
                        "type": "object",
                        "properties": {
                            "email": {"type": "string"}
                        },
                        "required": ["email"]
                    },
                ]
            },
            o.to_dict()
        )

    def test_all_off(self):
        with_name = primitives.Object(
            properties={"name": primitives.Str(required=True)}
        )
        with_email = primitives.Object(
            properties={"email": primitives.Str(required=True)}
        )
        o = primitives.Object(all_of=(with_name, with_email,))
        self.assertEqual(
            {
                "type": "object",
                "allOf": [
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"}
                        },
                        "required": ["name"]
                    },
                    {
                        "type": "object",
                        "properties": {
                            "email": {"type": "string"}
                        },
                        "required": ["email"]
                    },
                ]
            },
            o.to_dict()
        )

    def test_any_off(self):
        with_name = primitives.Object(
            properties={"name": primitives.Str(required=True)}
        )
        with_email = primitives.Object(
            properties={"email": primitives.Str(required=True)}
        )
        o = primitives.Object(any_of=(with_name, with_email,))
        self.assertEqual(
            {
                "type": "object",
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"}
                        },
                        "required": ["name"]
                    },
                    {
                        "type": "object",
                        "properties": {
                            "email": {"type": "string"}
                        },
                        "required": ["email"]
                    },
                ]
            },
            o.to_dict()
        )


class TestArray(utils.TestCase):

    def test_to_dict(self):
        a = primitives.Array()
        self.assertEqual({"type": "array"}, a.to_dict())

    def test_items(self):
        a = primitives.Array(items=primitives.Str())
        self.assertEqual(
            {"type": "array", "items": {"type": "string"}},
            a.to_dict()
        )

    def test_tuples(self):
        a = primitives.Array(
            items=(primitives.Str(), primitives.Int()),
            additional_items=False
        )
        self.assertEqual(
            {
                "type": "array",
                "items": [{"type": "string"},  {"type": "integer"}],
                "additionalItems": False
            },
            a.to_dict()
        )

    def test_size(self):
        a = primitives.Array(items=primitives.Str(), min=2, max=3)
        self.assertEqual(
            {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
                "maxItems": 3,
            },
            a.to_dict()
        )

    def test_is_set(self):
        a = primitives.Array(items=primitives.Str(), is_set=True)
        self.assertEqual(
            {
                "type": "array",
                "items": {"type": "string"},
                "uniqueItems": True
            },
            a.to_dict()
        )


class TestBool(utils.TestCase):

    def test_to_dict(self):
        b = primitives.Bool()
        self.assertEqual({"type": "boolean"}, b.to_dict())

