### **Chapter 4: Advanced SQL - Aggregates, Grouping, and Subqueries**

This chapter delves into powerful SQL constructs that enable data summarization, conditional grouping, and the creation of nested or modular queries. You'll learn to extract deeper insights from your data and structure complex queries for clarity and performance.

-----

Let's ensure our sample database is ready for these advanced queries. If you've been following along, your `employees`, `departments`, `projects`, and `employee_projects` tables should be in good shape. Let's add a few more data points to cover edge cases for aggregates and subqueries.

```sql
-- Add a new employee with a NULL salary for AVG/SUM examples
INSERT INTO employees (first_name, last_name, employee_email, department, department_id)
VALUES ('Zack', 'Johnson', 'zack.j@example.com', 'Sales', (SELECT dept_id FROM departments WHERE dept_name = 'Sales'));

-- Add another employee with a new department for GROUP BY examples
INSERT INTO departments (dept_name, location) VALUES ('R&D', 'Austin');
INSERT INTO employees (first_name, last_name, employee_email, salary, department, department_id)
VALUES ('Yara', 'Ahmed', 'yara.a@example.com', 95000.00, 'R&D', (SELECT dept_id FROM departments WHERE dept_name = 'R&D'));

-- Add more project assignments to make aggregates interesting
INSERT INTO employee_projects (employee_id, project_id, role) VALUES
((SELECT employee_id FROM employees WHERE first_name = 'Peter' AND last_name = 'Jones'),
 (SELECT project_id FROM projects WHERE project_name = 'Sales Analytics'), 'Analyst'),
((SELECT employee_id FROM employees WHERE first_name = 'Grace' AND last_name = 'Miller'),
 (SELECT project_id FROM projects WHERE project_name = 'Cloud Migration'), 'Lead Architect');
```

-----

#### **1. Aggregate Functions: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`**

Aggregate functions perform calculations on a set of rows and return a single summary value. They are typically used with the `GROUP BY` clause to summarize data for each group, or on the entire result set if `GROUP BY` is omitted.

  * **`COUNT()`**: Counts the number of rows or non-NULL values.

      * `COUNT(*)`: Counts all rows, including those with NULL values in any column.
      * `COUNT(column_name)`: Counts non-NULL values in the specified column.
      * `COUNT(DISTINCT column_name)`: Counts unique, non-NULL values in the specified column.

    **Example:**

    ```sql
    -- Count total number of employees
    SELECT COUNT(*) AS total_employees FROM employees;

    -- Count employees with an email address
    SELECT COUNT(employee_email) AS employees_with_email FROM employees;

    -- Count distinct departments
    SELECT COUNT(DISTINCT department) AS distinct_departments FROM employees;
    ```

      * **Alternatives and Ineffectiveness:** Fetching all rows and counting/de-duplicating in application code is highly inefficient for large datasets, consumes more memory and network bandwidth, and shifts processing burden from the optimized database engine to the application.

  * **`SUM(column_name)`**: Calculates the sum of all non-NULL values in a numeric column.

    **Example:**

    ```sql
    -- Calculate total salary expense
    SELECT SUM(salary) AS total_salary_expense FROM employees;
    ```

      * **Ineffectiveness:** Similar to `COUNT()`, summing in application code is inefficient.

  * **`AVG(column_name)`**: Calculates the average of all non-NULL values in a numeric column.

    **Example:**

    ```sql
    -- Calculate the average salary
    SELECT AVG(salary) AS average_salary FROM employees;
    ```

      * **Note on NULLs:** `AVG()` (and `SUM()`, `MIN()`, `MAX()`) **ignores NULL values**. So, Emily Chen's `salary` (if NULL) and Zack Johnson's `salary` (if NULL) would be excluded from the average calculation. If you want to treat NULLs as zero, you need to use `COALESCE`: `AVG(COALESCE(salary, 0))`.

  * **`MIN(column_name)`**: Returns the minimum non-NULL value in a column.

  * **`MAX(column_name)`**: Returns the maximum non-NULL value in a column.

    **Example:**

    ```sql
    -- Find the highest and lowest salary
    SELECT
        MIN(salary) AS lowest_salary,
        MAX(salary) AS highest_salary
    FROM employees;

    -- Find the earliest and latest hire dates
    SELECT
        MIN(hire_date) AS earliest_hire_date,
        MAX(hire_date) AS latest_hire_date
    FROM employees;
    ```

-----

#### **2. `GROUP BY` Clause: Summarizing Data**

The `GROUP BY` clause is used with aggregate functions to group rows that have the same values in specified columns into summary rows. It allows you to perform calculations *per group* rather than on the entire dataset.

**Syntax:**

```sql
SELECT column1, aggregate_function(column2)
FROM table_name
GROUP BY column1, column3, ...; -- All non-aggregated columns in SELECT must be in GROUP BY
```

**Rule:** Any column present in the `SELECT` list that is *not* an aggregate function (e.g., `COUNT(*)`, `SUM(salary)`) *must* appear in the `GROUP BY` clause. This is because the database needs to know which columns define the groups.

**Example:**

```sql
-- Calculate the average salary for each department
SELECT
    department,
    AVG(salary) AS average_department_salary
FROM
    employees
GROUP BY
    department;

-- Count employees in each department and show the department's location
SELECT
    d.dept_name,
    d.location,
    COUNT(e.employee_id) AS num_employees
FROM
    departments AS d
LEFT JOIN -- Use LEFT JOIN to include departments with no employees
    employees AS e ON d.dept_id = e.department_id
GROUP BY
    d.dept_name, d.location -- Both non-aggregated columns from SELECT must be here
ORDER BY
    num_employees DESC;
```

  * **Alternatives and Ineffectiveness:** Without `GROUP BY`, you'd have to retrieve all detailed rows and then loop through them in application code, performing manual aggregation. This is incredibly inefficient for large datasets, prone to errors, and puts a heavy processing load on the application rather than the highly optimized database.

-----

#### **3. `HAVING` Clause: Filtering Grouped Data**

The `HAVING` clause is used to filter the results of a `GROUP BY` query, applying conditions to the *aggregated* values. It is applied *after* `GROUP BY` and *before* `ORDER BY` and `LIMIT`.

**Important Distinction: `WHERE` vs. `HAVING`**

  * **`WHERE`**: Filters *individual rows* *before* grouping and aggregation.
  * **`HAVING`**: Filters *groups* *after* grouping and aggregation.

**Syntax:**

```sql
SELECT column1, aggregate_function(column2)
FROM table_name
GROUP BY column1
HAVING aggregate_condition;
```

**Example:**

```sql
-- Find departments with an average salary greater than 70000
SELECT
    department,
    AVG(salary) AS average_salary
FROM
    employees
GROUP BY
    department
HAVING
    AVG(salary) > 70000;

-- Find departments that have more than 2 employees
SELECT
    d.dept_name,
    COUNT(e.employee_id) AS num_employees
FROM
    departments AS d
INNER JOIN -- Using INNER JOIN because we only care about departments with employees
    employees AS e ON d.dept_id = e.department_id
GROUP BY
    d.dept_name
HAVING
    COUNT(e.employee_id) > 2;
```

  * **Alternatives and Ineffectiveness:** Trying to use `WHERE` with aggregate functions will result in an error (`aggregate functions are not allowed in WHERE clause`). Simulating `HAVING` in application code would require fetching all aggregated groups, then iterating and filtering, which is less efficient and more cumbersome.

-----

#### **4. Subqueries**

A **subquery** (or inner query, nested query) is a query embedded inside another SQL query. Subqueries can return a single value (scalar), a single row, a single column, or an entire table. They must always be enclosed in parentheses.

**4.1. Scalar Subqueries**

  * **Returns:** A single value (one row, one column).
  * **Usage:** Can be used anywhere an expression is expected (e.g., `SELECT` list, `WHERE` clause, `SET` clause in `UPDATE`).

**Example:**

```sql
-- Find employees whose salary is greater than the overall average salary
SELECT
    first_name,
    last_name,
    salary
FROM
    employees
WHERE
    salary > (SELECT AVG(salary) FROM employees); -- Scalar subquery
```

  * **Alternatives and Ineffectiveness:** Without a scalar subquery, you'd have to run two separate queries (one to get the average, then another to get employees), potentially involving application-level processing and state management, which is less efficient and less atomic.

**4.2. Row Subqueries**

  * **Returns:** A single row with multiple columns.
  * **Usage:** Typically used in `WHERE` clauses, often with comparison operators that can compare multiple column values simultaneously.

**Example:**

```sql
-- Find the employee who has the highest salary in the 'Engineering' department
-- (Assuming unique highest salary in that dept)
SELECT
    first_name,
    last_name,
    salary,
    department
FROM
    employees
WHERE
    (department, salary) = (SELECT 'Engineering', MAX(salary) FROM employees WHERE department = 'Engineering');
```

  * **Alternatives and Ineffectiveness:** Trying to achieve this with multiple `WHERE` clauses (`WHERE department = 'Engineering' AND salary = (SELECT MAX(salary) FROM employees WHERE department = 'Engineering')`) is often less readable for complex multi-column comparisons or might not accurately capture the intent if multiple rows could match one of the conditions.

**4.3. Table Subqueries**

  * **Returns:** An entire virtual table (multiple rows, multiple columns).
  * **Usage:** Can be used in the `FROM` clause (acting like a derived table or inline view) or with operators like `IN`, `EXISTS`.

**Example:**

```sql
-- Find employees who work on projects (using the employee_projects table)
SELECT
    e.first_name,
    e.last_name,
    e.employee_email
FROM
    employees AS e
WHERE
    e.employee_id IN (SELECT DISTINCT employee_id FROM employee_projects);

-- Using a table subquery in the FROM clause (derived table)
SELECT
    d.dept_name,
    emp_counts.num_employees
FROM
    departments AS d
JOIN
    (SELECT department_id, COUNT(*) AS num_employees FROM employees GROUP BY department_id) AS emp_counts
ON
    d.dept_id = emp_counts.department_id
WHERE
    emp_counts.num_employees > 1;
```

  * **Alternatives and Ineffectiveness:** Without table subqueries, you'd be forced into more complex `JOIN` structures or multiple separate queries, often leading to less readable or less performant solutions.

**4.4. Correlated Subqueries**

  * **Definition:** A subquery that depends on the outer query for its values. It executes once for *each row* processed by the outer query.
  * **Performance Note:** Can be less performant than other subquery types or joins because of their row-by-row execution. Use them when other options are not suitable, or when the outer query's result set is small.
  * **Usage:** Commonly used with `EXISTS` or `NOT EXISTS` operators.

**Example:**

```sql
-- Find departments that have at least one employee earning more than 80000
SELECT
    d.dept_name
FROM
    departments AS d
WHERE EXISTS (
    SELECT 1 -- We just need to know if any row exists
    FROM employees AS e
    WHERE e.department_id = d.dept_id -- Correlated part: 'd.dept_id' comes from the outer query
      AND e.salary > 80000
);

-- Find employees whose salary is higher than the average salary *in their own department*
SELECT
    e1.first_name,
    e1.last_name,
    e1.salary,
    e1.department
FROM
    employees AS e1
WHERE
    e1.salary > (
        SELECT AVG(e2.salary)
        FROM employees AS e2
        WHERE e2.department_id = e1.department_id -- Correlated part
    );
```

  * **Alternatives and Ineffectiveness:** For the second example, without a correlated subquery, you'd likely need to use window functions (covered in a later chapter) or a more complex join with aggregation, which might be overkill or less intuitive for this specific logic. However, for large datasets, `JOIN` with `GROUP BY` or window functions are often more performant than correlated subqueries.

-----

#### **5. Common Table Expressions (CTEs) with `WITH` Clause: Improving Readability and Reusability**

CTEs (also known as `WITH` queries) allow you to define a temporary, named result set that you can reference within a single SQL statement (`SELECT`, `INSERT`, `UPDATE`, `DELETE`). They are immensely powerful for breaking down complex queries into smaller, more readable, and manageable parts.

  * **Benefits:**
      * **Readability:** Simplifies complex, multi-step queries.
      * **Reusability:** A CTE can be referenced multiple times within the same query.
      * **Modularity:** Makes queries easier to debug and understand.
      * **Recursion:** Enables recursive queries (for hierarchical data like organizational charts), which we'll explore in a later chapter.

**Syntax:**

```sql
WITH cte_name_1 AS (
    SELECT ...
),
cte_name_2 AS (
    SELECT ... FROM cte_name_1 ...
)
SELECT ... FROM cte_name_1 JOIN cte_name_2 ...;
```

**Example:**
Let's find departments with more than 2 employees and their average salary, using CTEs.

```sql
WITH DepartmentEmployeeCounts AS (
    SELECT
        d.dept_id,
        d.dept_name,
        COUNT(e.employee_id) AS num_employees
    FROM
        departments AS d
    LEFT JOIN
        employees AS e ON d.dept_id = e.department_id
    GROUP BY
        d.dept_id, d.dept_name
    HAVING
        COUNT(e.employee_id) > 2
),
DepartmentAverageSalaries AS (
    SELECT
        department_id,
        AVG(salary) AS avg_dept_salary
    FROM
        employees
    WHERE
        salary IS NOT NULL -- Exclude employees with NULL salaries from average calculation
    GROUP BY
        department_id
)
SELECT
    dec.dept_name,
    dec.num_employees,
    das.avg_dept_salary
FROM
    DepartmentEmployeeCounts AS dec
JOIN
    DepartmentAverageSalaries AS das ON dec.dept_id = das.department_id
ORDER BY
    dec.num_employees DESC;
```

  * **Alternatives and Ineffectiveness:** Without CTEs, you'd often resort to deeply nested subqueries in the `FROM` clause, making the SQL extremely difficult to read, debug, and maintain. For instance, the example above would involve nesting the `DepartmentEmployeeCounts` query and `DepartmentAverageSalaries` query directly, which quickly becomes unmanageable. CTEs are essential for complex, multi-step data transformations.

-----

#### **6. Set Operations: `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`**

Set operations combine the result sets of two or more `SELECT` statements. For these operations to work, the `SELECT` statements must have:

1.  The same number of columns.
2.  Corresponding columns with compatible data types (implicit type casting might occur).

**6.1. `UNION`**

  * **Purpose:** Combines the result sets of two or more `SELECT` statements and returns *distinct* rows. It automatically removes duplicates.

**Syntax:**

```sql
SELECT column1, column2 FROM table1
UNION
SELECT column1, column2 FROM table2;
```

**Example:**
Let's find unique last names from employees and project names that resemble surnames.

```sql
SELECT last_name AS name_or_project FROM employees
UNION
SELECT project_name FROM projects WHERE project_name LIKE '%App%' OR project_name LIKE '%Site%';
```

  * **Result:** A single list of unique values from both queries. Duplicates are removed.
  * **Ineffectiveness of `UNION` without `DISTINCT` or application-side de-duplication:** Fetching all data and de-duplicating in the application is slow and resource-intensive for large result sets.

**6.2. `UNION ALL`**

  * **Purpose:** Combines the result sets of two or more `SELECT` statements and returns *all* rows, including duplicates. It is generally faster than `UNION` because it doesn't perform a de-duplication step.

**Syntax:**

```sql
SELECT column1, column2 FROM table1
UNION ALL
SELECT column1, column2 FROM table2;
```

**Example:**
Combine all first names and last names from employees into one list, showing duplicates.

```sql
SELECT first_name AS employee_part_name FROM employees
UNION ALL
SELECT last_name FROM employees;
```

  * **Result:** A list of all first and last names, including any duplicates.
  * **When to use `UNION ALL` vs. `UNION`:** Use `UNION ALL` when you know there are no duplicates or when you *want* to keep duplicates (e.g., for counting total occurrences). Use `UNION` when you specifically need distinct results.

**6.3. `INTERSECT`**

  * **Purpose:** Returns only the rows that are present in *both* result sets.

**Syntax:**

```sql
SELECT column1, column2 FROM table1
INTERSECT
SELECT column1, column2 FROM table2;
```

**Example:**
Find departments that appear in both the `employees` table (via `department` column) and the `departments` table (via `dept_name`).

```sql
SELECT department FROM employees WHERE department IS NOT NULL
INTERSECT
SELECT dept_name FROM departments;
```

  * **Result:** Only department names that exist in *both* lists. (e.g., 'Sales', 'Marketing', 'Engineering', 'Human Resources', 'Finance', 'R\&D').

**6.4. `EXCEPT` (or `MINUS` in some other SQL dialects like Oracle)**

  * **Purpose:** Returns rows that are present in the *first* `SELECT` statement but *not* in the second `SELECT` statement.

**Syntax:**

```sql
SELECT column1, column2 FROM table1
EXCEPT
SELECT column1, column2 FROM table2;
```

**Example:**
Find departments mentioned in the `employees` table that *do not* have a corresponding entry in the `departments` table. (This could indicate data inconsistency if foreign keys weren't strictly enforced).

```sql
SELECT department FROM employees WHERE department IS NOT NULL
EXCEPT
SELECT dept_name FROM departments;
```

  * **Result:** This query should ideally return an empty set if your data is perfectly consistent with foreign keys. If an employee had `department = 'IT'` but there's no 'IT' in `departments`, 'IT' would appear here.

  * **Alternatives and Ineffectiveness for `INTERSECT` and `EXCEPT`:** Simulating these with `JOIN`s (e.g., `INNER JOIN` for `INTERSECT` or `LEFT JOIN` with `WHERE column IS NULL` for `EXCEPT`) is possible but often less readable and potentially less optimized by the database engine for these specific set operations. Direct set operators are clearer and more concise for their intended purpose.