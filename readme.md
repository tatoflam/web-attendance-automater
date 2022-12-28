# Web attendance automater

勤怠管理Webシステムを自動入力する簡易スクリプトです。

- 土日祝日を除く平日のみ実行します
- vacation.yamlに休日のリストを以下の形式で記載すると、該当日は休暇中と見做して実行しません

  ```yaml
  vacation: 
  - 2022-12-29
  - 2022-12-30
  - 2022-12-30
  ```

- ログイン情報、WebページのDOM情報等(const.py)はGitリポジトリに含めていません。

## 動作環境

- Mac OS Monterey (12.3) (Apple M1 Pro)
- Raspberry Pi zero W

## Install

```
python -m venv env1
source env1/bin/activate
pip install -r requirements.txt
```

## Run

Come

```
./run.sh come
```

Break start

```
./run.sh break_start
```

Break end

```
./run.sh break_end
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