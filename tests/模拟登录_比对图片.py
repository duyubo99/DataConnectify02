import time
from io import BytesIO
from PIL import Image

"""
    比较两张图片相同位置像素是否相似
"""
def is_pixel_equal(image1, image2, x, y):
    print(f"x:{x},y:{y}")
    pixel1 = image1.load()[x, y]
    print(f"pixel1{pixel1}")
    pixel2 = image2.load()[x, y]

    # 设置比较值
    threshold = 60

    delta_r = abs(pixel1[0] - pixel2[0])
    delta_g = abs(pixel1[1] - pixel2[1])
    delta_b = abs(pixel1[2] - pixel2[2])

    print(f"delta_r:{delta_r},delta_g:{delta_g},delta_b:{delta_b}")

    if delta_r < threshold and delta_g < threshold and delta_b < threshold:
        return True
    else:
        return False

image1 = Image.open("../down/img/001.png")
# 对比图片
image2 = Image.open("../down/img/001_yy.png")

left = 0

print(f"image1.size[0]:{image1.size[0]}")
print(f"image1.size[1]:{image1.size[1]}")

for i, pixel_x in enumerate(range(left, image1.size[0])):
    for j, pixel_y in enumerate(range(image1.size[1])):
        # 判断相似度，超过设定的相似度则表示找到拼图阴影
        if not is_pixel_equal(image1, image2, pixel_x, pixel_y):
            left = i
            break

print(left)

