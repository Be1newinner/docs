### **Chapter 2: SQL Fundamentals - The Language of Data**

This chapter introduces you to the core syntax and concepts of SQL, the declarative language used to communicate with relational databases like PostgreSQL. You'll learn how to retrieve, manipulate, and define your database's structure.

-----

To make this practical, let's start by setting up a sample database with some data. In your `psql` terminal (connected to `my_app_db` as shown in Chapter 1), execute the following:

```sql
-- Create a simple 'employees' table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE DEFAULT CURRENT_DATE,
    salary NUMERIC(10, 2),
    department VARCHAR(50)
);

-- Insert some sample data
INSERT INTO employees (first_name, last_name, email, hire_date, salary, department) VALUES
('John', 'Doe', 'john.doe@example.com', '2022-01-15', 60000.00, 'Sales'),
('Jane', 'Smith', 'jane.smith@example.com', '2021-03-01', 75000.00, 'Marketing'),
('Peter', 'Jones', 'peter.jones@example.com', '2023-07-20', 50000.00, 'Sales'),
('Alice', 'Brown', 'alice.brown@example.com', '2022-11-10', 80000.00, 'Engineering'),
('David', 'Lee', 'david.lee@example.com', '2023-01-05', 62000.00, 'Engineering'),
('Emily', 'Chen', NULL, '2024-02-14', 55000.00, 'Marketing'),
('Frank', 'White', 'frank.white@example.com', '2022-09-01', 70000.00, 'Sales'),
('Grace', 'Miller', 'grace.miller@example.com', '2021-06-20', 90000.00, 'Engineering');

-- Create a 'projects' table
CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    start_date DATE,
    end_date DATE,
    budget NUMERIC(12, 2)
);

INSERT INTO projects (project_name, start_date, end_date, budget) VALUES
('Website Redesign', '2024-03-01', '2024-09-30', 150000.00),
('Mobile App Dev', '2024-04-15', NULL, 200000.00),
('Sales Analytics', '2023-10-01', '2024-03-31', 80000.00),
('Cloud Migration', '2025-01-01', NULL, 300000.00);
```

-----

#### **1. The `SELECT` Statement: Retrieving Data**

The `SELECT` statement is the most frequently used SQL command. It allows you to query the database and retrieve data from one or more tables.

**Basic Syntax:**

```sql
SELECT column1, column2, ...
FROM table_name
[WHERE condition]
[GROUP BY column1, column2, ...]
[HAVING condition]
[ORDER BY column1 [ASC|DESC], ...]
[LIMIT number]
[OFFSET number];
```

*(Clauses in `[]` are optional and will be covered in this or later chapters.)*

**1.1. `SELECT *` vs. `SELECT column1, column2, ...`**

  * **`SELECT *`**: Retrieves all columns from the specified table. Convenient for quick checks, but generally **discouraged in production code** for performance and maintainability reasons.

      * **Ineffectiveness of `SELECT *` in Production:**
          * **Performance:** Retrieving unnecessary columns wastes network bandwidth and database processing time, especially with wide tables and large datasets.
          * **Application Impact:** If a new column is added to the table, your application might unexpectedly receive it, potentially breaking code that assumes a fixed number of columns or types.
          * **Clarity:** Explicitly listing columns improves readability and self-documentation of your query's intent.

  * **`SELECT column1, column2, ...`**: Retrieves only the specified columns. This is the **best practice**.

**Example:**

```sql
-- Retrieve all columns from the employees table (for exploration)
SELECT * FROM employees;

-- Retrieve specific columns: first_name, last_name, and salary
SELECT first_name, last_name, salary
FROM employees;
```

**1.2. `FROM` Clause**
Specifies the table(s) from which to retrieve data. This is mandatory for most `SELECT` statements.

**Example:**

```sql
SELECT project_name, budget
FROM projects;
```

**1.3. `WHERE` Clause: Filtering Data**
Used to filter rows based on a specified condition. Only rows that satisfy the condition will be included in the result set.

**Example:**

```sql
-- Get employees in the 'Sales' department
SELECT first_name, last_name, department
FROM employees
WHERE department = 'Sales';

-- Get employees earning more than 70000
SELECT first_name, last_name, salary
FROM employees
WHERE salary > 70000;
```

**1.4. `ORDER BY` Clause: Sorting Results**
Sorts the result set by one or more columns.

  * `ASC`: Ascending order (default).
  * `DESC`: Descending order.

**Example:**

```sql
-- Order employees by salary in descending order
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC;

-- Order employees by department (ascending), then by last name (ascending)
SELECT first_name, last_name, department, salary
FROM employees
ORDER BY department ASC, last_name ASC;
```

**1.5. `LIMIT` and `OFFSET` Clauses: Paginating Results**

  * **`LIMIT number`**: Restricts the number of rows returned by the query. Useful for pagination or retrieving top N records.
  * **`OFFSET number`**: Skips a specified number of rows before beginning to return rows. Used in conjunction with `LIMIT` for pagination.

**Example:**

```sql
-- Get the top 3 highest-paid employees
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3;

-- Get the next 3 highest-paid employees (e.g., for page 2, assuming 3 per page)
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3 OFFSET 3; -- Skips the first 3, returns the next 3
```

  * **Alternatives and Ineffectiveness:** While you could fetch all rows and filter/sort in your application code, this is highly inefficient.
      * **Network Overhead:** Transfers massive amounts of unnecessary data.
      * **Memory Usage:** Application needs to hold all data in memory.
      * **Processing Load:** Database is optimized for these operations; application is not.

**1.6. `DISTINCT` Values**
Used to retrieve only unique values from a specified column or combination of columns. It eliminates duplicate rows from the result set.

**Example:**

```sql
-- Get a list of unique departments
SELECT DISTINCT department
FROM employees;

-- Get unique combinations of department and hire year
SELECT DISTINCT department, EXTRACT(YEAR FROM hire_date) AS hire_year
FROM employees;
```

  * **Alternatives and Ineffectiveness:** Without `DISTINCT`, you'd have to fetch all values and de-duplicate them in your application, which is less efficient and more complex to manage outside the database.

**1.7. Aliases (`AS`)**
Used to give a temporary name (alias) to a column or a table in a query. This improves readability, especially in complex queries, and can avoid naming conflicts.

  * **Column Alias:** `column_name AS alias_name` (or just `column_name alias_name`)
  * **Table Alias:** `table_name AS alias_name` (or just `table_name alias_name`)

**Example:**

```sql
-- Alias columns for better readability
SELECT
    first_name AS "Employee First Name",
    last_name AS "Employee Last Name",
    salary AS annual_salary
FROM employees;

-- Alias tables (more common with joins, see Chapter 3)
SELECT e.first_name, e.last_name, p.project_name
FROM employees AS e, projects AS p; -- This is a CROSS JOIN, covered in Chapter 3
```

-----

#### **2. Data Manipulation Language (DML)**

DML commands are used to interact with the data *inside* the tables.

**2.1. `INSERT`: Adding New Records**
Adds new rows of data into a table.

**Syntax:**

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);

-- To insert multiple rows
INSERT INTO table_name (column1, column2, ...)
VALUES (value1_row1, value2_row1, ...),
       (value1_row2, value2_row2, ...),
       ...;

-- To insert all columns (order of values must match table's column order)
INSERT INTO table_name VALUES (value1, value2, ...);
```

**Example:**

```sql
-- Insert a single new employee
INSERT INTO employees (first_name, last_name, email, hire_date, salary, department)
VALUES ('Maria', 'Garcia', 'maria.g@example.com', '2024-05-20', 68000.00, 'Marketing');

-- Insert a new project, letting 'end_date' be NULL
INSERT INTO projects (project_name, start_date, budget)
VALUES ('Customer Feedback System', '2025-01-10', 95000.00);

-- Insert multiple employees at once
INSERT INTO employees (first_name, last_name, department) VALUES
('Chris', 'Green', 'HR'),
('Sarah', 'Blue', 'HR');

-- Verify insertion
SELECT * FROM employees WHERE first_name IN ('Maria', 'Chris', 'Sarah');
```

  * **Alternatives and Ineffectiveness:** Directly manipulating data files or using custom scripts for insertion bypasses database constraints, transactions, and security, leading to data corruption, inconsistency, and major headaches. The database's `INSERT` command ensures ACID properties are maintained.

**2.2. `UPDATE`: Modifying Existing Records**
Modifies existing data in a table. It's crucial to use the `WHERE` clause with `UPDATE` to target specific rows; otherwise, *all* rows in the table will be updated\!

**Syntax:**

```sql
UPDATE table_name
SET column1 = new_value1, column2 = new_value2, ...
[WHERE condition];
```

**Example:**

```sql
-- Increase John Doe's salary
UPDATE employees
SET salary = 65000.00
WHERE email = 'john.doe@example.com';

-- Update the end date for 'Mobile App Dev' project
UPDATE projects
SET end_date = '2025-03-31', budget = 220000.00
WHERE project_name = 'Mobile App Dev';

-- Give a 10% raise to all employees in the 'Sales' department
UPDATE employees
SET salary = salary * 1.10
WHERE department = 'Sales';

-- Verify updates
SELECT first_name, last_name, salary, department FROM employees WHERE department = 'Sales' OR email = 'john.doe@example.com';
SELECT project_name, end_date, budget FROM projects WHERE project_name = 'Mobile App Dev';
```

  * **Alternatives and Ineffectiveness:** Similar to `INSERT`, direct file manipulation is disastrous. Using `UPDATE` ensures atomicity and consistency, especially important when multiple fields or rows need to be changed in a coherent way.

**2.3. `DELETE`: Removing Records**
Removes rows from a table. Again, the `WHERE` clause is critical to specify which rows to delete. Omitting `WHERE` will delete *all* rows in the table\!

**Syntax:**

```sql
DELETE FROM table_name
[WHERE condition];
```

**Example:**

```sql
-- Delete the employee named 'Chris Green'
DELETE FROM employees
WHERE first_name = 'Chris' AND last_name = 'Green';

-- Delete all projects that have a budget less than 100000
DELETE FROM projects
WHERE budget < 100000.00;

-- Verify deletions
SELECT * FROM employees WHERE first_name = 'Chris';
SELECT * FROM projects WHERE budget < 100000.00;

-- !!! DANGER ZONE: This deletes ALL rows from the table !!!
-- DELETE FROM employees;
```

  * **Alternatives and Ineffectiveness:** Manual deletion from underlying files is not feasible. `DELETE` ensures transactionality, referential integrity (if foreign keys are set up, see Chapter 3), and proper index maintenance. Using `TRUNCATE TABLE` (DDL) is faster for emptying a table entirely but does not log individual row deletions and cannot use a `WHERE` clause.

-----

#### **3. Data Definition Language (DDL)**

DDL commands are used to define, modify, or delete the *structure* of your database objects (like tables, indexes, views, etc.).

**3.1. `CREATE TABLE`: Defining Your Schema**
Used to create a new table in the database. You define its name, columns, data types, and constraints. (We already used this extensively above).

**Syntax:**

```sql
CREATE TABLE [IF NOT EXISTS] table_name (
    column1_name DATATYPE [CONSTRAINT],
    column2_name DATATYPE [CONSTRAINT],
    ...
    [TABLE_CONSTRAINT]
);
```

**Example:**

```sql
-- Create a new table 'customers' with primary key and unique constraint
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY, -- SERIAL automatically creates a sequence for auto-incrementing IDs
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

  * **Alternatives and Ineffectiveness:** Manually defining table structures would be prone to errors, lack consistency, and make it impossible for the database to enforce integrity rules. DDL provides a standardized, robust way to define schemas.

**3.2. `ALTER TABLE`: Modifying Table Structures**
Used to modify the structure of an existing table. Common operations include adding, dropping, or modifying columns, and adding or removing constraints.

**Syntax (Common Operations):**

```sql
-- Add a column
ALTER TABLE table_name ADD COLUMN new_column_name DATATYPE [CONSTRAINT];

-- Drop a column
ALTER TABLE table_name DROP COLUMN column_name [CASCADE | RESTRICT];

-- Rename a column
ALTER TABLE table_name RENAME COLUMN old_column_name TO new_column_name;

-- Change a column's data type
ALTER TABLE table_name ALTER COLUMN column_name TYPE new_datatype;

-- Add a constraint
ALTER TABLE table_name ADD CONSTRAINT constraint_name TYPE (column_name);

-- Drop a constraint
ALTER TABLE table_name DROP CONSTRAINT constraint_name;
```

**Example:**

```sql
-- Add a 'country' column to the employees table
ALTER TABLE employees ADD COLUMN country VARCHAR(50) DEFAULT 'USA';

-- Change the data type of 'phone_number' in customers to something shorter, if applicable (careful with data loss!)
-- ALTER TABLE customers ALTER COLUMN phone_number TYPE VARCHAR(15); -- Uncomment and run if needed, but be aware of existing data!

-- Rename the 'email' column in employees to 'employee_email'
ALTER TABLE employees RENAME COLUMN email TO employee_email;

-- Add a CHECK constraint to projects table (budget must be positive)
ALTER TABLE projects ADD CONSTRAINT chk_positive_budget CHECK (budget > 0);

-- Verify changes (using \d command in psql)
\d employees
\d projects
```

  * **Alternatives and Ineffectiveness:** Directly editing database system files to modify schema is a recipe for disaster and can corrupt your entire database. `ALTER TABLE` is the controlled, transactional way to evolve your schema.

**3.3. `DROP TABLE`: Deleting Tables**
Used to delete an existing table (and all its data and associated indexes, triggers, etc.) from the database. This operation is irreversible\!

**Syntax:**

```sql
DROP TABLE [IF EXISTS] table_name [CASCADE | RESTRICT];
```

  * `IF EXISTS`: Prevents an error if the table doesn't exist.
  * `CASCADE`: Automatically drops objects that depend on the table (e.g., views, foreign key constraints in other tables). Use with extreme caution\!
  * `RESTRICT` (default): Prevents dropping the table if any dependent objects exist, forcing you to remove dependencies first.

**Example:**

```sql
-- Create a temporary table
CREATE TABLE temp_data (id INT, value TEXT);
INSERT INTO temp_data VALUES (1, 'test');

-- Drop the temporary table safely
DROP TABLE IF EXISTS temp_data;

-- Verify deletion
\dt -- should not list temp_data anymore
```

  * **Alternatives and Ineffectiveness:** Similar to other DDL, manual deletion is impossible. `DROP TABLE` is the only safe way, but its `CASCADE` option highlights the need for careful dependency management.

-----

#### **4. Basic Operators: Comparison, Logical, Arithmetic**

SQL provides a rich set of operators for constructing conditions and performing calculations.

**4.1. Comparison Operators (used in `WHERE` clauses):**

  * `=` : Equal to
  * `!=` or `<>` : Not equal to
  * `>` : Greater than
  * `<` : Less than
  * `>=` : Greater than or equal to
  * `<=` : Less than or equal to
  * `BETWEEN value1 AND value2`: Checks if a value is within a range (inclusive).
  * `LIKE pattern`: Pattern matching for strings (`%` matches any sequence of characters, `_` matches any single character). Case-sensitive.
  * `ILIKE pattern`: Pattern matching for strings (case-insensitive in PostgreSQL).
  * `IN (value1, value2, ...)`: Checks if a value matches any value in a list.
  * `IS NULL`: Checks if a value is NULL.
  * `IS NOT NULL`: Checks if a value is not NULL.

**Example:**

```sql
-- Employees with salary between 60000 and 70000 (inclusive)
SELECT first_name, last_name, salary
FROM employees
WHERE salary BETWEEN 60000 AND 70000;

-- Employees whose first name starts with 'J'
SELECT first_name, last_name
FROM employees
WHERE first_name LIKE 'J%';

-- Employees whose first name contains 'a' (case-insensitive)
SELECT first_name, last_name
FROM employees
WHERE first_name ILIKE '%a%';

-- Employees in 'Sales' or 'Marketing'
SELECT first_name, last_name, department
FROM employees
WHERE department IN ('Sales', 'Marketing');

-- Employees with a non-null email
SELECT first_name, last_name, employee_email
FROM employees
WHERE employee_email IS NOT NULL;
```

**4.2. Logical Operators (combine conditions in `WHERE` clauses):**

  * `AND`: Both conditions must be true.
  * `OR`: At least one condition must be true.
  * `NOT`: Negates a condition.

**Example:**

```sql
-- Employees in 'Sales' with salary greater than 60000
SELECT first_name, last_name, department, salary
FROM employees
WHERE department = 'Sales' AND salary > 60000;

-- Employees in 'Engineering' OR hired before 2022
SELECT first_name, last_name, department, hire_date
FROM employees
WHERE department = 'Engineering' OR hire_date < '2022-01-01';

-- Projects that are NOT currently in progress (no end date)
SELECT project_name, start_date, end_date
FROM projects
WHERE NOT end_date IS NULL; -- Equivalent to WHERE end_date IS NOT NULL
```

**4.3. Arithmetic Operators (for calculations):**

  * `+`: Addition
  * `-`: Subtraction
  * `*`: Multiplication
  * `/`: Division
  * `%`: Modulo (remainder)

**Example:**

```sql
-- Calculate annual salary plus a bonus for employees
SELECT
    first_name,
    last_name,
    salary AS base_salary,
    salary * 0.10 AS bonus,
    salary * 1.10 AS total_compensation
FROM employees;

-- Calculate days since hire for each employee
SELECT
    first_name,
    last_name,
    hire_date,
    (CURRENT_DATE - hire_date) AS days_since_hire
FROM employees;
```

-----

#### **5. Null Values and Three-Valued Logic**

`NULL` is a special marker in SQL that represents the absence of a value. It is *not* equivalent to zero, an empty string, or false. It means "unknown" or "not applicable."

  * **Representing Missing Data:** Use `NULL` for fields where data is genuinely missing, unknown, or irrelevant. For example, `end_date` for an ongoing project.
  * **Impact on Operators:** Most standard comparison operators (`=`, `!=`, `>`, etc.) return `UNKNOWN` when compared to `NULL`. This leads to SQL's **three-valued logic**: `TRUE`, `FALSE`, and `UNKNOWN`.

**Three-Valued Logic (3VL):**
When a condition involves `NULL`, the result might not be `TRUE` or `FALSE` but `UNKNOWN`.

| Operator | TRUE | FALSE | UNKNOWN |
| :------- | :--- | :---- | :------ |
| `NOT TRUE` | FALSE |       |         |
| `NOT FALSE` | TRUE |       |         |
| `NOT UNKNOWN` | UNKNOWN |       |         |
| `TRUE AND TRUE` | TRUE |       |         |
| `TRUE AND FALSE` | FALSE |       |         |
| `TRUE AND UNKNOWN` | UNKNOWN |       |         |
| `FALSE AND FALSE` | FALSE |       |         |
| `FALSE AND UNKNOWN` | FALSE |       |         |
| `UNKNOWN AND UNKNOWN` | UNKNOWN |       |         |
| `TRUE OR TRUE` | TRUE |       |         |
| `TRUE OR FALSE` | TRUE |       |         |
| `TRUE OR UNKNOWN` | TRUE |       |         |
| `FALSE OR FALSE` | FALSE |       |         |
| `FALSE OR UNKNOWN` | UNKNOWN |       |         |
| `UNKNOWN OR UNKNOWN` | UNKNOWN |       |         |

**Consequences for `WHERE` Clause:**
A `WHERE` clause only filters for rows where the condition evaluates to `TRUE`. Rows where the condition evaluates to `FALSE` or `UNKNOWN` are *excluded*.

**Example:**

```sql
-- This will NOT return Emily Chen because her email is NULL,
-- and 'NULL = 'some_value'' evaluates to UNKNOWN, not FALSE.
SELECT first_name, employee_email FROM employees WHERE employee_email = 'john.doe@example.com';

-- Correct way to check for NULLs: `IS NULL` or `IS NOT NULL`
-- Get employees without an email
SELECT first_name, last_name, employee_email
FROM employees
WHERE employee_email IS NULL;

-- Get employees with an email
SELECT first_name, last_name, employee_email
FROM employees
WHERE employee_email IS NOT NULL;
```

  * **Ineffectiveness of `= NULL` or `!= NULL`:** Using standard comparison operators with `NULL` (e.g., `column = NULL`, `column != NULL`) will *always* return `UNKNOWN`, meaning those rows will never be included in your result set, leading to silent data exclusion and incorrect query results. Always use `IS NULL` or `IS NOT NULL`.

-----

#### **6. Comments in SQL**

Comments are non-executable text within your SQL code, used for documentation and to explain complex logic. They are ignored by the database engine.

  * **Single-line comments:** Start with `--`
  * **Multi-line comments:** Enclosed within `/*` and `*/`

**Example:**

```sql
-- This is a single-line comment.
SELECT
    first_name, -- This column stores the employee's first name
    last_name,  /* This column stores the employee's last name */
    salary
FROM
    employees   -- Retrieve data from the employees table
WHERE
    salary > 70000; -- Filter for high earners

/*
This is a multi-line comment.
It can span several lines.
Useful for describing complex queries or blocks of DDL.
*/
```

**RESETING THE SERIAL SEQUNCE ID**
```sql
ALTER SEQUENCE RESTART WITH new_value;
```
  * **Alternatives and Ineffectiveness:** No comments make your code unreadable and difficult to maintain for anyone (including your future self). Proper commenting is a hallmark of professional development.
