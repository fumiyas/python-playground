#!/usr/bin/env python3
## -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

import datetime


## 現在時刻、ローカル時間、タイムゾーン情報なし
dt_wo_tz = datetime.datetime.now()
print(f"{dt_wo_tz.isoformat()} {dt_wo_tz.tzinfo}")
## → 2024-10-08T15:09:03.042399 None

## ローカル時間、タイムゾーン情報なし → ローカル時間、タイムゾーン情報あり
dt_as_local = dt_wo_tz.astimezone()
print(f"{dt_as_local.isoformat()} {dt_as_local.tzinfo}")
## → 2024-10-08T15:09:03.042399+09:00 JST

## ローカル時間、タイムゾーン情報なし → UTC、タイムゾーン情報あり
dt_as_utc = dt_wo_tz.astimezone(datetime.timezone.utc)
print(f"{dt_as_utc.isoformat()} {dt_as_utc.tzinfo}")
## → 2024-10-08T06:00:03.042399+00:00 UTC

## ローカル時間、タイムゾーン情報なし → UTC、タイムゾーン情報あり (ゾーン変更)
dt_replace_tz = dt_wo_tz.replace(tzinfo=datetime.timezone.utc)
print(f"{dt_replace_tz.isoformat()} {dt_replace_tz.tzinfo}")
## → 2024-10-08T06:09:03.042399+00:00 UTC

## UTC、タイムゾーン情報あり → ローカル時間、タイムゾーン情報あり
dt_utc2local = dt_as_utc.astimezone()
print(f"{dt_utc2local.isoformat()} {dt_utc2local.tzinfo}")
## → 2024-10-08T15:09:03.042399+09:00 JST

## 現在時刻、UTC、タイムゾーン情報あり
dt_w_tz_utc = datetime.datetime.now(datetime.timezone.utc)
print(f"{dt_w_tz_utc.isoformat()} {dt_w_tz_utc.tzinfo}")
## → 2024-10-08T06:09:03.042430+00:00 UTC

## 現在時刻、ローカル時間、タイムゾーン情報あり
## ローカルタイムゾーンを持つほかの datetime オブジェクトを利用
## (tzinfo プロパティ) せずにローカルタイムゾーンオブジェクトを生成する方法は?
dt_w_tz_local = datetime.datetime.now(dt_utc2local.tzinfo)
print(f"{dt_w_tz_local.isoformat()} {dt_w_tz_local.tzinfo}")
## → 2024-10-08T15:09:03.042462+00:00 JST
