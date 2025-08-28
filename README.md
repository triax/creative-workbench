# Posters - 画像背景除去プロジェクト

## 概要
画像から背景を自動的に除去するPythonプロジェクトです。`rembg`ライブラリを使用して高精度な背景除去を実現します。

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

### 基本的な使い方
```python
from rembg import remove
from PIL import Image

# 画像を開く
input_img = Image.open('input.jpg')

# 背景を除去
output_img = remove(input_img)

# 結果を保存（PNG形式で透明背景）
output_img.save('output.png')
```

### スクリプトの実行

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

#### ヘルプの表示
```bash
uv run python scripts/remove_background.py --help
```

## ファイル構成
```
posters/
├── .venv/                      # 仮想環境ディレクトリ
├── input/                      # 処理対象の画像ファイル
├── output/                     # 背景除去後の画像ファイル
├── scripts/                    # Pythonスクリプト
│   └── remove_background.py    # 汎用背景除去スクリプト
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