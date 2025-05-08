-- -------------------------------------------------------------
--  Database Creation and Selection
-- -------------------------------------------------------------
--  * Create a new database for the Library Management System.
--  * If the database already exists, drop it first to start fresh.
--  * Select the newly created database for use.
-- -------------------------------------------------------------
DROP DATABASE IF EXISTS library_management_system;
CREATE DATABASE library_management_system;
USE library_management_system;

-- -------------------------------------------------------------
--  Table: Books
-- -------------------------------------------------------------
--  * Stores information about individual books.
--  * book_id: Unique identifier for each book (Primary Key).
--  * title: Title of the book.
--  * isbn: International Standard Book Number (Unique).
--  * published_date: Date when the book was published.
--  * publisher_id: Foreign Key referencing the Publishers table.
-- -------------------------------------------------------------
CREATE TABLE Books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    published_date DATE,
    publisher_id INT,
    INDEX (publisher_id) -- Add index on foreign key
);

-- -------------------------------------------------------------
--  Table: Authors
-- -------------------------------------------------------------
--  * Stores information about authors.
--  * author_id: Unique identifier for each author (Primary Key).
--  * first_name: First name of the author.
--  * last_name: Last name of the author.
-- -------------------------------------------------------------
CREATE TABLE Authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

-- -------------------------------------------------------------
--  Table: BookAuthors (Many-to-Many Relationship)
-- -------------------------------------------------------------
--  * Represents the relationship between books and authors.
--  * A book can have multiple authors, and an author can write multiple books.
--  * book_id: Foreign Key referencing the Books table.
--  * author_id: Foreign Key referencing the Authors table.
--  * Primary Key is a composite of (book_id, author_id).
-- -------------------------------------------------------------
CREATE TABLE BookAuthors (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (author_id) REFERENCES Authors(author_id),
    INDEX (book_id), -- Add index on foreign key
    INDEX (author_id)  -- Add index on foreign key
);

-- -------------------------------------------------------------
--  Table: Publishers
-- -------------------------------------------------------------
--  * Stores information about publishers.
--  * publisher_id: Unique identifier for each publisher (Primary Key).
--  * name: Name of the publisher.
--  * address: Address of the publisher.
-- -------------------------------------------------------------
CREATE TABLE Publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255)
);

-- -------------------------------------------------------------
--  Table: Members
-- -------------------------------------------------------------
--  * Stores information about library members.
--  * member_id: Unique identifier for each member (Primary Key).
--  * first_name: First name of the member.
--  * last_name: Last name of the member.
--  * email: Email address of the member (Unique).
--  * phone_number: Phone number of the member.
--  * address: Address of the member.
--  * membership_start_date: Date when the membership started.
-- -------------------------------------------------------------
CREATE TABLE Members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    address VARCHAR(255),
    membership_start_date DATE NOT NULL
);

-- -------------------------------------------------------------
--  Table: Loans
-- -------------------------------------------------------------
--  * Stores information about book loans.
--  * loan_id: Unique identifier for each loan (Primary Key).
--  * book_id: Foreign Key referencing the Books table.
--  * member_id: Foreign Key referencing the Members table.
--  * loan_date: Date when the book was loaned.
--  * return_date: Date when the book was returned (NULL if not returned).
--  * due_date: Date when the book is due.
-- -------------------------------------------------------------
CREATE TABLE Loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    member_id INT,
    loan_date DATE NOT NULL,
    return_date DATE,
    due_date DATE NOT NULL,
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    INDEX (book_id), -- Add index on foreign key
    INDEX (member_id)  -- Add index on foreign key
);

-- -------------------------------------------------------------
--  Table: Fines
-- -------------------------------------------------------------
--  * Stores information about fines for overdue books.
--  * fine_id: Unique identifier for each fine (Primary Key).
--  * loan_id: Foreign Key referencing the Loans table.
--  * amount: Amount of the fine.
--  * payment_date: Date when the fine was paid (NULL if not paid).
-- -------------------------------------------------------------
CREATE TABLE Fines (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE,
    FOREIGN KEY (loan_id) REFERENCES Loans(loan_id),
    INDEX (loan_id)  -- Add index on foreign key
);

-- -------------------------------------------------------------
--  Table: BookReservations
-- -------------------------------------------------------------
--  * Stores information about book reservations.
--  * reservation_id: Unique identifier for each reservation.
--  * book_id: Foreign Key referencing the Books table.
--  * member_id: Foreign Key referencing the Members table.
--  * reservation_date: Date when the reservation was made.
--  * status: Status of the reservation (e.g., 'Pending', 'Active', 'Cancelled', 'Completed').
-- -------------------------------------------------------------
CREATE TABLE BookReservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    member_id INT,
    reservation_date DATE NOT NULL,
    status ENUM('Pending', 'Active', 'Cancelled', 'Completed') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    INDEX (book_id),  -- Add index on foreign key
    INDEX (member_id)   -- Add index on foreign key
);

-- -------------------------------------------------------------
--  Table: Categories
-- -------------------------------------------------------------
--  * Stores information about book categories.
--  * category_id: Unique identifier for each category.
--  * name: Name of the category (e.g., 'Fiction', 'Sci-Fi', 'History').
-- -------------------------------------------------------------
CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- -------------------------------------------------------------
--  Table: BookCategories (Many-to-Many Relationship)
-- -------------------------------------------------------------
--  * Represents the relationship between books and categories.
--  * A book can belong to multiple categories, and a category can have multiple books.
--  * book_id: Foreign Key referencing the Books table.
--  * category_id: Foreign Key referencing the Categories table.
--  * Primary Key is a composite of (book_id, category_id).
-- -------------------------------------------------------------
CREATE TABLE BookCategories (
    book_id INT,
    category_id INT,
    PRIMARY KEY (book_id, category_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    INDEX (book_id),   -- Add index on foreign key
    INDEX (category_id)    -- Add index on foreign key
);

-- -------------------------------------------------------------
--  Table: Reviews
-- -------------------------------------------------------------
--  * Stores reviews for books.
--  * review_id: Unique identifier for each review.
--  * book_id: Foreign Key referencing the Books table.
--  * member_id: Foreign Key referencing the Members table.
--  * rating: Rating given by the member (e.g., 1 to 5 stars).
--  * comment: Text of the review.
--  * review_date: Date when the review was submitted.
-- -------------------------------------------------------------
CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    member_id INT,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    INDEX (book_id),  -- Add index on foreign key
    INDEX (member_id)   -- Add index on foreign key
);

-- -------------------------------------------------------------
--  Table: LibraryStaff
-- -------------------------------------------------------------
--  * Stores information about library staff members.
--  * staff_id: Unique identifier for each staff member.
--  * first_name: First name of the staff member.
--  * last_name: Last name of the staff member.
--  * email: Email address of the staff member (Unique).
--  * phone_number: Phone number of the staff member.
--  * job_title: Job title of the staff member.
--  * hire_date: Date when the staff member was hired.
-- -------------------------------------------------------------
CREATE TABLE LibraryStaff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    job_title VARCHAR(100),
    hire_date DATE NOT NULL
);

-- -------------------------------------------------------------
--  Table: StaffRoles (Many-to-Many Relationship)
-- -------------------------------------------------------------
--    * Stores the roles of the staff.
--    * role_id: Unique identifier for each role.
--    * role_name: Name of the role.
-- -------------------------------------------------------------
CREATE TABLE StaffRoles (
  role_id INT AUTO_INCREMENT PRIMARY KEY,
  role_name VARCHAR(255) NOT NULL UNIQUE
);

-- -------------------------------------------------------------
--  Table: LibraryStaffRoles
-- -------------------------------------------------------------
--  * Junction table to link LibraryStaff and StaffRoles.
--  * staff_id: Foreign Key referencing LibraryStaff.
--  * role_id: Foreign Key referencing StaffRoles.
-- -------------------------------------------------------------
CREATE TABLE LibraryStaffRoles (
    staff_id INT,
    role_id INT,
    PRIMARY KEY (staff_id, role_id),
    FOREIGN KEY (staff_id) REFERENCES LibraryStaff(staff_id),
    FOREIGN KEY (role_id) REFERENCES StaffRoles(role_id),
    INDEX (staff_id),  -- Add index on foreign key
    INDEX (role_id)   -- Add index on foreign key
);

-- -------------------------------------------------------------
--  Table: SystemSettings
-- -------------------------------------------------------------
--  * Stores system-wide settings for the library management system.
--  * setting_id: Unique identifier for each setting.
--  * setting_name: Name of the setting.
--  * setting_value: Value of the setting.
--  * description: Description of the setting.
-- -------------------------------------------------------------
CREATE TABLE SystemSettings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    setting_name VARCHAR(255) NOT NULL UNIQUE,
    setting_value VARCHAR(255),
    description TEXT
);

-- -------------------------------------------------------------
--  Table: Notifications
-- -------------------------------------------------------------
--  * Stores notifications for members and staff.
--  * notification_id: Unique identifier for each notification.
--  * recipient_id: ID of the recipient (can be member_id or staff_id).
--  * recipient_type: Type of recipient ('Member' or 'Staff').
--  * message: Content of the notification.
--  * notification_date: Date and time when the notification was created.
--  * status: Status of the notification (e.g., 'Sent', 'Read', 'Archived').
-- -------------------------------------------------------------
CREATE TABLE Notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_id INT,
    recipient_type ENUM('Member', 'Staff') NOT NULL,
    message TEXT NOT NULL,
    notification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Sent', 'Read', 'Archived') NOT NULL DEFAULT 'Sent',
    INDEX (recipient_id),
    INDEX (recipient_type)
);

-- -------------------------------------------------------------
--  Foreign Key Constraints (Adding them after table creation)
-- -------------------------------------------------------------
--  * Ensures data integrity by defining relationships between tables.
--  * Prevents orphaned records and enforces consistency.
-- -------------------------------------------------------------
ALTER TABLE Books ADD FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id);
