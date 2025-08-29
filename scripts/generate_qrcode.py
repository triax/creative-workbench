#!/usr/bin/env python3
"""
QRコード生成スクリプト
任意のURLから、任意のアイコン画像を中央に配置したQRコードを生成する
"""

import argparse
import qrcode
from PIL import Image
import os
from pathlib import Path


def create_qr_with_icon(url, icon_path=None, output_path=None, size=1024, icon_size_ratio=0.3,
                        fill_color="black", back_color="white"):
    """
    URLからQRコードを生成し、オプションでアイコンを中央に配置する
    
    Args:
        url (str): QRコードに埋め込むURL
        icon_path (str): アイコン画像のパス（オプション）
        output_path (str): 出力ファイルパス
        size (int): QRコード画像のサイズ（ピクセル）
        icon_size_ratio (float): QRコードサイズに対するアイコンサイズの比率
        fill_color (str): QRコードの前景色（デフォルト: black）
        back_color (str): QRコードの背景色（デフォルト: white）
    """
    # QRコード生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高エラー訂正（アイコンを重ねるため）
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # QRコード画像生成（カスタム色を適用）
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # 指定サイズにリサイズ
    qr_img = qr_img.resize((size, size), Image.Resampling.LANCZOS)
    
    # アイコンを配置する場合
    if icon_path and os.path.exists(icon_path):
        # アイコン読み込み
        icon = Image.open(icon_path)
        
        # アイコンサイズ計算
        icon_size = int(size * icon_size_ratio)
        
        # アイコンを正方形にクロップ（中央切り抜き）
        icon_width, icon_height = icon.size
        min_dimension = min(icon_width, icon_height)
        
        left = (icon_width - min_dimension) // 2
        top = (icon_height - min_dimension) // 2
        right = left + min_dimension
        bottom = top + min_dimension
        
        icon = icon.crop((left, top, right, bottom))
        
        # アイコンをリサイズ
        icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        
        # 背景色でパディングを作成（アイコンの背後）
        padding_bg = Image.new('RGB', (icon_size + 20, icon_size + 20), back_color)
        
        # アイコンがRGBAの場合、背景色と合成
        if icon.mode == 'RGBA':
            icon_bg = Image.new('RGB', icon.size, back_color)
            icon_bg.paste(icon, mask=icon.split()[3])
            icon = icon_bg
        
        # 背景にアイコンを配置
        padding_bg.paste(icon, (10, 10))
        
        # QRコードの中央にアイコンを配置
        qr_img = qr_img.convert('RGB')
        position = ((size - icon_size - 20) // 2, (size - icon_size - 20) // 2)
        qr_img.paste(padding_bg, position)
    
    return qr_img


def main():
    parser = argparse.ArgumentParser(
        description='QRコード生成スクリプト - URLからQRコードを生成し、オプションでアイコンを中央に配置'
    )
    parser.add_argument('url', help='QRコードに埋め込むURL')
    parser.add_argument('--icon', '-i', help='中央に配置するアイコン画像のパス')
    parser.add_argument('--output', '-o', help='出力ファイルパス（デフォルト: output/qrcode.png）')
    parser.add_argument('--size', '-s', type=int, default=1024, 
                       help='QRコード画像のサイズ（ピクセル、デフォルト: 1024）')
    parser.add_argument('--icon-size', type=float, default=0.3,
                       help='QRコードサイズに対するアイコンサイズの比率（0.1-0.4、デフォルト: 0.3）')
    parser.add_argument('--fill-color', '-f', default='black',
                       help='QRコードの前景色（デフォルト: black）。色名またはHEXコード（#FF0000）を指定')
    parser.add_argument('--back-color', '-b', default='white',
                       help='QRコードの背景色（デフォルト: white）。色名またはHEXコード（#00FF00）を指定')
    
    args = parser.parse_args()
    
    # アイコンサイズ比率の検証
    if args.icon_size < 0.1 or args.icon_size > 0.4:
        print("警告: アイコンサイズ比率は0.1から0.4の範囲を推奨します")
    
    # 出力パスの設定
    if args.output:
        output_path = args.output
    else:
        # デフォルト出力ディレクトリの作成
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        # ファイル名の生成
        if args.icon:
            icon_name = Path(args.icon).stem
            output_path = output_dir / f'qrcode_with_{icon_name}.png'
        else:
            output_path = output_dir / 'qrcode.png'
    
    # QRコード生成
    try:
        qr_img = create_qr_with_icon(
            args.url,
            args.icon,
            str(output_path),
            args.size,
            args.icon_size,
            args.fill_color,
            args.back_color
        )
        
        # 保存
        qr_img.save(str(output_path))
        print(f"✅ QRコードを生成しました: {output_path}")
        
        # 詳細情報表示
        print(f"   URL: {args.url}")
        print(f"   サイズ: {args.size}x{args.size}px")
        if args.icon:
            print(f"   アイコン: {args.icon}")
            print(f"   アイコンサイズ比率: {args.icon_size}")
        if args.fill_color != 'black' or args.back_color != 'white':
            print(f"   前景色: {args.fill_color}")
            print(f"   背景色: {args.back_color}")
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
