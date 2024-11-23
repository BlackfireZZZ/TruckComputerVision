import cv2
import os


def extract_frames_by_frequency(video_path, frequency, root_output_dir):
    """
    Извлекает кадры из видео с заданной частотой и сохраняет их как изображения.

    :param video_path: Путь к видеофайлу.
    :param frequency: Частота извлечения кадров в секундах.
    :param root_output_dir: Директория для сохранения изображений.
    """
    # Открываем видеофайл
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Не удалось открыть видеофайл: {video_path}")
        return

    # Получаем частоту кадров (FPS)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Не удалось определить FPS видео.")
        cap.release()
        return

    # Расчет временных меток кадров, которые нужно извлечь
    video_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    elapsed_times = [i for i in range(0, int(video_duration), frequency)]

    # Проходим по каждому времени и извлекаем кадр
    for elapsed_time in elapsed_times:
        output_dir = (root_output_directory + '/related_images/' + root_output_dir + '-' + str(elapsed_time // frequency)
                      + '_pcd')
        # Рассчитываем целевой кадр
        frame_number = int(elapsed_time * fps)

        # Переходим к нужному кадру
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # Читаем кадр
        ret, frame = cap.read()
        if not ret:
            print(f"Не удалось извлечь кадр на времени {elapsed_time} сек.")
            continue

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Формируем имя для файла
        output_path = output_dir + '/' + root_output_dir + '-' + str(elapsed_time // frequency) + '.jpg'

        # Сохраняем кадр в формате JPG
        cv2.imwrite(output_path, frame)
        print(f"Кадр на {elapsed_time} сек. успешно сохранен: {output_path}")

    # Освобождаем ресурсы
    cap.release()


# Пример использования
video_file = "input_mp4/run-3.mp4"  # Путь к видеофайлу
frequency = 2  # Частота извлечения кадров в секундах (например, каждые 2 секунды)
root_output_directory = "run-3"  # Директория для сохранения изображений

extract_frames_by_frequency(video_file, frequency, root_output_directory)
