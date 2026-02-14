# CLAUDE.md

This file provides guidance for AI assistants working with the **nasubiy** repository.

## Repository Overview

- **Repository**: `yumaspecialite-ui/nasubiy`
- **Description**: Instagram リール動画の台本作成ツール
- **Language**: Python 3.9+

## Project Structure

```
nasubiy/
├── CLAUDE.md              # AI assistant guidance (this file)
├── pyproject.toml         # プロジェクト設定・依存関係
├── reel_script/           # メインパッケージ
│   ├── __init__.py
│   ├── __main__.py        # python -m reel_script エントリーポイント
│   ├── cli.py             # CLIインターフェース（対話モード + 引数モード）
│   ├── formatter.py       # 出力フォーマッター（text / markdown / json）
│   ├── generator.py       # 台本生成ロジック
│   ├── models.py          # データモデル（ReelScript, ReelDuration, ReelStyle等）
│   └── templates/         # テンプレートデータ
│       ├── __init__.py
│       ├── hooks.py       # フック（冒頭のつかみ）テンプレート
│       └── structures.py  # スタイル別の台本構成テンプレート
└── tests/                 # テストディレクトリ
```

## Development Setup

- **Language**: Python 3.9+
- **Dependencies**: 標準ライブラリのみ（外部依存なし）
- **Install**: `pip install -e .`
- **Run**: `python -m reel_script` または `reel-script`

## Usage

```bash
# 対話モード
python -m reel_script

# コマンドライン引数モード
python -m reel_script --topic "朝のルーティン" --style vlog --duration 30
python -m reel_script --topic "Python入門" --style tutorial --duration 60 --format markdown -o script.md
```

## Testing

テストは `tests/` ディレクトリに配置。`pytest` で実行。

```bash
pytest tests/
```

## Git Conventions

- **Branch naming**: Feature branches use the pattern `claude/<description>-<session-id>`
- **Commits**: Use clear, descriptive commit messages
- **Remote**: `yumaspecialite-ui/nasubiy`

## Key Conventions for AI Assistants

1. **Read before editing** — Always read existing files before proposing changes.
2. **Minimal changes** — Only modify what is directly requested. Avoid unnecessary refactors.
3. **No guessing** — If the project structure or conventions are unclear, explore first.
4. **Update this file** — When significant project setup occurs (new framework, test config, CI/CD), update this CLAUDE.md to reflect the current state.
5. **Security** — Never commit secrets, credentials, or `.env` files.
