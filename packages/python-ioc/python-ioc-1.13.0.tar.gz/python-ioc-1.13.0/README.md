# Python Inversion-of-Control framework

## Synopsis

The `ioc` module provides a framework to dynamically inject dependencies
in Python applications. This intends to reduce coupling between application
and infrastructure, and application and third-party libraries.

## Usage

### Basic
In it's most basic usage, dependencies can be declared and invoked using a few simple
calls to functions in the `ioc` library.

```
>>> import ioc
>>>
>>> req = ioc.require('MY_REQUIREMENT')
>>> ioc.provide('MY_REQUIREMENT', 'foo')
>>> print(req)
'foo'
```

The procedure is simple: state your requirement by a symbolic name and call to `ioc.require()`, and then provide the requirement using `ioc.provide()`.

When an application fails to provide a dependency for a requirement, an exception is raised upon invocation:

```
>>> import ioc
>>>
>>> req = ioc.require('MY_REQUIREMENT')
>>> print(req)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "requirement.py", line 11, in inner
    self._setup()
  File "ioc/requirement.py", line 58, in _setup
    self._injected = self._provider.resolve(self._names[0])
  File "ioc/provider.py", line 33, in resolve
    raise UnsatisfiedDependency(name)
ioc.exc.UnsatisfiedDependency: MY_REQUIREMENT
```

### Class properties
A call to `ioc.require()` will not return the actual dependency (it might not be resolved yet) but a wrapper that mimics the behavior of the (to-be) injected dependency.

```
>>> import ioc
>>>
>>> repr(ioc.require('not_resolved'))
'<ioc.requirement.DeclaredRequirement object at 0x101db7ac8>'
```

This might not always be a desirable property, for example with Python C-extensions that enforce datatypes on their input parameters. To solve this problem, the `ioc` module provides the `ioc.class_property()` decorator. This adds a descriptor to a class that will always return the dependency as it was injected.

```
>>> import ioc
>>>
>>> class Foo:
...     bar = ioc.class_property('bar')
...
>>>
>>> ioc.provide('bar', 'baz')
>>>
>>> repr(Foo.bar)
'<property object at 0x101ce5ae8>'
>>>
>>> foo = Foo()
>>> repr(foo.bar)
"'baz'"
```

## Advanced usage

## Changelog

### 1.3

- Append ``symbol`` dependencies to an existing iterable.
- Load literal dependencies from environment variables.
- Fix parser loading literal dependencies as symbols.
- Allow default arguments in signatures with `ArgumentDependencyInjector`.
- `marshmallow` 3.0.0b11 compatibility.

### 1.2

- Add support for `copy.copy()` and `copy.deepcopy()`.
- Allow `default` argument with `ioc.class_property()`.
- Make `ioc.class_property()` a real class property.
- Allow overriding dependencies at runtime.
