import re
import os
from pathlib import Path

class RuleBlock:
    def __init__(self):
        self.metadata = {}
        self.content = ""

def parse_rule_blocks(file_content):
    """解析规则块，返回RuleBlock对象列表"""
    # 使用正则表达式匹配规则块
    pattern = r'---\n(.*?)\n---\n(.*?)(?=(?:\n---\n)|$)'
    matches = re.finditer(pattern, file_content, re.DOTALL)
    
    blocks = []
    for match in matches:
        block = RuleBlock()
        
        # 解析元数据部分
        metadata_str = match.group(1)
        for line in metadata_str.strip().split('\n'):
            if ':' in line:
                key, value = [x.strip() for x in line.split(':', 1)]
                # 处理布尔值
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                block.metadata[key] = value
        
        # 保存内容部分
        block.content = match.group(2).strip()
        blocks.append(block)
    
    return blocks

def save_rule_file(block, output_dir, index):
    """保存单个规则文件"""
    # 如果没有描述，使用默认名称
    description = block.metadata.get('description', f'rule_{index}')
    # 创建文件名：将描述转换为文件名安全的格式
    filename = re.sub(r'[^w\\-_]', '_', description.lower()) + '.mdc'
    
    file_path = Path(output_dir) / filename
    
    # 构建文件内容
    content = ['---']
    # 写入元数据
    for key, value in block.metadata.items():
        content.append(f'{key}: {value}')
    content.append('---\n')
    # 写入主要内容
    content.append(block.content)
    
    # 保存文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    return filename

def process_rules_file(input_file, output_dir='.'): 
    """处理规则文件并分割成独立的文件"""
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析规则块
    blocks = parse_rule_blocks(content)
    
    # 保存每个规则块
    saved_files = []
    for index, block in enumerate(blocks, 1):
        filename = save_rule_file(block, output_dir, index)
        saved_files.append(filename)
        print(f"已创建规则文件: {filename}")
    
    return saved_files

def main():
    input_file = input('请输入输入文件路径: ')
    output_dir = input('请输入输出目录: ')
    
    # 导入os模块并创建输出目录
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    process_rules_file(input_file, output_dir)
    print("所有规则文件已生成完成！")

if __name__ == "__main__":
    main() 