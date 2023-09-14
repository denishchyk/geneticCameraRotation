
import cv2
import numpy as np

def calculate_rotation_angle(old, yang, matches):
    """
    Функция для вычисления угла поворота между двумя кадрами.

    Аргументы:

    Возвращает:
    Угол поворота между кадрами в градусах.
    """

    keypoints_old = [ch.KeyPoint for ch in old]
    keypoints_yang = [ch.KeyPoint for ch in yang]

    # Фильтрация матчей по расстоянию
    matches = sorted(matches, key=lambda x: x[0].distance)
    good_matches = matches[:int(len(matches) * 0.1)]  # Выбор лучших 10% матчей

    # Оценка матрицы трансформации
    src_pts = np.float32([keypoints_old[match[0].queryIdx].pt for match in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints_yang[match[0].trainIdx].pt for match in good_matches]).reshape(-1, 1, 2)

    # Вычисление матрицы гомографии
    M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Извлечение угла поворота из матрицы гомографии

    rotation_angle_rad = np.arctan2(M[1, 0], M[0, 0]) if M is not None else 1

    rotation_angle_deg = np.degrees(rotation_angle_rad)
    return rotation_angle_deg