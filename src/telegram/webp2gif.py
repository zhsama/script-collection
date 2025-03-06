import argparse
import logging
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from multiprocessing import cpu_count
from pathlib import Path

import cv2
import numpy as np
import psutil
from PIL import Image
from tqdm import tqdm


def setup_logging():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'webp_to_gif_conversion_{timestamp}.log'

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def create_output_dir(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        logging.info(f"创建输出目录: {output_path}")


def get_optimal_workers():
    """获取最优的工作进程数"""
    cpu_cores = cpu_count()
    memory = psutil.virtual_memory()
    # 根据可用内存和CPU核心数计算合适的工作进程数
    memory_based_workers = max(1, int(memory.available / (2 * 1024 * 1024 * 1024)))  # 每个进程预留2GB内存
    return min(cpu_cores, memory_based_workers, 16)  # 最大限制16个进程


def convert_single_file(args):
    """单个文件转换函数"""
    input_path, output_path, quality, optimize, max_colors, fps, max_width = args
    try:
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise Exception("无法打开文件")

        frames = []
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # 使用用户指定的fps，如果未指定则使用原始fps
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        actual_fps = fps if fps > 0 else original_fps
        duration = int(1000 / actual_fps) if actual_fps > 0 else 50

        # 添加帧采样逻辑
        frame_index = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 缩放图像到合适尺寸
            height, width = frame.shape[:2]
            if width > max_width:  # 使用配置的最大宽度
                scale = max_width / width
                new_width = max_width
                new_height = int(height * scale)
                frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

            # 转换颜色空间并减少色彩
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)

            # 减少颜色数量
            pil_image = pil_image.quantize(colors=max_colors, method=2).convert('RGB')

            frames.append(pil_image)
            frame_index += 1

        cap.release()

        if not frames:
            img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
            if img is None:
                raise Exception("无法读取图像")

            if img.shape[-1] == 4:
                bgr = img[:, :, :3]
                alpha = img[:, :, 3]
                white_background = np.ones_like(bgr) * 255
                alpha_3d = np.stack((alpha,) * 3, axis=-1) / 255.0
                final_img = (bgr * alpha_3d + white_background * (1 - alpha_3d)).astype(np.uint8)
            else:
                final_img = img

            rgb_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)
            frames = [Image.fromarray(rgb_img)]

        if len(frames) > 1:
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0,
                optimize=optimize,
                quality=quality,
                colors=max_colors,
                disposal=2  # 添加disposal参数优化帧处理方式
            )
        else:
            frames[0].save(output_path, 'GIF')

        return True, input_path, None
    except Exception as e:
        return False, input_path, str(e)


def batch_convert(input_dir, output_dir, quality=80, optimize=False, max_colors=256, fps=0, max_width=800):
    """批量转换目录中的所有WEBP文件"""
    logger = setup_logging()
    create_output_dir(output_dir)

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
        conversion_args.append((
            str(webp_file),
            str(output_file),
            quality,
            optimize,
            max_colors,
            fps,
            max_width
        ))

    # 获取最优的工作进程数
    workers = get_optimal_workers()
    logger.info(f"使用 {workers} 个工作进程进行并行转换")

    # 使用进程池进行并行处理
    success_count = 0
    failed_count = 0

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(convert_single_file, args) for args in conversion_args]

        with tqdm(total=total_files, desc="转换进度") as pbar:
            for future in as_completed(futures):
                success, input_path, error = future.result()
                if success:
                    success_count += 1
                else:
                    failed_count += 1
                    with open('failed_conversions.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{input_path}\t{error}\n")

                pbar.set_postfix({
                    "成功": success_count,
                    "失败": failed_count,
                    "当前进度": f"{((success_count + failed_count) / total_files) * 100:.1f}%"
                })
                pbar.update(1)

    logger.info("转换完成！统计信息：")
    logger.info(f"总文件数: {total_files}")
    logger.info(f"成功转换: {success_count}")
    logger.info(f"转换失败: {failed_count}")


def get_user_input(prompt, default_value, validator=None, value_type=str):
    """获取用户输入，支持默认值"""
    while True:
        user_input = input(f"{prompt} (默认: {default_value}): ").strip()
        if not user_input:  # 用户直接回车
            return default_value

        try:
            value = value_type(user_input)
            if validator and not validator(value):
                raise ValueError
            return value
        except ValueError:
            print("输入无效，请重试")


def parse_arguments():
    """解析命令行参数，支持交互式输入"""
    parser = argparse.ArgumentParser(description='将WEBP文件转换为GIF格式')
    parser.add_argument('--input', '-i', default=None,
                        help='输入目录路径，包含WEBP文件 (默认: ./webp)')
    parser.add_argument('--output', '-o', default=None,
                        help='输出目录路径，存放转换后的GIF文件 (默认: ./gif)')
    parser.add_argument('--quality', '-q', type=int, default=None,
                        help='GIF质量 (1-100, 默认: 80)')
    parser.add_argument('--optimize', '-opt', action='store_true',
                        help='是否优化GIF文件大小')
    parser.add_argument('--max-colors', '-c', type=int, default=None,
                        help='GIF调色板最大颜色数 (2-256, 默认: 256)')
    parser.add_argument('--fps', '-f', type=float, default=None,
                        help='指定GIF帧率，0表示使用原始帧率 (默认: 0)')
    parser.add_argument('--max-width', '-w', type=int, default=None,
                        help='GIF最大宽度，超过会等比例缩放 (默认: 800)')

    args = parser.parse_args()

    # 如果没有通过命令行指定参数，则提示用户输入
    print("\n请设置转换参数（直接回车使用默认值）：")

    if args.input is None:
        args.input = get_user_input("输入目录路径", "./webp")

    if args.output is None:
        args.output = get_user_input("输出目录路径", "./gif")

    if args.quality is None:
        args.quality = get_user_input(
            "GIF质量 (1-100)",
            80,
            lambda x: 1 <= x <= 100,
            int
        )

    if args.max_colors is None:
        args.max_colors = get_user_input(
            "最大颜色数 (2-256)",
            256,
            lambda x: 2 <= x <= 256,
            int
        )

    if args.fps is None:
        args.fps = get_user_input(
            "帧率 (0表示使用原始帧率)",
            0,
            lambda x: x >= 0,
            float
        )

    if args.max_width is None:
        args.max_width = get_user_input(
            "最大图片宽度 (像素)",
            800,
            lambda x: x > 0,
            int
        )

    if not args.optimize:
        optimize_input = get_user_input(
            "是否优化GIF文件大小 (y/n)",
            "n"
        ).lower()
        args.optimize = optimize_input.startswith('y')

    # 参数验证
    if not 1 <= args.quality <= 100:
        parser.error('质量参数必须在1到100之间')
    if not 2 <= args.max_colors <= 256:
        parser.error('最大颜色数必须在2到256之间')
    if args.fps < 0:
        parser.error('帧率必须大于或等于0')

    return args


if __name__ == "__main__":
    args = parse_arguments()

    # 记录开始时间
    start_time = datetime.now()
    print(f"开始转换WEBP文件到GIF... 开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"转换参数:")
    print(f"- 输入目录: {args.input}")
    print(f"- 输出目录: {args.output}")
    print(f"- 图片质量: {args.quality}")
    print(f"- 优化启用: {args.optimize}")
    print(f"- 最大颜色: {args.max_colors}")
    print(f"- 帧率设置: {args.fps if args.fps > 0 else '使用原始帧率'}")
    print(f"- 最大宽度: {args.max_width}像素")

    batch_convert(args.input, args.output,
                  quality=args.quality,
                  optimize=args.optimize,
                  max_colors=args.max_colors,
                  fps=args.fps,
                  max_width=args.max_width)

    # 记录结束时间和总耗时
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"\n转换完成！")
    print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {duration}")
