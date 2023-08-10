from PIL import Image
import logging
from datetime import datetime
import os

"""
    滑块验证-图像色差比对
"""
class SliderRecognizer:


    # 获取当前时间，并将其格式化为指定的字符串格式
    current_time = datetime.now().strftime('%Y-%m-%d %H')

    # 拼接带有时间的日志文件名称
    log_file = os.path.join("E:\product\pycharm\DataCollectify02", 'logs', f'SliderRecognizer_{current_time}.log')

    # 配置日志记录
    logging.basicConfig(filename=log_file, level=logging.INFO,encoding='utf-8')
    print(log_file)

    @staticmethod
    def find_slider_cursor(image1_path, image2_path):
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        unit_type = "Y"
        n = 10
        m = None

        _, _, max_drop_diff_cursor2, _ = SliderRecognizer.compare_pixels(image1, image2, unit_type, n, m)

        return max_drop_diff_cursor2

    @staticmethod
    def compare_pixels(image1, image2, unit_type, n, m=None):

        width1, height1 = image1.size
        width2, height2 = image2.size

        if unit_type == "P":
            unit_size_x = n
            unit_size_y = n
        elif unit_type == "X":
            unit_size_x = width1
            unit_size_y = n
        elif unit_type == "Y":
            unit_size_x = n
            unit_size_y = height1
        else:
            unit_size_x = n
            unit_size_y = m

        similarities = []
        cursor = 1
        current_x = 0
        current_y = 0

        max_drop_diff = 0
        max_drop_diff_cursor1 = 0
        max_drop_diff_cursor2 = 0

        while current_y < height1:
            while current_x < width1:
                end_x = min(current_x + unit_size_x, width1)
                end_y = min(current_y + unit_size_y, height1)

                # 获取当前基本单元内的所有像素颜色
                unit1 = [image1.getpixel((x, y)) for x in range(current_x, end_x) for y in range(current_y, end_y)]
                unit2 = [image2.getpixel((x, y)) for x in range(current_x, end_x) for y in range(current_y, end_y)]

                # 计算像素颜色的平均值
                average1 = sum([sum(pixel1) for pixel1 in unit1]) // (len(unit1) * 3)
                average2 = sum([sum(pixel2) for pixel2 in unit2]) // (len(unit2) * 3)

                similarity = round(100 - abs(average1 - average2), 2)
                similarities.append(similarity)

                # 输出基本单元信息和相似度
                unit_info = f"单元信息：{unit_size_x}*{unit_size_y}的矩阵"
                similarity_info = f"ID:(游标){cursor}：相似度{similarity}%"

                logging.info(f"{unit_info}\n{similarity_info}\n")

                # 更新最大下降值的单元游标和下降值
                if cursor > 1:
                    diff = similarities[cursor - 2] - similarity
                    if diff > max_drop_diff:
                        max_drop_diff = diff
                        max_drop_diff_cursor1 = cursor - 1
                        max_drop_diff_cursor2 = cursor

                cursor += 1
                current_x += unit_size_x

            current_x = 0
            current_y += unit_size_y
        logging.info(f"\n下降最大的单元游标：{max_drop_diff_cursor2}")
        logging.info(f"最大下降值：{max_drop_diff}")
        return similarities, max_drop_diff_cursor1, max_drop_diff_cursor2, max_drop_diff
