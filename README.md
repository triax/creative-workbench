# Posters - 画像処理プロジェクト

## 概要
画像処理機能を提供するPythonプロジェクトです。以下の機能を含みます：
- **背景除去**: `rembg`ライブラリを使用して高精度な背景除去を実現
- **QRコード生成**: カスタマイズ可能なQRコード生成（アイコン・カラー対応）
- **画像2値化**: 画像を純粋な白黒に変換
- **シルエット化**: 透過画像の不透明部分を黒色に変換

## 必要要件
- Python 3.9（必須）
- uv（パッケージマネージャー）

## インストール

### 1. uvのインストール
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# または pip経由
pip install uv
```

### 2. プロジェクトのセットアップ
```bash
# リポジトリのクローン
git clone [repository-url]
cd posters

# Python 3.9で仮想環境を作成
uv venv .venv --python 3.9

# 仮想環境をアクティベート
source .venv/bin/activate  # macOS/Linux
# または
.venv\Scripts\activate  # Windows

# 依存パッケージをインストール
uv pip install -r requirements.txt
```

## 使用方法

### 1. 背景除去機能

#### 単一ファイルの処理
```bash
# uvを使って実行（推奨）
uv run python scripts/remove_background.py input/photo.jpg

# 出力ファイル名を指定
uv run python scripts/remove_background.py input/photo.jpg -o output/result.png
```

#### 複数ファイルの一括処理
```bash
# inputディレクトリの全JPGファイルを処理
uv run python scripts/remove_background.py "input/*.jpg" --batch

# 特定の出力ディレクトリに保存
uv run python scripts/remove_background.py "input/*" --batch -d processed
```

### 2. QRコード生成機能

#### 基本的なQRコード生成
```bash
# シンプルなQRコード
uv run python scripts/generate_qrcode.py "https://example.com"

# 出力ファイル名を指定
uv run python scripts/generate_qrcode.py "https://example.com" -o custom_qr.png
```

#### アイコン付きQRコード
```bash
# ロゴを中央に配置
uv run python scripts/generate_qrcode.py "https://example.com" --icon logo.png

# サイズとアイコン比率をカスタマイズ
uv run python scripts/generate_qrcode.py "https://example.com" \
  --icon logo.png --size 512 --icon-size 0.25
```

#### カスタムカラー
```bash
# 色名で指定
uv run python scripts/generate_qrcode.py "https://example.com" \
  --fill-color "navy" --back-color "lightblue"

# HEXコードで指定
uv run python scripts/generate_qrcode.py "https://example.com" \
  --fill-color "#FF5722" --back-color "#FFF3E0"
```

### 3. 画像2値化機能

#### 白黒変換
```bash
# 単一ファイルの2値化
uv run python scripts/binarize_image.py input.png

# しきい値を指定（デフォルト: 128）
uv run python scripts/binarize_image.py input.png --threshold 100

# 複数ファイルの一括処理
uv run python scripts/binarize_image.py "input/*.png"
```

### 4. シルエット化機能

#### 透過画像のシルエット化
```bash
# 単一ファイルのシルエット化
uv run python scripts/make_silhouette.py input/logo.png

# 複数ロゴの一括処理
uv run python scripts/make_silhouette.py "input/logos/*.png"

# 出力ディレクトリ指定
uv run python scripts/make_silhouette.py "input/*.png" -d output/silhouettes/
```

### 5. バッチ処理

#### YAMLレシピによるQRコード一括生成
```yaml
# recipe/qrcode.yaml
jobs:
  - title: ロゴ付きQRコード
    input:
      icon: input/logos/logo_silhouette.png
      url: https://example.com
      fill-color: "#000000"
    output: output/qr_example.png
```

#### ヘルプの表示
```bash
uv run python scripts/remove_background.py --help
uv run python scripts/generate_qrcode.py --help
uv run python scripts/binarize_image.py --help
uv run python scripts/make_silhouette.py --help
```

## ファイル構成
```
posters/
├── .venv/                      # 仮想環境ディレクトリ
├── input/                      # 処理対象の画像ファイル
├── output/                     # 処理後の画像ファイル（背景除去、QRコード）
├── scripts/                    # Pythonスクリプト
│   ├── remove_background.py    # 汎用背景除去スクリプト
│   ├── generate_qrcode.py      # QRコード生成スクリプト
│   ├── binarize_image.py       # 画像2値化スクリプト
│   └── make_silhouette.py      # シルエット化スクリプト
├── recipe/                     # バッチ処理レシピ
│   └── qrcode.yaml            # QRコードバッチ生成設定
├── knowledge/                  # プロジェクトドキュメント
│   ├── qrcode-generation.md   # QRコード生成機能の詳細
│   └── image-processing.md    # 画像処理スクリプトの詳細
├── requirements.txt            # 依存パッケージリスト
├── CLAUDE.md                   # 開発環境の詳細情報
└── README.md                   # このファイル
```

## トラブルシューティング

### Python バージョンエラー
`numba`の互換性問題により、Python 3.10以降では動作しません。必ずPython 3.9を使用してください。

### 仮想環境のアクティベートを忘れた場合
```bash
source .venv/bin/activate
```
を実行してから作業を開始してください。

## ライセンス
[ライセンス情報を追加]