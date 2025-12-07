CREATE database smart_library;

CREATE TABLE authors (
    author_id   SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    biography   TEXT
);

-- 2. Books
CREATE TABLE books (
    book_id         SERIAL PRIMARY KEY,
    isbn            VARCHAR(20) UNIQUE,
    title           VARCHAR(300) NOT NULL,
    author_id       INT REFERENCES authors(author_id) ON DELETE SET NULL,
    genre           VARCHAR(50),
    published_year  INT CHECK (published_year >= 1000),
    copies_total    INT NOT NULL DEFAULT 1 CHECK (copies_total >= 1),
    copies_available INT NOT NULL DEFAULT 1
);

-- 3. Members
CREATE TABLE members (
    member_id   SERIAL PRIMARY KEY,
    full_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    phone       VARCHAR(20),
    join_date   DATE DEFAULT CURRENT_DATE
);

-- 4. Users (Authentication)
CREATE TABLE users (
    user_id     SERIAL PRIMARY KEY,
    username    VARCHAR(100) UNIQUE NOT NULL,  -- same as member's email or admin email
    password    VARCHAR(255) NOT NULL,
    role        VARCHAR(20) CHECK (role IN ('Librarian', 'Member')) NOT NULL
);

-- 5. Loans
CREATE TABLE loans (
    loan_id      SERIAL PRIMARY KEY,
    book_id      INT REFERENCES books(book_id) ON DELETE CASCADE,
    member_id    INT REFERENCES members(member_id) ON DELETE CASCADE,
    loan_date    DATE DEFAULT CURRENT_DATE,
    due_date     DATE NOT NULL DEFAULT (CURRENT_DATE + INTERVAL '7 days'),
    return_date  DATE,
    CONSTRAINT one_copy_at_a_time UNIQUE (book_id, return_date)
);

-- 6. Book Clubs
CREATE TABLE book_clubs (
    club_id      SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    description  TEXT,
    created_date DATE DEFAULT CURRENT_DATE
);

-- 7. Club Membership (Many-to-Many)
CREATE TABLE club_membership (
    club_id     INT REFERENCES book_clubs(club_id) ON DELETE CASCADE,
    member_id   INT REFERENCES members(member_id) ON DELETE CASCADE,
    joined_date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (club_id, member_id)
);

INSERT INTO authors (name, biography) VALUES
('George Orwell', 'Author of 1984'),
('J.K. Rowling', 'Harry Potter series'),
('S.K and crew', 'Clarify');

INSERT INTO books (isbn, title, author_id, genre, published_year, copies_total, copies_available) VALUES
('9780451524935', '1984', 1, 'Dystopia', 1949, 5, 3),
('9780439708180', 'Harry Potter', 2, 'Fantasy', 1997, 8, 8),
('9780439702920','Clarify',3, 'friction',2005, 6, 4);

INSERT INTO members (full_name, email, phone) VALUES
('John Doe', 'john@example.com', '0123456789'),
('Jane Smith', 'jane@example.com', '0987654321'),
('Abass bundu', 'abassbundu@gmail.com','079111333');

INSERT INTO users (username, password, role) VALUES
('admin@limkokwing.edu', 'admin123', 'Librarian'),
('john@example.com', '123', 'Member'),
('jane@example.com', '123', 'Member'),
('stevenstelaamara','STEVRINA','Librarian'),
('Ramadanfatimabah','Fula123','Librarian'),
('Jaraidem','Fula456','Librarian');

INSERT INTO book_clubs (name, description) VALUES
('Sci-Fi Club', 'We love science fiction!'),
('Fantasy Readers', 'Harry Potter, LOTR,');
