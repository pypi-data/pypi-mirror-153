# pylint: skip-file
import asyncio
import unittest
import unittest.mock

import ioc


class AsyncInjectionTestCase(unittest.TestCase):

    class context_manager_class:

        def __init__(self):
            self.__aenter__ = unittest.mock.AsyncMock()
            self.__aexit__ = unittest.mock.AsyncMock()

    def setUp(self):
        pass

    def tearDown(self):
        ioc.teardown()

    def test_inject_function(self):
        dep = lambda x: x
        ioc.provide('foo', dep)
        self.assertEqual(asyncio.run(f()), dep)

    def test_inject_async_function(self):
        async def dep():
            pass
        ioc.provide('foo', dep)
        self.assertEqual(asyncio.run(f()), dep)

    def test_inject_async_context_manager(self):
        dep = self.context_manager_class()
        ioc.provide('foo', dep)
        result = asyncio.run(f())
        dep.__aenter__.assert_called_once()
        dep.__aexit__.assert_called_once_with(None, None, None)

    def test_inject_async_context_manager_with_exception(self):
        exc = Exception()
        dep = self.context_manager_class()
        dep.__aenter__ = unittest.mock.AsyncMock(side_effect=exc)
        ioc.provide('foo', dep)
        with self.assertRaises(Exception):
            result = asyncio.run(f())
        dep.__aenter__.assert_called_once()
        dep.__aexit__.assert_called_once_with(Exception, exc, None)

    def test_inject_async_context_manager_preserved_initial_state(self):
        dep = self.context_manager_class()

        @ioc.context('foo', 'foo')
        async def f(foo):
            foo.bar = 1
            self.assertNotEqual(dep, foo)

        ioc.provide('foo', dep)
        asyncio.run(f())
        self.assertTrue(not hasattr(dep, 'bar'))


@ioc.context('injected', 'foo')
async def f(injected):
    return injected
