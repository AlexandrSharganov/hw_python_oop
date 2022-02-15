from dataclasses import dataclass
from typing import Dict, List, Union, Optional


@dataclass(repr=False, eq=False)
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        text_message: str = (f'Тип тренировки: {self.training_type}; '
                             f'Длительность: {self.duration:.3f} ч.; '
                             f'Дистанция: {self.distance:.3f} км; '
                             f'Ср. скорость: {self.speed:.3f} км/ч; '
                             f'Потрачено ккал: {self.calories:.3f}.')
        return text_message


@dataclass(repr=False, eq=False)
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES_IN_HOUR = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Определите run в {type(self).__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass(repr=False, eq=False)
class Running(Training):
    """Тренировка: бег."""

    CALORIES_SPEED_MULTIPLIER = 18
    CALORIES_SPEED_SUBTRACT = 20

    def get_spent_calories(self):
        return ((self.CALORIES_SPEED_MULTIPLIER
                * self.get_mean_speed() - self.CALORIES_SPEED_SUBTRACT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MINUTES_IN_HOUR))


@dataclass(repr=False, eq=False)
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_POWER = 2
    CALORIES_WEIGHT_COEFF = 0.029

    def get_spent_calories(self):
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed()**self.CALORIES_SPEED_POWER)
                 // self.height)
                * self.CALORIES_WEIGHT_COEFF * self.weight)
                * self.duration * self.MINUTES_IN_HOUR)


@dataclass(repr=False, eq=False)
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: float

    LEN_STEP = 1.38
    CALORIES_SPEED_MULTIPLIER = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / (self.duration))

    def get_spent_calories(self):
        return ((self.get_mean_speed()
                + self.CALORIES_SPEED_MULTIPLIER)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight)


def read_package(workout_type: str,
                 data: List[Union[int, float]]) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    dictionary: Dict[Union[str, Training]] = {'SWM': Swimming,
                                              'RUN': Running,
                                              'WLK': SportsWalking}
    traning_type: Optional[Training] = dictionary.get(workout_type)
    if traning_type is not None:
        return traning_type(*data)
    elif traning_type is None:
        return traning_type


def main(training: Training) -> None:
    """Главная функция."""
    if training is not None:
        info: Training = training.show_training_info()
        print(info.get_message())
    elif training is None:
        print('Ошибка!Такого типа тренировки не существует!')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('SMTH', [9, 1, 90, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
