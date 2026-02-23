from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name: str, employee_id: str) -> None:
        
        if not isinstance(name, str):
            raise TypeError(f'Name must be string')
        self.name = name
        
        if not isinstance(employee_id, str):
            raise TypeError(f'Employee ID must be string')
        self.employee_id = employee_id
        
        self._base_salary: float = 0
    
    @abstractmethod
    def calculate_monthly_pay(self) -> float:
        # return NotImplemented inside abstractmethod implies they might return something, 
        # which is confusing. The convention is simply pass!
        pass
    
    @abstractmethod
    def get_role(self) -> str:
        pass
    
    def generate_payslip(self) -> str:
        return f"{self.name.capitalize()}'s payslip: {self.get_role()} | Monthly Pay: ${self.calculate_monthly_pay():.2f}"
    
    
class FullTimeEmployee(Employee):
    def __init__(self, name: str, employee_id: str, base_salary: float) -> None:
        super().__init__(name=name, employee_id=employee_id)
        
        if not isinstance(base_salary, (float, int)):
            raise TypeError("Base Salary has to be a number")
        
        if base_salary <= 0:
            raise ValueError("Base Salary must be positive")
        
        self._base_salary = float(base_salary)
        self.__role = "Full-Time Employee"
    
    def calculate_monthly_pay(self) -> float:
        return self._base_salary / 12
    
    def get_role(self) -> str:
        return self.__role

class ContractEmployee(Employee):
    def __init__(
        self, name: str, 
        employee_id: str, 
        hourly_rate: float, 
        hours_worked_this_month: int
        ) -> None:
        super().__init__(name=name, employee_id=employee_id)
        
        if not isinstance(hourly_rate, (float, int)):
            raise TypeError("Hourly rate must be a number")
        
        self.__hourly_rate = float(hourly_rate)
        
        if not isinstance(hours_worked_this_month, int):
            raise TypeError("hours_worked_this_month must be a integer")
        
        if hours_worked_this_month < 0:
            raise ValueError("hours_worked_this_month must be zero or positive number")

        self.__hours_worked_this_month = hours_worked_this_month
        self.__role = "Contractor"
    
    def calculate_monthly_pay(self) -> float:
        return self.__hourly_rate * self.__hours_worked_this_month
    
    def get_role(self) -> str:
        return self.__role
        
class CommissionEmployee(Employee):
    def __init__(
        self, 
        name: str, 
        employee_id: str, 
        base_monthly_salary: float, 
        commission_rate: float,
        ) -> None:
        super().__init__(name=name, employee_id=employee_id)
        self.__role = "Commission-Based Employee"
        
        if not isinstance(base_monthly_salary, (float, int)):
            raise TypeError("base monthly salary must be a number")
        
        if base_monthly_salary <= 0:
            raise ValueError("base monthly salary must be positive")
        
        self.__base_monthly_salary = float(base_monthly_salary)
        
        if not isinstance(commission_rate, float):
            raise TypeError("commission_rate rate must be a float")
        
        self.__commission_rate = commission_rate
        self.__total_sale = 0
    
    def add_sale(self, amount: float) -> None:
        
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number")
        
        if amount <= 0:
            raise ValueError("Amount should be positive")
        
        self.__total_sale += float(amount)
    
    def calculate_monthly_pay(self) -> float:
        return self.__base_monthly_salary + (self.__total_sale * self.__commission_rate)
    
    def get_role(self) -> str:
        return self.__role
    
def run_payroll(employees: list[Employee]) -> None:
    for e in employees:
        print(e.generate_payslip())
        
if __name__ == "__main__":
    employees = [
        FullTimeEmployee("Alice", "E001", base_salary=120000),
        ContractEmployee("Bob", "E002", hourly_rate=85.0, hours_worked_this_month=160),
        CommissionEmployee("Carol", "E003", base_monthly_salary=3000, commission_rate=0.08),
        ]

    employees[2].add_sale(5000)
    employees[2].add_sale(12000)
    
    run_payroll(employees)