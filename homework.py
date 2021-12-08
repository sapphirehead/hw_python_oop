from typing import List, Dict, Type, Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    TRAINING_MESSAGE: str = ("Тип тренировки: {type}; "
                             "Длительность: {duration:.3f} ч.; "
                             "Дистанция: {distance:.3f} км; "
                             "Ср. скорость: {speed:.3f} км/ч; "
                             "Потрачено ккал: {calories:.3f}.")

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вывод сообщений о тренировке на экран"""
        return self.TRAINING_MESSAGE.format(type=self.training_type,
                                            duration=self.duration,
                                            distance=self.distance,
                                            speed=self.speed,
                                            calories=self.calories)


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    HOUR_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f"Определите get_spent_calories в {self.__class__.__name__}.")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALOR_1: int = 18
    COEFF_CALOR_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALOR_1
                * self.get_mean_speed()
                - self.COEFF_CALOR_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.HOUR_IN_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALOR_3: float = 0.035
    COEFF_CALOR_4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALOR_3 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALOR_4 * self.weight)
                * (self.duration * self.HOUR_IN_MIN))


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_CALOR_5: float = 1.1
    COEFF_CALOR_6: float = 2.0
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_CALOR_5)
                * self.COEFF_CALOR_6 * self.weight)


def read_package(workout_type: str, data: List[int]) -> Union[Swimming,
                                                              Running,
                                                              SportsWalking]:
    """Прочитать данные полученные от датчиков."""
    classes_types: Dict[str, Type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in classes_types.keys():
        raise KeyError("Неизвестный тип тренировки")

    return classes_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
