# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rfc']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.8.0,<5.0.0', 'netlink-logging>=0.1.0,<0.2.0', 'pyrfc>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'netlink-sap-rfc',
    'version': '0.1.2',
    'description': 'Access SAP via RFC',
    'long_description': "# netlink-sap-rfc\n\nTools for SAP RFC\n\n# Connect\n\nThe default .XML files describing the landscape for SAPGUI are used for access via System ID.\n\n### login_sid\n\nReturns a Connection object.\n\n| Parameter | Description                 | Default        |\n|-----------|-----------------------------|----------------|\n| sysid     | System ID (a.k.a. <SID>)    |                |\n| client    | SAP Client (Mandant)        |                |\n| passwd    | Password                    |                |\n| user      | SAP user ID (BNAME)         | Logged on user |\n| language  | Language                    | EN             |\n| raw       | Don't convert date / time   | False          |\n\n\n### sso\n\nReturns a Connection object.\n\n| Parameter | Description                 | Default        |\n|-----------|-----------------------------|----------------|\n| sysid     | System ID (a.k.a. <SID>)    |                |\n| client    | SAP Client (Mandant)        |                |\n| user      | SAP user ID (BNAME)         | Logged on user |\n| language  | Language                    | EN             |\n| raw       | Don't convert date / time   | False          |\n\n\n # Connection Object\n\nUse one of the functions above to instantiate.\n\n## Methods\n\nAny Remote enabled Function Module can be called as a method (case-insensitive).\n\n### close()\n\nClose the connection. Should always be called before the program is finished, otherwise an error will be logged on the SAP system.\n\n### select(table, *args, **kwargs)\n\nGet contents of a table using `RFC_READ_TABLE`. Returns a list of Records.\n\nColumns within a Record can be access by index (int), name (case-insensitive), or attribute (case-insensitive).\n\n**table** (required) table name (case-insensitive)\n\n***args** (optional) when specified, only the columns listed will be returned\n\n****kwars** (optional) select rows (only equality is supported)\n\n#### Example\n\nrecords = rfc_connection.select('t000', 'mtext', 'ort01', mandt='000')\n\nwould return a list with one item:\n\n```python\n>>> records = c.select('t000', 'mtext', 'ort01', mandt='000')\n>>> len(records)\n1\n>>> records[0][0]\n'SAP SE'\n>>> records[0][1]\n'Walldorf'\n>>> records[0]['mtext']\n'SAP SE'\n>>> records[0]['ort01']\n'Walldorf'\n>>> records[0].mtext\n'SAP SE'\n>>> records[0].ort01\n'Walldorf'\n```\n\n\n\n",
    'author': 'Bernhard Radermacher',
    'author_email': 'bernhard.radermacher@netlink-consulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/netlink-consulting/netlink-sap-rfc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
