from typing import Optional, Iterable

class Product:
    def __init__(self, name: str, sku: str, price: float, stock: int) -> None:
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise TypeError("Product name must be a non-empty string")
        self.__name: str = name
        
        Product.isvalid_product_sku(sku=sku)
        self.__sku: str = sku
        
        if not isinstance(price, (float, int)):
            raise TypeError("Product Price must be a number")
        if price <= 0:
            raise ValueError("Product Price cannot be 0 or negative")
        self.__price: float = float(price)
        
        if not isinstance(stock, (float, int)):
            raise TypeError("Product Stock must be a number")
        if stock < 0:
            raise ValueError("Product Stock cannot be negative")
        
        self.__stock: int = stock
    
    def add_stock(self, quantity: int) -> None:
        if not isinstance(quantity, (float, int)):
            raise TypeError("Product Quantity must be a number")
        if quantity <= 0:
            raise ValueError("Product Quantity cannot be 0 or negative")
        
        self.__stock += quantity
    
    def remove_stock(self, quantity: int) -> None:
        if not isinstance(quantity, (float, int)):
            raise TypeError("Product Quantity must be a number")
        if quantity <= 0:
            raise ValueError("Product Quantity cannot be 0 or negative")
        if quantity > self.__stock:
            raise ValueError(f"Current Product Stock is: {self.__stock}. Cannot remove {quantity}")
        
        self.__stock -= quantity
    
    def is_available(self) -> bool:
        return self.__stock > 0
    
    @property
    def stock(self) -> int:
        return self.__stock
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def price(self) -> int:
        return self.__price
    
    @property
    def sku(self) -> int:
        return self.__sku
    
    def __repr__(self) -> int:
        return f"Product: {self.name} | SKU: {self.sku} | Price: {self.price} | Stock: {self.stock}"
    
    def __lt__(self, other: 'Product') -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price
    
    def __gt__(self, other: 'Product') -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price > other.price
    
    @staticmethod
    def isvalid_product_sku(sku: str) -> None:
        if (not isinstance(sku, str)) and (len(sku) != 0):
            raise TypeError(f'SKU must be str type and should have atleast one character')
        if (not sku.startswith('SKU')) and (not sku[-3:].isdigit()):
            raise ValueError("SKU number does not match required format. SKU code always start with `SKU-` followed by three digits")

class Category:
    def __init__(self, name: str) -> None:
        if (not isinstance(name, str)) and (len(name) != 0):
            raise TypeError(f'Category Name must be str type and should have atleast one character')
        self.__name: str = name
        self.__products: list[Product] = []
        self.__sku_index: dict[str, Product] = {}
        
    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError('Not a valid product to add to a category')
        
        if product.sku in self.__sku_index:
            raise ValueError(f'Product with SKU already exists')
        
        self.__products.append(product)
        self.__sku_index[product.sku] = product
    
    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        Product.isvalid_product_sku(sku=sku)
        return self.__sku_index.get(sku, None)
            
    def get_products_in_price_range(self, min_price: float, max_price: float) -> list[Product]:
        if not isinstance(min_price, (float, int)):
            raise TypeError("Minimum price must be a number")
        if not (0 <= min_price < float('inf')):
            raise ValueError("Minimum price not in valid range")
        
        if not isinstance(max_price, (float, int)):
            raise TypeError("Maximum price must be a number")
        if not (0 < max_price < float('inf')):
            raise ValueError("Maximum price not in valid range")
        
        if not ( min_price <= max_price):
            raise ValueError("Mininum price > Maximum price, this is not valid")
        
        return list(filter(lambda x: min_price <= x.price <= max_price, self.__products))
    
    def most_expensive(self) -> Product:
        if self.__len__() == 0:
            raise ValueError(f"No Products exist in this category yet")
        return max(self.__products, key=lambda x: x.price)
    
    def __len__(self) -> int:
        return len(self.__products)
    
    def __iter__(self) -> Iterable:
        for p in self.__products:
            yield p
            
    def __repr__(self) -> str:
        return f"Products: {self.__products}"

class Warehouse:
    def __init__(self) -> None:
        self.__categories: list[Category] = []
    
    def __repr__(self) -> str:
        return f"Categories: {self.__categories}"
        
    def add_category(self, category: Category) -> None:
        if not isinstance(category, Category):
            raise TypeError("Not a valid category to add to warehouse")
        self.__categories.append(category)
    
    def find_product_by_sku(self, sku: str) -> Optional[Product]:
        Product.isvalid_product_sku(sku=sku)
        for category in self.__categories:
            result: Optional[Product] = category.get_product_by_sku(sku=sku)
            if result:
                return result
        
    def get_all_low_stock_products(self, threshold: int) -> list[Product]:
        if not isinstance(threshold, (float, int)):
            raise TypeError("Price Threshold price must be a number")
        if threshold <= 0:
            raise ValueError("Price Threshold cannot be 0 or negative")
        
        filtered_products: list[Product] = []
        for category in self.__categories:
            for product in category:
                if product.stock <= threshold:
                    filtered_products.append(product)
        return filtered_products
    
    def total_inventory_value(self) -> float:
        val: float = 0
        for category in self.__categories:
            for product in category:
                val += (product.price * product.stock)
        return val
    

if __name__ == "__main__":
    electronics = Category("Electronics")
    electronics.add_product(Product("Laptop", "SKU-001", 999.99, stock=15))
    electronics.add_product(Product("Mouse", "SKU-002", 29.99, stock=3))
    
    books = Category("Books")
    books.add_product(Product("Clean Code", "SKU-003", 45.00, stock=8))
    
    warehouse = Warehouse()
    warehouse.add_category(electronics)
    warehouse.add_category(books)
    
    # print(warehouse)
    
    print(warehouse.total_inventory_value())
    print(warehouse.get_all_low_stock_products(10))
    print(warehouse.find_product_by_sku("SKU-001"))
