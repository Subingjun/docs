#修改下面pattern = r'.*\.docx$'的docx部分匹配不同后缀
#重新运行会覆盖原本的结果，如果需要可以修改output_file_path = os.path.join(current_directory, 'output_file.txt')的output_file.txt保存到不同文件
import os
import re

def list_files(directory, output_file, pattern=None):
    # 检查目录是否存在
    if not os.path.isdir(directory):
        print(f"Error: {directory} 不是一个有效的目录")
        return
    
    # 编译正则表达式
    regex = re.compile(pattern) if pattern else None
    
    # 递归获取目录中的所有文件名
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.relpath(os.path.join(root, filename), directory)
            file_name = os.path.splitext(os.path.basename(file_path))[0]  # 获取不带后缀的文件名，去掉[0],可以得到后缀。
            if not regex or regex.search(file_path):
                files.append(file_name)
    
    # 将文件名写入到输出文件中
    with open(output_file, 'w') as f:
        for file in files:
            f.write(file + '\n')
    
    print(f"文件名已写入到 {output_file}")

# 获取当前脚本所在目录
current_directory = os.path.dirname(__file__)

# 指定输出文件路径
output_file_path = os.path.join(current_directory, 'output_file.txt')

# 正则表达式模式
pattern = r'.*\.docx$'  # 仅输出以 .docx 结尾的文件名，不包括路径和后缀名。删掉引号中的值可以获取全部文件。

# 调用函数
list_files(current_directory, output_file_path, pattern)
