"""
处理文件句柄
"""


def get_lines(file_path: str, mode="r", encoding="utf-8"):
    with open(file_path, mode=mode, encoding=encoding) as f:
        file_lines = [line.strip() for line in f.readlines()]
    return file_lines


def write_lines(file_path, lines=None, mode="w", encoding="utf-8", newline_separator="\n"):
    if lines is None:
        lines = []
    if lines is None or len(lines) == 0:
        return False
    with open(file_path, mode=mode, encoding=encoding) as target:
        for line in lines:
            line = line.strip()
            target.write(line)
            target.write(newline_separator)


class File:
    def __init__(self, file_path):
        pass


if __name__ == '__main__':
    pass
