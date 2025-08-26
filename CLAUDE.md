# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

画像背景除去プロジェクト - `rembg`ライブラリを使用して画像から背景を自動的に除去する

## Environment Requirements

- **Python 3.9** (必須 - numba==0.53.1の互換性制約により3.10以降は使用不可)
- **uv** パッケージマネージャー使用
- 仮想環境: `./.venv`

## Common Commands

### Setup
```bash
# 仮想環境作成
uv venv .venv --python 3.9

# アクティベート
source .venv/bin/activate

# 依存パッケージインストール
uv pip install -r requirements.txt
```

### Development
```bash
# 背景除去スクリプト実行
python scripts/remove_bg.py

# requirements.txt更新
uv pip freeze > requirements.txt

# 新規パッケージ追加
uv pip install <package-name>
```

## Project Structure

```
posters/
├── input/           # 処理対象の画像ファイル
├── output/          # 背景除去後の画像ファイル
├── scripts/         # Pythonスクリプト
│   └── remove_bg.py # メイン背景除去スクリプト
└── requirements.txt # 依存パッケージリスト
```

## Code Architecture

### 背景除去処理フロー
1. `PIL.Image`で入力画像を読み込み
2. `rembg.remove()`で背景除去処理
3. PNG形式（透明背景）で出力保存

### スクリプト構造
- `scripts/remove_bg.py`: ハードコードされたパスで単一画像を処理
- 入力: `input/`ディレクトリのJPEG画像
- 出力: `output/`ディレクトリのPNG画像（透明背景）

## Critical Dependencies

- `rembg==2.0.61`: 背景除去コアライブラリ
- `numba==0.60.0`: rembgの依存（Python 3.9制約の原因）
- `pillow==11.3.0`: 画像I/O処理