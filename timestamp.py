from datetime import datetime, timedelta


def get_timestamp(start_time_str, elapsed_time):
    # Парсим начальное время и переводим в UTC
    start_time_msk = datetime.strptime(start_time_str, "%Y-%m-%d %I:%M:%S.%f %p")
    start_time_utc = start_time_msk # MSK -> UTC

    # Вычисляем целевую временную метку в UTC
    target_time_utc = start_time_utc + timedelta(seconds=elapsed_time)

    # Конвертируем в UNIX timestamp
    target_timestamp = target_time_utc.timestamp()

    print(f"Target timestamp (UTC): {target_timestamp:.6f}")
    return target_timestamp

