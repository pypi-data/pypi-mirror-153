# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['observ']

package_data = \
{'': ['*']}

install_requires = \
['patchdiff>=0.3.3,<0.4.0']

setup_kwargs = {
    'name': 'observ',
    'version': '0.9.3',
    'description': 'Reactive state management for Python',
    'long_description': "[![PyPI version](https://badge.fury.io/py/observ.svg)](https://badge.fury.io/py/observ)\n[![CI status](https://github.com/fork-tongue/observ/workflows/CI/badge.svg)](https://github.com/fork-tongue/observ/actions)\n\n# Observ 👁\n\nObserv is a Python port of [Vue.js](https://vuejs.org/)' [computed properties and watchers](https://v3.vuejs.org/api/basic-reactivity.html). It is event loop/framework agnostic and has only one pure-python dependency ([patchdiff](https://github.com/Korijn/patchdiff)) so it can be used in any project targeting Python >= 3.7.\n\nObserv provides the following two benefits for stateful applications:\n\n1) You no longer need to manually invalidate and recompute state (e.g. by dirty flags):\n    * computed state is invalidated automatically\n    * computed state is lazily re-evaluated\n2) You can react to changes in state (computed or not), enabling unidirectional flow:\n    * _state changes_ lead to _view changes_ (e.g. a state change callback updates a UI widget)\n    * the _view_ triggers _input events_ (e.g. a mouse event is triggered in the UI)\n    * _input events_ lead to _state changes_ (e.g. a mouse event updates the state)\n\n## API\n\n`from observ import reactive, computed, watch`\n\n* `state = reactive(state)`\n\nObserve nested structures of dicts, lists, tuples and sets. Returns an observable proxy that wraps the state input object.\n\n* `watcher = watch(func, callback, deep=False, immediate=False)`\n\nReact to changes in the state accessed in `func` with `callback(old_value, new_value)`. Returns a watcher object. `del`elete it to disable the callback.\n\n* `wrapped_func = computed(func)`\n\nDefine computed state based on observable state with `func` and recompute lazily. Returns a wrapped copy of the function which only recomputes the output if any of the state it depends on becomes dirty. Can be used as a function decorator.\n\n**Note:** The API has evolved and become more powerful since the original creation of this README. Track issue #10 to follow updates to observ's documentation.\n\n## Quick start and examples\n\nInstall observ with pip/pipenv/poetry:\n\n`pip install observ`\n\nCheck out [`examples/observe_qt.py`](https://github.com/Korijn/observ/blob/master/examples/observe_qt.py) for a simple example using observ.\n\nCheck out [`examples/store_with_undo_redo.py`](https://github.com/Korijn/observ/blob/master/examples/store_with_undo_redo.py) for a simple example using the included undo/redo-capable Store abstraction.\n\n## Caveat\n\nObserv keeps references to the object passed to the `reactive` in order to keep track of dependencies and proxies for that object. When the object that is passed into `reactive` is not managed by other code, then observ should cleanup its references automatically when the proxy is destroyed. However, if there is another reference to the original object, then observ will only release its own reference when the garbage collector is run and all other references to the object are gone. For this reason, the **best practise** is to keep **no references** to the raw data, and instead work with the reactive proxies **only**.\n",
    'author': 'Korijn van Golen',
    'author_email': 'korijn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fork-tongue/observ',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
