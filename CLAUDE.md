# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

画像処理プロジェクト - 背景除去とQRコード生成機能を提供
- `rembg`ライブラリを使用した画像背景の自動除去
- カスタマイズ可能なQRコード生成（アイコン・カラー対応）
- 画像の2値化処理（純粋な白黒変換）
- 透過画像のシルエット化処理

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
# 背景除去スクリプト実行（uvを使用）
# 単一ファイル
uv run python scripts/remove_background.py input/photo.jpg

# 複数ファイルバッチ処理
uv run python scripts/remove_background.py "input/*.jpg" --batch

# QRコード生成
# 基本
uv run python scripts/generate_qrcode.py "https://example.com"

# アイコン・カラー付き
uv run python scripts/generate_qrcode.py "https://example.com" \
  --icon logo.png --fill-color "#FF5722" --back-color "#FFF3E0"

# 画像の2値化（白黒変換）
uv run python scripts/binarize_image.py "input/*.png" --threshold 128

# 画像のシルエット化（透過部分以外を黒に）
uv run python scripts/make_silhouette.py "input/logos/*.png"

# YAMLレシピによるバッチQRコード生成
uv run python scripts/batch_qrcode.py recipe/qrcode.yaml

# requirements.txt更新
uv pip freeze > requirements.txt

# 新規パッケージ追加
uv pip install <package-name>
```

## Project Structure

```
posters/
├── input/                    # 処理対象の画像ファイル
├── output/                   # 処理後の画像ファイル（背景除去、QRコード）
├── scripts/                  # Pythonスクリプト
│   ├── remove_background.py # 汎用背景除去スクリプト
│   ├── generate_qrcode.py   # QRコード生成スクリプト
│   ├── binarize_image.py    # 画像2値化スクリプト
│   └── make_silhouette.py   # シルエット化スクリプト
├── recipe/                   # バッチ処理レシピ
│   └── qrcode.yaml          # QRコードバッチ生成設定
├── knowledge/                # プロジェクトドキュメント
│   ├── qrcode-generation.md # QRコード生成機能の詳細
│   └── image-processing.md  # 画像処理スクリプトの詳細
└── requirements.txt          # 依存パッケージリスト
```

## Code Architecture

### 背景除去処理フロー
1. `PIL.Image`で入力画像を読み込み
2. `rembg.remove()`で背景除去処理
3. PNG形式（透明背景）で出力保存

### QRコード生成フロー
1. `qrcode.QRCode`でQRコード生成（高エラー訂正レベル）
2. オプションでアイコン画像を中央に配置
3. カスタムカラー適用（前景色・背景色）
4. PNG形式で出力保存

### 画像2値化処理フロー
1. 入力画像をグレースケールに変換
2. しきい値で各ピクセルを判定
3. 純粋な白黒画像として出力

### シルエット化処理フロー
1. 入力画像のアルファチャンネルを解析
2. 不透明部分のRGB値を黒に変換
3. アルファチャンネル保持で出力

### スクリプト構造
- `scripts/remove_background.py`: 汎用背景除去スクリプト
  - コマンドライン引数で柔軟な入出力指定
  - 単一ファイル/複数ファイルバッチ処理対応
  - ワイルドカードパターンサポート

- `scripts/generate_qrcode.py`: QRコード生成スクリプト
  - URLからQRコード生成
  - アイコン画像の中央配置（自動クロップ・リサイズ）
  - カラーカスタマイズ（色名/HEXコード対応）
  - サイズ調整可能（デフォルト: 1024x1024px）

- `scripts/binarize_image.py`: 画像2値化スクリプト
  - グレースケール変換後、しきい値で白黒化
  - 出力は純粋な黒(#000000)と白(#FFFFFF)
  - しきい値カスタマイズ可能

- `scripts/make_silhouette.py`: シルエット化スクリプト
  - 透過部分以外を黒色に変換
  - アルファチャンネル保持
  - ロゴのシルエット化に最適

## Critical Dependencies

- `rembg==2.0.61`: 背景除去コアライブラリ
- `numba==0.60.0`: rembgの依存（Python 3.9制約の原因）
- `pillow==11.3.0`: 画像I/O処理
- `qrcode==8.2`: QRコード生成ライブラリ