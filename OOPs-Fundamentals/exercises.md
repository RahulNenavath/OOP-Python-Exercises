# OOP Fundamentals — Pre-Design Patterns Mastery Exercises
**Course:** Object-Oriented Programming in Python
**Prerequisite To:** Design Patterns & Software Engineering Principles  
**Difficulty Progression:** Tier 1 (Introductory) → Tier 4 (Advanced)
**Total Exercises:** 8  

---

> **How to use this file**
> - Work through exercises **in order** — each builds on the last
> - Write your solution before looking anything up beyond Python syntax
> - Create one `.py` file per exercise: `ex1_bank_account.py`, `ex2_library.py`, etc.
> - The goal is not just correct code — it is **clean, well-reasoned code** that shows you understand *why* you made each design decision

---

## Table of Contents

| # | Exercise | Tier | Core Concepts |
|---|----------|------|---------------|
| 1 | Bank Account | Warm-Up | Classes, access modifiers, dunder methods |
| 2 | Library Book System | Warm-Up | Object relationships, protected attributes, filtering |
| 3 | Employee Payroll System | Inheritance | ABC, polymorphism, template method preview |
| 4 | Shape Area Calculator | Inheritance | ABC, polymorphism, typed collections |
| 5 | Notification System | Composition | Composition over inheritance, dependency injection preview |
| 6 | Inventory System | Composition | Dunder methods, `__iter__`, domain modeling |
| 7 | Decorator Library | Advanced | Decorators, closures, higher-order functions |
| 8 | Mini Plugin Pipeline | Capstone | Everything combined — real production thinking |

---

---

# Tier 1 — Warm Up
### *Basic Class Mechanics*

---

## Exercise 1: Bank Account

### Background
Encapsulation is one of the four pillars of OOP. In this exercise you will build a class that protects its own internal state, validates inputs, and exposes a clean public interface — exactly as production financial software does.

### Requirements

Build a `BankAccount` class that enforces the following rules:

**Attributes:**
- Balance is **private** and starts at `0`
- No direct external access to balance is permitted

**Methods:**

| Method | Behavior |
|--------|----------|
| `deposit(amount: float) -> None` | Accepts only positive amounts. Raises `ValueError` otherwise |
| `withdraw(amount: float) -> None` | Raises `ValueError` if amount is negative or exceeds current balance |
| `get_balance() -> float` | Returns the current balance |
| `transfer(amount: float, target: 'BankAccount') -> None` | Withdraws from self, deposits into target account |
| `__str__` | Returns `"Account[balance=$250.00]"` |
| `__eq__` | Two accounts are equal if their balances are equal |

### Expected Behavior

```python
acc1 = BankAccount()
acc2 = BankAccount()

acc1.deposit(500)
acc1.withdraw(200)
print(acc1)                    # Account[balance=$300.00]

acc1.transfer(100, acc2)
print(acc1)                    # Account[balance=$200.00]
print(acc2)                    # Account[balance=$100.00]

acc1.deposit(-50)              # raises ValueError
acc1.withdraw(99999)           # raises ValueError
```

### What This Tests
Class construction · private access modifiers · dunder methods · input validation · object-to-object interaction

---

## Exercise 2: Library Book System

### Background
Real systems model relationships between objects. Here you will build two classes that interact — a `Book` and a `Library` — and practice protected attributes, filtering collections, and making classes behave naturally in Python via dunder methods.

### Requirements

**`Book` class:**

| Attribute / Method | Detail |
|---|---|
| `title`, `author`, `isbn` | Public attributes |
| `_is_checked_out` | Protected attribute, starts as `False` |
| `check_out() -> None` | Marks book as checked out. Raises `RuntimeError` if already checked out |
| `return_book() -> None` | Marks book as available. Raises `RuntimeError` if not checked out |
| `__repr__` | Returns something informative, e.g. `"Book('Dune', 'Herbert', checked_out=False)"` |

**`Library` class:**

| Method | Detail |
|---|---|
| `add_book(book: Book) -> None` | Adds a book to the internal collection |
| `find_by_author(author: str) -> list[Book]` | Returns all books by that author |
| `get_available_books() -> list[Book]` | Returns only books not currently checked out |
| `__len__` | Returns total number of books in the library |

### Expected Behavior

```python
library = Library()
b1 = Book("Dune", "Frank Herbert", "978-0441013593")
b2 = Book("Foundation", "Isaac Asimov", "978-0553293357")
b3 = Book("I, Robot", "Isaac Asimov", "978-0553294385")

library.add_book(b1)
library.add_book(b2)
library.add_book(b3)

print(len(library))                          # 3
b2.check_out()
print(library.get_available_books())         # [b1, b3]
print(library.find_by_author("Isaac Asimov")) # [b2, b3]

b2.check_out()                               # raises RuntimeError
```

### What This Tests
Object relationships · protected attributes · list filtering · dunder methods · `RuntimeError` for state violations

---

---

# Tier 2 — Inheritance & Polymorphism

---

## Exercise 3: Employee Payroll System

### Background
At companies like Google and Amazon, payroll systems must handle many different compensation models without the calling code needing to know which type it's dealing with. This is polymorphism in action. You will also get a first glimpse of the **Template Method** pattern — one of the behavioral design patterns we will study formally later.

### Requirements

**Abstract base class `Employee`:**

| Attribute / Method | Detail |
|---|---|
| `name: str` | Public |
| `employee_id: str` | Public |
| `_base_salary: float` | Protected |
| `calculate_monthly_pay() -> float` | **Abstract** — each subclass must implement |
| `get_role() -> str` | **Abstract** — each subclass must implement |
| `generate_payslip() -> str` | **Concrete** — calls the two abstract methods above and returns a formatted payslip string |

**Three concrete subclasses:**

**`FullTimeEmployee`**
- Monthly pay = `_base_salary / 12`
- Role = `"Full-Time Employee"`

**`ContractEmployee`**
- Additional attributes: `hourly_rate: float`, `hours_worked_this_month: int`
- Monthly pay = `hourly_rate × hours_worked_this_month`
- Role = `"Contractor"`

**`CommissionEmployee`**
- Additional attributes: `base_monthly_salary: float`, `commission_rate: float`
- Method: `add_sale(amount: float) -> None` — records a sale
- Monthly pay = `base_monthly_salary + sum(all sales) × commission_rate`
- Role = `"Commission-Based Employee"`

**Standalone function:**
```python
def run_payroll(employees: list[Employee]) -> None:
    ...
```
This function must call `generate_payslip()` on every employee **without using `isinstance()` or checking types**.

### Expected Behavior

```python
employees = [
    FullTimeEmployee("Alice", "E001", base_salary=120000),
    ContractEmployee("Bob", "E002", hourly_rate=85.0, hours_worked_this_month=160),
    CommissionEmployee("Carol", "E003", base_monthly_salary=3000, commission_rate=0.08),
]

employees[2].add_sale(5000)
employees[2].add_sale(12000)

run_payroll(employees)

# Alice's payslip: Full-Time Employee | Monthly Pay: $10000.00
# Bob's payslip:   Contractor         | Monthly Pay: $13600.00
# Carol's payslip: Commission-Based   | Monthly Pay: $4360.00
```

### What This Tests
`ABC` and `@abstractmethod` · concrete shared methods · polymorphism · type hints on collections · the Template Method pattern preview

---

## Exercise 4: Shape Area Calculator

### Background
This is a classic exercise taught in CMU's 15-214 and MIT's 6.009 specifically because it forces clean thinking about interface contracts. Every shape must honor the same API, allowing a single function to work across all of them — that is the power of polymorphism.

### Requirements

**Abstract base class `Shape`:**

| Method | Detail |
|---|---|
| `area() -> float` | Abstract |
| `perimeter() -> float` | Abstract |
| `describe() -> str` | Abstract — returns a human-readable description |
| `is_larger_than(other: 'Shape') -> bool` | Concrete — compares areas of two shapes |

**Implement all four concrete shapes:**
- `Circle(radius: float)`
- `Rectangle(width: float, height: float)`
- `Triangle(a: float, b: float, c: float)` — use Heron's formula for area
- `RightTriangle(base: float, height: float)`

**Standalone functions:**

```python
def largest_shape(shapes: list[Shape]) -> Shape: ...
def total_area(shapes: list[Shape]) -> float: ...
def shapes_larger_than(threshold: float, shapes: list[Shape]) -> list[Shape]: ...
```

### Expected Behavior

```python
shapes = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 4, 5),
    RightTriangle(3, 4),
]

print(total_area(shapes))             # sum of all areas
print(largest_shape(shapes))          # Circle with r=5
print(shapes_larger_than(20, shapes)) # [Circle]

c = Circle(10)
r = Rectangle(4, 6)
print(c.is_larger_than(r))            # True
```

### Hint
Heron's formula for a triangle with sides `a`, `b`, `c`:
```
s = (a + b + c) / 2
area = sqrt(s × (s-a) × (s-b) × (s-c))
```

### What This Tests
`ABC` · polymorphism · typed collections · mathematical implementation · writing utility functions that operate on abstract types

---

---

# Tier 3 — Composition & Design Thinking

---

## Exercise 5: Notification System Using Composition

### Background
This is a real architectural problem. At scale, users need to be reachable through multiple channels — email, SMS, push notifications, Slack, and others that haven't been invented yet. A system that uses inheritance to add new channels breaks every time a new channel is added. A system built with **composition** can accept new channels with **zero changes** to the core service. This exercise directly previews the **Open/Closed Principle** from SOLID.

### Requirements

**Three channel classes** — each implements a shared abstract interface:

```python
class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool: ...

    @abstractmethod
    def channel_type(self) -> str: ...
```

| Class | Constructor Args | `channel_type()` returns |
|---|---|---|
| `EmailChannel` | `smtp_server: str`, `sender_address: str` | `"email"` |
| `SMSChannel` | `api_key: str` | `"sms"` |
| `PushNotificationChannel` | `app_id: str` | `"push"` |

**`NotificationService` class (uses composition — holds channels, does not inherit from them):**

| Method | Detail |
|---|---|
| `__init__(channels: list[NotificationChannel])` | Stores the list of channels |
| `notify(recipient: str, message: str) -> None` | Sends through **all** channels |
| `notify_via(channel_type: str, recipient: str, message: str) -> bool` | Sends through one specific channel type. Returns `False` if channel type not found |
| `add_channel(channel: NotificationChannel) -> None` | Adds a new channel at runtime |
| `remove_channel(channel_type: str) -> None` | Removes a channel by type |

### Expected Behavior

```python
service = NotificationService([
    EmailChannel("smtp.gmail.com", "alerts@company.com"),
    SMSChannel("twilio-api-key-xyz"),
])

service.notify("user@example.com", "Your order has shipped!")
# Sends via email AND sms

service.add_channel(PushNotificationChannel("app-id-123"))
service.notify_via("push", "user@example.com", "Flash sale — 2 hours only!")
# Sends via push only

service.remove_channel("sms")
service.notify("user@example.com", "Invoice ready")
# Sends via email and push only — sms is gone
```

### Challenge Requirement
Adding a brand new `SlackChannel` class should require **zero changes** to `NotificationService`. Verify this by implementing `SlackChannel(webhook_url: str)` and dropping it into the service. If you have to touch `NotificationService` to make it work, revisit your design.

### What This Tests
Composition over inheritance · flexible runtime behavior · dependency injection preview · Open/Closed Principle preview · abstract interfaces

---

## Exercise 6: Warehouse Inventory System

### Background
This exercise models a real e-commerce warehouse. It pushes your understanding of composition, dunder methods (including making a class iterable), and domain-driven design thinking. Stanford's CS106B uses inventory-style exercises specifically to test whether students can model a domain cleanly before adding complexity.

### Requirements

**`Product` class:**

| Attribute / Method | Detail |
|---|---|
| `name: str`, `sku: str`, `price: float` | Public |
| `__stock: int` | Private, set in constructor |
| `add_stock(quantity: int) -> None` | Validates quantity > 0 |
| `remove_stock(quantity: int) -> None` | Raises `ValueError` if insufficient stock |
| `is_available() -> bool` | Returns `True` if stock > 0 |
| `get_stock() -> int` | Returns current stock level |
| `__lt__` and `__gt__` | Compare products by **price** |
| `__repr__` | Informative representation |

**`Category` class:**

| Method | Detail |
|---|---|
| `__init__(name: str)` | Stores name, initializes empty product list |
| `add_product(product: Product) -> None` | Adds to internal list |
| `get_products_in_price_range(min_price: float, max_price: float) -> list[Product]` | Filters by price |
| `most_expensive() -> Product` | Returns the most expensive product |
| `__len__` | Returns number of products in category |
| `__iter__` | Makes the category iterable — `for product in category` must work |

**`Warehouse` class (uses composition — has categories, does not inherit from them):**

| Method | Detail |
|---|---|
| `add_category(category: Category) -> None` | Adds a category |
| `find_product_by_sku(sku: str) -> Optional[Product]` | Searches all categories. Returns `None` if not found |
| `get_all_low_stock_products(threshold: int) -> list[Product]` | Returns products where stock ≤ threshold across all categories |
| `total_inventory_value() -> float` | Sum of `price × stock` for every product in every category |

### Expected Behavior

```python
from typing import Optional

electronics = Category("Electronics")
electronics.add_product(Product("Laptop", "SKU-001", 999.99, stock=15))
electronics.add_product(Product("Mouse", "SKU-002", 29.99, stock=3))

books = Category("Books")
books.add_product(Product("Clean Code", "SKU-003", 45.00, stock=8))

warehouse = Warehouse()
warehouse.add_category(electronics)
warehouse.add_category(books)

print(warehouse.total_inventory_value())          # (999.99×15) + (29.99×3) + (45.00×8)
print(warehouse.get_all_low_stock_products(5))    # [Mouse, Clean Code]
print(warehouse.find_product_by_sku("SKU-001"))   # Laptop

for product in electronics:                       # __iter__ in action
    print(product)
```

### What This Tests
Composition · `__iter__` and `__len__` · `__lt__` / `__gt__` · `Optional` type hint · realistic domain modeling · searching nested data structures

---

---

# Tier 4 — Decorators & Advanced Mechanics
### *MIT / CMU Level*

---

## Exercise 7: Build Your Own Decorator Library

### Background
In production Python codebases at companies like Google and Stripe, decorators handle authentication, caching, retry logic, rate limiting, and observability — all without polluting core business logic. In this exercise you build three production-grade decorators from scratch. This is exactly the kind of problem asked in CMU 15-214 assignments.

### Requirements

Build the following three decorators. Each must use `@functools.wraps` to preserve the original function's metadata.

---

**Decorator 1: `@validate_types`**

Inspects the type hints on any function and raises `TypeError` at runtime if any argument does not match its annotated type. Must work generically on any function without being hardcoded to a specific signature.

```python
@validate_types
def transfer_funds(amount: float, account_id: int, description: str) -> bool:
    return True

transfer_funds(100.0, 42, "rent")       # works fine
transfer_funds("hundred", 42, "rent")   # TypeError: 'amount' expected float, got str
transfer_funds(100.0, "42", "rent")     # TypeError: 'account_id' expected int, got str
```

**Hint:** Use `func.__annotations__` to access type hints at runtime.

---

**Decorator 2: `@retry_on_failure(max_attempts, delay_seconds)`**

Retries the decorated function if it raises any exception, up to `max_attempts` times with `delay_seconds` between attempts. If all attempts fail, re-raises the last exception. Prints a message on each failed attempt.

```python
attempt_count = 0

@retry_on_failure(max_attempts=3, delay_seconds=0.5)
def unstable_api_call() -> str:
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise ConnectionError("Network timeout")
    return "success"

result = unstable_api_call()
# Attempt 1 failed: Network timeout. Retrying in 0.5s...
# Attempt 2 failed: Network timeout. Retrying in 0.5s...
print(result)   # success
```

---

**Decorator 3: `@execution_timer`**

Measures and prints how long the decorated function took to execute. Must still return the function's original return value unchanged.

```python
@execution_timer
def heavy_computation(n: int) -> int:
    return sum(range(n))

result = heavy_computation(10_000_000)
# [execution_timer] heavy_computation completed in 0.412s
print(result)   # 49999995000000
```

### What This Tests
Decorators · `functools.wraps` · closures · `__annotations__` introspection · higher-order functions · parameterized decorators

---

## Exercise 8: Mini Plugin Pipeline *(Capstone)*

### Background
This is the capstone exercise. It combines every concept covered in this set and directly previews two major design patterns: **Chain of Responsibility** and **Strategy**. This style of pipeline architecture is used in real data engineering systems at companies like Airbnb, Uber, and LinkedIn for ETL (Extract, Transform, Load) workloads.

Complete this exercise and you are genuinely ready to begin learning design patterns.

### Requirements

**Abstract base class `DataProcessor`:**

| Method | Detail |
|---|---|
| `process(data: list[dict]) -> list[dict]` | Abstract — transforms and returns the data |
| `get_processor_name() -> str` | Abstract — returns a human-readable name |
| `validate_input(data: list[dict]) -> None` | Concrete — raises `ValueError` if data is not a non-empty list of dicts |

**Three concrete processors:**

**`FilterProcessor(field: str, value)`**
- Keeps only records where `record[field] == value`
- Name: `f"Filter({field}={value})"`

**`TransformProcessor(field: str, transform_func: callable)`**
- Applies `transform_func` to the specified field in every record (returns modified copies, does not mutate originals)
- Name: `f"Transform({field})"`

**`AggregatorProcessor(group_by_field: str, aggregate_field: str)`**
- Groups records by `group_by_field` and sums the `aggregate_field` for each group
- Returns one dict per group: `{group_by_field: group_value, aggregate_field: total}`
- Name: `f"Aggregate({group_by_field} → sum of {aggregate_field})"`

**`Pipeline` class:**

| Method | Detail |
|---|---|
| `__init__()` | Starts with an empty list of processors |
| `add_step(processor: DataProcessor) -> 'Pipeline'` | Adds a processor. **Returns `self`** to allow method chaining |
| `run(data: list[dict]) -> list[dict]` | Passes data through each processor in sequence. Must be decorated with your `@execution_timer` from Exercise 7 |
| `get_summary() -> str` | Returns a readable string describing all steps in order |

### Test Data & Expected Output

```python
pipeline = (
    Pipeline()
    .add_step(FilterProcessor("status", "active"))
    .add_step(TransformProcessor("revenue", lambda x: round(x * 1.10, 2)))
    .add_step(AggregatorProcessor("region", "revenue"))
)

data = [
    {"id": 1, "status": "active",   "revenue": 1000.0, "region": "North"},
    {"id": 2, "status": "inactive", "revenue":  500.0, "region": "North"},
    {"id": 3, "status": "active",   "revenue":  750.0, "region": "South"},
    {"id": 4, "status": "active",   "revenue":  300.0, "region": "North"},
]

result = pipeline.run(data)
print(result)
# [{"region": "North", "revenue": 1430.0},
#  {"region": "South", "revenue": 825.0}]

print(pipeline.get_summary())
# Pipeline Steps:
#   1. Filter(status=active)
#   2. Transform(revenue)
#   3. Aggregate(region → sum of revenue)
```

### Derivation Walkthrough
To verify your solution:

1. **After FilterProcessor** — records 1, 3, 4 remain (record 2 is `inactive`)
2. **After TransformProcessor** — revenues become: `1100.0`, `825.0`, `330.0`
3. **After AggregatorProcessor** — `North: 1100.0 + 330.0 = 1430.0`, `South: 825.0`

### Bonus Challenge *(Optional)*
Add a `@validate_types` decorator (from Exercise 7) to `add_step` so it raises a `TypeError` if anything other than a `DataProcessor` is passed in.

### What This Tests
Everything: `ABC` · polymorphism · composition · decorators · type hints · method chaining · real algorithmic thinking · **Chain of Responsibility preview** · **Strategy pattern preview**

---

---

## Submission Checklist

Before considering any exercise complete, verify the following:

- [ ] Code runs without errors
- [ ] All edge cases raise the correct exception types
- [ ] Type hints are present on all method signatures
- [ ] No use of `isinstance()` in functions that should use polymorphism
- [ ] Access modifiers (public / protected / private) are applied correctly throughout
- [ ] `@functools.wraps` is used in all decorators (Exercise 7 and 8)
- [ ] Exercise 8 pipeline produces the exact expected output