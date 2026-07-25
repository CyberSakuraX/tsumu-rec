# 開発環境 — iPhone / Windows / Mac の3端末で進める

このプロジェクトは「編集する場所」と「実際に動く場所」が分かれている。
先にその役割を押さえると、どの端末で何をやるかが迷わなくなる。

| 端末 | 主な役割 | できること / できないこと |
|---|---|---|
| iPhone | **実行環境**(唯一の書き込み経路) | ショートカット作成・実機テスト・日々の記録。コード編集は不向き |
| Mac | 編集環境(フル) | ドキュメント編集・`setup_db.py` 実行・git操作すべて |
| Windows | 編集環境(フル) | 同上。Pythonと文字コードだけ後述の注意あり |

Notion DB は3端末から同じものを見る。DBの実体はクラウド上に1つだけなので、
「端末ごとにDBを作る」必要はない。作るのは最初の1回だけ。

## 同期の原則

コードとドキュメントは **GitHub 経由でのみ同期する**。
iCloud や Dropbox でリポジトリごと共有するのはやめる(`.git` が壊れる原因になる)。

作業を始める前と終わったあとに、必ず以下をやる。端末をまたぐ以上これが唯一の防御線になる。

```
# 作業前
git pull origin <branch>

# 作業後
git add -A
git commit -m "..."
git push -u origin <branch>
```

別端末に移る前に push し忘れると、次の端末で古い状態から書き始めてコンフリクトする。
「端末を離れるときは push」を習慣にする。

## シークレットの扱い

Notion Integration Token は**リポジトリに絶対に入れない**。

- `notion/.env` は `.gitignore` 済み。各端末でローカルに作る(コミットされない)
- iPhone 側のトークンは iCloud Drive の `Shortcuts/notion_config.json` に置く(git管理外)
- 端末間でトークンを渡すときは、パスワードマネージャか、Notionの管理画面から再取得する

トークンは1つを3端末で使い回して問題ない。Integration単位の権限なので端末は区別されない。

## Mac での準備

追加インストールはほぼ不要(Pythonは標準搭載、なければ `brew install python`)。

```
git clone https://github.com/CyberSakuraX/tsumu-rec.git
cd tsumu-rec/notion
cp .env.example .env      # エディタで NOTION_TOKEN / NOTION_PARENT_PAGE_ID を埋める
export $(cat .env | xargs)
python3 setup_db.py
```

## Windows での準備

Pythonは https://www.python.org/downloads/ から導入(インストーラの
「Add python.exe to PATH」に必ずチェック)。コマンドは PowerShell を想定。

```powershell
git clone https://github.com/CyberSakuraX/tsumu-rec.git
cd tsumu-rec\notion
Copy-Item .env.example .env    # エディタで中身を埋める

# .env を読み込んで実行(PowerShell には export がないため)
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#=]+)=(.*)$') {
    [Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim())
  }
}
$env:PYTHONUTF8 = "1"
python setup_db.py
```

Windows 固有の注意が2つある。

1. **文字コード**: DB名やプロパティ名が日本語なので、`PYTHONUTF8=1` を付けないと
   コンソール出力が文字化けしたり `UnicodeEncodeError` で落ちることがある。上の手順に含めてある。
2. **改行コード**: Mac/Windows を行き来すると差分が全行変更になることがある。
   クローン直後に一度だけ設定しておく。

```powershell
git config --global core.autocrlf input
```

## iPhone での進め方

iPhone は「コードを書く端末」ではなく「作って試す端末」として使う。

- **ショートカット作成・修正**: `docs/iphone-shortcuts.md` を見ながらショートカットAppで直接作る。
  これは iPhone でしかできない作業で、Mac/Windows からは代行できない
- **実機テスト**: 記録 → Notion側に行が増えたか確認、のループ
- **ドキュメントの軽微な修正**: GitHub の Web / iOSアプリから直接編集してコミットできる。
  ただし iPhone で編集したら、Mac/Windows 側で作業を再開する前に `git pull` を忘れない
- **ショートカット本体は git 管理外**: ショートカットAppの中身はファイルとして取り出せないため、
  設計は `docs/iphone-shortcuts.md` を正としてテキストで残す。実物を変更したら
  ドキュメント側も直す、という運用にする

## 分担の目安

最初の立ち上げは、この順番が一番詰まりにくい。

1. **Mac か Windows**: Notion Integration 作成 → 親ページ作成 → `setup_db.py` で DB作成 → `database_id` を控える
2. **iPhone**: `notion_config.json` と `peaking_flag.txt` を iCloud Drive に配置 → ショートカット4本作成 → 通知設定
3. **iPhone**: 数日ぶん記録して実際に溜める
4. **どの端末でも**: Claude に分析を依頼(Notion MCP と Strava MCP を使うので端末を問わない)

1 は片方の PC でやれば十分で、もう片方でやり直す必要はない。
