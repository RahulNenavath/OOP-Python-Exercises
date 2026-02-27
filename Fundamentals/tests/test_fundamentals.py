"""
OOP Fundamentals — Pytest Test Suite
=====================================
Covers all 8 exercises in the Fundamentals module.

Tests are grouped by exercise and organized from basic to edge cases,
mirroring the structure used in university-level automated graders
(e.g., MIT Gradescope, CMU Autolab).

Usage:
    Run all tests:         pytest tests/test_fundamentals.py -v
    Run one exercise:      pytest tests/test_fundamentals.py -v -k "TestBankAccount"
    Run with coverage:     pytest tests/test_fundamentals.py -v --tb=short
    Stop on first fail:    pytest tests/test_fundamentals.py -v -x

Skipping unimplemented exercises:
    Tests for exercises you haven't completed yet are marked with
    @pytest.mark.skipif and will be skipped automatically until
    the corresponding file exists and the class is importable.
"""

import pytest
import math
import time
import sys
import os

# ---------------------------------------------------------------------------
# Path setup — makes imports work regardless of where pytest is invoked from
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# ---------------------------------------------------------------------------
# Safe import helpers — skips entire test class if exercise not yet written
# ---------------------------------------------------------------------------

def _try_import(module_name: str, class_name: str):
    """Attempt to import a class from a module. Returns None if not found."""
    try:
        module = __import__(module_name)
        return getattr(module, class_name, None)
    except ModuleNotFoundError:
        return None


# ===========================================================================
# EXERCISE 1 — BankAccount
# ===========================================================================

BankAccount = _try_import("ex1_bank_account", "BankAccount")

@pytest.mark.skipif(BankAccount is None, reason="ex1_bank_account.py not found or BankAccount not defined")
class TestBankAccount:
    """Tests for Exercise 1: BankAccount"""

    # --- Setup ---

    def setup_method(self):
        """Fresh accounts before each test."""
        self.acc = BankAccount()
        self.acc2 = BankAccount()

    # --- Initialization ---

    def test_initial_balance_is_zero(self):
        assert self.acc.get_balance() == 0

    def test_balance_is_private(self):
        """Balance must not be directly accessible."""
        assert not hasattr(self.acc, "balance"), \
            "balance should be private (__balance), not public"
        assert not hasattr(self.acc, "_balance"), \
            "balance should be private (__balance), not protected"

    # --- Deposit ---

    def test_deposit_positive_amount(self):
        self.acc.deposit(100)
        assert self.acc.get_balance() == 100

    def test_deposit_multiple_times(self):
        self.acc.deposit(100)
        self.acc.deposit(250)
        assert self.acc.get_balance() == 350

    def test_deposit_float_amount(self):
        self.acc.deposit(99.99)
        assert self.acc.get_balance() == pytest.approx(99.99)

    def test_deposit_zero_raises_value_error(self):
        with pytest.raises(ValueError):
            self.acc.deposit(0)

    def test_deposit_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            self.acc.deposit(-50)

    # --- Withdraw ---

    def test_withdraw_reduces_balance(self):
        self.acc.deposit(500)
        self.acc.withdraw(200)
        assert self.acc.get_balance() == 300

    def test_withdraw_entire_balance(self):
        self.acc.deposit(100)
        self.acc.withdraw(100)
        assert self.acc.get_balance() == 0

    def test_withdraw_zero_raises_value_error(self):
        self.acc.deposit(100)
        with pytest.raises(ValueError):
            self.acc.withdraw(0)

    def test_withdraw_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            self.acc.withdraw(-10)

    def test_withdraw_exceeds_balance_raises_value_error(self):
        self.acc.deposit(100)
        with pytest.raises(ValueError):
            self.acc.withdraw(200)

    def test_withdraw_from_empty_account_raises_value_error(self):
        with pytest.raises(ValueError):
            self.acc.withdraw(1)

    # --- Transfer ---

    def test_transfer_moves_funds_correctly(self):
        self.acc.deposit(500)
        self.acc.transfer(200, self.acc2)
        assert self.acc.get_balance() == 300
        assert self.acc2.get_balance() == 200

    def test_transfer_wrong_type_raises_type_error(self):
        with pytest.raises(TypeError):
            self.acc.transfer(100, "not_an_account")

    def test_transfer_more_than_balance_raises_value_error(self):
        self.acc.deposit(100)
        with pytest.raises(ValueError):
            self.acc.transfer(500, self.acc2)

    def test_transfer_zero_raises_value_error(self):
        self.acc.deposit(100)
        with pytest.raises(ValueError):
            self.acc.transfer(0, self.acc2)

    # --- __str__ ---

    def test_str_format_zero_balance(self):
        assert str(self.acc) == "Account[balance=$0.00]"

    def test_str_format_with_balance(self):
        self.acc.deposit(250)
        assert str(self.acc) == "Account[balance=$250.00]"

    def test_str_format_two_decimal_places(self):
        self.acc.deposit(99.9)
        assert str(self.acc) == "Account[balance=$99.90]"

    # --- __eq__ ---

    def test_equal_accounts_same_balance(self):
        self.acc.deposit(100)
        self.acc2.deposit(100)
        assert self.acc == self.acc2

    def test_unequal_accounts_different_balance(self):
        self.acc.deposit(100)
        self.acc2.deposit(200)
        assert self.acc != self.acc2

    def test_eq_with_non_account_returns_not_implemented(self):
        result = self.acc.__eq__("not_an_account")
        assert result is NotImplemented


# ===========================================================================
# EXERCISE 2 — Library Book System
# ===========================================================================

Book = _try_import("ex2_library_system", "Book")
Library = _try_import("ex2_library_system", "Library")

@pytest.mark.skipif(Book is None or Library is None, reason="ex2_library_system.py not found or classes not defined")
class TestBook:
    """Tests for Exercise 2: Book class"""

    def setup_method(self):
        self.book = Book("Dune", "Frank Herbert", "978-0441013593")

    def test_attributes_are_set(self):
        assert self.book.title == "Dune"
        assert self.book.author == "Frank Herbert"
        assert self.book.isbn == "978-0441013593"

    def test_initially_available(self):
        assert self.book.is_available() is True

    def test_check_out_makes_unavailable(self):
        self.book.check_out()
        assert self.book.is_available() is False

    def test_return_makes_available(self):
        self.book.check_out()
        self.book.return_book()
        assert self.book.is_available() is True

    def test_check_out_already_checked_out_raises(self):
        self.book.check_out()
        with pytest.raises(RuntimeError):
            self.book.check_out()

    def test_return_book_not_checked_out_raises(self):
        with pytest.raises(RuntimeError):
            self.book.return_book()

    def test_repr_contains_key_info(self):
        r = repr(self.book)
        assert "Dune" in r
        assert "Frank Herbert" in r

    def test_is_checked_out_is_protected(self):
        assert not hasattr(self.book, "is_checked_out"), \
            "_is_checked_out should be protected (single underscore)"


@pytest.mark.skipif(Book is None or Library is None, reason="ex2_library_system.py not found or classes not defined")
class TestLibrary:
    """Tests for Exercise 2: Library class"""

    def setup_method(self):
        self.library = Library()
        self.b1 = Book("Dune", "Frank Herbert", "978-0441013593")
        self.b2 = Book("Foundation", "Isaac Asimov", "978-0553293357")
        self.b3 = Book("I, Robot", "Isaac Asimov", "978-0553294385")

    def test_empty_library_len_is_zero(self):
        assert len(self.library) == 0

    def test_add_book_increments_len(self):
        self.library.add_book(self.b1)
        assert len(self.library) == 1

    def test_add_multiple_books(self):
        self.library.add_book(self.b1)
        self.library.add_book(self.b2)
        self.library.add_book(self.b3)
        assert len(self.library) == 3

    def test_find_by_author_returns_correct_books(self):
        self.library.add_book(self.b1)
        self.library.add_book(self.b2)
        self.library.add_book(self.b3)
        result = self.library.find_by_author("Isaac Asimov")
        assert len(result) == 2
        assert self.b2 in result
        assert self.b3 in result

    def test_find_by_author_not_found_returns_empty(self):
        self.library.add_book(self.b1)
        result = self.library.find_by_author("Unknown Author")
        assert result == []

    def test_get_available_books_all_available(self):
        self.library.add_book(self.b1)
        self.library.add_book(self.b2)
        assert len(self.library.get_available_books()) == 2

    def test_get_available_books_excludes_checked_out(self):
        self.library.add_book(self.b1)
        self.library.add_book(self.b2)
        self.library.add_book(self.b3)
        self.b2.check_out()
        available = self.library.get_available_books()
        assert self.b2 not in available
        assert self.b1 in available
        assert self.b3 in available

    def test_find_by_author_returns_copy_not_internal_list(self):
        """Mutating the returned list should not affect the library internals."""
        self.library.add_book(self.b2)
        result = self.library.find_by_author("Isaac Asimov")
        result.clear()
        assert len(self.library.find_by_author("Isaac Asimov")) == 1

    def test_add_book_wrong_type_raises_type_error(self):
        with pytest.raises(TypeError):
            self.library.add_book("not a book")


# ===========================================================================
# EXERCISE 3 — Employee Payroll System
# ===========================================================================

FullTimeEmployee = _try_import("ex3_employee_payroll", "FullTimeEmployee")
ContractEmployee = _try_import("ex3_employee_payroll", "ContractEmployee")
CommissionEmployee = _try_import("ex3_employee_payroll", "CommissionEmployee")

@pytest.mark.skipif(
    any(c is None for c in [FullTimeEmployee, ContractEmployee, CommissionEmployee]),
    reason="ex3_employee_payroll.py not found or employee classes not defined"
)
class TestEmployeePayroll:
    """Tests for Exercise 3: Employee Payroll System"""

    def test_full_time_monthly_pay(self):
        emp = FullTimeEmployee("Alice", "E001", base_salary=120_000)
        assert emp.calculate_monthly_pay() == pytest.approx(10_000.0)

    def test_full_time_role(self):
        emp = FullTimeEmployee("Alice", "E001", base_salary=120_000)
        assert isinstance(emp.get_role(), str)
        assert len(emp.get_role()) > 0

    def test_contract_employee_monthly_pay(self):
        emp = ContractEmployee("Bob", "E002", hourly_rate=85.0, hours_worked_this_month=160)
        assert emp.calculate_monthly_pay() == pytest.approx(13_600.0)

    def test_contract_employee_zero_hours(self):
        emp = ContractEmployee("Bob", "E002", hourly_rate=85.0, hours_worked_this_month=0)
        assert emp.calculate_monthly_pay() == 0

    def test_commission_employee_no_sales(self):
        emp = CommissionEmployee("Carol", "E003", base_monthly_salary=3000, commission_rate=0.08)
        assert emp.calculate_monthly_pay() == pytest.approx(3000.0)

    def test_commission_employee_with_sales(self):
        emp = CommissionEmployee("Carol", "E003", base_monthly_salary=3000, commission_rate=0.08)
        emp.add_sale(5000)
        emp.add_sale(12000)
        assert emp.calculate_monthly_pay() == pytest.approx(4360.0)

    def test_generate_payslip_returns_string(self):
        emp = FullTimeEmployee("Alice", "E001", base_salary=120_000)
        payslip = emp.generate_payslip()
        assert isinstance(payslip, str)
        assert len(payslip) > 0

    def test_payslip_contains_name(self):
        emp = FullTimeEmployee("Alice", "E001", base_salary=120_000)
        assert "Alice" in emp.generate_payslip()

    def test_run_payroll_works_without_isinstance(self):
        """run_payroll must handle all types polymorphically."""
        try:
            from ex3_employee_payroll import run_payroll
        except ImportError:
            pytest.skip("run_payroll function not found")

        employees = [
            FullTimeEmployee("Alice", "E001", base_salary=120_000),
            ContractEmployee("Bob", "E002", hourly_rate=85.0, hours_worked_this_month=160),
            CommissionEmployee("Carol", "E003", base_monthly_salary=3000, commission_rate=0.08),
        ]
        # Should not raise — polymorphism handles all types
        run_payroll(employees)

    def test_cannot_instantiate_base_employee(self):
        """Abstract base class must not be directly instantiable."""
        try:
            from ex3_employee_payroll import Employee
        except ImportError:
            pytest.skip("Employee base class not found")
        with pytest.raises(TypeError):
            Employee("Test", "E000", 50_000)


# ===========================================================================
# EXERCISE 4 — Shape Area Calculator
# ===========================================================================

Circle = _try_import("ex4_shape_calculator", "Circle")
Rectangle = _try_import("ex4_shape_calculator", "Rectangle")
Triangle = _try_import("ex4_shape_calculator", "Triangle")
RightTriangle = _try_import("ex4_shape_calculator", "RightTriangle")

@pytest.mark.skipif(
    any(c is None for c in [Circle, Rectangle, Triangle, RightTriangle]),
    reason="ex4_shape_calculator.py not found or shape classes not defined"
)
class TestShapes:
    """Tests for Exercise 4: Shape Area Calculator"""

    # --- Circle ---

    def test_circle_area(self):
        c = Circle(5)
        assert c.area() == pytest.approx(math.pi * 25, rel=1e-5)

    def test_circle_perimeter(self):
        c = Circle(5)
        assert c.perimeter() == pytest.approx(2 * math.pi * 5, rel=1e-5)

    def test_circle_describe_returns_string(self):
        assert isinstance(Circle(5).describe(), str)

    # --- Rectangle ---

    def test_rectangle_area(self):
        r = Rectangle(4, 6)
        assert r.area() == pytest.approx(24.0)

    def test_rectangle_perimeter(self):
        r = Rectangle(4, 6)
        assert r.perimeter() == pytest.approx(20.0)

    def test_square_is_valid_rectangle(self):
        r = Rectangle(5, 5)
        assert r.area() == pytest.approx(25.0)

    # --- Triangle (Heron's formula) ---

    def test_triangle_area_345(self):
        t = Triangle(3, 4, 5)
        assert t.area() == pytest.approx(6.0, rel=1e-5)

    def test_triangle_perimeter(self):
        t = Triangle(3, 4, 5)
        assert t.perimeter() == pytest.approx(12.0)

    # --- RightTriangle ---

    def test_right_triangle_area(self):
        rt = RightTriangle(3, 4)
        assert rt.area() == pytest.approx(6.0)

    def test_right_triangle_perimeter(self):
        rt = RightTriangle(3, 4)
        assert rt.perimeter() == pytest.approx(12.0)

    # --- is_larger_than ---

    def test_is_larger_than_true(self):
        c = Circle(10)
        r = Rectangle(4, 6)
        assert c.is_larger_than(r) is True

    def test_is_larger_than_false(self):
        r = Rectangle(4, 6)
        c = Circle(1)
        assert r.is_larger_than(c) is True

    # --- Standalone functions ---

    def test_largest_shape(self):
        try:
            from ex4_shape_calculator import largest_shape
        except ImportError:
            pytest.skip("largest_shape function not found")
        shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
        result = largest_shape(shapes)
        assert isinstance(result, Circle)

    def test_total_area(self):
        try:
            from ex4_shape_calculator import total_area
        except ImportError:
            pytest.skip("total_area function not found")
        shapes = [Rectangle(4, 5), Rectangle(2, 3)]
        assert total_area(shapes) == pytest.approx(26.0)

    def test_shapes_larger_than(self):
        try:
            from ex4_shape_calculator import shapes_larger_than
        except ImportError:
            pytest.skip("shapes_larger_than function not found")
        shapes = [Circle(5), Rectangle(2, 2), Triangle(3, 4, 5)]
        result = shapes_larger_than(20, shapes)
        assert any(isinstance(s, Circle) for s in result)
        assert all(s.area() > 20 for s in result)

    def test_cannot_instantiate_base_shape(self):
        try:
            from ex4_shape_calculator import Shape
        except ImportError:
            pytest.skip("Shape base class not found")
        with pytest.raises(TypeError):
            Shape()


# ===========================================================================
# EXERCISE 5 — Notification System
# ===========================================================================

NotificationService = _try_import("ex5_notification_system", "NotificationService")
EmailChannel = _try_import("ex5_notification_system", "EmailChannel")
SMSChannel = _try_import("ex5_notification_system", "SMSChannel")
PushNotificationChannel = _try_import("ex5_notification_system", "PushNotificationChannel")

@pytest.mark.skipif(
    any(c is None for c in [NotificationService, EmailChannel, SMSChannel, PushNotificationChannel]),
    reason="ex5_notification_system.py not found or classes not defined"
)
class TestNotificationSystem:
    """Tests for Exercise 5: Notification System"""

    def setup_method(self):
        self.email = EmailChannel("smtp.gmail.com", "alerts@company.com")
        self.sms = SMSChannel("test-api-key")
        self.push = PushNotificationChannel("test-app-id")
        self.service = NotificationService([self.email, self.sms])

    def test_channel_type_email(self):
        assert self.email.channel_type() == "email"

    def test_channel_type_sms(self):
        assert self.sms.channel_type() == "sms"

    def test_channel_type_push(self):
        assert self.push.channel_type() == "push"

    def test_notify_calls_all_channels(self, capsys):
        self.service.notify("user@example.com", "Hello!")
        output = capsys.readouterr().out
        assert len(output) > 0  # something was printed/executed

    def test_notify_via_specific_channel(self):
        result = self.service.notify_via("email", "user@example.com", "Test")
        assert result is True

    def test_notify_via_missing_channel_returns_false(self):
        result = self.service.notify_via("push", "user@example.com", "Test")
        assert result is False

    def test_add_channel(self):
        self.service.add_channel(self.push)
        result = self.service.notify_via("push", "user@example.com", "Test")
        assert result is True

    def test_remove_channel(self):
        self.service.remove_channel("sms")
        result = self.service.notify_via("sms", "user@example.com", "Test")
        assert result is False

    def test_new_channel_requires_no_service_changes(self):
        """
        Adding a new channel type should work with zero changes to NotificationService.
        This tests the Open/Closed Principle.
        """
        try:
            from ex5_notification_system import SlackChannel
            slack = SlackChannel("https://hooks.slack.com/test")
            self.service.add_channel(slack)
            assert self.service.notify_via(slack.channel_type(), "user", "test") is True
        except ImportError:
            pytest.skip("SlackChannel not implemented yet — bonus challenge")


# ===========================================================================
# EXERCISE 6 — Warehouse Inventory System
# ===========================================================================

Product = _try_import("ex6_warehouse_inventory", "Product")
Category = _try_import("ex6_warehouse_inventory", "Category")
Warehouse = _try_import("ex6_warehouse_inventory", "Warehouse")

@pytest.mark.skipif(
    any(c is None for c in [Product, Category, Warehouse]),
    reason="ex6_warehouse_inventory.py not found or classes not defined"
)
class TestWarehouseInventory:
    """Tests for Exercise 6: Warehouse Inventory System"""

    def setup_method(self):
        self.laptop = Product("Laptop", "SKU-001", 999.99, stock=15)
        self.mouse = Product("Mouse", "SKU-002", 29.99, stock=3)
        self.book = Product("Clean Code", "SKU-003", 45.00, stock=8)
        self.electronics = Category("Electronics")
        self.electronics.add_product(self.laptop)
        self.electronics.add_product(self.mouse)
        self.books_cat = Category("Books")
        self.books_cat.add_product(self.book)
        self.warehouse = Warehouse()
        self.warehouse.add_category(self.electronics)
        self.warehouse.add_category(self.books_cat)

    # --- Product ---

    def test_product_initial_stock(self):
        assert self.laptop.stock == 15

    def test_product_add_stock(self):
        self.laptop.add_stock(5)
        assert self.laptop.stock == 20

    def test_product_remove_stock(self):
        self.laptop.remove_stock(5)
        assert self.laptop.stock == 10

    def test_product_remove_stock_insufficient_raises(self):
        with pytest.raises(ValueError):
            self.laptop.remove_stock(9999)

    def test_product_is_available_true(self):
        assert self.laptop.is_available() is True

    def test_product_is_available_false_when_out_of_stock(self):
        p = Product("Empty", "SKU-000", 10.0, stock=0)
        assert p.is_available() is False

    def test_product_comparison_lt(self):
        assert self.mouse < self.laptop

    def test_product_comparison_gt(self):
        assert self.laptop > self.mouse

    # --- Category ---

    def test_category_len(self):
        assert len(self.electronics) == 2

    def test_category_is_iterable(self):
        products = list(self.electronics)
        assert len(products) == 2

    def test_category_price_range(self):
        result = self.electronics.get_products_in_price_range(0, 50)
        assert self.mouse in result
        assert self.laptop not in result

    def test_category_most_expensive(self):
        assert self.electronics.most_expensive() == self.laptop

    # --- Warehouse ---

    def test_total_inventory_value(self):
        expected = (999.99 * 15) + (29.99 * 3) + (45.00 * 8)
        assert self.warehouse.total_inventory_value() == pytest.approx(expected, rel=1e-4)

    def test_find_product_by_sku_found(self):
        result = self.warehouse.find_product_by_sku("SKU-001")
        assert result == self.laptop

    def test_find_product_by_sku_not_found_returns_none(self):
        result = self.warehouse.find_product_by_sku("SKU-999")
        assert result is None

    def test_get_low_stock_products(self):
        result = self.warehouse.get_all_low_stock_products(threshold=5)
        assert self.mouse in result
        assert self.laptop not in result


# ===========================================================================
# EXERCISE 7 — Decorator Library
# ===========================================================================

validate_types = _try_import("ex7_decorator_library", "validate_types")
retry_on_failure = _try_import("ex7_decorator_library", "retry_on_failure")
execution_timer = _try_import("ex7_decorator_library", "execution_timer")

@pytest.mark.skipif(
    any(d is None for d in [validate_types, retry_on_failure, execution_timer]),
    reason="ex7_decorator_library.py not found or decorators not defined"
)
class TestDecoratorLibrary:
    """Tests for Exercise 7: Decorator Library"""

    # --- @validate_types ---

    def test_validate_types_correct_args_passes(self):
        @validate_types
        def add(x: int, y: int) -> int:
            return x + y
        assert add(1, 2) == 3

    def test_validate_types_wrong_type_raises_type_error(self):
        @validate_types
        def transfer(amount: float, account_id: int) -> bool:
            return True
        with pytest.raises(TypeError):
            transfer("hundred", 42)

    def test_validate_types_wrong_second_arg_raises_type_error(self):
        @validate_types
        def transfer(amount: float, account_id: int) -> bool:
            return True
        with pytest.raises(TypeError):
            transfer(100.0, "42")

    def test_validate_types_preserves_function_name(self):
        @validate_types
        def my_function(x: int) -> int:
            return x
        assert my_function.__name__ == "my_function"

    # --- @retry_on_failure ---

    def test_retry_succeeds_on_first_attempt(self):
        @retry_on_failure(max_attempts=3, delay_seconds=0)
        def always_works():
            return "ok"
        assert always_works() == "ok"

    def test_retry_succeeds_after_failures(self):
        attempts = {"count": 0}

        @retry_on_failure(max_attempts=3, delay_seconds=0)
        def flaky():
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise ConnectionError("fail")
            return "success"

        assert flaky() == "success"
        assert attempts["count"] == 3

    def test_retry_raises_after_all_attempts_fail(self):
        @retry_on_failure(max_attempts=3, delay_seconds=0)
        def always_fails():
            raise ValueError("always broken")

        with pytest.raises(ValueError):
            always_fails()

    def test_retry_preserves_function_name(self):
        @retry_on_failure(max_attempts=2, delay_seconds=0)
        def my_func():
            pass
        assert my_func.__name__ == "my_func"

    # --- @execution_timer ---

    def test_execution_timer_returns_correct_value(self):
        @execution_timer
        def compute(n: int) -> int:
            return sum(range(n))
        assert compute(100) == 4950

    def test_execution_timer_prints_output(self, capsys):
        @execution_timer
        def quick():
            return 42
        quick()
        output = capsys.readouterr().out
        assert len(output) > 0

    def test_execution_timer_preserves_function_name(self):
        @execution_timer
        def my_timed_func():
            pass
        assert my_timed_func.__name__ == "my_timed_func"

    def test_execution_timer_measures_time(self, capsys):
        @execution_timer
        def slow():
            time.sleep(0.1)
        slow()
        output = capsys.readouterr().out
        # The output should contain some numeric time value
        assert any(char.isdigit() for char in output)


# ===========================================================================
# EXERCISE 8 — Mini Plugin Pipeline (Capstone)
# ===========================================================================

FilterProcessor = _try_import("ex8_pipeline_capstone", "FilterProcessor")
TransformProcessor = _try_import("ex8_pipeline_capstone", "TransformProcessor")
AggregatorProcessor = _try_import("ex8_pipeline_capstone", "AggregatorProcessor")
Pipeline = _try_import("ex8_pipeline_capstone", "Pipeline")

@pytest.mark.skipif(
    any(c is None for c in [FilterProcessor, TransformProcessor, AggregatorProcessor, Pipeline]),
    reason="ex8_pipeline_capstone.py not found or classes not defined"
)
class TestPipeline:
    """Tests for Exercise 8: Mini Plugin Pipeline"""

    def setup_method(self):
        self.data = [
            {"id": 1, "status": "active",   "revenue": 1000.0, "region": "North"},
            {"id": 2, "status": "inactive", "revenue":  500.0, "region": "North"},
            {"id": 3, "status": "active",   "revenue":  750.0, "region": "South"},
            {"id": 4, "status": "active",   "revenue":  300.0, "region": "North"},
        ]

    # --- FilterProcessor ---

    def test_filter_keeps_matching_records(self):
        f = FilterProcessor("status", "active")
        result = f.process(self.data)
        assert len(result) == 3
        assert all(r["status"] == "active" for r in result)

    def test_filter_removes_non_matching(self):
        f = FilterProcessor("status", "inactive")
        result = f.process(self.data)
        assert len(result) == 1

    def test_filter_processor_name(self):
        f = FilterProcessor("status", "active")
        assert "status" in f.get_processor_name()
        assert "active" in f.get_processor_name()

    # --- TransformProcessor ---

    def test_transform_applies_function(self):
        t = TransformProcessor("revenue", lambda x: x * 2)
        result = t.process([{"revenue": 100.0}])
        assert result[0]["revenue"] == pytest.approx(200.0)

    def test_transform_does_not_mutate_original(self):
        original = [{"revenue": 100.0}]
        t = TransformProcessor("revenue", lambda x: x * 2)
        t.process(original)
        assert original[0]["revenue"] == 100.0  # original unchanged

    def test_transform_processor_name(self):
        t = TransformProcessor("revenue", lambda x: x)
        assert "revenue" in t.get_processor_name()

    # --- AggregatorProcessor ---

    def test_aggregator_groups_and_sums(self):
        active_data = [r for r in self.data if r["status"] == "active"]
        agg = AggregatorProcessor("region", "revenue")
        result = agg.process(active_data)
        result_dict = {r["region"]: r["revenue"] for r in result}
        assert result_dict["North"] == pytest.approx(1300.0)
        assert result_dict["South"] == pytest.approx(750.0)

    def test_aggregator_processor_name(self):
        agg = AggregatorProcessor("region", "revenue")
        assert "region" in agg.get_processor_name()
        assert "revenue" in agg.get_processor_name()

    # --- Pipeline ---

    def test_full_pipeline_produces_correct_result(self):
        pipeline = (
            Pipeline()
            .add_step(FilterProcessor("status", "active"))
            .add_step(TransformProcessor("revenue", lambda x: round(x * 1.10, 2)))
            .add_step(AggregatorProcessor("region", "revenue"))
        )
        result = pipeline.run(self.data)
        result_dict = {r["region"]: r["revenue"] for r in result}
        assert result_dict["North"] == pytest.approx(1430.0, rel=1e-4)
        assert result_dict["South"] == pytest.approx(825.0, rel=1e-4)

    def test_pipeline_method_chaining(self):
        """add_step must return self to support chaining."""
        p = Pipeline()
        returned = p.add_step(FilterProcessor("status", "active"))
        assert returned is p

    def test_pipeline_get_summary_contains_step_names(self):
        pipeline = Pipeline()
        pipeline.add_step(FilterProcessor("status", "active"))
        pipeline.add_step(AggregatorProcessor("region", "revenue"))
        summary = pipeline.get_summary()
        assert isinstance(summary, str)
        assert "status" in summary
        assert "region" in summary

    def test_pipeline_run_is_timed(self, capsys):
        """Pipeline.run should print timing output via @execution_timer."""
        pipeline = Pipeline()
        pipeline.add_step(FilterProcessor("status", "active"))
        pipeline.run(self.data)
        output = capsys.readouterr().out
        assert len(output) > 0

    def test_cannot_instantiate_base_processor(self):
        try:
            from ex8_pipeline_capstone import DataProcessor
        except ImportError:
            pytest.skip("DataProcessor base class not found")
        with pytest.raises(TypeError):
            DataProcessor()

    def test_validate_input_raises_on_empty_list(self):
        f = FilterProcessor("status", "active")
        with pytest.raises(ValueError):
            f.validate_input([])

    def test_validate_input_raises_on_non_list(self):
        f = FilterProcessor("status", "active")
        with pytest.raises(ValueError):
            f.validate_input("not a list")