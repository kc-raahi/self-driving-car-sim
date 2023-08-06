from car import Car


def test_outline():
    car = Car(100, 0, None, False)
    print(car.get_outline())