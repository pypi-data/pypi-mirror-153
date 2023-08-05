# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitmproxy2swagger']

package_data = \
{'': ['*']}

install_requires = \
['json-stream>=1.3.0,<2.0.0',
 'mitmproxy>=8.0.0,<9.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0']

entry_points = \
{'console_scripts': ['mitmproxy2swagger = '
                     'mitmproxy2swagger.mitmproxy2swagger:main']}

setup_kwargs = {
    'name': 'mitmproxy2swagger',
    'version': '0.5.4',
    'description': '',
    'long_description': '# mitmproxy2swagger\n\n\n[![PyPI version](https://badge.fury.io/py/mitmproxy2swagger.svg)](https://badge.fury.io/py/mitmproxy2swagger)\n\n\nhttps://user-images.githubusercontent.com/5400940/168086818-c48f60ab-3f95-42eb-b435-c8b1a6326b81.mp4\n\n\n\nA tool for automatically converting [mitmproxy](https://mitmproxy.org/) captures to [OpenAPI 3.0](https://swagger.io/specification/) specifications. This means that you can automatically reverse-engineer REST APIs by just running the apps and capturing the traffic.\n\n---\n**🆕 NEW!**\n\nAdded support for processing HAR exported from the browser DevTools. See [Usage - HAR](#har) for more details.\n\n---\n\n## Installation\n\nFirst you will need python3 and pip3.\n\n```bash\n$ pip install mitmproxy2swagger \n# ... or ...\n$ pip3 install mitmproxy2swagger\n```\n\nThen clone the repo and run `mitmproxy2swagger` as per examples below.\n\n## Usage\n\n### Mitmproxy\n\nTo create a specification by inspecting HTTP traffic you will need to:\n\n1. Capture the traffic by using the mitmproxy tool. I personally recommend using mitmweb, which is a web interface built-in to mitmproxy.\n\n    ```bash\n    $ mitmweb\n    Web server listening at http://127.0.0.1:8081/\n    Proxy server listening at http://*:9999\n    ...\n    ```\n    **IMPORTANT**\n\n    To configure your client to use the proxy exposed by mitm proxy, please consult the [mitmproxy documentation](https://docs.mitmproxy.org/stable/) for more information.\n\n2. Save the traffic to a flow file.\n\n    In mitmweb you can do this by using the "File" menu and selecting "Save":\n    \n    ![](./docs/mitmweb_save.png)\n\n3. Run the first pass of mitmproxy2swagger:\n\n    ```bash\n    $ mitmproxy2swagger -i <path_to_mitmptoxy_flow> -o <path_to_output_schema> -p <api_prefix>\n    ```\n\n    Please note that you can use an existing schema, in which case the existing schema will be extended with the new data. You can also run it a few times with different flow captures, the captured data will be safely merged.\n\n    `<api_prefix>` is the base url of the API you wish to reverse-engineer. You will need to obtain it by observing the requests being made in mitmproxy.\n\n    For example if an app has made requests like these:\n\n    ```\n    https://api.example.com/v1/login\n    https://api.example.com/v1/users/2\n    https://api.example.com/v1/users/2/profile\n    ```\n\n    The likely prefix is `https://api.example.com/v1`.\n\n4. Running the first pass should have created a section in the schema file like this:\n\n    ```yaml\n    x-path-templates:\n    # Remove the ignore: prefix to generate an endpoint with its URL\n    # Lines that are closer to the top take precedence, the matching is greedy\n    - ignore:/addresses\n    - ignore:/basket\n    - ignore:/basket/add\n    - ignore:/basket/checkouts\n    - ignore:/basket/coupons/attach/{id}\n    - ignore:/basket/coupons/attach/104754\n    ```\n\n    You should edit the schema file with a text editor and remove the `ignore:` prefix from the paths you wish to be generated. You can also adjust the parameters appearing in the paths.\n\n5. Run the second pass of mitmproxy2swagger:\n\n    ```bash\n    $ mitmproxy2swagger -i <path_to_mitmptoxy_flow> -o <path_to_output_schema> -p <api_prefix> [--examples]\n    ```\n\n    Run the command a second time (with the same schema file). It will pick up the edited lines and generate endpoint descriptions. \n\n    Please note that mitmproxy2swagger will not overwrite existing endpoint descriptions, if you want to overwrite them, you can delete them before running the second pass.\n\n    Passing `--examples` will add example data to requests and responses. Take caution when using this option, as it may add sensitive data (tokens, passwords, personal information etc.) to the schema.\n\n### HAR\n\n1. Capture and export the traffic from the browser DevTools.\n\n    In the browser DevTools, go to the Network tab and click the "Export HAR" button.\n\n    ![A screenshot showing where the export har button is located](./docs/export_har_button.png)\n2. Continue the same way you would do with the mitmproxy dump. `mitmproxy2swagger` will automatically detect the HAR file and process it.\n\n## Example output\n\nSee the [examples](./example_outputs/). You will find a generated schema there and an html file with the generated documentation (via [redoc-cli](https://www.npmjs.com/package/redoc-cli)).\n\nSee the generated html file [here](https://raw.githack.com/alufers/mitmproxy2swagger/master/example_outputs/lisek-static.html).\n\n## License\nMIT\n\n',
    'author': 'alufers',
    'author_email': 'alufers@wp.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
