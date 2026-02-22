class BankAccount:
    def __init__(self) -> None:
        self.__balance = 0
    
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Negative deposit is not allowed")
        
        self.__balance += amount
        
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Negative amount cannot be withdrawn")
        
        if amount > self.__balance:
            raise ValueError("You do not have enough balance to withdraw")
        
        self.__balance -= amount
        
    def get_balance(self) -> float:
        return self.__balance
    
    def transfer(self, amount: float, other: 'BankAccount') -> None:
        if not isinstance(other, BankAccount):
            raise TypeError
        self.withdraw(amount)
        other.deposit(amount)
    
    def __str__(self) -> str:
        return f"Account[balance=${self.__balance:.2f}]"
    
    def __eq__(self, other: 'BankAccount') -> bool:
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.__balance == other.get_balance()
    
if __name__ == "__main__":
    acc1 = BankAccount()
    acc2 = BankAccount()

    acc1.deposit(500)
    acc1.withdraw(200)
    
    print(acc1)
    
    acc1.transfer(100, acc2)
    
    print(acc1)
    print(acc2)
    
    # Notes:
    # 1. Do not have print statements in class methods! A method that moves money shouldn't also be deciding how to communicate that to the user. In real systems these would be log statements at most, and the UI layer handles user-facing messages.
    # 2. How to decide when to use ValueError & NotImplementedError? 
    # # ValueError — use when the data itself is wrong but the type is what you expected. 
    # # TypeError — use when the type itself is wrong. The caller passed something that is fundamentally the wrong kind of thing.
    # # NotImplemented (not an exception — a special return value) — this one is completely different from the other two and only belongs in dunder comparison methods like __eq__, __lt__, __gt__. You return it, never raise it. It's a signal to Python's runtime saying "I don't know how to compare myself with this type — ask the other object if it knows how."