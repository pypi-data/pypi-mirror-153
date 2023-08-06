# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['beautifulspoon']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10,<5.0']

entry_points = \
{'console_scripts': ['beautifulspoon = beautifulspoon.cli:main',
                     'bspoon = beautifulspoon.cli:main']}

setup_kwargs = {
    'name': 'beautifulspoon',
    'version': '0.0.3',
    'description': '',
    'long_description': '# beautifulspoon\n\nThe project is a command line tool build upon [beautifulsoup](https://beautiful-soup-4.readthedocs.io/), or say this is a oneliner\'s tool for dealing with html files. With beautifulspoon, you can easily modify html files in the shell or within the scripts.\n\n## Install\n\n```\npip install beautifulspoon\n```\n\n## Usage\n\nLet\'s prepare a test.html as below:\n\n```\n<html>\n <head>\n  <title>\n   Hello World\n  </title>\n </head>\n <body>\n  <div class="container" id="root">\n   <a href="https://www.google.com">\n    Google\n   </a>\n  </div>\n </body>\n</html>\n```\n\nWe can explore the functions of beautifulspoon as follow.\n\n- Get the first HTML element matched selectors in `--select`.\n```\nbspoon test.html --select \'#root a\'\n```\n\n- `--set_name`, change the name of the selected tag.\n```\n$ bspoon debug/test.html --select a --set_name button|bspoon --select button\n<button href="https://www.google.com">\n Google\n</button>\n```\n\n- `--set_attr`, set attributes for the seleted tag.\n```\n$ bspoon test.html --select a --set_attr class link|bspoon --select a\n<a class="link" href="https://www.google.com">\n Google\n</a>\n```\n\n- `--append`, append a node(HTML) inside the selected node.\n```\n$ bspoon test.html --select a --append \'<b>Home</b>\'|bspoon --select a\n<a href="https://www.google.com">\n Google\n <b>\n  Home\n </b>\n</a>\n```\n\n- `--extend`, extend the string(text) of the selected node. Adding `--smooth` may help _smooth_ the extended content. \n```\n$ bspoon test.html --select a --extend \' It\' --smooth|bspoon --select a\n<a href="https://www.google.com">\n Google\n    It\n</a>\n\n$ bspoon test.html --select a --extend \' It\' --smooth|bspoon --select a\n<a href="https://www.google.com">\n Google It\n</a>\n```\n\n- `--insert`, insert a node(HTML) at the POS position inside the selected node. Arguments `--insert_before` and `--insert_after` are the same with `--insert`, with insert position specified at the first and the last slots.\n```\n$ bspoon test.html --select div --insert 0 \'<br/>\'| bspoon --select div\n<div class="container" id="root">\n <br/>\n <a href="https://www.google.com">\n  Google\n </a>\n</div>\n```\n\n-- `--insert_before`(`--ib`), insert a node(HTML) before the selected node.\n```\n$ bspoon test.html --select a --insert_before \'<br/>\'|bspoon --select div\n<div class="container" id="root">\n <br/>\n <a href="https://www.google.com">\n  Google\n </a>\n</div>\n```\n \n-- `--insert_after`(`--ia`), insert a node(HTML) next to the position of the selected node.\n```\n$ bspoon test.html --select a --ia \'<br/>\'|bspoon --select div\n<div class="container" id="root">\n <a href="https://www.google.com">\n  Google\n </a>\n <br/>\n</div>\n```\n\n- `--clear`, clear the inner content of the seleted node.\n```\n$ bspoon test.html --select div --clear| bspoon --select div\n<div class="container" id="root">\n</div>\n```\n\n- `--decompose`, remove the node along with its inner content of the seleted node.\n```\n$ bspoon test.html --select div --decompose|bspoon --select body\n<body>\n</body>\n```\n\n- `--replace_with`, replace the seleted node with HTML.\n```\n$ bspoon test.html --select a --replace_with \'<br/>\'| bspoon --select div\n<div class="container" id="root">\n <br/>\n</div>\n```\n\n- `--comment`, Comment the selected node.\n```\n$ bspoon test.html --select a --comment|bspoon --select div\n<div class="container" id="root">\n <!-- <a href="https://www.google.com">Google</a> -->\n</div>\n```\n\n- `--wrap`, wrap the seleted node with tag provided(HTML).\n```\n$ bspoon test.html --select a --wrap \'<p></p>\'\n| bspoon --select p\n<p>\n <a href="https://www.google.com">\n  Google\n </a>\n</p>\n```\n\n- `--unwrap`, unwrap the selected node.\n```\n$ bspoon test.html --select a --unwrap|bspoon --select div\n<div class="container" id="root">\n Google\n</div>\n```\n\n',
    'author': 'Gongziting Tech Ltd.',
    'author_email': None,
    'url': 'https://github.com/gzttech/beautifulspoon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
