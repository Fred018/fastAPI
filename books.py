from http.client import HTTPException

from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {
        "title": "Book 1",
        "author": "Author one",
        "category": "Science",
    },
    {
        "title": "Book 2",
        "author": "Author two",
        "category": "Science",
    },
    {
        "title": "Book 3",
        "author": "Author tree",
        "category": "history",
    },
    {
        "title": "Book 4",
        "author": "Author tree",
        "category": "math",
    },
    {
        "title": "Book 5",
        "author": "Author tree",
        "category": "math",
    },
    {
        "title": "Book 6",
        "author": "Author six",
        "category": "math",
    },


]


@app.get("/books")
async  def read_all_books():
    return BOOKS

@app.get("/books/author_books")
async def delete_author_books(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return

@app.get("/books/{book_title}")
async def get_book(book_title: str):
    for book in BOOKS:
        if book["title"] == book_title:
            return book
        else:
            continue
    return {"detail": "Book not found"}


@app.get("/books/")
async def read_category_by_query(category: str):
    return_books = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            return_books.append(book)
    return return_books

@app.get("/books/{book_author}/")
async def read_author_cathegory_by_query(book_author:str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold() and  book.get("category").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book= Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == updated_book["title"].casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            BOOKS.remove(book)



