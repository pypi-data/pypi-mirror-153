# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asserto', 'asserto.descriptors', 'asserto.handlers']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.4.1,<13.0.0']

setup_kwargs = {
    'name': 'asserto',
    'version': '0.0.5a0',
    'description': 'A fluent DSL for python assertions.',
    'long_description': '![Asserto](.github/images/logo.png)\n\n![version](https://img.shields.io/pypi/v/asserto?color=%2342f54b&label=asserto&style=flat-square)\n[![codecov](https://codecov.io/gh/symonk/asserto/branch/main/graph/badge.svg)](https://codecov.io/gh/symonk/asserto)\n[![docs](https://img.shields.io/badge/documentation-online-brightgreen.svg)](https://symonk.github.io/asserto/)\n\n## Asserto:\n\nAsserto is a clean, fluent and powerful assertion library for python.  We recommend using `pytest` as a test\nrunner but asserto will work well with any test runner.\n\n>Asserto was developed using pytest as it\'s test runner and has a `pytest-asserto` plugin that exposes asserto\n>through a fixture.  Asserto will work on any runner or even without one.  Note: It is common practice for a\n>test runner to apply assertion rewriting to change the behaviour of the `assert` keyword under the hood.\n\nThe main features of asserto are (and will be):\n\n+ Chainable and Fluent API.\n+ Ability for both `Hard` and `Soft` assertions.\n+ Rich diffs to highlight problems, reduce churn and improve effeciency and debuggability.\n+ Dynamic assertions; check any obj attribute or invoke any of it\'s function types.\n+ Robust set of methods out of the box for common types.\n+ Extensibility.  Bolt on your own assertions at runtime.\n+ Human error detection, elaborate warnings when something is amiss.\n+ Much more to come.\n\n\n## Feature Set:\n\n#### Fluent API:\n\n`Asserto` exposes a fully fluent API for chaining assertions against a value.\n\n```python\nfrom asserto import asserto\n\n\ndef test_multiple_assert_fluency() -> None:\n    asserto("Hello").has_length(5).match(r"\\w{5}$").ends_with("lo").starts_with("Hel")\n```\n\n----\n\n#### Soft Assertions:\n\n\n`Asserto` Has `soft` capabilities; allowing multiple assertions to be performed before failing with a\nsummary of the failures.\n\n```python\nfrom asserto import asserto\n\ndef test_baz() -> None:\n    with asserto("Baz") as context:\n        # asserto when used in a python context is run in \'soft\' mode;\n        # upon exiting the context; congregated errors are subsequently raised (if any)\n        context.starts_with("B").ends_with("z").is_equal_to("Baz").has_length(2)  # Ends in a failure.\n```\n\nWill result in the following:\n\n```shell\n    def test_foo(asserto) -> None:\n>       with asserto("Bar") as context:\nE       AssertionError: 1 Soft Assertion Failures\nE       [AssertionError("Length of: \'Bar\' was not equal to: 2")]\n```\n\n-----\n\n#### Exception Handling:\n\n`Asserto` has the ability to assert exceptions are raised on `callables` using a simple API.\n\n```python\nfrom asserto import asserto\nimport typing\n\n\ndef simple_callable(x: int) -> typing.NoReturn:\n    raise ValueError(x)\n\n\ndef test_exc_handling():\n    asserto(simple_callable).should_raise(ValueError).when_called_with(x=25)\n```\n\n-----\n\n#### Dynamic Lookups:\n\n`Asserto` has the ability to dynamically lookup attributes on any object type.  This is\nhandled using the `attr_is(expected)` syntax.\n\n```python\nfrom asserto import asserto\n\n\nclass Foo:\n\n    def __init__(self, x) -> None:\n        self.x = x\n\n    def double_x(self) -> int:\n        return self.x * 2\n\n\ndef test_foo_dynamically() -> None:\n     # dynamically looking up `x` (attr) or `double_x` bound method & invoking it!\n    asserto(Foo(10)).x_is(10).double_x_is(20)\n```\n\n-----\n\n#### Dynamic assert registration\n\n`Asserto` allows users to easily bolt on their assertion functions.\n\n```python\nfrom asserto import asserto\nfrom asserto import register_assert\n\n@register_assert  # Option 1.\ndef custom_assert(self):\n    if self.actual != 5:\n        self.error(f"{self.actual} did not equal five!")\n\nregister_assert(custom_assert)  # Option 2\n\n\ndef test_user_defined_callables() -> None:\n    asserto(6).custom_assert()\n```\n\nyields the following:\n\n```console\nE       AssertionError: 6 did not equal five!\n```\n\n-----\n',
    'author': 'symonk',
    'author_email': 'jackofspaces@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
