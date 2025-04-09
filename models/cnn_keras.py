from keras.models import load_model
import cv2
import numpy as np


class StancesKerasClassify:
    def __init__(self, filename):
        self.model = load_model(filename)
        self.image = None
        self.prediction = None

    @staticmethod
    def _img_resize(np_image: np.array, target_height=256, target_width=256, channels=3) -> np.array:
        # Получаем текущие размеры изображения
        print(f'исходное {np_image.shape}')
        current_height, current_width, current_channels = np_image.shape
        # ресайз входного изображения чтобы размеры не привышали максимальных
        if current_height > target_height or current_width > target_width:
            scale = min(target_width / current_width, target_height / current_height)
            np_image = cv2.resize(np_image, (int(scale * current_width), int(scale * current_height)))
            current_height, current_width, current_channels = np_image.shape
            print(f'измененный размер {np_image.shape}')

        # Создаем пустой массив требуемой формы, заполненный нулями
        resized_image = np.zeros((target_height, target_width, channels), dtype=np_image.dtype)
        # Вычисляем координаты для размещения исходного изображения в центре целевого
        y_offset = max((target_height - current_height) // 2, 0)
        x_offset = max((target_width - current_width) // 2, 0)
        # Определяем границы для обрезки или вставки изображения
        y_start = y_offset
        x_start = x_offset
        y_end = y_offset + min(current_height, target_height)
        x_end = x_offset + min(current_width, target_width)
        # Определяем границы исходного изображения для копирования
        src_y_start = max(0, (current_height - target_height) // 2)
        src_x_start = max(0, (current_width - target_width) // 2)
        src_y_end = src_y_start + (y_end - y_start)
        src_x_end = src_x_start + (x_end - x_start)
        # Копируем данные из исходного изображения в новый массив
        resized_image[y_start:y_end, x_start:x_end] = np_image[src_y_start:src_y_end, src_x_start:src_x_end]

        return resized_image

    def classify(self, np_image: np.array, conf_threshold=0.5, show=False) -> dict:
        if np_image is not None:
            # изменение размера для соответствия входному слою
            self.image = self._img_resize(np_image)
            if show:
                cv2.imshow('', self.image)
                cv2.waitKey(0)
            # добавление дополнительной оси для соответствия входному слою
            self.image = np.expand_dims(self.image, axis=0)
            # проводим классификацию
            self.prediction = self.model.predict(self.image)
            predicted_class = np.argmax(self.prediction, axis=1).item()  # Индексы классов
            predicted_probabilities = np.max(self.prediction, axis=1).item()  # Вероятности для предсказанных классов

            return {'class': predicted_class,
                    'prob': predicted_probabilities if predicted_probabilities >= conf_threshold else 0}


if __name__ == '__main__':
    classify_model = StancesKerasClassify('best_model.keras')
    image = cv2.imread('l-kokutsu-dachi_000003.jpg')
    result = classify_model.classify(image)
    print(result)
