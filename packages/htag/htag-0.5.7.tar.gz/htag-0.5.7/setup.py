# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htag', 'htag.runners']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'htag',
    'version': '0.5.7',
    'description': 'GUI toolkit for building GUI toolkits (and create beautiful applications for mobile, web, and desktop from a single python3 codebase)',
    'long_description': '# HTag : "[H]TML Tag"\n\nA new python library to create UI (or UI toolkit), which can be rendered in anything which can render **html/js/css**.\nThoses can be a browser, a pywebview, or anything based on cef, depending on an "htag runner" (`*`)\xa0!\n\n * For a **desktop app** : You can use the "PyWebView runner", which will run the UI in a pywebview container (or "ChromeApp runner", in a local chrome app mode).\xa0\n * For a **web app** : You can use the "WebHTTP runner", which will run the UI in a web server, and serve the UI on client side, in a browser.\xa0\n * For a **android app** : You can use the "Guy runner", which will run the UI in a kiwi webview, and can be embedded in an apk (`**`)\n * For a **pyscript app** : you can use the "PyScript runner", which will run completly in client side\n\nBut yes … the promise is here : it\'s a GUI toolkit for building "beautiful" applications for mobile, web, and desktop from a single codebase.\n\n(`*`) **HTag** provides somes [`runners`](htag/runners) ootb. But they are just here for the show. IRL: you should build your own, for your needs.\n\n(`**`) **HTag** is not tied to [guy](https://github.com/manatlan/guy), but can use it as is. So, a **HTag app** could be packaged in an apk/android, using [a guy method](https://manatlan.github.io/guy/howto_build_apk_android/). But in the future, **HTag** will come with its own "android runner" (without *guy* !)\n\n\n[DEMO/TUTORIAL](https://htag.glitch.me/)\n\n[Changelog](changelog.md)\n\n[Available on pypi.org](https://pypi.org/project/htag/)\n\n\n\n## To have a look\n\nSee the [demo source code](https://github.com/manatlan/htag/blob/main/examples/demo.py)\n\nTo try it :\n\n    $ pip3 install htag pywebview\n    $ wget https://raw.githubusercontent.com/manatlan/htag/main/examples/demo.py\n    $ python3 demo.py\n\nThere will be docs in the future ;-)\n\n## ROADMAP to 1.0.0\n\n * rock solid (need more tests)\n * ~~top level api could change (Tag() -> create a Tag, Tag.mytag() -> create a TagBase ... can be a little bit ambiguous)~~\n * add a runner with WS with stdlib ? (not starlette!)\n * ~~I don\'t really like the current way to generate js in interaction : need to found something more solid.~~\n * ~~the current way to initiate the statics is odd (only on real (embedded) Tag\'s) : should find a better way (static like gtag ?!)~~\n\n\n## History\n\nAt the beginning, there was [guy](https://github.com/manatlan/guy), which was/is the same concept as [python-eel](https://github.com/ChrisKnott/Eel), but more advanced.\nOne day, I\'ve discovered [remi](https://github.com/rawpython/remi), and asked my self, if it could be done in a *guy way*. The POC was very good, so I released\na version of it, named [gtag](https://github.com/manatlan/gtag). It worked well despite some drawbacks, but was too difficult to maintain. So I decided to rewrite all\nfrom scratch, while staying away from *guy* (to separate, *rendering* and *runners*)... and [htag](https://github.com/manatlan/htag) was born. The codebase is very short, concepts are better implemented, and it\'s very easy to maintain.\n\n\n',
    'author': 'manatlan',
    'author_email': 'manatlan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/manatlan/htag',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
