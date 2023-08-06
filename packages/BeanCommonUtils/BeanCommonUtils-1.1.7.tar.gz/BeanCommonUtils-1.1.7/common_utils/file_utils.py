import os


def traversal_dir(dir_path):
    """
    遍历制定目录下的所有文件, 自动过滤掉短链接的文件
    :param dir_path:
    :return:
    """
    files_path = list()
    check_traversal_params(dir_path)

    for parent, dir_names, file_names in os.walk(dir_path, followlinks=True):
        for file_name in file_names:
            file_path = os.path.join(parent, file_name)

            if os.path.islink(file_path):
                continue
            else:
                files_path.append(file_path)

    return files_path


def check_traversal_params(dir_path):
    if not os.path.exists(dir_path):
        raise FileNotFoundError("参数错误, 请传入存在的目录路径")

    if not os.path.isdir(dir_path):
        raise ValueError("参数错误, 请传入需要遍历的目录路径")


if __name__ == '__main__':
    temp = traversal_dir("/Users/hly/Desktop/hlyDir/python_project/CommonUtils")
    # temp = traversal_dir("/Users/hly/Desktop/hlyDir/pytho_project/CommonUtils/common_utils/file_utils.py")
    print(temp)
