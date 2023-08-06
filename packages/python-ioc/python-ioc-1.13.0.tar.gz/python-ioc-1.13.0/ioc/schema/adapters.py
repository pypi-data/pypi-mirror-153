import marshmallow
import six

from ioc.schema.requirement import SchemaRequirement
from ioc.schema.dependency import LiteralDependency
from ioc.schema.dependency import SimpleDependency
from ioc.schema.dependency import NestedDependency
from ioc.schema.dependency import DependencyCollection
from ioc.utils import is_valid_identifier


class BaseDependencyAdapter(marshmallow.Schema):

    @marshmallow.post_load
    def initialize_dependency(self, params, **kwargs):
        return SchemaRequirement(**params)

    @marshmallow.validates_schema
    def validate_value(self, params, **kwargs):
        if params.get('type') not in ('symbol','ioc'):
            return

        if not isinstance(params.get('value'), six.string_types):
            raise marshmallow.ValidationError(
                "'value' must hold a valid name",'value')

        if params.get('type') == 'symbol'\
        and not is_valid_identifier(params.get('value')):
            raise marshmallow.ValidationError(
                "'value' must hold a valid name",'value')


class ArgumentDependencyAdapter(BaseDependencyAdapter):
    type = marshmallow.fields.String(
        validate=marshmallow.validate.OneOf(['symbol','ioc','literal']),
        required=True)
    value = marshmallow.fields.Field(required=True)


class CallableDependencyAdapter(BaseDependencyAdapter):
    type = marshmallow.fields.String(
        validate=marshmallow.validate.OneOf(['symbol','ioc']),
        required=True)
    value = marshmallow.fields.Field(required=True)


class FileDependencyAdapter(marshmallow.Schema):
    type = marshmallow.fields.String(validate=marshmallow.validate.OneOf(['file']),
        required=True)
    name = marshmallow.fields.String(required=True)
    path = marshmallow.fields.String(required=True)

    @marshmallow.post_load
    def resolve(self, params, **kwargs):
        with open(params.pop('path'), 'rb') as f:
            params['value'] = f.read()
        return LiteralDependency(**params)


class SymbolDependencyAdapter(marshmallow.Schema):
    type = marshmallow.fields.String(validate=marshmallow.validate.OneOf(['symbol']),
        required=True)
    name = marshmallow.fields.String(required=True)
    value = marshmallow.fields.String(required=True)
    visibility = marshmallow.fields.String(missing='public', choices=['public','internal'])
    invoke = marshmallow.fields.Boolean(data_key='callable', missing=False)
    args = marshmallow.fields.List(marshmallow.fields.Field, missing=list)
    kwargs = marshmallow.fields.Dict(
        keys=marshmallow.fields.String,
        values=marshmallow.fields.Field,
        missing=dict
    )
    tags = marshmallow.fields.List(
        marshmallow.fields.String,
        required=False,
        missing=list
    )
    mode = marshmallow.fields.String(
        required=False,
        missing='declare',
        validate=[marshmallow.validate.OneOf(['append'])]
    )

    @marshmallow.post_load
    def resolve_symbol(self, params, **kwargs):
        symbol = params['value']
        if symbol == 'bytes':
            params['value'] = 'ioc.utils.bytesequence'
        return SimpleDependency(**params)


class LiteralDependencyAdapter(marshmallow.Schema):
    type = marshmallow.fields.String(
        validate=marshmallow.validate.OneOf(['literal']),
        required=False,
        missing='literal')
    name = marshmallow.fields.String(required=True)
    value = marshmallow.fields.Field(required=True)
    visibility = marshmallow.fields.String(missing='public', choices=['public','internal'])
    tags = marshmallow.fields.List(
        marshmallow.fields.String,
        required=False,
        missing=list
    )

    @marshmallow.post_load
    def resolve(self, params, **kwargs):
        return LiteralDependency(**params)


class NestedDependencyAdapter(marshmallow.Schema):
    name = marshmallow.fields.String(required=True)
    visibility = marshmallow.fields.String(missing='public', choices=['public','internal'])
    factory = marshmallow.fields.Nested(CallableDependencyAdapter, required=True)
    args = marshmallow.fields.List(
        marshmallow.fields.Nested(ArgumentDependencyAdapter),
        required=False,
        missing=list
    )
    kwargs = marshmallow.fields.Dict(
        keys=marshmallow.fields.String,
        values=marshmallow.fields.Nested(ArgumentDependencyAdapter),
        required=False,
        missing=dict
    )
    chain = marshmallow.fields.List(
        marshmallow.fields.Nested(ArgumentDependencyAdapter),
        required=False,
        missing=list
    )
    tags = marshmallow.fields.List(
        marshmallow.fields.String,
        required=False,
        missing=list
    )

    @marshmallow.post_load
    def resolve(self, params, **kwargs):
        if params.get('kwargs'):
            params['kwargs'] = {x: y
                for x,y in params.pop('kwargs').items()}

        return NestedDependency(**params)


class DependencyCollectionAdapter(marshmallow.Schema):
    name = marshmallow.fields.String(required=True)
    members = marshmallow.fields.List(
        marshmallow.fields.String,
        required=True
    )

    @marshmallow.post_load
    def resolve(self, params, **kwargs):
        return DependencyCollection(**params)

