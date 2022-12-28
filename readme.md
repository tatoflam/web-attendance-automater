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

Come

```
./run.sh come
```

Leave

```
./run.sh leave
```

## Schedule

### Cron

For scheduling, add `crontab.txt` configuration by `crontab crontab.txt` (CAUTION: this will overwrite existing crontab content. If you do not want to overwrite cron, prepare entire cron configuration file at somewhere like `~/etc/crontab`), add necessary line to the file, then run `crontab ~/etc/crontab`. 

### Mac configuration

System Preference > Battery > Schedule > Start up or wake

Note that this is not perfect as the Mac(Monterey) allows only one waking point per a day time unit.  