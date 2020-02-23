import csv
import os
import sqlalchemy

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():


    f = open("books.csv")
    reader = csv.reader(f)

    x = 0
    for isbn, title, author, year in reader:
        x = x + 1
        if x == 2500:
            print(x)
            db.execute("insert into books (isbn, title, author, year) values (:isbn, :title, :author, :year)",
                       {"isbn": isbn, "title": title, "author": author, "year": year})
            db.commit()

        elif x == 3500:
            print(x)
            db.execute("insert into books (isbn, title, author, year) values (:isbn, :title, :author, :year)",
                       {"isbn": isbn, "title": title, "author": author, "year": year})
            db.commit()

        elif x == 4500:
            print(x)
            db.execute("insert into books (isbn, title, author, year) values (:isbn, :title, :author, :year)",
                       {"isbn": isbn, "title": title, "author": author, "year": year})
            db.commit()

        else:
            db.execute("insert into books (isbn, title, author, year) values (:isbn, :title, :author, :year)", {"isbn":isbn, "title": title, "author":author, "year":year})
            db.commit()







if __name__ == "__main__":
    main()
