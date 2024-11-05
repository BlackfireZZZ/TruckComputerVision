import pandas as pd


def csv_to_pcd(csv_file_path, pcd_file_path):
    # Чтение данных из csv файла, игнорируя все, кроме столбцов X, Y, Z
    df = pd.read_csv(csv_file_path, usecols=['X', 'Y', 'Z'])

    # Определение количества точек
    num_points = len(df)

    # Создание PCD файла
    with open(pcd_file_path, 'w') as f:
        # Запись заголовка PCD файла
        f.write("# .PCD v0.7 - Point Cloud Data file format\n")
        f.write("VERSION 0.7\n")
        f.write("FIELDS x y z\n")
        f.write("SIZE 4 4 4\n")
        f.write("TYPE F F F\n")
        f.write("COUNT 1 1 1\n")
        f.write(f"WIDTH {num_points}\n")
        f.write("HEIGHT 1\n")
        f.write("VIEWPOINT 0 0 0 1 0 0 0\n")
        f.write(f"POINTS {num_points}\n")
        f.write("DATA ascii\n")

        # Запись точек в формате X Y Z
        for _, row in df.iterrows():
            f.write(f"{row['X']} {row['Y']} {row['Z']}\n")


# Пути к файлам
csv_path = 'Points_2024-11-05_20-30-16.csv'
pcd_path = f'output_{csv_path[:-4]}.pcd'

# Создание PCD файла с RGB и дополнительными полями
csv_to_pcd(csv_path, pcd_path)
