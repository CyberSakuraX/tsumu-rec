# 開発環境 — 時間帯によって変わる端末で、同じ作業を継続する

朝は iPhone、日中は Windows、夜は Mac —— のように、**時間帯によって手元にある端末が変わる**。
どの端末も「同じ作業の続き」ができる状態にしておくのがこのドキュメントの目的。
端末ごとに役割を固定しない(「この作業はMacでしかできない」を作らない)。

そのために必要なのは実質2つだけ。

1. **作業状態が常にクラウド側にある**こと(手元の端末にしか無い状態を作らない)
2. **どの端末からでも同じ環境に入れる**こと

## 作業状態はどこにあるか

このプロジェクトの状態は3か所に分かれている。どれも既にクラウド側にあるので、
端末を変えても失われない。

| 状態 | 置き場所 | 端末を変えたときの扱い |
|---|---|---|
| コード・ドキュメント | GitHub | `git pull` で追いつく |
| 記録データ | Notion | 何もしなくていい。常に最新 |
| Integrationトークン | 各端末のローカル `.env` / iCloud | 端末ごとに1回だけ設置(後述) |

**唯一の弱点はコード側**で、手元でコミットせずに端末を離れると、そのぶんは次の端末から見えない。
ここだけ意識的に運用でカバーする。

## 端末を離れるときの作法

これが一番効く。区切りが悪くても、**離れるときは必ず push する**。

```
git add -A
git commit -m "wip: 〜の途中"
git push -u origin <branch>
```

`wip:` のコミットは後でまとめて整理すればいいので、粒度は気にしなくていい。
「キリのいいところまでやってからコミット」を守ろうとすると、
中途半端な状態が手元の端末に取り残されて、次の時間帯に別端末で再開できなくなる。
**コミットは完成の宣言ではなく、端末間の受け渡し**と考える。

再開するときは必ず最初に:

```
git pull origin <branch>
```

pull を忘れて古い状態から書き始めるのが、複数端末で唯一起きる面倒なトラブル(コンフリクト)。
逆に言えば、push と pull さえ守れば他に気をつけることはない。

なお、コードとドキュメントの同期は **GitHub 経由でのみ**行うこと。
iCloud や Dropbox でリポジトリのフォルダごと共有するのは避ける(`.git` が壊れる)。

## iPhone しかない時間帯にどこまでできるか

「iPhone だから編集は無理」とはならない。**Claude Code on the web**(https://claude.ai/code)を
使えば、iPhone のブラウザから今と同じようにコード編集・コミット・push まで全部できる。
リポジトリはクラウド上のコンテナにクローンされるので、iPhone 側に開発環境を作る必要もない。
朝の通勤中に思いついた修正をその場で入れる、といった使い方ができる。

iPhone から実行できないのは、実質これだけ:

- **ローカルで `setup_db.py` を叩く** → ただし Claude Code on the web 側から実行できるし、
  そもそも DB作成は最初の1回きりなので、この制約が効く場面はほぼ無い

逆に **iPhone でしかできない**ことが1つある:

- **ショートカットApp の編集**。ショートカット本体はファイルとして取り出せないため、
  git にも載らず、Mac/Windows から編集もできない

なのでショートカットを直す作業だけは、iPhone が手元にある時間帯に回す必要がある。
設計は `docs/iphone-shortcuts.md` をテキストの「正」として残してあるので、
PC の時間帯に「どう直すか」を書いておいて、iPhone の時間帯に実物へ反映する、という分け方ができる。

## 各端末の初期セットアップ(1回だけ)

以下は端末ごとに1回やれば、あとはどの時間帯でもそのまま使える。

### Mac

```
git clone https://github.com/CyberSakuraX/tsumu-rec.git
cd tsumu-rec/notion
cp .env.example .env      # NOTION_TOKEN / NOTION_PARENT_PAGE_ID を埋める
```

### Windows

Python は https://www.python.org/downloads/ から(インストーラの
「Add python.exe to PATH」にチェック)。PowerShell 前提。

```powershell
git clone https://github.com/CyberSakuraX/tsumu-rec.git
cd tsumu-rec\notion
Copy-Item .env.example .env    # 中身を埋める
git config --global core.autocrlf input
```

`core.autocrlf input` は Mac と往復したときに改行コードで全行差分になるのを防ぐため、
クローン直後に必ず入れておく。時間帯ごとに端末を行き来する以上、これが無いと差分が読めなくなる。

`setup_db.py` を Windows で実行する場合のみ、日本語のプロパティ名が文字化け・
`UnicodeEncodeError` になるので `PYTHONUTF8=1` を付ける:

```powershell
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#=]+)=(.*)$') {
    [Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim())
  }
}
$env:PYTHONUTF8 = "1"
python setup_db.py
```

### iPhone

- ブラウザで https://claude.ai/code を開き、このリポジトリを選べる状態にしておく
- iCloud Drive の `Shortcuts/` に `notion_config.json` と `peaking_flag.txt` を配置
  (`docs/iphone-shortcuts.md` 参照)

## トークンの扱い

Notion Integration Token は Integration 単位の権限なので、
**1つを3端末で使い回して問題ない**。端末は区別されない。

ただしリポジトリには絶対に入れないこと。`notion/.env` は `.gitignore` 済み。
端末間で渡すときはパスワードマネージャ経由か、Notion の管理画面から再取得する。
