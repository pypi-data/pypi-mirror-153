'''Provides tooling to 'setup_test' pytest market'''

from typing import TYPE_CHECKING, Any, Callable, MutableMapping, Tuple

import mock

import nawah.utils
from nawah.config import Config
from nawah.utils._config import config_module

if TYPE_CHECKING:
    from nawah.classes import L10N, Module


class MockCallRegistry:
    calls: MutableMapping[str, Callable]


class MockCall(mock.AsyncMock):
    '''MockCall is used as mock for 'call' Utility. In combination with 'setup_test' it is used to
    set the return of 'call' Utility based on values returned from 'calls' callables'''

    # pylint: disable=too-many-ancestors

    def __call__(self, *args, **kwargs):
        if args[0] in MockCallRegistry.calls:

            async def _():
                return MockCallRegistry.calls[args[0]](**kwargs)

            return _()

        if args[0].split('/')[0] in Config.modules:
            return _call(args[0], **kwargs)

        raise Exception(
            f'Call to endpoint \'{args[0]}\' not mocked, nor its module is setup for test'
        )


_call = nawah.utils.call
nawah.utils.call = MockCall()


def setup_test(
    *,
    module: 'Module' = None,
    mock_callables: bool = True,
    calls: MutableMapping[str, Callable] = None,
    l10n: MutableMapping[str, 'L10N'] = None,
    vars: MutableMapping[str, Any] = None,
    types=None,
):
    '''Setup Nawah runtime config for testing'''

    # pylint: disable=redefined-builtin

    Config.modules = {}
    Config.l10n = {}
    Config.vars = {}
    Config.types = {}

    if module:
        config_module(module_name=module.name, module=module)
        Config.modules[module.name] = module

        if mock_callables:
            for func in module.funcs.values():
                func.callable = mock.AsyncMock()

    if calls:
        MockCallRegistry.calls = calls

    if l10n:
        Config.l10n = l10n

    if vars:
        Config.vars = vars

    if types:
        Config.types = types
