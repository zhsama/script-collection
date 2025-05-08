import os
from pathlib import Path
import logging
from datetime import datetime
import sys
import cv2
import numpy as np
from PIL import Image
import io
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import threading
from queue import Queue
import time
from functools import partial
import psutil

class ProgressBar:
    def __init__(self, total):
        self.total = total
        self.counter = 0
        self.lock = threading.Lock()
        self.last_update = time.time()
        self.update_interval = 0.1  # 更新间隔（秒）

    def update(self):
        with self.lock:
            self.counter += 1
            current_time = time.time()
            if current_time - self.last_update >= self.update_interval:
                self.last_update = current_time
                percentage = (self.counter / self.total) * 100
                completed = '=' * int(percentage / 2)
                remaining = ' ' * (50 - len(completed))
                sys.stdout.write(f'\r进度: [{completed}{remaining}] {percentage:.1f}% ({self.counter}/{self.total})')
                sys.stdout.flush()

def setup_logging():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'webp_to_gif_conversion_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def optimize_image_size(image, max_size=800):
    """优化图像尺寸以减少内存使用"""
    width, height = image.size
    if width > max_size or height > max_size:
        ratio = min(max_size/width, max_size/height)
        new_size = (int(width*ratio), int(height*ratio))
        return image.resize(new_size, Image.LANCZOS)
    return image

def convert_single_file(args):
    """单个文件转换函数"""
    input_path, output_path, optimize_size = args
    try:
        # 读取webp文件
        img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise Exception("无法读取图像")
        
        # 检查是否有alpha通道
        if len(img.shape) > 2 and img.shape[2] == 4:
            # 分离alpha通道
            bgr = img[:, :, :3]
            alpha = img[:, :, 3]
            # 创建白色背景
            white_background = np.ones_like(bgr) * 255
            # 根据alpha混合图像
            alpha_3d = np.stack((alpha,) * 3, axis=-1) / 255.0
            final_img = (bgr * alpha_3d + white_background * (1 - alpha_3d)).astype(np.uint8)
        else:
            final_img = img

        # 转换BGR到RGB
        rgb_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_img)

        # 如果需要优化尺寸
        if optimize_size:
            pil_img = optimize_image_size(pil_img)

        # 保存为GIF
        pil_img.save(output_path, 'GIF', optimize=True)
        return True, input_path
    except Exception as e:
        return False, input_path

def get_optimal_workers():
    """获取最优的工作进程数"""
    cpu_cores = cpu_count()
    memory = psutil.virtual_memory()
    # 根据可用内存和CPU核心数计算合适的工作进程数
    memory_based_workers = int(memory.available / (1024 * 1024 * 1024))  # 每个进程预留1GB内存
    return min(cpu_cores, memory_based_workers, 16)  # 最大限制16个进程

def batch_convert(input_dir, output_dir, optimize_size=True):
    """批量转换目录中的所有WEBP文件"""
    logger = setup_logging()
    os.makedirs(output_dir, exist_ok=True)
    
    # 收集所有需要转换的文件
    webp_files = list(Path(input_dir).rglob("*.webp"))
    total_files = len(webp_files)
    
    if total_files == 0:
        logger.warning(f"在 {input_dir} 中没有找到WEBP文件")
        return
    
    logger.info(f"找到 {total_files} 个WEBP文件待转换")
    
    # 准备转换参数
    conversion_args = []
    for webp_file in webp_files:
        relative_path = webp_file.relative_to(input_dir)
        output_file = Path(output_dir) / relative_path.with_suffix('.gif')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        conversion_args.append((str(webp_file), str(output_file), optimize_size))

    # 创建进度条
    progress = ProgressBar(total_files)
    
    # 获取最优的工作进程数
    workers = get_optimal_workers()
    logger.info(f"使用 {workers} 个工作进程进行转换")

    # 使用进程池进行并行处理
    success_count = 0
    failed_files = []
    
    with ProcessPoolExecutor(max_workers=workers) as executor:
        future_to_file = {executor.submit(convert_single_file, args): args[0] 
                         for args in conversion_args}
        
        for future in as_completed(future_to_file):
            success, input_path = future.result()
            if success:
                success_count += 1
            else:
                failed_files.append(input_path)
            progress.update()

    # 输出最终统计信息
    print("\n转换完成！统计信息：")
    print(f"总文件数: {total_files}")
    print(f"成功转换: {success_count}")
    print(f"转换失败: {len(failed_files)}")

    # 记录失败的文件
    if failed_files:
        with open('failed_conversions.txt', 'w', encoding='utf-8') as f:
            for file in failed_files:
                f.write(f"{file}\n")
        print("失败的文件已记录到 failed_conversions.txt")

def main():
    input_directory = "./webp"
    output_directory = "./gif"
    
    print("开始转换WEBP文件到GIF...")
    start_time = time.time()
    
    batch_convert(input_directory, output_directory)
    
    end_time = time.time()
    print(f"\n总耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    main()
