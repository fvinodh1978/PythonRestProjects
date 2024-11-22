import pytest
from CrossCheck.src.calculator import (
    summation,
    subtraction,
    multiplication,
    division
)

class TestMe:
    """A class to test basic math operations."""
    def test_summation(self):
        """
        Testing Summation function
        """
        for i in range(10):
            print("Vinodh")

        assert summation(2, 10) == 12
        assert summation(3, 5) == 8
        assert summation(4, 6) == 10


    def test_summation1(self):
        """
        Testing Summation function

        """
        for i in range(10):
            print("Vinodh")

        assert summation(2, 10) == 12
        assert summation(3, 5) == 8
        assert summation(4, 6) == 10


    def test_subtraction(self):
        """
        Testing Subtraction function
        """
        assert subtraction(8, 2) == 6
        assert subtraction(7, 5) == 2
        assert subtraction(4, 2) == 2


    def test_multiplication(self):
        """
        Testing Multiplication function
        """
        assert multiplication(2, 2) == 4
        assert multiplication(7, 2) == 14
        assert multiplication(10, 2) == 20


    def test_Division(self):
        """
        Testing Division function
        """
        assert division(5, 5) == 1
        assert division(70, 10) == 7
        assert division(16, 4) == 4
