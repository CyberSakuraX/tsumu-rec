# セットアップ状況

## 完了済み

### Notion側(2026-07-27)
Claudeが Notion MCP 経由で以下を作成済み。手動作業は不要。

| 項目 | 値 |
|---|---|
| 親ページ | 🏃 マラソン管理 — https://app.notion.com/p/3aae273ad43b813691f6ef321c0423f3 |
| DB | 食事・コンディション ログ — https://app.notion.com/p/0e691aca69b34d49866d5c3494222d5c |
| **database_id** | `0e691aca69b34d49866d5c3494222d5c` |

プロパティは `docs/notion-schema.md` の設計どおり17項目すべて作成済み(select系の選択肢・色も設定済み)。
`notion/setup_db.py` は同じDBを別ワークスペースに再作成したい場合のためだけに残してある。通常は実行不要。

## 残作業(山崎さん側でのiPhone設定)

### 1. Notion Integration Token の取得
iPhoneショートカットはNotion **API** を直接叩くため、Claudeが使っているMCP接続とは別に
Internal Integration の Token が必要。

1. https://www.notion.so/my-integrations → 「New integration」
2. 名前は任意(例: `tsumu-rec-shortcuts`)、ワークスペースは上記DBのあるものを選択
3. Capabilities は **Read content / Update content / Insert content** にチェック
4. 作成後の `Internal Integration Secret`(`ntn_` または `secret_` で始まる文字列)を控える
5. Notionで「🏃 マラソン管理」ページを開き、右上「…」→「コネクト」→ 作成したIntegrationを追加
   (親ページに追加すれば配下のDBにも権限が継承される)

### 2. iCloud Drive に設定ファイルを置く
「ファイル」App → iCloud Drive → `Shortcuts` フォルダに以下2つを作成する。

`notion_config.json`
```json
{
  "token": "<上で取得したIntegration Secret>",
  "database_id": "0e691aca69b34d49866d5c3494222d5c"
}
```

`peaking_flag.txt`(中身は1行だけ)
```
false
```

### 3. ショートカットを4つ作成
`docs/iphone-shortcuts.md` の設計に従って「ご飯記録」「朝コンディション」「夜コンディション」
「ピーキング切替」を作成する。リクエストボディの具体形は `docs/notion-api-payloads.md` を参照。

### 4. 通知(オートメーション)を設定
`docs/notifications.md` の手順で朝7:00・夜21:30の時刻オートメーションを設定する。

### 5. 動作確認
「ご飯記録」を1回実行し、Notionの「食事・コンディション ログ」に当日の行ができることを確認する。
2回目以降(別の食事種別や夜ナッジ)で**行が増えず、同じ行が更新される**ことも併せて確認する。
