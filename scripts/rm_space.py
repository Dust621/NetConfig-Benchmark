import os

# 目标文件夹路径
folder_path = "datasets/Huawei/extracted_images"

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 判断是否是 PNG 文件
    if filename.lower().endswith(".png"):
        # 去掉空格
        new_filename = filename.replace(" ", "")

        # 如果有变化，才进行重命名
        if new_filename != filename:
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)

            os.rename(old_path, new_path)
            print(f"已重命名: {filename} -> {new_filename}")

print("处理完成！")
