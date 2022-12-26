# Web attendance automater

勤怠管理Webシステムを自動入力する簡易スクリプトです。
ログイン情報、WebページのDOM情報等(const.py)はGitリポジトリに含めていません。

## Install

```
python -m venv env1
source env1/bin/activate
pip install -r requirements.txt
```

## Run (mac)

```
source env1/bin/activate
./run.sh
```

## Cron

Ref. crontab.txt