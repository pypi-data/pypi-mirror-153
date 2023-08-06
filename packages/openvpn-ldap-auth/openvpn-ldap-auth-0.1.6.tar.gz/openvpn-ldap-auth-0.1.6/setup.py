# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openvpn_ldap_auth']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0', 'PyYAML>=5.4.1,<6.0.0', 'python-ldap>=3.3.1,<4.0.0']

entry_points = \
{'console_scripts': ['openvpn-ldap-auth = openvpn_ldap_auth.main:main']}

setup_kwargs = {
    'name': 'openvpn-ldap-auth',
    'version': '0.1.6',
    'description': 'An auth verify script for OpenVPN to authenticate via LDAP.',
    'long_description': '# Python OpenVPN LDAP Auth\n\n[![PyPI license](https://img.shields.io/pypi/l/openvpn-ldap-auth.svg)](https://pypi.python.org/pypi/openvpn-ldap-auth/)\n[![PyPI status](https://img.shields.io/pypi/status/openvpn-ldap-auth.svg)](https://pypi.python.org/pypi/openvpn-ldap-auth/)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/openvpn-ldap-auth.svg)](https://pypi.python.org/pypi/openvpn-ldap-auth/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/openvpn-ldap-auth.svg)](https://pypi.python.org/pypi/openvpn-ldap-auth/)\n![main build status](https://github.com/phihos/Python-OpenVPN-LDAP-Auth/actions/workflows/test.yml/badge.svg?branch=main)\n\nAn auth verify script for [OpenVPN](https://community.openvpn.net) to authenticate via LDAP. Each VPN login is\nforwarded to this script and the script in turn attempts a simple bind against the specified LDAP server. When the bind\nis successful the script returns exit code 0 telling OpenVPN that the credentials are valid.\n\nAlthough there already is the [openvpn-auth-ldap](https://github.com/threerings/openvpn-auth-ldap) plugin I felt the\nneed to write this auth script. First the source code is more accessible due to it being written in Python. Second it\noffers more possibilities regarding\nOpenVPN\'s [`static-challenge`](https://openvpn.net/community-resources/reference-manual-for-openvpn-2-4/) parameter (see\nbelow).\n\nThe downsides of using a script instead of a C-plugin\nare [less performance and slightly reduced security](https://openvpn.net/community-resources/using-alternative-authentication-methods/).\nIf you are fine with that go ahead.\n\n## Quickstart\n\nInstall the package via pip:\n\n```shell\npip install openvpn-ldap-auth\n```\n\nThen create `/etc/openvpn/ldap.yaml`:\n\n```yaml\nldap:\n  url: \'ldaps://first.ldap.tld:636/ ldaps://second.ldap.tld:636/\'\n  bind_dn: \'uid=readonly,dc=example,dc=org\'\n  password: \'somesecurepassword\'\n  timeout: 5 # optional\nauthorization:\n  base_dn: \'ou=people,dc=example,dc=org\'\n  search_filter: \'(uid={})\' # optional, {} will be replaced with the username\n  static_challenge: \'ignore\' # optional, other values are prepend, append \n```\n\nFind out where `openvpn-ldap-auth` lives:\n\n```shell\nwhich openvpn-ldap-auth\n```\n\nAdd the following line to your OpenVPN server configuration:\n\n```\nscript-security 2\nauth-user-pass-verify /path/to/openvpn-ldap-auth via-file\n```\n\nNow you can start your OpenVPN server and try to connect with a client.\n\n## Installation\n\n### Single Executable\n\nFor those who wish to [sacrifice a little more performance](https://pyinstaller.readthedocs.io/en/stable/operating-mode.html#how-the-one-file-program-works) for not having to install or compile a Python interpreter or you just want to quickly try the script out this option might be interesting.\nEach [release](https://github.com/phihos/python-openvpn-ldap-auth/releases) also has executables attached to it: *openvpn-ldap-auth-&lt;distro&gt;-&lt;distro-version&gt;-&lt;arch&gt;*. They are created via [PyInstaller](https://www.pyinstaller.org/) on the respective Linux distro, version and architecture. They might also work on other distros provided they use the same or a later libc version that the distro uses.\n\n**Important: /tmp must not be read only.**\n\n### From Source\n\nDownload or clone this repository, cd into it and run\n\n```shell\npip install poetry\npoetry install --no-dev\npoetry build\npip install --upgrade --find-links=dist openvpn-ldap-auth\n```\n\nExchange `pip` with `pip3` if applicable.\n\n## Configuration\n\n### Static Challenge\n\nIf you want users to provide a normal password combined with a one-time-password OpenVPN\'s\n[`static-challenge`](https://openvpn.net/community-resources/reference-manual-for-openvpn-2-4/) parameter is what you\nare looking for.\n\nIn the client configuration you need to add a line like\n\n```\nstatic-challenge "Enter OTP" 1 # use 0 if the OTP should not be echoed\n```\n\nWhen connecting you will now be prompted for your password and your OTP. By setting `authorization.static_challenge` you\ncan now influence how the OTP is used:\n\n- *ignore (default)*: Just use the password for binding.\n- *prepend*: Prepend the OTP to your password and use that for binding.\n- *append*: Append the OTP to your password and use that for binding.\n\nThe last two options are useful if your LDAP server offers internal 2FA validation \nlike [oath-ldap](https://oath-ldap.stroeder.com/).\n\n### Using `via-env`\n\nIn the server configuration the following alternative setting is also supported but discouraged:\n\n```\nauth-user-pass-verify /path/to/openvpn-ldap-auth via-env\n```\n\nOpenVPN\'s manpage about that topic:\n\n*If method is set to "via-env", OpenVPN will call script with the environmental variables username and password set to \nthe username/password strings provided by the client. Be aware that this method is insecure on some platforms which \nmake the environment of a process publicly visible to other unprivileged processes.*\n\nIf you still want to use `via-env` make sure to set `script-security` to `3`.\n\n## Running Tests\n\nFirst make sure to install [Docker](https://docs.docker.com/engine/install/)\nwith [docker-compose](https://docs.docker.com/compose/install/)\nand [tox](https://tox.readthedocs.io/en/latest/install.html). Then run\n\n```shell\ntox\n```\n\nTo run a specific Python-OpenVPN combination run something like\n\n```shell\ntox -e python38-openvpn25\n```\n\nTo see a full list of current environment see the `tool.tox` section in [pyproject.toml](pyproject.toml).\n',
    'author': 'Philipp Hossner',
    'author_email': 'philipph@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phihos/python-openvpn-ldap-auth/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
