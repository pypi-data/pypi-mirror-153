# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easypki']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=37.0.1,<38.0.0', 'typing-extensions==4.1']

setup_kwargs = {
    'name': 'easypki',
    'version': '0.0.1',
    'description': 'Build a self-signed pki',
    'long_description': "# easypki\n\nBuild a Private Certificate Authority (PKI).\n\n\n### Feature\n\n- Issuing a CA certificate\n- Issuing a server certificate\n- Issuing a client certificate\n- Issuing a pkcs12 file containing the client certificate and CA certificate\n- Issuance of CRL certificate\n\n### Setup\n\n```shell\npip install easypki\n```\n\n### How to use\n\n#### Certificate creation\n\n```python\n# module import\nfrom easypki import pki\n\n# make instance\nprivate_pki = pki.BuildPKI()\n\n# make ca cert\nca_cert, ca_key, ca_csr = private_pki.make_ca(\n    country_name='JP',\n    organization_name='Example Company',\n    common_name='Private RootCA',\n    cert_expire_days=36500\n)\n\n# make server cert\nserver_cert, server_key, server_csr = private_pki.make_server(\n    ca_cert=ca_cert,\n    ca_key=ca_key,\n    common_name='example.com',\n    san=['192.168.1.1', '*.example.com', 'example.net']\n    cert_expire_days=365\n)\n\n# make client cert\nclient_cert, client_key, client_csr = private_pki.make_client(\n    ca_cert=ca_cert,\n    ca_key=ca_key,\n    common_name='user name',\n    email_address='admin@example.com',\n    cert_expire_days=365\n)\n\n# make pkcs12 data\npkcs12 = private_pki.make_pkcs12(\n    ca_cert=ca_cert,\n    client_cert=client_cert,\n    client_key=client_key\n)\n\n# make crl\ncrl_cert, crl_key = private_pki.make_crl(\n    expire_cert=server_cert,\n    expire_date=7,\n    crl_cert=crl_cert,\n    ca_cert=ca_cert,\n)\n\n\n# save file\n# Please specify the stored variable and file name\nwith open('ca_cert.pem','wb') as f:\n    f.write(ca_cert)\n```\n\nVariables output from the instance method are saved in pem data format, so they can be saved as they are.\n\nThe certificate is also stored in the instance variable.\nTherefore, you can also create it as follows.\n\n```python\n    prvpki = pki.BuildPKI()\n    ca_cert, ca_key, ca_csr = prvpki.make_ca(\n        common_name='Private RootCA'\n    )\n    server_cert, server_key, server_csr = prvpki.make_server(\n        common_name='example.com'\n    )\n    client_cert, client_key, client_csr = prvpki.make_client()\n\n    pkcs12 = prvpki.make_pkcs12()\n```\n\nIf you already have a CA certificate and CA key created\nIt can also be created as follows.\n\n```python\n    prvca = pki.BuildPKI()\n    ca_cert, ca_key, ca_csr = prvca.make_ca(\n        common_name='Private RootCA'\n    )\n    del prvca\n    \n    prvpki = pki.BuildPKI(\n        ca_cert=ca_cert,\n        ca_key=ca_key\n    )\n    server_cert, server_key, server_csr = prvpki.make_server(\n        common_name='example.com'\n    )\n    client_cert, client_key, client_csr = prvpki.make_client()\n\n    pkcs12 = prvpki.make_pkcs12()\n```\n\n\n\n",
    'author': 'ymrsk',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ymrsk/easypki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
