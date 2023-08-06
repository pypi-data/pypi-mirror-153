# pylint: skip-file
import ioc


ioc.provide('SomeDependency', "Hello world!")


@ioc.inject('greeting', 'SomeDependency')
def f(greeting):
    return greeting


@ioc.inject('bar', 'SomeDependency')
@ioc.inject('baz', 'SomeDependency')
class Foo:
    taz = ioc.class_property('SomeDependency')


print(f"f() = {f()}")
print(f"ioc.require('SomeDependency') = {ioc.require('SomeDependency')}")
print(f"Foo.bar = {Foo.bar}")
print(f"Foo.baz = {Foo.baz}")
print(f"Foo.taz = {Foo.taz}")
