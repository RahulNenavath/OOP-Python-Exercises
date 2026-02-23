from abc import ABC, abstractmethod
from math import sqrt, pi

class Shape(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    @abstractmethod
    def describe(self) -> str:
        pass
    
    def is_larger_than(self, other: 'Shape') -> bool:
        if not isinstance(other, Shape):
            raise TypeError(f"{other} is not a shape")
        return self.area() > other.area()
    
    def _validate_number(self, number: float, min_val: float, max_value: float) -> None:
        if not isinstance(number, (int, float)):
            raise TypeError(f"{number} is not a number")
        if not (min_val < number < max_value):
            raise ValueError(f'{number} is not valid value')
        return None
    
    def __gt__(self, other: 'Shape') -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() > other.area()
    
    def __lt__(self, other: 'Shape') -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() < other.area()
    
    def __eq__(self, other: 'Shape') -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() == other.area()
    
    def __repr__(self) -> str:
        return self.describe()
        
    
class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self._validate_number(number=radius, min_val=0, max_value=float('inf'))
        self.__radius = float(radius)
    
    def area(self) -> float:
        return pi * (self.__radius**2)
    
    def perimeter(self) -> float:
        return 2 * pi * self.__radius
    
    def radius(self) -> float:
        return self.__radius
    
    def describe(self) -> str:
        return f'Circle with radius: {self.__radius}, area: {self.area()}, perimeter: {self.perimeter()}'


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self._validate_number(number=width, min_val=0, max_value=float('inf'))
        self._validate_number(number=height, min_val=0, max_value=float('inf'))
        self.__width = float(width)
        self.__height = float(height)
        
    def area(self) -> float:
        return self.__width * self.__height
    
    def perimeter(self) -> float:
        return 2 * (self.__width + self.__height)
    
    def describe(self) -> str:
        return f"Rectangle with width: {self.__width}, height: {self.__height}, area: {self.area()}, perimeter: {self.perimeter()}"
        

class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float) -> None:
        self._validate_number(number=a, min_val=0, max_value=float('inf'))
        self._validate_number(number=b, min_val=0, max_value=float('inf'))
        self._validate_number(number=c, min_val=0, max_value=float('inf'))
        
        self.__a = float(a)
        self.__b = float(b)
        self.__c = float(c)
        
        self.__s = (self.__a + self.__b + self.__c) * 0.5
        self.__s_a = self.__s - self.__a
        self.__s_b = self.__s - self.__b
        self.__s_c = self.__s - self.__c
        
        self.__area = sqrt(self.__s * self.__s_a * self.__s_b * self.__s_c)
        
    def area(self) -> float:
        return self.__area
    
    def perimeter(self) -> float:
        return self.__a + self.__b + self.__c
    
    def describe(self) -> str:
        return f"Triangle with sides ({self.__a}, {self.__b}, {self.__c})"

class RightTriangle(Triangle):
    def __init__(self, base: float, height: float) -> None:
        super().__init__(a = base, b = height, c = sqrt((base ** 2) + (height ** 2)))
        self.__base = base
        self.__height = height
    
    def describe(self) -> str:
        return f"Right Triangle with sides ({self.__base}, {self.__height})"
    
    
def largest_shape(shapes: list[Shape]) -> Shape:
    return max(shapes, key=lambda x: x.area())
    
def total_area(shapes: list[Shape]) -> float:
    curr_total: float = 0.0
    for shape in shapes:
        curr_total += shape.area()
    return curr_total

def shapes_larger_than(threshold: float, shapes: list[Shape]) -> list[Shape]:
    filtered_shapes = [i for i in shapes if i.area() > threshold]
    return filtered_shapes
    

if __name__ == "__main__":
    shapes = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 4, 5),
        RightTriangle(3, 4)
    ]
    print(total_area(shapes))
    print(largest_shape(shapes))
    print(shapes_larger_than(20, shapes))
    
    c = Circle(10)
    r = Rectangle(4, 6)
    print(c.is_larger_than(r))