from rembg import remove
from PIL import Image

input_path = 'kanemoto.jpg'
output_path = 'kanemoto_no_bg.png'

input_img = Image.open(input_path)
output_img = remove(input_img)
output_img.save(output_path)

print(f"背景を除去した画像を {output_path} に保存しました")