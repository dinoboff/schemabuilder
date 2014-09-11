===================
JSON-Schema builder
===================

Helpers to build you define JSON schema for either validation or publication.

Requirements
============

It requires Python 2.7 and ``jsonschema``. ``jsonschema`` or ``setuptools``
should be installed with Python.


Install
=======

Using pip::

    pip install schemabuilder

Or easy_install::

    easty_install schemabuilder


You may install it manually::

    git clone https://github.com/dinoboff/schemabuilder.git
    cd schemabuilder
    python setup.py install


Usage
=====

Primitives
----------

JSON schema primitives are represented by object of type:

* ``schemabuilder.Str``
* ``schemabuilder.Bool``
* ``schemabuilder.Number``
* ``schemabuilder.Int``
* ``schemabuilder.Object``
* ``schemabuilder.Array``


.. code-block:: python

    >>> import schemabuilder as jsb
    >>> import pprint
    >>>
    >>> name = jsb.Str(pattern="^[a-zA-Z][- 'a-zA-Z0-9]+")
    >>> email = jsb.Str(format="email")
    >>> user = jsb.Object(properties={
    ...   'name': name(required=True),
    ...   'email': email(),
    ...   'home': jsb.Str(format='uri'),
    ... })
    >>> pprint.pprint(user.to_dict())
    {'properties': {'email': {'type': 'string'},
                    'home': {'format': 'uri', 'type': 'string'},
                    'name': {'type': 'string'}},
     'required': ['name'],
     'type': 'object'}


Schema
------

Schema collects those definitions for validation (using ``jsonschema``) or
publication.

.. code-block:: python

    >>> import schemabuilder as jsb
    >>> import pprint
    >>>
    >>> my_schemas = jsb.Schema(id='http://example.com/schemas.json#')
    >>> name = my_schemas.define(
    ...   'name', jsb.Str(pattern="^[a-zA-Z][- 'a-zA-Z0-9]+")
    ... )
    >>> email = my_schemas.define('email', jsb.Str(format="email"))
    >>> user = my_schemas.define('user', jsb.Object(properties={
    ...   'name': name(required=True),
    ...   'email': email(required=True),
    ... }))
    >>>
    >>> user.validate({'name': 'bob'})
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "schemabuilder/schema.py", line 50, in validate
        validator.validate(data)
      File "/Users/bob/pyenv/lib/python2.7/site-packages/jsonschema/validators.py", line 117, in validate
        raise error
    jsonschema.exceptions.ValidationError: 'email' is a required property
    
    Failed validating 'required' in schema:
        {'properties': {'email': {'$ref': '#/definitions/email'},
                        'name': {'$ref': '#/definitions/name'}},
         'required': ['name', 'email'],
         'type': 'object'}
    
    On instance:
        {'name': 'bob'}
    >>>
    >>> user.validate({'name': 'bob', 'email': 'bob@example.com'})
    >>>
    >>> import json
    >>> print json.dumps(my_schemas.to_dict(), indent=4)
    {
        "definitions": {
            "email": {
                "type": "string", 
                "format": "email"
            }, 
            "user": {
                "required": [
                    "name", 
                    "email"
                ], 
                "type": "object", 
                "properties": {
                    "name": {
                        "$ref": "#/definitions/name"
                    }, 
                    "email": {
                        "$ref": "#/definitions/email"
                    }
                }
            }, 
            "name": {
                "pattern": "^[a-zA-Z][- 'a-zA-Z0-9]+", 
                "type": "string"
            }
        }, 
        "id": "http://example.com/schemas.json#", 
        "$schema": "http://json-schema.org/draft-04/schema#"
    }

