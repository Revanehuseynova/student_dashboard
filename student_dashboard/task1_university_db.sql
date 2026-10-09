-- ============================================================================
-- Task 1: UniversityDB, Students table, stored procedures
-- Run in SSMS or:  sqlcmd -S ".\SQLEXPRESS" -E -i task1_university_db.sql
-- ============================================================================
IF DB_ID(N'UniversityDB') IS NULL
    CREATE DATABASE UniversityDB;
GO

USE UniversityDB;
GO

IF OBJECT_ID(N'dbo.Students', N'U') IS NULL
    CREATE TABLE dbo.Students (
        Id        INT IDENTITY(1,1) PRIMARY KEY,
        Name      NVARCHAR(100) NOT NULL,
        Score     INT NOT NULL CONSTRAINT CK_Students_Score CHECK (Score BETWEEN 0 AND 100),
        CreatedAt DATETIME NOT NULL CONSTRAINT DF_Students_CreatedAt DEFAULT GETDATE()
    );
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Students)
    INSERT INTO dbo.Students (Name, Score)
    VALUES (N'Ali', 85), (N'Leyla', 72), (N'Murad', 48), (N'Aysel', 91), (N'Kamran', 63);
GO

-- GetStudentResult: all students, or those whose name contains @StudentName.
CREATE OR ALTER PROCEDURE dbo.GetStudentResult
    @StudentName NVARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT Id, Name, Score
    FROM dbo.Students
    WHERE @StudentName IS NULL
       OR LTRIM(RTRIM(@StudentName)) = N''
       OR Name LIKE N'%' + LTRIM(RTRIM(@StudentName)) + N'%'
    ORDER BY Id;
END;
GO

-- AddStudent: validates and inserts one student.
CREATE OR ALTER PROCEDURE dbo.AddStudent
    @Name  NVARCHAR(100),
    @Score INT
AS
BEGIN
    SET NOCOUNT ON;

    IF @Name IS NULL OR LTRIM(RTRIM(@Name)) = N''
        THROW 50001, N'Student name cannot be empty.', 1;
    IF @Score NOT BETWEEN 0 AND 100
        THROW 50002, N'Score must be between 0 and 100.', 1;

    INSERT INTO dbo.Students (Name, Score)
    VALUES (LTRIM(RTRIM(@Name)), @Score);
END;
GO

-- Examples
-- EXEC dbo.GetStudentResult;
-- EXEC dbo.GetStudentResult @StudentName = N'Ali';
