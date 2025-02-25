import os
import shutil

from config import Config
from frames_from_mp4 import extract_frames_by_frequency
from mcap_to_pcd import find_and_save_points_by_time
from timestamp import get_timestamp, get_start_time, get_frames_num

run_name = Config.run_name
# Пример использования
video_files = [
    f"input_mp4/{run_name}-0.mp4",
    f"input_mp4/{run_name}-90.mp4",
    f"input_mp4/{run_name}-180.mp4",
    f"input_mp4/{run_name}-270.mp4"
]
frequency = Config.frequency  # Частота извлечения кадров в секундах
root_output_directory = run_name  # Корневая директория для сохранения изображений

extract_frames_by_frequency(video_files, frequency, root_output_directory)

# Задаем параметры
input_mcap_file = f"input_mcap/{Config.run_name}.mcap"
input_metadate_file = f"input_mcap/{Config.run_name}_metadata.yaml"
start_time = get_start_time(input_metadate_file)
elapsed_time = Config.elapsed_time

if not os.path.exists(f"{Config.run_name}/pointcloud"):
    os.makedirs(f"{Config.run_name}/pointcloud")

root_output_dir = Config.run_name
frames_num = get_frames_num(input_metadate_file, Config.elapsed_time, Config.frequency)
for i in range(frames_num):
    output_pcd_file = root_output_dir + "/pointcloud/" + root_output_dir + "-" + str(i).zfill(3) + ".pcd"
    # Парсим начальное время и переводим в UTC
    target_timestamp = get_timestamp(start_time, elapsed_time)
    # Вызов функции
    find_and_save_points_by_time(input_mcap_file, output_pcd_file, target_timestamp)
    elapsed_time += Config.frequency


output_dir = "output_zip"
# Создание пути к архиву
archive_path = os.path.join(output_dir, run_name)
# Архивируем папку без сжатия
shutil.make_archive(archive_path, 'zip', root_dir=run_name)
# Удаляем исходную папку
shutil.rmtree(run_name)
print(f"Папка {run_name} архивирована в {output_dir}/{run_name}.zip и удалена")
