# schemabuilder

Helper to build json schema definitions


```
import schemabuilder as jsb

my_service = jsb.Schema(
    id='http://example.com/definitions#',
    desc='Schema for my services API data'
)


name = my_service.define('name', jsb.String(
    pattern=r'^[a-zA-Z][a-zA-Z0-9 \']+$'
))

user = my_service.define('user', jsb.Object(
    properties={
        'id': jsb.String(required=True)
        'name': name(required=True)
        'email': jsb.String(required=True, format='email')
    }
))



json_data = {
    'id': 'abc',
    'name': 'Damien',
    'email': 'damien@example.com'
}

user.validate(json_data)
# or
my_service.ref('user').validate(json_data)

```

