class Book:
    def __init__(self, title: str, author: str, isbn: str) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn
        self._is_checked_out = False
    
    def is_available(self) -> bool:
        return not self._is_checked_out
    
    def check_out(self) -> None:
        if not self.is_available():
            raise RuntimeError("Book is already checked out.")
        self._is_checked_out = True
    
    def return_book(self) -> None:
        if self.is_available():
            raise RuntimeError("Book is marked as available.")
        self._is_checked_out = False
    
    def __repr__(self) -> str:
        return f"Book('{self.title}', '{self.author}', checked_out={self._is_checked_out})"
    
class Library:
    def __init__(self) -> None:
        self.__db = {} # author name : List[Book]
        self.__all_books = [] # list of all books - flattened duplicate of all books to avoid copying
         
    def add_book(self, book: Book) -> None:
        
        if not isinstance(book, Book):
            raise TypeError("book parameter is not of Book type")
        
        # addition - O(1)
        
        self.__db.setdefault(book.author, []).append(book)
        
        self.__all_books.append(book)
    
    def find_by_author(self, author: str) -> list[Book]:
        
        if not isinstance(author, str):
            raise TypeError("Author must be a string!")
        
        # search by author  - O(1)
        if author not in self.__db:
            return []
        return list(self.__db[author])
    
    def get_available_books(self) -> list[Book]:
        # return only those books which are not checked out? - O(n)
        return list(filter(lambda book: book.is_available(), self.__all_books))
    
    def __len__(self) -> int:
        return len(self.__all_books)
    
if __name__ == "__main__":
    library = Library()
    b1 = Book("Dune", "Frank Herbert", "978-0441013593")
    b2 = Book("Foundation", "Isaac Asimov", "978-0553293357")
    b3 = Book("I, Robot", "Isaac Asimov", "978-0553294385")
    
    library.add_book(b1)
    library.add_book(b2)
    library.add_book(b3)
    
    print(len(library))
    b2.check_out()
    print(library.get_available_books())
    print(library.find_by_author("Isaac Asimov"))
    
    b2.check_out()