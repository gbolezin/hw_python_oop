class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> None:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    # default step lenght
    LEN_STEP = 0.65
    # coeff for converting meters -> kilometers
    M_IN_KM = 1000
    # const seconds in hour
    MINUTES = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight
        self.training_type: str = ''

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        Training.__init__(self, action, duration, weight)
        self.training_type: str = 'Running'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.MINUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_WEIGHT_SHIFT = 0.029
    CALORIES_KMS_IN_MS = 0.278
    CALORIES_CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        Training.__init__(self, action, duration, weight)
        self.training_type: str = 'SportsWalking'
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        return (
            ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
              + ((self.get_mean_speed() * self.CALORIES_KMS_IN_MS)**2
                 / (self.height / self.CALORIES_CM_IN_M))
              * self.CALORIES_WEIGHT_SHIFT * self.weight)
                * self.duration * self.MINUTES)
        )


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    # default step lenght
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        Training.__init__(self, action, duration, weight)
        self.training_type: str = 'Swimming'
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    training = None
    if workout_type in training_types:
        training: Training = training_types[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    # if training:
    info = training.show_training_info()
    print(info.get_message())
    # else:
    #    print('Ошибка при определении типа тренировки')


if __name__ == '__main__':
    # SWM - count of steps, duration in hours, weight, length_pool, count_pool
    # RUN - count of steps, duration in hours, weight
    # WLK - count of steps, duration in hours, weight, height
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
