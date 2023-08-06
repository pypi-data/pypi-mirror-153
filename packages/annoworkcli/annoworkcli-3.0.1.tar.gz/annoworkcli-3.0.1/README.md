
# annowork-cli
AnnoWorkのCLIです。


[![Build Status](https://app.travis-ci.com/kurusugawa-computer/annowork-cli.svg?branch=main)](https://app.travis-ci.com/kurusugawa-computer/annowork-cli)
[![CodeQL](https://github.com/kurusugawa-computer/annowork-cli/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kurusugawa-computer/annowork-cli/actions/workflows/codeql-analysis.yml)
[![PyPI version](https://badge.fury.io/py/annoworkcli.svg)](https://badge.fury.io/py/annoworkcli)
[![Python Versions](https://img.shields.io/pypi/pyversions/annoworkcli.svg)](https://pypi.org/project/annoworkcli/)
[![Documentation Status](https://readthedocs.org/projects/annowork-cli/badge/?version=latest)](https://annowork-cli.readthedocs.io/ja/latest/?badge=latest)


# Requirements
* Python3.8+


# Install
```
$ pip install annoworkcli
```


# Usage


## 認証情報の設定

### `.netrc`

`$HOME/.netrc`ファイルに以下を記載する。

```
machine annowork.com
login annowork_user_id
password annowork_password
```


### 環境変数
* 環境変数`ANNOWORK_USER_ID` , `ANNOWORK_PASSWORD`

### `annoworkcli annofab`コマンドを利用する場合
`annoworkcli annofab`コマンドはannofabのwebapiにアクセスするため、annofabのwebapiの認証情報を指定する必要があります。
* 環境変数`ANNOFAB_USER_ID` , `ANNOFAB_PASSWORD`
* `$HOME/.netrc`ファイル

```
machine annofab.com
login annofab_user_id
password annofab_password
```




## コマンドの使い方

```
vagrant@example:~$ annoworkcli -h
usage: annoworkcli [-h] [--version] {account,actual_working_time,annofab,expected_working_time,job,migration,my,workspace_member,workspace_tag,schedule} ...

Command Line Interface for AnnoFab

positional arguments:
  {account,actual_working_time,annofab,expected_working_time,job,migration,my,workspace_member,workspace_tag,schedule}
    account             ユーザアカウントに関するサブコマンド

    actual_working_time
                        実績作業時間関係のサブコマンド

    annofab             AnnoFabにアクセスするサブコマンド

    expected_working_time
                        予定稼働時間関係のサブコマンド

    job                 ジョブ関係のサブコマンド

    my                  自分自身に関するサブコマンド

    workspace_member
                        ワークスペースメンバ関係のサブコマンド

    workspace_tag    ワークスペースタグ関係のサブコマンド

    schedule            作業計画関係のサブコマンド

optional arguments:
  -h, --help            show this help message and exit

  --version             show program's version number and exit
```


```
$ annoworkcli workspace_member list -h
usage: annoworkcli workspace_member list [-h] [--endpoint_url ENDPOINT_URL | --is_development | --is_staging] -org workspace_ID
                                            [-org_tag workspace_TAG_ID [workspace_TAG_ID ...]] [-o OUTPUT] [-f {csv,json}]

ワークスペースメンバの一覧を出力します。無効化されたメンバも出力します。

optional arguments:
  -h, --help            show this help message and exit

  --endpoint_url ENDPOINT_URL
                        AnnoWork WebAPIのエンドポイントを指定します。指定しない場合は'https://annowork.com'です。 (default: None)

  -org workspace_ID, --workspace_id workspace_ID
                        対象のワークスペースID (default: None)

  -org_tag workspace_TAG_ID [workspace_TAG_ID ...], --workspace_tag_id workspace_TAG_ID [workspace_TAG_ID ...]
                        指定したワークスペースタグが付与されたワークスペースメンバを出力します。 (default: None)

  -o OUTPUT, --output OUTPUT
                        出力先 (default: None)

  -f {csv,json}, --format {csv,json}
                        出力先 (default: csv)
```

```
# CSV出力
$ annoworkcli workspace_member list -org org -o out.csv
$ cat out.csv
workspace_member_id,workspace_id,account_id,user_id,username,role,status,created_datetime,updated_datetime,workspace_tag_ids,workspace_tag_names,inactivated_datetime
12345678-abcd-1234-abcd-1234abcd5678,org,12345678-abcd-1234-abcd-1234abcd5678,alice,Alice,manager,active,2021-11-04T04:27:57.702Z,2021-11-04T04:27:57.702Z,['company_kurusugawa'],['company:来栖川電算'],
...


# CSV出力
$ annoworkcli workspace_member list -org org -o out.json -f json
$ cat out.json
[
  {
    "workspace_member_id": "12345678-abcd-1234-abcd-1234abcd5678",
    "workspace_id": "org",
    "account_id": "12345678-abcd-1234-abcd-1234abcd5678",
    "user_id": "alice",
    "username": "Alice",
    "role": "worker",
    "status": "active",
    "created_datetime": "2021-10-28T06:48:40.077Z",
    "updated_datetime": "2021-11-09T01:07:30.766Z",
    "inactivated_datetime": NaN,
    "workspace_tag_ids": [
      "company_kurusugawa",
      "type_monitored"
    ],
    "workspace_tag_names": [
      "company:来栖川電算",
      "type:monitored"
    ]
  },
  ...
```




### 開発環境に対して操作する場合

```
$ annoworkcli member list --output foo.csv --is_development 
```



# VSCode Devcontainerを使って開発する方法
1. 以下の環境変数を定義します。
    * `ANNOFAB_USER_ID`
    * `ANNOFAB_PASSWORD`
    * `ANNOWORK_USER_ID`
    * `ANNOWORK_PASSWORD`

2. VSCodeのdevcontainerを起動します。



