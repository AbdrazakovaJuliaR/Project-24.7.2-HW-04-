import pytest
from app.calc import Calculator

class TestCalc:
    def setup_method(self):
        """Создает объект калькулятора перед каждым тестом"""
        self.calc = Calculator()

    # Тесты для сложения
    def test_adding_success(self):
        """Позитивный тест: проверка сложения"""
        assert self.calc.adding(7, 3) == 10

    # дополнительный тест
    def test_adding_zero(self):
        """Позитивный тест: сложение с нулем"""
        assert self.calc.adding(0, 5) == 5

    # Тесты для вычитания
    def test_subtraction_success(self):
        """Позитивный тест: проверка вычитания"""
        assert self.calc.subtraction(15, 5) == 10

    def test_subtraction_negative_result(self):
        """Позитивный тест: вычитание, дающее отрицательный результат"""
        assert self.calc.subtraction(3, 10) == -7

    # Тесты для умножения
    def test_multiply_success(self):
        """Позитивный тест: проверка умножения"""
        assert self.calc.multiply(6, 2) == 12

    def test_multiply_by_one(self):
        """Позитивный тест: умножение на 1"""
        assert self.calc.multiply(9, 1) == 9

    # Тесты для деления
    def test_division_success(self):
        """Позитивный тест: проверка деления"""
        assert self.calc.division(20, 4) == 5

    def test_division_by_one(self):
        """Позитивный тест: деление на 1"""
        assert self.calc.division(12, 1) == 12

    def teardown_method(self):
        """Вызывается после каждого теста"""
        print("Тест завершён")
