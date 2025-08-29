#!/usr/bin/env python3
"""
画像の透過部分以外をすべて黒（#000000）にしてシルエット化するスクリプト

使用例:
    # 単一ファイル
    python scripts/make_silhouette.py input/logos/logo.png
    
    # 複数ファイル（ワイルドカード）
    python scripts/make_silhouette.py "input/logos/*.png"
    
    # カスタム出力先
    python scripts/make_silhouette.py input.png --output output_silhouette.png
"""

import argparse
import sys
from pathlib import Path
from typing import List
import glob
from PIL import Image


def make_silhouette(input_path: Path, output_path: Path = None) -> Path:
    """
    透過部分以外を黒色にしてシルエット化
    
    Args:
        input_path: 入力画像パス
        output_path: 出力画像パス（省略時は自動生成）
    
    Returns:
        出力画像パス
    """
    try:
        img = Image.open(input_path)
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        pixels = img.load()
        width, height = img.size
        
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a > 0:
                    pixels[x, y] = (0, 0, 0, a)
        
        if output_path is None:
            stem = input_path.stem
            suffix = input_path.suffix
            output_path = input_path.parent / f"{stem}_silhouette{suffix}"
        
        img.save(output_path)
        
        print(f"✅ 変換完了: {input_path} → {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ エラー: {input_path} の処理に失敗しました: {e}", file=sys.stderr)
        raise


def process_files(pattern: str, output_dir: Path = None) -> List[Path]:
    """
    複数ファイルを処理
    
    Args:
        pattern: ファイルパターン（ワイルドカード可）
        output_dir: 出力ディレクトリ（省略時は元ファイルと同じ場所）
    
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
            output_path = output_dir / f"{input_path.stem}_silhouette{input_path.suffix}"
        else:
            output_path = None
        
        try:
            result = make_silhouette(input_path, output_path)
            results.append(result)
        except Exception:
            continue
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='画像の透過部分以外を黒色にしてシルエット化',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 単一ファイル処理
  %(prog)s input.png
  
  # 出力ファイル名指定
  %(prog)s input.png --output output_silhouette.png
  
  # 複数ファイル処理（ワイルドカード）
  %(prog)s "input/logos/*.png"
  
  # 出力ディレクトリ指定
  %(prog)s "input/*.png" --output-dir output/silhouettes/
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
    
    args = parser.parse_args()
    
    if args.output_dir and not args.output_dir.exists():
        args.output_dir.mkdir(parents=True, exist_ok=True)
    
    if '*' in args.input or '?' in args.input:
        results = process_files(args.input, args.output_dir)
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
            make_silhouette(input_path, output_path)
            print("\n✨ 完了")
        except Exception:
            sys.exit(1)


if __name__ == '__main__':
    main()