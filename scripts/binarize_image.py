#!/usr/bin/env python3
"""
画像を純粋な白黒（2値化）に変換するスクリプト
黒 (#000000) と白 (#FFFFFF) のみに変換

使用例:
    # 単一ファイル
    python scripts/binarize_image.py input.png
    
    # 複数ファイル（ワイルドカード）
    python scripts/binarize_image.py "output/qrcode_*.png"
    
    # カスタム出力先
    python scripts/binarize_image.py input.png --output output_bw.png
    
    # しきい値指定（デフォルト: 128）
    python scripts/binarize_image.py input.png --threshold 100
"""

import argparse
import sys
from pathlib import Path
from typing import List
import glob
from PIL import Image


def binarize_image(input_path: Path, output_path: Path = None, threshold: int = 128) -> Path:
    """
    画像を純粋な白黒（2値化）に変換
    
    Args:
        input_path: 入力画像パス
        output_path: 出力画像パス（省略時は自動生成）
        threshold: 2値化のしきい値（0-255、デフォルト128）
    
    Returns:
        出力画像パス
    """
    try:
        img = Image.open(input_path)
        
        gray_img = img.convert('L')
        
        bw_img = gray_img.point(lambda x: 0 if x < threshold else 255, '1')
        
        bw_img = bw_img.convert('RGB')
        
        if output_path is None:
            stem = input_path.stem
            suffix = input_path.suffix
            output_path = input_path.parent / f"{stem}_bw{suffix}"
        
        bw_img.save(output_path)
        
        print(f"✅ 変換完了: {input_path} → {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ エラー: {input_path} の処理に失敗しました: {e}", file=sys.stderr)
        raise


def process_files(pattern: str, output_dir: Path = None, threshold: int = 128) -> List[Path]:
    """
    複数ファイルを処理
    
    Args:
        pattern: ファイルパターン（ワイルドカード可）
        output_dir: 出力ディレクトリ（省略時は元ファイルと同じ場所）
        threshold: 2値化のしきい値（0-255、デフォルト128）
    
    Returns:
        処理済みファイルパスのリスト
    """
    files = glob.glob(pattern)
    
    if not files:
        print(f"⚠️ 警告: '{pattern}' に一致するファイルが見つかりません", file=sys.stderr)
        return []
    
    results = []
    for file_path in files:
        input_path = Path(file_path)
        
        if output_dir:
            output_path = output_dir / f"{input_path.stem}_bw{input_path.suffix}"
        else:
            output_path = None
        
        try:
            result = binarize_image(input_path, output_path, threshold)
            results.append(result)
        except Exception:
            continue
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='画像を純粋な白黒（2値化）に変換',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 単一ファイル処理
  %(prog)s input.png
  
  # 出力ファイル名指定
  %(prog)s input.png --output output_bw.png
  
  # 複数ファイル処理（ワイルドカード）
  %(prog)s "output/qrcode_*.png"
  
  # 出力ディレクトリ指定
  %(prog)s "input/*.jpg" --output-dir output/bw/
  
  # しきい値指定
  %(prog)s input.png --threshold 100
        """
    )
    
    parser.add_argument(
        'input',
        help='入力画像ファイルまたはパターン（ワイルドカード可）'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='出力ファイルパス（単一ファイル処理時のみ有効）'
    )
    
    parser.add_argument(
        '--output-dir', '-d',
        type=Path,
        help='出力ディレクトリ（複数ファイル処理時に使用）'
    )
    
    parser.add_argument(
        '--threshold', '-t',
        type=int,
        default=128,
        help='2値化のしきい値（0-255、デフォルト: 128）'
    )
    
    args = parser.parse_args()
    
    if args.output_dir and not args.output_dir.exists():
        args.output_dir.mkdir(parents=True, exist_ok=True)
    
    if '*' in args.input or '?' in args.input:
        results = process_files(args.input, args.output_dir, args.threshold)
        if results:
            print(f"\n✨ 完了: {len(results)} ファイルを処理しました")
        else:
            sys.exit(1)
    else:
        input_path = Path(args.input)
        
        if not input_path.exists():
            print(f"❌ エラー: ファイルが見つかりません: {input_path}", file=sys.stderr)
            sys.exit(1)
        
        output_path = Path(args.output) if args.output else None
        
        try:
            binarize_image(input_path, output_path, args.threshold)
            print("\n✨ 完了")
        except Exception:
            sys.exit(1)


if __name__ == '__main__':
    main()