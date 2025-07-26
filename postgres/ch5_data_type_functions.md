### **Chapter 5: Data Types and Functions in PostgreSQL**

This chapter provides a comprehensive overview of PostgreSQL's diverse data types, from common numerical and textual types to specialized types like JSONB and arrays. You'll also learn to wield PostgreSQL's powerful arsenal of built-in functions to perform complex data transformations and calculations directly within your SQL queries, along with an introduction to creating your own custom functions.

-----

Let's ensure our sample database is ready for these examples. We'll add some columns to existing tables and maybe create a new one to demonstrate certain data types and functions.

```sql
-- Add a UUID column to employees (for demonstration)
ALTER TABLE employees ADD COLUMN unique_id UUID DEFAULT gen_random_uuid();

-- Add a JSONB column to employees (for demo)
ALTER TABLE employees ADD COLUMN metadata JSONB;
UPDATE employees SET metadata = '{"preferred_contact": "email", "office_location": "Building A"}' WHERE employee_id = 1;
UPDATE employees SET metadata = '{"preferred_contact": "phone", "is_manager": true}' WHERE employee_id = 4;

-- Add an array column to projects
ALTER TABLE projects ADD COLUMN assigned_tags TEXT[];
UPDATE projects SET assigned_tags = ARRAY['web', 'frontend', 'design'] WHERE project_name = 'Website Redesign';
UPDATE projects SET assigned_tags = ARRAY['mobile', 'android', 'ios'] WHERE project_name = 'Mobile App Dev';

-- Create a table for ENUM demonstration
CREATE TYPE traffic_light_state AS ENUM ('red', 'yellow', 'green');
CREATE TABLE intersections (
    intersection_id SERIAL PRIMARY KEY,
    location TEXT NOT NULL,
    current_state traffic_light_state DEFAULT 'red'
);
INSERT INTO intersections (location, current_state) VALUES
('Main & Elm', 'red'),
('Oak & Pine', 'green');

-- Create a table for Range Type demonstration
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    room_number INT NOT NULL,
    booking_period TSRANGE -- Time Stamp Range
);
INSERT INTO bookings (room_number, booking_period) VALUES
(101, '[2025-08-01 10:00:00, 2025-08-01 12:00:00)'), -- Inclusive start, exclusive end
(102, '[2025-08-05 14:00:00, 2025-08-05 16:00:00)');
```

-----

#### **1. Common Data Types**

PostgreSQL offers a rich set of built-in data types. Choosing the correct one is crucial for efficient storage, performance, and data integrity.

  * **`INTEGER` (`INT`), `SMALLINT`, `BIGINT`:**

      * **Purpose:** Whole numbers. Choose based on the expected range of values.
      * `SMALLINT`: -32,768 to +32,767 (2 bytes)
      * `INTEGER`: -2,147,483,648 to +2,147,483,647 (4 bytes) - Most common choice for IDs and counts.
      * `BIGINT`: -9,223,372,036,854,775,808 to +9,223,372,036,854,775,807 (8 bytes) - For very large numbers, like social media post counts or financial transactions.
      * **`SERIAL`, `BIGSERIAL`**: Pseudo-types that automatically create a sequence and assign `NOT NULL` to an `INTEGER` or `BIGINT` column, often used for auto-incrementing primary keys.
      * **Example:** `employee_id SERIAL PRIMARY KEY`

  * **`NUMERIC(precision, scale)` / `DECIMAL(precision, scale)`:**

      * **Purpose:** Exact numeric values. Use for monetary amounts, measurements, or any value where exact precision is required.
      * `precision`: Total number of digits (before and after the decimal point).
      * `scale`: Number of digits after the decimal point.
      * **Example:** `salary NUMERIC(10, 2)` can store up to 10 digits in total, with 2 digits after the decimal (e.g., 99999999.99).
      * **Ineffectiveness of `FLOAT` or `REAL` for monetary data:** While `FLOAT` and `REAL` are faster for calculations, they are *approximate* numeric types due to floating-point arithmetic. This can lead to rounding errors that are unacceptable for financial data. Always use `NUMERIC` for precise values.

  * **`VARCHAR(n)`, `TEXT`:**

      * **Purpose:** Character strings.
      * `VARCHAR(n)`: Variable-length string with a specified maximum length `n`.
      * `TEXT`: Variable-length string with virtually unlimited length (up to 1 GB).
      * **When to use which:**
          * `VARCHAR(n)`: When you have a strict maximum length (e.g., a country code `VARCHAR(3)`). The database still stores `VARCHAR` efficiently (only using space for actual characters), but the length constraint provides data validation.
          * `TEXT`: For long, free-form text like descriptions, comments, or articles. Generally, for performance, there's little difference between `VARCHAR` without a length and `TEXT`. PostgreSQL optimizes storage for both.
      * **Example:** `product_name VARCHAR(255)`, `description TEXT`

  * **`BOOLEAN`:**

      * **Purpose:** True/false values.
      * **Storage:** Stored as a single byte.
      * **Accepts:** `TRUE`, `FALSE`, `'t'`, `'f'`, `'true'`, `'false'`, `'y'`, `'n'`, `'yes'`, `'no'`, `'1'`, `'0'`.
      * **Example:** `is_active BOOLEAN DEFAULT TRUE`

  * **`DATE`:**

      * **Purpose:** Stores only a calendar date (year, month, day).
      * **Example:** `hire_date DATE` (`'2025-07-26'`)

  * **`TIME`:**

      * **Purpose:** Stores only a time of day (hour, minute, second).
      * **Variations:** `TIME [ (p) ] [ WITHOUT TIME ZONE ]`, `TIME [ (p) ] WITH TIME ZONE`. `(p)` is precision for fractional seconds.
      * **Example:** `start_time TIME` (`'13:30:00'`)

  * **`TIMESTAMP` (`TIMESTAMP WITHOUT TIME ZONE`), `TIMESTAMPTZ` (`TIMESTAMP WITH TIME ZONE`):**

      * **Purpose:** Stores both date and time.
      * **`TIMESTAMP` (without time zone):** Stores the date and time exactly as provided. It does *not* store any time zone information.
      * **`TIMESTAMPTZ` (with time zone):** Stores the date and time in UTC (Coordinated Universal Time). When you insert a value, PostgreSQL converts it from your session's time zone to UTC. When you retrieve it, it converts it back to your session's time zone. This is generally preferred for applications that need to handle global users or distributed systems, as it avoids time zone ambiguities.
      * **Example:** `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`, `last_updated TIMESTAMPTZ`

  * **`JSONB`:**

      * **Purpose:** Stores JSON data in a decomposed binary format. This is incredibly powerful for semi-structured data, enabling indexing and efficient querying within the JSON structure.
      * **Advantages over `JSON` (which stores raw text):**
          * **Efficiency:** Faster processing because it's pre-parsed.
          * **Indexing:** Can be indexed for performance (using GIN indexes).
          * **Validation:** Automatically removes insignificant whitespace and duplicate keys.
      * **Example:** `metadata JSONB`
        ```json
        {"preferred_contact": "email", "office_location": "Building A"}
        ```
      * **Ineffectiveness of `TEXT` for JSON:** Storing JSON as `TEXT` means you can't query inside the JSON document directly in SQL without complex string manipulations, and you can't index it for performance, making it highly inefficient for searching or filtering on JSON content.

  * **`UUID` (Universally Unique Identifier):**

      * **Purpose:** 128-bit numbers used to uniquely identify information in distributed computing environments. Extremely low probability of collision.
      * **Advantages:** Can be generated by clients or database, useful in distributed systems, avoids sequence contention in high-write scenarios.
      * **Disadvantages:** Larger than `BIGINT`, can lead to index fragmentation if not carefully managed (e.g., using `uuid_ossp` extension's `uuid_generate_v1mc()` or storing UUIDs as `TEXT` and indexing carefully).
      * **Example:** `unique_id UUID DEFAULT gen_random_uuid()` (requires `pgcrypto` or `uuid-ossp` extension to be enabled for `gen_random_uuid()` or `uuid_generate_v4()`).

-----

#### **2. Specialized Data Types**

PostgreSQL extends beyond common types with powerful specialized data types for complex scenarios.

  * **Arrays (`[]`):**

      * **Purpose:** Stores a list of values of a single data type in a single column.
      * **Syntax:** `DATATYPE[]`
      * **Example:** `assigned_tags TEXT[]` (an array of text strings).
        ```sql
        -- Querying array data
        SELECT project_name, assigned_tags
        FROM projects
        WHERE 'web' = ANY(assigned_tags); -- Find projects with 'web' tag

        -- Accessing array elements
        SELECT assigned_tags[1] AS first_tag, assigned_tags[2] AS second_tag
        FROM projects WHERE project_name = 'Website Redesign';
        ```
      * **Ineffectiveness of storing comma-separated strings:** Storing lists as comma-separated strings (`'tag1,tag2,tag3'`) in a `VARCHAR`/`TEXT` column violates 1NF (atomic values). It makes querying (e.g., "find all records containing 'tag2'") incredibly difficult and inefficient, requiring `LIKE` patterns or complex string parsing. Arrays provide native, indexed support for lists.

  * **Composite Types (Row Types):**

      * **Purpose:** Allows you to define a custom data type that is a structured collection of fields, similar to a `STRUCT` or `RECORD` in other programming languages.
      * **Use Cases:** Passing complex data structures to/from functions, or defining columns that are themselves structured.
      * **Example:**
        ```sql
        -- Define a composite type for an address
        CREATE TYPE address_type AS (
            street VARCHAR(100),
            city VARCHAR(50),
            zip_code VARCHAR(10)
        );

        -- Use it as a column type
        ALTER TABLE employees ADD COLUMN mailing_address address_type;

        -- Insert data into composite type
        UPDATE employees
        SET mailing_address = ('123 Main St', 'Anytown', '12345')
        WHERE employee_id = 1;

        -- Accessing fields within a composite type
        SELECT (mailing_address).city FROM employees WHERE employee_id = 1;
        ```
      * **Ineffectiveness:** Without composite types, you'd have to use separate columns for each field (e.g., `street_address`, `city_address`, `zip_code_address`), which can make schemas more verbose for logically grouped data.

  * **Range Types:**

      * **Purpose:** Represents a range of values of a specific base type (e.g., integers, dates, timestamps).
      * **Built-in:** `INT4RANGE` (integer), `INT8RANGE` (bigint), `NUMRANGE` (numeric), `DATERANGE` (date), `TSRANGE` (timestamp), `TSTZRANGE` (timestamptz).
      * **Operators:** Support for various range operators (`@>` contains, `<@` contained by, `&&` overlaps, `+` union, `-` difference).
      * **Use Cases:** Scheduling, booking systems, validity periods.
      * **Example:** `booking_period TSRANGE`
        ```sql
        -- Check for overlapping bookings
        SELECT b1.booking_id, b2.booking_id
        FROM bookings b1, bookings b2
        WHERE b1.booking_id != b2.booking_id
          AND b1.room_number = b2.room_number
          AND b1.booking_period && b2.booking_period; -- The '&&' operator checks for overlap
        ```
      * **Ineffectiveness:** Manually managing ranges with two separate `start_date` and `end_date` columns requires more complex `WHERE` clauses (e.g., `(start1 <= end2 AND end1 >= start2)`) and doesn't allow for native indexing of the range itself.

  * **`ENUM` (Enumerated Types):**

      * **Purpose:** Creates a static, ordered list of values for a column. The column can only store one of the values defined in the `ENUM` type.
      * **Advantages:** Improved data integrity (ensures only valid values are stored), better readability than magic strings/integers, more storage efficient than `VARCHAR` for a small, fixed set of values.
      * **Example:** `traffic_light_state AS ENUM ('red', 'yellow', 'green')`
        ```sql
        SELECT location, current_state FROM intersections;
        -- UPDATE intersections SET current_state = 'blue'; -- This would cause an error!
        UPDATE intersections SET current_state = 'green' WHERE location = 'Main & Elm';
        ```
      * **Ineffectiveness of `VARCHAR` with `CHECK` constraints:** While you can use `VARCHAR` with a `CHECK (column IN ('red', 'yellow', 'green'))` constraint, `ENUM` types are more explicit, provide better type safety, and can be more performant as they are stored internally as integers.

-----

#### **3. Built-in Functions**

PostgreSQL provides hundreds of built-in functions to manipulate and transform data.

**3.1. String Functions:**

  * **`LOWER(string)` / `UPPER(string)`:** Converts string to lowercase/uppercase.
    ```sql
    SELECT LOWER(first_name), UPPER(last_name) FROM employees LIMIT 2;
    ```
  * **`LENGTH(string)`:** Returns the length of the string in characters.
    ```sql
    SELECT first_name, LENGTH(first_name) AS name_length FROM employees LIMIT 2;
    ```
  * **`SUBSTRING(string, start, length)`:** Extracts a portion of a string.
    ```sql
    SELECT SUBSTRING('PostgreSQL', 5, 4); -- Result: 'greS'
    ```
  * **`TRIM([BOTH | LEADING | TRAILING] [characters FROM] string)`:** Removes characters from the beginning, end, or both.
    ```sql
    SELECT TRIM('   Hello World   '); -- Result: 'Hello World'
    SELECT TRIM(BOTH 'x' FROM 'xxHello Worldxx'); -- Result: 'Hello World'
    ```
  * **`CONCAT(string1, string2, ...)` / `||` operator:** Concatenates strings.
    ```sql
    SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees LIMIT 2;
    SELECT first_name || ' ' || last_name AS full_name FROM employees LIMIT 2;
    ```
  * **`REPLACE(string, from, to)`:** Replaces all occurrences of a substring.
    ```sql
    SELECT REPLACE('Hello World', 'World', 'PostgreSQL'); -- Result: 'Hello PostgreSQL'
    ```
  * **`POSITION(substring IN string)`:** Returns the starting position of the first occurrence of a substring.
    ```sql
    SELECT POSITION('SQL' IN 'PostgreSQL'); -- Result: 5
    ```

**3.2. Numeric Functions:**

  * **`ROUND(number, decimal_places)`:** Rounds a number to a specified number of decimal places.
    ```sql
    SELECT ROUND(75.1234, 2); -- Result: 75.12
    ```
  * **`CEIL(number)` / `CEILING(number)`:** Rounds a number up to the nearest integer.
    ```sql
    SELECT CEIL(75.12); -- Result: 76
    ```
  * **`FLOOR(number)`:** Rounds a number down to the nearest integer.
    ```sql
    SELECT FLOOR(75.99); -- Result: 75
    ```
  * **`ABS(number)`:** Returns the absolute value of a number.
    ```sql
    SELECT ABS(-100); -- Result: 100
    ```
  * **`POWER(base, exponent)`:** Raises a base to the power of an exponent.
    ```sql
    SELECT POWER(2, 3); -- Result: 8
    ```
  * **`MOD(dividend, divisor)`:** Returns the remainder of a division.
    ```sql
    SELECT MOD(10, 3); -- Result: 1
    ```

**3.3. Date and Time Functions:**

  * **`NOW()` / `CURRENT_TIMESTAMP`:** Returns the current date and time with time zone (as `TIMESTAMPTZ`).
    ```sql
    SELECT NOW(), CURRENT_TIMESTAMP;
    ```
  * **`CURRENT_DATE`:** Returns the current date (as `DATE`).
    ```sql
    SELECT CURRENT_DATE;
    ```
  * **`CURRENT_TIME`:** Returns the current time with time zone (as `TIMESTAMPTZ`).
    ```sql
    SELECT CURRENT_TIME;
    ```
  * **`EXTRACT(field FROM source)`:** Extracts a specific part (e.g., year, month, day, hour) from a date/time value.
    ```sql
    SELECT
        first_name,
        hire_date,
        EXTRACT(YEAR FROM hire_date) AS hire_year,
        EXTRACT(MONTH FROM hire_date) AS hire_month
    FROM employees
    LIMIT 3;
    ```
  * **`AGE(timestamp1, timestamp2)`:** Calculates the difference between two timestamps as an interval.
    ```sql
    SELECT AGE(CURRENT_DATE, '2022-01-15'); -- How long since 2022-01-15
    -- Result: 3 years 6 mons 11 days (approx based on current date)
    ```
  * **`TO_CHAR(timestamp, format)`:** Formats a date/time/numeric value into a string according to a specified format. Very useful for presentation.
    ```sql
    SELECT TO_CHAR(CURRENT_TIMESTAMP, 'YYYY-MM-DD HH24:MI:SS');
    SELECT TO_CHAR(salary, 'FM99,999.00') FROM employees LIMIT 1;
    ```
  * **`TO_DATE(string, format)` / `TO_TIMESTAMP(string, format)`:** Converts a string to a `DATE` or `TIMESTAMP` based on a format. Essential for parsing date strings from external sources.
    ```sql
    SELECT TO_DATE('2025/07/26', 'YYYY/MM/DD');
    SELECT TO_TIMESTAMP('2025-07-26 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
    ```

**3.4. Type Casting (`::` operator or `CAST()` function):**

  * **Purpose:** Explicitly converts a value from one data type to another.
  * **Syntax:** `value::target_datatype` or `CAST(value AS target_datatype)`
  * **When to use:** When PostgreSQL cannot implicitly convert a type, or to ensure a specific type for an operation or function.

**Example:**

```sql
-- Convert an integer to text
SELECT 123::TEXT; -- Result: '123'

-- Convert a text string to an integer
SELECT '456'::INTEGER; -- Result: 456

-- Calculate average salary as a numeric with 0 decimal places
SELECT AVG(salary)::NUMERIC(10, 0) FROM employees;

-- Convert salary to text for concatenation (though || implicitly handles this)
SELECT first_name || ' earns ' || CAST(salary AS TEXT) || ' per year.' FROM employees LIMIT 2;
```

  * **Ineffectiveness of relying solely on implicit casting:** While PostgreSQL often performs implicit casting, explicit casting makes your intentions clear, prevents unexpected errors (e.g., trying to cast a non-numeric string to an integer), and can sometimes aid the query planner.

-----

#### **4. User-Defined Functions (UDFs) and Stored Procedures (PL/pgSQL Basics)**

Beyond built-in functions, PostgreSQL allows you to create your own custom logic in the form of User-Defined Functions (UDFs) and Stored Procedures using various procedural languages, most commonly **PL/pgSQL**.

  * **User-Defined Functions (UDFs):**

      * **Purpose:** Encapsulate a piece of logic that returns a value (or a set of values/rows). They can take input parameters.
      * **Calling:** Can be called directly in `SELECT` statements, `WHERE` clauses, or as part of expressions, just like built-in functions.
      * **`RETURNS` Clause:** Mandatory, specifies the data type of the value(s) returned.
      * **`LANGUAGE plpgsql`:** Specifies the procedural language used.

    **Example: Scalar Function**

    ```sql
    CREATE OR REPLACE FUNCTION get_full_name(
        p_first_name VARCHAR,
        p_last_name VARCHAR
    )
    RETURNS VARCHAR
    LANGUAGE plpgsql
    AS $$
    BEGIN
        RETURN p_first_name || ' ' || p_last_name;
    END;
    $$;

    -- Call the function
    SELECT get_full_name('Alice', 'Brown'); -- Result: 'Alice Brown'
    SELECT get_full_name(first_name, last_name) FROM employees WHERE employee_id = 1;
    ```

    **Example: Function Returning a Table (SETOF)**

    ```sql
    CREATE OR REPLACE FUNCTION get_employees_by_department(
        p_department_name VARCHAR
    )
    RETURNS SETOF employees -- Returns a set of rows with the structure of the employees table
    LANGUAGE plpgsql
    AS $$
    BEGIN
        RETURN QUERY
        SELECT *
        FROM employees
        WHERE department = p_department_name
        ORDER BY last_name, first_name;
    END;
    $$;

    -- Call the function
    SELECT * FROM get_employees_by_department('Sales');
    ```

  * **Stored Procedures (PostgreSQL 11+):**

      * **Purpose:** Perform a sequence of operations that typically do *not* return a value but rather manage state, execute DDL, or control transactions.
      * **Key Difference from Functions:** Procedures can commit or rollback transactions within the procedure, whereas a function is always executed within the transaction it was called in and cannot perform transaction control directly. Procedures use `CALL` instead of `SELECT`.
      * **`LANGUAGE plpgsql`:** Specifies the procedural language.

    **Example: Stored Procedure**

    ```sql
    CREATE OR REPLACE PROCEDURE transfer_funds(
        sender_account_id INT,
        receiver_account_id INT,
        amount NUMERIC
    )
    LANGUAGE plpgsql
    AS $$
    BEGIN
        -- Start a transaction implicitly by the CALL, or explicitly with BEGIN;
        UPDATE Accounts SET balance = balance - amount WHERE account_id = sender_account_id;
        UPDATE Accounts SET balance = balance + amount WHERE account_id = receiver_account_id;

        -- Example of conditional logic and error handling (more in later chapters)
        IF (SELECT balance FROM Accounts WHERE account_id = sender_account_id) < 0 THEN
            RAISE EXCEPTION 'Insufficient funds in sender account %', sender_account_id;
        END IF;

        -- Implicit COMMIT if no errors, or explicit COMMIT;
    END;
    $$;

    -- Call the procedure (assuming an 'Accounts' table exists from Chapter 1's ACID example)
    -- CALL transfer_funds(1, 2, 100.00);
    ```

  * **PL/pgSQL Basics (Procedural Language for PostgreSQL):**

      * **Blocks:** All PL/pgSQL code is structured in blocks, often with `DECLARE`, `BEGIN`, and `END` sections.
      * **Variables:** Declared in the `DECLARE` section.
      * **Control Structures:** `IF/THEN/ELSIF/ELSE/END IF`, `LOOP`, `FOR`, `WHILE`.
      * **Error Handling:** `EXCEPTION` blocks (`BEGIN ... EXCEPTION ... END`).
      * **Dynamic SQL:** `EXECUTE` statement for constructing and running SQL commands dynamically.

  * **Why use UDFs/Procedures (Alternatives and Ineffectiveness):**

      * **Encapsulation & Reusability:** Avoids repeating complex SQL logic across multiple application codebases.
      * **Performance:** Reduces network round trips between application and database. Can sometimes enable the database to perform optimizations if the logic stays within the database.
      * **Security:** Grants execution privileges on the function/procedure without granting direct table access, enhancing security.
      * **Business Logic Enforcement:** Critical business rules can be enforced at the database level, ensuring consistency regardless of which application uses the data.
      * **Ineffectiveness of solely application-side logic:** While modern applications often prefer business logic in the application layer, crucial, highly performant, or security-sensitive operations often benefit immensely from being encapsulated in database functions/procedures. Relying entirely on the application for complex multi-step data operations means more network calls, potentially slower execution, and scattered business logic.