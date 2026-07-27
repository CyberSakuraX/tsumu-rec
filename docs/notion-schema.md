# Notion DB スキーマ設計

## データモデル
「1日1行」のログとする。同じ日に朝食ログ→夜ナッジ、のように複数回書き込みが発生するため、
各ショートカットは書き込み前に「今日の日付の行が既に存在するか」をクエリし、
- 存在しなければ新規ページ作成(POST `/v1/pages`)
- 存在すれば該当プロパティのみ更新(PATCH `/v1/pages/{page_id}`)

という upsert 方式で書き込む(該当行以外のプロパティは変更されない)。

DB名: `食事・コンディション ログ`

## プロパティ一覧

| プロパティ名 | 型 | 内容 | 入力元 |
|---|---|---|---|
| 名前(Title) | title | 日付文字列(例: `2026-07-23`)を格納。Notionの必須タイトル項目 | 全ショートカット共通 |
| 日付 | date | 当日の日付(検索・分析用の実体) | 全ショートカット共通 |
| 朝食 | rich_text | 朝食の発話内容そのまま | 食事ログ |
| 昼食 | rich_text | 昼食の発話内容そのまま | 食事ログ |
| 夕食 | rich_text | 夕食の発話内容そのまま | 食事ログ |
| 間食 | rich_text | 間食の発話内容そのまま | 食事ログ |
| 目覚め | number | 1〜4(1=悪い〜4=絶好調) | 朝ナッジ |
| 睡眠時間 | select | `5h未満` / `5-6h` / `6-7h` / `7-8h` / `8h以上` | 朝ナッジ |
| 体感 | select | `軽` / `並` / `重` | 夜ナッジ |
| 気分指数 | number | 1〜5 | 夜ナッジ |
| 不快指数 | number | 1〜5 | 夜ナッジ |
| 開放 | select | `自慰` / `性行為` / `なし` | 夜ナッジ |
| 好調・不調メモ | rich_text | 自由記述(任意、空欄可) | 夜ナッジ |
| ピーキングフラグ | checkbox | true/false。iCloud上のフラグファイルの値を反映 | 朝ナッジ・夜ナッジ・食事ログ全て |
| 炭水化物比率の体感 | select | `少なめ` / `適量` / `多め`。ピーキングフラグ=trueの時のみ入力 | 夜ナッジ(ピーキング期のみ) |
| 塩分電解質メモ | rich_text | 自由記述。ピーキングフラグ=trueの時のみ入力 | 夜ナッジ(ピーキング期のみ) |
| 胃腸の負担感 | select | `なし` / `軽度` / `中度` / `重度`。ピーキングフラグ=trueの時のみ入力 | 夜ナッジ(ピーキング期のみ) |

## 作成状況
このスキーマのDBは Notion 上に**作成済み**。

- database_id: `0e691aca69b34d49866d5c3494222d5c`
- URL: https://app.notion.com/p/0e691aca69b34d49866d5c3494222d5c
- 親ページ: 🏃 マラソン管理

別ワークスペースに同じDBを再作成したい場合のみ `notion/setup_db.py` を使う(通常は実行不要)。

## Notion API 書き込み例

新規作成(該当日がまだ無い場合):
```json
POST https://api.notion.com/v1/pages
{
  "parent": { "database_id": "<DATABASE_ID>" },
  "properties": {
    "名前": { "title": [{ "text": { "content": "2026-07-23" } }] },
    "日付": { "date": { "start": "2026-07-23" } },
    "昼食": { "rich_text": [{ "text": { "content": "うまかっちゃん" } }] }
  }
}
```

既存行の更新(該当日が既にある場合):
```json
PATCH https://api.notion.com/v1/pages/<PAGE_ID>
{
  "properties": {
    "体感": { "select": { "name": "並" } },
    "気分指数": { "number": 4 }
  }
}
```

該当日を検索するクエリ:
```json
POST https://api.notion.com/v1/databases/<DATABASE_ID>/query
{
  "filter": {
    "property": "日付",
    "date": { "equals": "2026-07-23" }
  }
}
```

いずれもヘッダーに以下を付与する。
```
Authorization: Bearer <NOTION_TOKEN>
Notion-Version: 2022-06-28
Content-Type: application/json
```
