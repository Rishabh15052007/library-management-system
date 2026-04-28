DROP DATABASE IF EXISTS librarydb;
CREATE DATABASE librarydb;
USE librarydb;

-- ================= STUDENTS =================
CREATE TABLE Students (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    SNo INT,
    Name VARCHAR(50),
    Course VARCHAR(50),
    Department VARCHAR(50),
    Year INT,
    RollNo INT UNIQUE,
    EntryTime DATETIME,
    ExitTime DATETIME
);

-- ================= BOOKS =================
CREATE TABLE Books (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(100),
    Author VARCHAR(100),
    Category VARCHAR(50),
    Pages INT
);

-- ================= ISSUE =================
CREATE TABLE Issue (
    IssueID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT,
    BookID INT,
    IssueDate DATE,
    ReturnDate DATE,
    Fine INT DEFAULT 0,

    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE CASCADE
);
