import os
import csv
from enum import Enum, auto


class ParserException(Exception):
    pass


class CarType(Enum):
    car = auto()
    truck = auto()
    spec_machine = auto()


class Header(Enum):
    car_type = 0
    brand = 1
    passenger_seats_count = 2
    photo_file_name = 3
    body_whl = 4
    carrying = 5
    extra = 6


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        _, ext = os.path.splitext(self.photo_file_name)
        return ext

    @property
    def car_type(self):
        raise NotImplementedError


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)

    @CarBase.car_type.getter
    def car_type(self):
        return CarType.car.name

    def __repr__(self):
        return f"Car ({self.car_type}, {self.brand}, {self.photo_file_name}, {self.carrying}, " \
               f"{self.passenger_seats_count})"


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        if body_whl == "":
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0
        else:
            dimension_strings = body_whl.split("x")
            if len(dimension_strings) != 3:
                raise ParserException("Body whl components invalid")
            self.body_length = float(dimension_strings[0])
            self.body_width = float(dimension_strings[1])
            self.body_height = float(dimension_strings[2])

    @CarBase.car_type.getter
    def car_type(self):
        return CarType.truck.name

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height

    def __repr__(self):
        return f"Truck ({self.car_type}, {self.brand}, {self.photo_file_name}, {self.carrying}, " \
               f"{self.body_length}, {self.body_width}, {self.body_height}, {self.get_body_volume()})"


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    @CarBase.car_type.getter
    def car_type(self):
        return CarType.spec_machine.name

    def __repr__(self):
        return f"SpecMachine ({self.car_type}, {self.brand}, {self.photo_file_name}, {self.carrying}, {self.extra})"


class CarParser:
    # headers = [e.name for e in Header]
    # header_to_index_dict = {key: value for (key, value) in enumerate(headers)}

    @staticmethod
    def parse_car_object(columns):
        if len(columns) < len(Header):
            raise ParserException("Too few columns")

        type_to_parsing_func = {
            CarType.car.name: CarParser.parse_car,
            CarType.truck.name: CarParser.parse_truck,
            CarType.spec_machine.name: CarParser.parse_spec,
        }

        try:
            parsing_func = type_to_parsing_func[columns[0]]
            car_obj = parsing_func(columns)
            return car_obj
        except KeyError:
            raise ParserException

    @staticmethod
    def parse_car(columns):
        brand = columns[Header.brand.value]
        photo_file_name = columns[Header.photo_file_name.value]
        carrying = columns[Header.carrying.value]
        passenger_seats_count = columns[Header.passenger_seats_count.value]
        return Car(brand, photo_file_name, carrying, passenger_seats_count)

    @staticmethod
    def parse_truck(columns):
        brand = columns[Header.brand.value]
        photo_file_name = columns[Header.photo_file_name.value]
        carrying = columns[Header.carrying.value]
        body_whl = columns[Header.body_whl.value]
        return Truck(brand, photo_file_name, carrying, body_whl)

    @staticmethod
    def parse_spec(columns):
        brand = columns[Header.brand.value]
        photo_file_name = columns[Header.photo_file_name.value]
        carrying = columns[Header.carrying.value]
        extra = columns[Header.extra.value]
        return SpecMachine(brand, photo_file_name, carrying, extra)


def get_car_list(csv_filename):
    # for e in Header:
    #    print(int(e.value), e.name)

    # print(CarParser.headers)
    # print(CarParser.header_to_index_dict)

    car_list = []

    try:
        with open(csv_filename) as csv_fd:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)  # пропускаем заголовок
            for row in reader:
                car_parser = CarParser()
                try:
                    car_obj = car_parser.parse_car_object(row)
                    car_list.append(car_obj)
                except ParserException as err:
                    # print("ParserException ", err)
                    pass
    except IOError:
        pass

    return car_list


cars = get_car_list("cars.csv")
print(cars)
ext_list = list(map(lambda x: x.get_photo_file_ext(), cars))
print(ext_list)
