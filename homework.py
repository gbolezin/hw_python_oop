# импорт библиотеки dataclasses
from dataclasses import dataclass
import dataclasses


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    # формат сообщения о тренировке
    MESSAGE_FORMAT = (
        'Тип тренировки: {training_type:}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возвращает информацию о тренировке."""
        return self.MESSAGE_FORMAT.format(**dataclasses.asdict(self))


class Training:
    """Базовый класс тренировки."""
    # длина шага по-умолчанию
    LEN_STEP = 0.65
    # коэффициент для перевода метров в километры
    M_IN_KM = 1000.0
    # количество минут в часе
    MINUTES_IN_HOUR = 60.0

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:

        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Функция get_spent_calories() '
            f'должна быть реализована '
            f'в дочерних классах {type(self).__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    # коэффициент средней скорости для вычисления потраченных калорий
    CALORIES_MEAN_SPEED_MULTIPLIER = 18.0
    # еще один коэффициент средней скорости для вычисления потраченных калорий
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:

        Training.__init__(self, action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM * self.duration
            * self.MINUTES_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # коэффициент средней скорости для вычисления потраченных калорий
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    # коэффициент веса для вычисления потраченных калорий
    CALORIES_WEIGHT_SHIFT = 0.029
    # коэффициент для перевода км/с в м/с
    CALORIES_KMS_IN_MS = 0.278
    # коэффициент для перевода сантиметров в метры
    CALORIES_CM_IN_M = 100.0

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float
    ) -> None:

        Training.__init__(self, action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        return (
            (
                (
                    self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                    + (
                        (self.get_mean_speed() * self.CALORIES_KMS_IN_MS)**2
                        / (
                            self.height / self.CALORIES_CM_IN_M
                        )
                    )
                    * self.CALORIES_WEIGHT_SHIFT * self.weight
                )
                * self.duration * self.MINUTES_IN_HOUR
            )
        )


class Swimming(Training):
    """Тренировка: плавание."""
    # коэффициент веса для вычисления потраченных калорий
    CALORIES_WEIGHT_MULTIPLIER = 2.0
    # коэффициент средней скорости для вычисления потраченных калорий
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    # длина шага (гребка) по-умолчанию для класса Swimming
    LEN_STEP = 1.38

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float
    ) -> None:

        Training.__init__(self, action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight * self.duration
        )


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_types:
        # получить доступные типы тренировок
        available_training_types = ', '.join(training_types.keys())
        raise ValueError(
            f'''Ошибка данных - неизвестный тип тренировки "{workout_type}".
            Возможные следующие типы тренировок: {available_training_types}'''
        )
    else:
        return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    # SWM - к-во гребков, длит-ть в часах, вес кг,
    #       длина бассейна в м, к-во "проплывов" бассейна
    # RUN - к-во шагов, длит-ть в часах, вес кг
    # WLK - к-во шагов, длит-ть в часах, вес кг, рост в см
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
