

class Library:
    _booksInLibrary = []
    _allBooks = []
    

    @classmethod
    def add_book(cls, book):
        Library.booksInLibrary.append(book)
        Library.allBooks.append(book)
    
    @classmethod
    def show_available(cls):
        print("Here are the list of books in the library:")
        for book in Library._booksInLibrary:
            print(book)

class Book:
    duration = 7
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre
        self._status = "available"
        self.borrowed_by = None

    def __str__(self):
        return f"{self.title} by {self.author}"

    def borrow_duration(self):
        print(f"This book duration is {self.duration}")

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if self.status == value:
            print("Cannot perform this operation")
        elif self._status == "available":
            self._status = value
        elif self._status == "borrowed":
            self._status = value

class User:
    def __init__(self, name):
        self.name = name
        self._borrowed_books = []
    
    
    def borrow_book(self, book_title):
        for book in Library.booksInLibrary:
            if book_title == book.title:
                try:
                    index = Library.booksInLibrary.index(book)
                    bookToBorrow = Library.booksInLibrary.pop(index)
                    bookToBorrow.status = "borrowed"
                    bookToBorrow.borrowed_by = self.name
                    self._borrowed_books.append(bookToBorrow)
                    print(f'Here is the book {self.name}')
                    book.borrow_duration()
                    break
                except ValueError:
                    print("value error")
                    break
        else:
            print("Book is not in the library")
    

    def return_book(self, book_title):
        for each_book in Library.allBooks:
            if book_title == each_book.title:
                for book in Library.booksInLibrary:
                    if book_title == book.title:
                        print("Book already returned")
                        break
                else:
                    try:
                        each_book.status = "available"
                        each_book.borrowed_by = None
                        Library.booksInLibrary.append(each_book)
                        indexOfBook = self._borrowed_books.index(each_book)
                        self._borrowed_books.pop(indexOfBook)
                        print("Thank you for returning the book")
                        break
                    except ValueError:
                        print("value error")
                        break
        else:       
            print("This book is not from this library")
        

    def booksInPossesion(self):
        if len(self._borrowed_books) == 0:
            print("There are no books in your possession")
        for book in self._borrowed_books:
            print(book.title)


class TextBook(Book):
    duration = 14
    def __init__(self, title, author, genre, subject):
        super().__init__(title, author, genre)
        self.subject = subject

    def borrow_duration(self):
        print(f"This book duration is {self.duration}") 

class Magazine(Book):
    duration = 7
    magazine_count = 0
    def __init__(self, title, author, genre):
        super().__init__(title, author, genre)
        self.issue_number = self.magazine_count + 1
        self.magazine_count += 1

    def borrow_duration(self):
        print(f"This book duration is {self.duration}")

book = Book('Things Fall Apart', "Chinue Achebe", "Drama")
Library.add_book(book)



user = User("Adetola")



textbook = TextBook('Understanding Calculus', 'Fred Grey', 'Education', 'Mathematics')


mag1 = Magazine('Forbes', 'Micheal Black', 'lifestyle')
mag2 = Magazine('NYT', 'Blue Fred', 'News')
Library.add_book(mag1)
Library.add_book(mag2)
Library.add_book(textbook)
Library.show_available()

user.borrow_book(textbook.title)
print(textbook._status)
user.return_book(textbook.title)
print(textbook._status)