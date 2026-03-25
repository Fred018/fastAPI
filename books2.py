from typing import Optional

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int 


    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="The id is not needed when creating a book, it will be generated automatically",
                              default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0, lt=2026)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "computer science pro",
                "author": "fred",
                "description": "A very nice book",
                "rating": 5,
                "published_date": 2020
            }
        }
    }

BOOKS = [
    Book(1,'computer science pro','fred','A very nice book', 5, 2020),
    Book(2,'be fast with fast api','fred','A great book', 5, 2021),
    Book(3,'Master endpoint','fred','And awesome book', 5, 2022),
    Book(4,'HP1','auther 1','Book description', 2, 2019),
    Book(5,'Hp2','auther 2','Book description', 3, 2020),
    Book(6,'hp3','auther 3','Book description', 1, 2021)
]



@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")



@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)
    return book_to_return


@app.get("/books/published/", status_code=status.HTTP_200_OK)
async def read_book_by_publication_date(published_date: int = Query(gt=0, lt=2026)):
    book_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            book_to_return.append(book)
    return book_to_return




@app.post("/Create-Book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book(new_book))
    return BookRequest(**BOOKS[-1].__dict__)


def find_book(book: Book):
    
    
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_updated = False
    for index, b in enumerate(BOOKS):
        if b.id == book.id:
            BOOKS[index] = book
            book_updated = True
    if not book_updated:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{books_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:  int = Path(gt=0)):

    book_deleted = False
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(index)
            book_deleted = True
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")





