class Calculator:
    """Простой калькулятор с базовыми арифметическими операциями"""

    def adding(self, x, y):
        return x + y

    def subtraction(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def division(self, x, y):
        if y == 0:
            raise ValueError("Деление на ноль невозможно")
        return x / y
