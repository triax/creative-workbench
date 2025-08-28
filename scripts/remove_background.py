#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Optional

from rembg import remove
from PIL import Image


def remove_background(
    input_path: str,
    output_path: Optional[str] = None,
    output_dir: Optional[str] = None
) -> str:
    """
    画像から背景を除去する

    Args:
        input_path: 入力画像のパス
        output_path: 出力画像のパス（省略時は自動生成）
        output_dir: 出力ディレクトリ（省略時はoutputディレクトリ）

    Returns:
        出力画像のパス
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"入力ファイルが見つかりません: {input_path}")
    
    # 出力パスの決定
    if output_path:
        output_file = Path(output_path)
    else:
        # デフォルトの出力ディレクトリ
        if output_dir:
            out_dir = Path(output_dir)
        else:
            out_dir = Path("output")
        
        out_dir.mkdir(exist_ok=True)
        
        # ファイル名に_no_bgを追加してPNG形式で保存
        stem = input_file.stem
        output_file = out_dir / f"{stem}_no_bg.png"
    
    # 背景除去処理
    print(f"処理中: {input_file}")
    input_img = Image.open(input_file)
    output_img = remove(input_img)
    output_img.save(output_file)
    
    print(f"✓ 背景を除去した画像を保存しました: {output_file}")
    return str(output_file)


def process_multiple_files(pattern: str, output_dir: Optional[str] = None) -> list:
    """
    複数ファイルを一括処理する

    Args:
        pattern: ファイルパターン（ワイルドカード使用可）
        output_dir: 出力ディレクトリ

    Returns:
        処理したファイルのリスト
    """
    from glob import glob
    
    files = glob(pattern)
    if not files:
        print(f"警告: パターン '{pattern}' に一致するファイルが見つかりません")
        return []
    
    processed = []
    for file_path in files:
        try:
            output = remove_background(file_path, output_dir=output_dir)
            processed.append(output)
        except Exception as e:
            print(f"エラー: {file_path} の処理に失敗しました - {e}")
    
    return processed


def main():
    parser = argparse.ArgumentParser(
        description="画像から背景を自動的に除去します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 単一ファイルの処理
  %(prog)s input/photo.jpg
  
  # 出力ファイル名を指定
  %(prog)s input/photo.jpg -o output/result.png
  
  # 複数ファイルを一括処理
  %(prog)s "input/*.jpg" --batch
  
  # inputディレクトリの全画像を処理
  %(prog)s "input/*" --batch -d processed
"""
    )
    
    parser.add_argument(
        "input",
        help="入力画像ファイルのパス（--batchモードではパターン）"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="出力ファイルのパス（省略時は自動生成）"
    )
    
    parser.add_argument(
        "-d", "--output-dir",
        help="出力ディレクトリ（デフォルト: output）"
    )
    
    parser.add_argument(
        "-b", "--batch",
        action="store_true",
        help="複数ファイルを一括処理"
    )
    
    args = parser.parse_args()
    
    try:
        if args.batch:
            # バッチ処理モード
            if args.output:
                print("警告: --batchモードでは--outputは無視されます")
            
            processed = process_multiple_files(args.input, args.output_dir)
            
            if processed:
                print(f"\n完了: {len(processed)}個のファイルを処理しました")
            else:
                sys.exit(1)
        else:
            # 単一ファイル処理
            remove_background(args.input, args.output, args.output_dir)
            
    except FileNotFoundError as e:
        print(f"エラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()