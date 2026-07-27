# tsumu-rec — 食事記録 & マラソンピーキング活用システム

日々の食事・コンディションをiPhoneからひとことで記録し、Notionに蓄積。
レース前2〜3週間のピーキング期には栄養関連の項目を追加で記録し、
依頼したタイミングでClaudeがStravaのトレーニングデータと突き合わせて分析する。

要件の詳細は `docs/requirements-v1.md`、未確定事項への回答は `docs/decisions.md` を参照。

## アーキテクチャ

```
[書き込み経路] ユーザー(iPhoneショートカット) → Notion API → 「食事・コンディション ログ」DB
[分析経路]     Claude ⇄ Notion MCP ⇄ 同DB
               Claude ⇄ Strava MCP
```

書き込み経路にClaudeは一切関与しない。分析は依頼されたときだけ、読み取り専用で行う。

## ディレクトリ構成

```
docs/
  requirements-v1.md   要件定義書(原本)
  decisions.md         未確定事項の決定内容
  setup-status.md       セットアップの完了状況と残作業(まずここを見る)
  notion-schema.md      NotionDBのプロパティ設計
  notion-api-payloads.md ショートカットから投げるリクエストボディのコピペ元
  iphone-shortcuts.md   iPhoneショートカットの設計(何を作るか)
  iphone-shortcuts-howto.md ショートカットの作成手順(どう作るか。タップ順)
  notifications.md      通知(時刻オートメーション)の設定手順
notion/
  setup_db.py           NotionにDBを作成するセットアップスクリプト
  requirements.txt
  .env.example
.claude/skills/marathon-nutrition-analysis/
  SKILL.md              Claudeが分析依頼時に従う手順(Notion MCP + Strava MCP)
```

## セットアップ手順

進捗と残作業の詳細は `docs/setup-status.md` を参照。

- [x] **親ページ・DB作成** — 作成済み。`database_id` = `0e691aca69b34d49866d5c3494222d5c`
      ([🏃 マラソン管理](https://app.notion.com/p/3aae273ad43b813691f6ef321c0423f3) 配下)
- [ ] **Notion Integration作成** — https://www.notion.so/my-integrations でTokenを取得し、
      「🏃 マラソン管理」ページにコネクトする(ショートカットがAPIを直接叩くために必要)
- [ ] **iPhone側の設定ファイル** — iCloud Drive の `Shortcuts` フォルダに
      `notion_config.json`(token・database_id)と `peaking_flag.txt`(初期値 `false`)を作成
- [ ] **ショートカット作成** — `docs/iphone-shortcuts-howto.md` のタップ手順に従い、
      ヘルパー「Notion書き込み」1つ + 本体4つを作成(30〜40分)
- [ ] **通知設定** — `docs/notifications.md` の手順で朝7:00・夜21:30の時刻オートメーションを設定
- [ ] **動作確認** — 同じ日に2回記録して、行が増えず更新されることを確認

準備ができたら、Claudeに「食事とパフォーマンスの相関を分析して」のように話しかけると、
`.claude/skills/marathon-nutrition-analysis/SKILL.md` の手順でNotion MCP + Strava MCPを使って分析する。

## 決定済みの仕様(要件定義書 v1.0 セクション8への回答)
- DB配置: 新規に親ページを作成しその配下に配置
- 発話の扱い: パースなし。食事種別はメニュー選択、内容は音声入力でそのまま保存
- 通知時刻: 朝7:00 / 夜21:30
- ピーキングフラグ: 手動切り替え(iCloud上のフラグファイル + 専用切替ショートカット)

詳細は `docs/decisions.md` を参照。
