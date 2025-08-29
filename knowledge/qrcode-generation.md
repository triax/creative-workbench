# QRコード生成機能

## 概要
`scripts/generate_qrcode.py`は、任意のURLからカスタマイズ可能なQRコードを生成するPythonスクリプトです。

## 主な機能

### 1. 基本的なQRコード生成
- 任意のURLをQRコードに変換
- 高エラー訂正レベル（ERROR_CORRECT_H）を使用
- デフォルトサイズ: 1024x1024ピクセル

### 2. アイコン配置機能
- QRコードの中央にカスタムアイコンを配置可能
- アイコンは自動的に正方形にクロップされる
- RGBA（透明背景）画像にも対応
- アイコンサイズはQRコードに対する比率で調整可能（推奨: 0.1-0.4）

### 3. カラーカスタマイズ
- 前景色（QRコードのパターン部分）のカスタマイズ
- 背景色のカスタマイズ
- 色指定方法:
  - 色名（例: "red", "blue", "navy"）
  - HEXコード（例: "#FF5722", "#00FF00"）

## 技術仕様

### 依存ライブラリ
- `qrcode`: QRコード生成ライブラリ
- `pillow`: 画像処理ライブラリ

### エラー訂正レベル
- `ERROR_CORRECT_H`（約30%）を使用
- アイコンを重ねても読み取り可能性を維持

### 画像処理
- リサンプリング: `LANCZOS`フィルタを使用（高品質）
- アイコンの背景: QRコードの背景色と同じ色でパディング追加

## 使用方法

### 基本コマンド
```bash
# シンプルなQRコード
uv run python scripts/generate_qrcode.py "https://example.com"

# アイコン付きQRコード
uv run python scripts/generate_qrcode.py "https://example.com" --icon logo.png

# カスタムカラー
uv run python scripts/generate_qrcode.py "https://example.com" \
  --fill-color "#FF5722" \
  --back-color "#FFF3E0"

# 全オプション使用例
uv run python scripts/generate_qrcode.py "https://example.com" \
  --icon logo.png \
  --output custom_qr.png \
  --size 512 \
  --icon-size 0.25 \
  --fill-color "navy" \
  --back-color "lightblue"
```

### コマンドラインオプション

| オプション | 短縮形 | 説明 | デフォルト |
|-----------|--------|------|------------|
| URL | - | QRコードに埋め込むURL（必須） | - |
| --icon | -i | 中央に配置するアイコン画像のパス | なし |
| --output | -o | 出力ファイルパス | output/qrcode.png |
| --size | -s | QRコード画像のサイズ（ピクセル） | 1024 |
| --icon-size | - | アイコンサイズ比率（0.1-0.4） | 0.3 |
| --fill-color | -f | QRコードの前景色 | black |
| --back-color | -b | QRコードの背景色 | white |

## 実装の詳細

### ファイル名の自動生成
- アイコンなし: `output/qrcode.png`
- アイコンあり: `output/qrcode_with_{icon_name}.png`

### アイコン処理フロー
1. アイコン画像を読み込み
2. 正方形にクロップ（中央切り抜き）
3. 指定サイズにリサイズ
4. RGBA画像の場合、背景色と合成
5. パディング（背景色）を追加
6. QRコードの中央に配置

### エラーハンドリング
- ファイルが存在しない場合は適切なエラーメッセージを表示
- アイコンサイズ比率が推奨範囲外の場合は警告を表示

## 今後の拡張案
- グラデーション対応
- 角丸スタイル対応
- SVG出力対応
- バッチ処理（複数URLの一括処理）