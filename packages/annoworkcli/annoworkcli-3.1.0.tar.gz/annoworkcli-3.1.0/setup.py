# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['annoworkcli',
 'annoworkcli.account',
 'annoworkcli.actual_working_time',
 'annoworkcli.annofab',
 'annoworkcli.common',
 'annoworkcli.expected_working_time',
 'annoworkcli.job',
 'annoworkcli.my',
 'annoworkcli.schedule',
 'annoworkcli.workspace',
 'annoworkcli.workspace_member',
 'annoworkcli.workspace_tag']

package_data = \
{'': ['*'], 'annoworkcli': ['data/*']}

install_requires = \
['annofabapi>=0.52.4',
 'annofabcli>=1.64.0',
 'annoworkapi>=3.0.1',
 'isodate',
 'more-itertools',
 'pandas',
 'pyyaml']

entry_points = \
{'console_scripts': ['annoworkcli = annoworkcli.__main__:main']}

setup_kwargs = {
    'name': 'annoworkcli',
    'version': '3.1.0',
    'description': '',
    'long_description': '\n# annowork-cli\nAnnoWorkのCLIです。\n\n\n[![Build Status](https://app.travis-ci.com/kurusugawa-computer/annowork-cli.svg?branch=main)](https://app.travis-ci.com/kurusugawa-computer/annowork-cli)\n[![CodeQL](https://github.com/kurusugawa-computer/annowork-cli/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kurusugawa-computer/annowork-cli/actions/workflows/codeql-analysis.yml)\n[![PyPI version](https://badge.fury.io/py/annoworkcli.svg)](https://badge.fury.io/py/annoworkcli)\n[![Python Versions](https://img.shields.io/pypi/pyversions/annoworkcli.svg)](https://pypi.org/project/annoworkcli/)\n[![Documentation Status](https://readthedocs.org/projects/annowork-cli/badge/?version=latest)](https://annowork-cli.readthedocs.io/ja/latest/?badge=latest)\n\n\n# Requirements\n* Python3.8+\n\n\n# Install\n```\n$ pip install annoworkcli\n```\n\n\n# Usage\n\n\n## 認証情報の設定\n\n### `.netrc`\n\n`$HOME/.netrc`ファイルに以下を記載する。\n\n```\nmachine annowork.com\nlogin annowork_user_id\npassword annowork_password\n```\n\n\n### 環境変数\n* 環境変数`ANNOWORK_USER_ID` , `ANNOWORK_PASSWORD`\n\n### `annoworkcli annofab`コマンドを利用する場合\n`annoworkcli annofab`コマンドはannofabのwebapiにアクセスするため、annofabのwebapiの認証情報を指定する必要があります。\n* 環境変数`ANNOFAB_USER_ID` , `ANNOFAB_PASSWORD`\n* `$HOME/.netrc`ファイル\n\n```\nmachine annofab.com\nlogin annofab_user_id\npassword annofab_password\n```\n\n\n\n\n## コマンドの使い方\n\n\n```\n# CSV出力\n$ annoworkcli actual_working_time list_daily --workspace_id foo \\\n --start_date 2022-05-01 --end_date 2022-05-10 --output out.csv\n\n$ cat out.csv\ndate,job_id,job_name,workspace_member_id,user_id,username,actual_working_hours,notes\n2022-05-02,5c39a2e8-90dd-4f20-b0a6-39d7f5129e3d,MOON,52ff73fb-c1d6-4ad6-a185-64386ee7169f,alice,Alice,11.233333333333334,\n2022-05-02,5c39a2e8-90dd-4f20-b0a6-39d7f5129e3d,MARS,c66acd58-c893-4908-bdcc-1414978bf06b,bob,Bob,8.0,\n\n```\n\n\n\n\n\n\n\n\n# VSCode Devcontainerを使って開発する方法\n1. 以下の環境変数を定義します。\n    * `ANNOFAB_USER_ID`\n    * `ANNOFAB_PASSWORD`\n    * `ANNOWORK_USER_ID`\n    * `ANNOWORK_PASSWORD`\n\n2. VSCodeのdevcontainerを起動します。\n\n\n\n',
    'author': 'yuji38kwmt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kurusugawa-computer/annowork-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
