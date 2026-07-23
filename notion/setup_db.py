"""
Notion に「食事・コンディション ログ」DBを作成するセットアップスクリプト。

事前準備:
  1. https://www.notion.so/my-integrations で Internal Integration を作成し、Token を取得する
  2. Notion 上に空の親ページ(例: 「マラソン管理」)を作成する
  3. その親ページの「コネクト」からこの Integration を招待する
  4. 親ページの URL 末尾32文字(ハイフンなし)を PARENT_PAGE_ID として控える

実行:
  export NOTION_TOKEN=secret_xxx
  export NOTION_PARENT_PAGE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  pip install -r requirements.txt
  python setup_db.py
"""

import json
import os
import sys
import urllib.request

NOTION_VERSION = "2022-06-28"
DB_TITLE = "食事・コンディション ログ"

PROPERTIES = {
    "日付": {"date": {}},
    "朝食": {"rich_text": {}},
    "昼食": {"rich_text": {}},
    "夕食": {"rich_text": {}},
    "間食": {"rich_text": {}},
    "目覚め": {"number": {"format": "number"}},
    "睡眠時間": {
        "select": {
            "options": [
                {"name": "5h未満"},
                {"name": "5-6h"},
                {"name": "6-7h"},
                {"name": "7-8h"},
                {"name": "8h以上"},
            ]
        }
    },
    "体感": {"select": {"options": [{"name": "軽"}, {"name": "並"}, {"name": "重"}]}},
    "気分指数": {"number": {"format": "number"}},
    "不快指数": {"number": {"format": "number"}},
    "開放": {
        "select": {
            "options": [{"name": "自慰"}, {"name": "性行為"}, {"name": "なし"}]
        }
    },
    "好調・不調メモ": {"rich_text": {}},
    "ピーキングフラグ": {"checkbox": {}},
    "炭水化物比率の体感": {
        "select": {"options": [{"name": "少なめ"}, {"name": "適量"}, {"name": "多め"}]}
    },
    "塩分電解質メモ": {"rich_text": {}},
    "胃腸の負担感": {
        "select": {
            "options": [
                {"name": "なし"},
                {"name": "軽度"},
                {"name": "中度"},
                {"name": "重度"},
            ]
        }
    },
    "名前": {"title": {}},
}


def create_database(token: str, parent_page_id: str) -> dict:
    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": DB_TITLE}}],
        "properties": PROPERTIES,
    }
    req = urllib.request.Request(
        "https://api.notion.com/v1/databases",
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))


def main() -> None:
    token = os.environ.get("NOTION_TOKEN")
    parent_page_id = os.environ.get("NOTION_PARENT_PAGE_ID")
    if not token or not parent_page_id:
        print(
            "環境変数 NOTION_TOKEN と NOTION_PARENT_PAGE_ID を設定してください。",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        result = create_database(token, parent_page_id)
    except urllib.error.HTTPError as e:
        print(f"Notion API エラー: {e.code} {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

    print("DB を作成しました。")
    print(f"database_id = {result['id']}")
    print("この database_id を docs/iphone-shortcuts.md の設定手順に従って")
    print("Shortcuts 用の設定ファイル(notion_config.json)に控えてください。")


if __name__ == "__main__":
    main()
