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
  notion-schema.md      NotionDBのプロパティ設計
  iphone-shortcuts.md   iPhoneショートカットの設計(食事ログ/朝夜ナッジ/ピーキング切替)
  notifications.md      通知(時刻オートメーション)の設定手順
  dev-environment.md    時間帯で変わる端末(iPhone/Windows/Mac)から作業を継続するための手順
notion/
  setup_db.py           NotionにDBを作成するセットアップスクリプト
  requirements.txt
  .env.example
.claude/skills/marathon-nutrition-analysis/
  SKILL.md              Claudeが分析依頼時に従う手順(Notion MCP + Strava MCP)
```

## セットアップ手順

1. **Notion Integration作成**: https://www.notion.so/my-integrations でIntegrationを作成しTokenを取得
2. **親ページ作成**: Notion上に空ページ(例:「マラソン管理」)を作り、作成したIntegrationを招待。ページIDを控える
3. **DB作成**:
   ```
   cd notion
   cp .env.example .env   # NOTION_TOKEN / NOTION_PARENT_PAGE_ID を編集
   export $(cat .env | xargs)
   python setup_db.py
   ```
   出力された `database_id` を控える
4. **iPhone側の設定ファイル**: iCloud Drive の `Shortcuts` フォルダに `notion_config.json`(token・database_id)と
   `peaking_flag.txt`(初期値 `false`)を作成
5. **ショートカット作成**: `docs/iphone-shortcuts.md` の設計に従い、
   「ご飯記録」「朝コンディション」「夜コンディション」「ピーキング切替」の4つを作成
6. **通知設定**: `docs/notifications.md` の手順で朝7:00・夜21:30の時刻オートメーションを設定
7. **分析**: 準備ができたら、Claudeに「食事とパフォーマンスの相関を分析して」のように話しかけると、
   `.claude/skills/marathon-nutrition-analysis/SKILL.md` の手順でNotion MCP + Strava MCPを使って分析する

## 決定済みの仕様(要件定義書 v1.0 セクション8への回答)
- DB配置: 新規に親ページを作成しその配下に配置
- 発話の扱い: パースなし。食事種別はメニュー選択、内容は音声入力でそのまま保存
- 通知時刻: 朝7:00 / 夜21:30
- ピーキングフラグ: 手動切り替え(iCloud上のフラグファイル + 専用切替ショートカット)

詳細は `docs/decisions.md` を参照。
