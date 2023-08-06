import copy
import unittest

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = False

from ioc.schema.parser import SchemaParser
from ioc.schema.resolver import SchemaResolver
from ioc import provider
import ioc



@unittest.skipIf(not sqlalchemy, "sqlalchemy is not installed")
class SQLAlchemyTestCase(unittest.TestCase):
    dependencies = [
        {
            "name": "SQLALCHEMY_CONNECTION_DSN",
            "value": "sqlite://"
        },
        {
            "name": "sqlalchemy.engine",
            "factory": {
                "type": "symbol",
                "value": "sqlalchemy.create_engine"
            },
            "args": [
                {"type": "ioc", "value": "SQLALCHEMY_CONNECTION_DSN"}
            ],
            "kwargs": {
                "echo": {"type":"literal", "value": True}
            }
        },
        {
            "name": "database.session_factory",
            "factory": {"type":"symbol","value":"sqlalchemy.orm.sessionmaker"},
            "kwargs": {
                "bind": {"type":"ioc","value":"sqlalchemy.engine"}
            },
            "chain": [
                {"type":"symbol","value":"sqlalchemy.orm.scoped_session"}
            ]
        }
    ]

    def setUp(self):
        self.parser = SchemaParser()
        self.resolver = SchemaResolver()
        self.schema = self.parser.load(self.dependencies)

    def tearDown(self):
        provider.teardown()


    def get_schema(self):
        return copy.deepcopy(self.schema)

    def test_dsn_gets_resolved(self):
        schema = self.parser.load(self.dependencies[:1])
        schema.resolve(self.resolver)

        self.assertTrue(provider.is_satisfied(self.dependencies[0]['name']))

    def test_engine_gets_resolved(self):
        schema = self.parser.load(self.dependencies[0:2])
        schema.resolve(self.resolver)

        self.assertTrue(provider.is_satisfied(self.dependencies[1]['name']))

    def test_scoped_session(self):
        # The behavior of the sqlalchemy scoped_session() must
        # be correctly proxied by the ioc framework.
        self.schema.resolve(self.resolver)
        session_factory = ioc.require('database.session_factory')
        s1 = session_factory()
        s2 = session_factory()
        self.assertEqual(s1, s2)
