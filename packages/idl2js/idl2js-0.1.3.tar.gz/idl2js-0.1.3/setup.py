# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idl2js',
 'idl2js.intermediate',
 'idl2js.js',
 'idl2js.js.built_in',
 'idl2js.std',
 'idl2js.webidl',
 'idl2js.webidl.generated']

package_data = \
{'': ['*'], 'idl2js.js.built_in': ['mime/*'], 'idl2js.webidl': ['idls/*']}

install_requires = \
['antlr4-python3-runtime==4.10',
 'attrs>=21.4.0,<22.0.0',
 'click>=8.0.4,<9.0.0',
 'graphviz>=0.19.1,<0.20.0',
 'more-itertools>=8.12.0,<9.0.0',
 'stringcase>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'idl2js',
    'version': '0.1.3',
    'description': 'Grammar-based Fuzzer that uses WebIDL as a grammar.',
    'long_description': "# idl2js\n\n**Grammar-based Fuzzer that uses WebIDL as a grammar.**\n\n[![Build Status](https://img.shields.io/travis/PrVrSs/idl2js/master?style=plastic)](https://travis-ci.org/github/PrVrSs/idl2js)\n[![Codecov](https://img.shields.io/codecov/c/github/PrVrSs/idl2js?style=plastic)](https://codecov.io/gh/PrVrSs/idl2js)\n[![Python Version](https://img.shields.io/badge/python-3.10-blue?style=plastic)](https://www.python.org/)\n[![License](https://img.shields.io/cocoapods/l/A?style=plastic)](https://github.com/PrVrSs/idl2js/blob/master/LICENSE)\n\n\n## Quick start\n\n```shell script\npip install idl2js\n```\n\n\n### Build from source\n\n*Get source and install dependencies*\n```shell script\ngit clone https://gitlab.com/PrVrSs/idl2js.git\ncd idl2js\npoetry install\n```\n\n*Download ANTLR tool*\n```shell script\nwget https://www.antlr.org/download/antlr-4.10.1-complete.jar\n```\n\n*Generate parser*\n```shell script\nmake grammar\n```\n\n*Run tests*\n```shell script\nmake unit\n```\n\n\n### Examples\n\n```python\nimport logging\nfrom pathlib import Path\nfrom pprint import pprint\n\nfrom idl2js import InterfaceTarget, Transpiler\n\n\nclass Module(InterfaceTarget):\n    kind = 'Module'\n\n\nclass Global(InterfaceTarget):\n    kind = 'Global'\n\n\nclass Table(InterfaceTarget):\n    kind = 'Table'\n\n\nclass Memory(InterfaceTarget):\n    kind = 'Memory'\n\n\ndef main():\n    logging.getLogger('idl2js').setLevel(logging.DEBUG)\n\n    transpiler = Transpiler(\n        idls=(\n            str((Path(__file__).parent / 'webassembly.webidl').resolve()),\n        )\n    )\n\n    transpiler.transpile(\n        targets=[\n            Module,\n            Global,\n            Table,\n            Memory,\n        ]\n    )\n\n    pprint(transpiler.js_instances)\n\n\nif __name__ == '__main__':\n    main()\n\n```\n\n\n#### Output\n\n```js\ntry {v_0805c1325a3048aca879de7ce5f8c9a5 = new Int8Array()} catch(e){}\ntry {v_cfa435d6211f41df8a6af0a8543b3b37 = new WebAssembly.Module(v_0805c1325a3048aca879de7ce5f8c9a5)} catch(e){}\ntry {v_5deaeb375b774b54b6140be12322296a = {value: 'v128', mutable: true}} catch(e){}\ntry {v_788c98fd9d97444688f48fedb824130b = 'meoein'} catch(e){}\ntry {v_c3fcd21aecdd4ef6bb2060cbb0bd70fb = new WebAssembly.Global(v_5deaeb375b774b54b6140be12322296a, v_788c98fd9d97444688f48fedb824130b)} catch(e){}\ntry {v_73a4bd166ae34681a13acc70c2a67876 = {element: 'anyfunc', initial: 290477176, maximum: 3297392043}} catch(e){}\ntry {v_061571cb277b42beb33546c8d8c3ed07 = 'pahfbx'} catch(e){}\ntry {v_0c4bc44857394e40a9ade62f0eaadfca = new WebAssembly.Table(v_73a4bd166ae34681a13acc70c2a67876, v_061571cb277b42beb33546c8d8c3ed07)} catch(e){}\ntry {v_06ab1c4441d543ae8d4289c13a07c895 = {initial: 2477011723, maximum: 3809510539}} catch(e){}\ntry {v_5e251ff6ba8647e48a2d633ba42386f8 = new WebAssembly.Memory(v_06ab1c4441d543ae8d4289c13a07c895)} catch(e){}\n```\n\n\n### Links\n\n* [searchfox - webidl](https://searchfox.org/mozilla-central/source/dom/webidl)\n* [original webidl parser](https://github.com/w3c/webidl2.js)\n* [TSJS-lib-generator](https://github.com/microsoft/TSJS-lib-generator/tree/master/inputfiles/idl)\n* [ECMAScript® 2021 Language Specification](https://tc39.es/ecma262/)\n* [Web IDL](https://heycam.github.io/webidl)\n* [Web IDL Spec](https://webidl.spec.whatwg.org/)\n\n\n## Contributing\n\nAny help is welcome and appreciated.\n\n\n## License\n\n*idl2js* is licensed under the terms of the Apache-2.0 License (see the file LICENSE).\n",
    'author': 'Sergey Reshetnikov',
    'author_email': 'resh.sersh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PrVrSs/idl2js',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
