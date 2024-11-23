from mcap.reader import make_reader
from mcap_ros2.decoder import DecoderFactory
from timestamp import get_timestamp
import numpy as np


# Описание структуры данных
dtype = np.dtype(
    [
        ("x", "float32"),
        ("y", "float32"),
        ("z", "float32"),
        ("intensity", "float32"),
        ("tag", "uint8"),
        ("line", "uint8"),
        ("timestamp", "float64"),
    ],
    align=False,
)


def save_pcd_manual(points, filename):
    """
    Сохраняет точки в формате PCD вручную.
    """
    xyz = np.stack((points["x"], points["y"], points["z"]), axis=-1)
    header = f"""# .PCD v0.7 - Point Cloud Data file format
        VERSION 0.7
        FIELDS x y z
        SIZE 4 4 4
        TYPE F F F
        COUNT 1 1 1
        WIDTH {xyz.shape[0]}
        HEIGHT 1
        VIEWPOINT 0 0 0 1 0 0 0
        POINTS {xyz.shape[0]}
        DATA ascii
        """
    with open(filename, "w") as f:
        f.write(header)
        np.savetxt(f, xyz, fmt="%.6f %.6f %.6f")

    print(f"Saved {xyz.shape[0]} points to {filename}")


def find_and_save_points_by_time(input_file, output_file, target_time, epsilon=1e-1):
    """
    Ищет и сохраняет облако точек для указанного времени.

    Args:
        input_file (str): Путь к файлу MCAP.
        output_file (str): Путь для сохранения PCD.
        target_time (float): Целевой timestamp (UNIX time).
        epsilon (float): Допустимое отклонение в секундах.
    """
    with open(input_file, "rb") as inp_file:
        reader = make_reader(inp_file, decoder_factories=[DecoderFactory()])
        found = False
        for schema, channel, message, ros_msg in reader.iter_decoded_messages(
                topics=["/livox/lidar"]
        ):
            timestamp = message.log_time / 1e9  # Преобразуем в секунды

            # Увеличенный диапазон проверки
            if abs(timestamp - target_time) <= epsilon:
                print(f"Target timestamp {target_time:.6f} found! Saving points.")
                points = np.frombuffer(ros_msg.data, dtype=dtype)
                save_pcd_manual(points, output_file)
                found = True
                break

        if not found:
            print(f"Timestamp {target_time} not found in the file.")


# Задаем параметры
input_mcap_file = "input_mcap/run-3.mcap"
start_time = "2024-11-17 4:33:42.475 PM"

for i in range(82):
    output_pcd_file = "run-3/pointcloud/" + "run-3-" + str(i) + ".pcd"
    elapsed_time = i * 2
    target_timestamp = get_timestamp(start_time, elapsed_time)
    # Вызов функции
    find_and_save_points_by_time(input_mcap_file, output_pcd_file, target_timestamp)



