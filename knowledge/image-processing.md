# 画像処理機能

## 概要
プロジェクトで使用する画像処理スクリプト群の仕様と使用方法

## スクリプト一覧

### 1. binarize_image.py
画像を純粋な白黒（2値化）に変換するスクリプト

#### 機能
- グレースケール変換後、しきい値で2値化
- 出力は純粋な黒（#000000）と白（#FFFFFF）のみ
- しきい値はカスタマイズ可能（デフォルト: 128）

#### 使用例
```bash
# 単一ファイル
uv run python scripts/binarize_image.py input.png

# 複数ファイル（ワイルドカード）
uv run python scripts/binarize_image.py "output/qrcode_*.png"

# しきい値指定
uv run python scripts/binarize_image.py input.png --threshold 100

# 出力先指定
uv run python scripts/binarize_image.py input.png --output output_bw.png
```

#### 出力
- デフォルト: `{元ファイル名}_bw.png`
- 形式: PNG（RGB）

### 2. make_silhouette.py
透過PNG画像をシルエット化するスクリプト

#### 機能
- 透過部分以外のすべてのピクセルを黒（#000000）に変換
- アルファチャンネル（透明度）は保持
- ロゴのシルエット化に最適

#### 使用例
```bash
# 単一ファイル
uv run python scripts/make_silhouette.py input/logos/logo.png

# 複数ファイル（ワイルドカード）
uv run python scripts/make_silhouette.py "input/logos/*.png"

# 出力先指定
uv run python scripts/make_silhouette.py logo.png --output logo_silhouette.png

# 出力ディレクトリ指定
uv run python scripts/make_silhouette.py "input/*.png" --output-dir output/silhouettes/
```

#### 出力
- デフォルト: `{元ファイル名}_silhouette.png`
- 形式: PNG（RGBA、透過保持）

## 処理フロー例

### QRコード用ロゴの準備
1. オリジナルロゴ（カラー）を `input/logos/` に配置
2. `make_silhouette.py` でシルエット化
3. シルエット化されたロゴを `generate_qrcode.py` でQRコードに埋め込み

```bash
# ロゴをシルエット化
uv run python scripts/make_silhouette.py "input/logos/*.png"

# シルエットロゴでQRコード生成
uv run python scripts/generate_qrcode.py "https://example.com" \
  --icon input/logos/logo_silhouette.png \
  --fill-color "#000000"
```

## 技術仕様

### 依存ライブラリ
- `Pillow`: 画像I/O、変換処理

### 画像処理アルゴリズム

#### 2値化（binarize_image.py）
1. 入力画像をグレースケール（'L'モード）に変換
2. 各ピクセルをしきい値と比較
3. しきい値未満 → 黒（0）、以上 → 白（255）
4. RGB形式で保存

#### シルエット化（make_silhouette.py）
1. 入力画像をRGBA形式に変換
2. 各ピクセルのアルファ値をチェック
3. アルファ > 0 の場合、RGB値を(0, 0, 0)に設定
4. アルファ値は保持したまま保存

## バッチ処理のためのYAML設定

`recipe/qrcode.yaml` でバッチ処理を定義可能：

```yaml
jobs:
  - title: ロゴ付きQRコード生成
    input:
      icon: input/logos/logo_silhouette.png
      url: https://example.com
      fill-color: "#000000"
    output: output/qr_example.png
```

## 注意事項
- 大量のファイル処理時はメモリ使用量に注意
- 出力ファイル名の重複に注意（上書きされる）
- ワイルドカード使用時はクォートで囲む（シェルの展開を防ぐため）