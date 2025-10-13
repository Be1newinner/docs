### **Chapter 6: Indexing for Performance**

This chapter demystifies the concept of database indexes, explaining why they are indispensable for query performance. You will learn the mechanics of various PostgreSQL index types, how to create them, and, crucially, when and when *not* to use them. We will also introduce `EXPLAIN ANALYZE`, your most powerful tool for understanding query execution.

-----

Let's continue with our `my_app_db` database. For indexing examples, having a reasonable amount of data is helpful. We'll stick to our `employees` and `projects` tables.

-----

#### **1. The Need for Indexes: Speeding Up Data Retrieval**

Imagine you have a physical encyclopedia with thousands of pages. If you want to find information about "PostgreSQL," you wouldn't start reading from page 1 until you found it. Instead, you'd go to the index at the back of the book, find "PostgreSQL," see the page numbers listed, and jump directly to those pages.

A database index works on the same principle.

  * **Without an Index (Sequential Scan / Full Table Scan):**

      * When you execute a `SELECT` query with a `WHERE` clause on a column that has no index (or the index is not used), the database engine must read *every single row* in the table, one by one, from beginning to end, to find the rows that match your condition.
      * This is called a **sequential scan** (or full table scan).
      * **Ineffectiveness:** For small tables, this is fine. For large tables (millions or billions of rows), a sequential scan is incredibly slow, consumes high I/O, and can bring your database to its knees, making your applications unresponsive.

  * **With an Index:**

      * An index is a special lookup table that the database search engine can use to speed up data retrieval.
      * It's a data structure (like a B-tree) that stores a sorted list of values from one or more columns, along with pointers (physical addresses or row IDs/TIDs) to the actual rows in the table where those values reside.
      * When a query uses an indexed column in its `WHERE` clause, the database can rapidly navigate the index to find the exact location of the relevant rows, instead of scanning the entire table.

**Analogy:** A phone book is indexed by last name. If you want to find "John Smith," you don't read every name. You jump to 'S', then 'Sm', etc. If it wasn't indexed, finding "John" would require reading every entry.

-----

#### **2. Understanding B-Tree Indexes: How They Work**

The **B-Tree** (Balanced Tree) is the default and most common type of index in PostgreSQL and most relational databases. It's incredibly versatile and efficient for a wide range of queries.

**How it Works:**

1.  **Tree Structure:** A B-Tree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time.
2.  **Nodes:**
      * **Root Node:** The top-most node.
      * **Internal Nodes:** Intermediate nodes that contain keys (indexed column values) and pointers to child nodes. They act like signposts, guiding the search down the tree.
      * **Leaf Nodes:** The bottom-most nodes that contain all the indexed values in sorted order, along with pointers (TIDs - Tuple IDs) to the actual data rows in the table.
3.  **Sorted Data:** All data within the B-Tree is kept in sorted order. This is key for range queries and sorting operations.
4.  **Balanced:** The "B" in B-Tree often stands for "balanced." This means that all leaf nodes are at the same depth, ensuring that the time to find any record is roughly consistent.
5.  **Search Process:**
      * To find a value, the database starts at the root node.
      * It compares the search value to the keys in the current node to determine which child node to descend into.
      * This process continues until it reaches a leaf node.
      * Once at the leaf node, it finds the specific key and uses the associated TID to jump directly to the data row in the table.

**Example: B-Tree on `last_name` column**

  * If you search `WHERE last_name = 'Smith'`, the database navigates the B-Tree quickly to the leaf node containing 'Smith' entries, then retrieves the corresponding table rows.
  * If you search `WHERE salary BETWEEN 50000 AND 70000`, the database finds the first relevant entry (50000) in the index and then traverses the sorted leaf nodes to find all entries up to 70000.

**Pros of B-Tree Indexes:**

  * Excellent for **equality comparisons** (`=`).
  * Excellent for **range queries** (`<`, `>`, `<=`, `>=`, `BETWEEN`).
  * Effective for **`ORDER BY`** clauses (as data is pre-sorted).
  * Effective for **`LIKE 'prefix%'`** searches (but not `'%'suffix'` or `'%substring%'`).
  * Support **multi-column indexes**, where the order of columns matters.

-----

#### **3. Creating Indexes: `CREATE INDEX`**

You use the `CREATE INDEX` statement to create a new index on one or more columns of a table.

**Basic Syntax:**

```sql
CREATE [UNIQUE] INDEX [index_name] ON table_name (column1 [ASC|DESC], column2 [ASC|DESC], ...);
```

  * **`UNIQUE` (Optional):** Creates a unique index, ensuring that all values in the indexed column(s) are unique across all rows. This effectively creates a `UNIQUE` constraint. `PRIMARY KEY` constraints automatically create a `UNIQUE B-Tree` index.
  * **`index_name` (Optional but Recommended):** A descriptive name for your index (e.g., `idx_employees_lastname_firstname`). If omitted, PostgreSQL generates a name.
  * **`table_name`:** The table on which the index is created.
  * **`column1, column2, ...`:** The column(s) to be indexed. For multi-column indexes, the order of columns is important (left-most columns are most effective for filtering).
  * **`ASC | DESC` (Optional):** Specifies ascending or descending order for each column. This can optimize `ORDER BY` queries.

**Example:**

```sql
-- Create a non-unique index on the last_name column
CREATE INDEX idx_employees_last_name ON employees (last_name);

-- Create a unique index on the employee_email column (to ensure uniqueness)
-- Note: We already added a UNIQUE constraint in Chapter 2, which implicitly creates this.
-- If not, this would be explicit:
-- CREATE UNIQUE INDEX uix_employees_email ON employees (employee_email);

-- Create a composite index on department and salary, useful for queries filtering by department
-- and then ordering or filtering by salary within that department.
CREATE INDEX idx_employees_dept_salary ON employees (department, salary DESC);
```

**`CREATE INDEX CONCURRENTLY` (Crucial for Production):**

  * When creating a large index, `CREATE INDEX` without `CONCURRENTLY` locks the table for writes (and sometimes reads) until the index is built. This can cause significant downtime in production.
  * `CREATE INDEX CONCURRENTLY` builds the index without taking a strong lock on the table. Writes can continue. It takes longer but minimizes downtime.
  * **Syntax:**
    ```sql
    CREATE INDEX CONCURRENTLY idx_employees_hire_date ON employees (hire_date);
    ```
  * **Ineffectiveness of `CREATE INDEX` without `CONCURRENTLY` in Production:** Causes application outages or severe performance degradation on busy tables. Always use `CONCURRENTLY` for schema changes in live systems.

-----

#### **4. Types of Indexes in PostgreSQL**

PostgreSQL supports several index types beyond the default B-Tree, each optimized for different data types and query patterns.

**4.1. B-Tree (Default)**

  * **Syntax:** `CREATE INDEX ... ON table (column);` (implicitly B-Tree)
  * **Primary Use Cases:**
      * Equality (`=`) and range (`<`, `>`, `BETWEEN`) queries on numeric, date, string, and UUID columns.
      * `JOIN` conditions.
      * `ORDER BY` and `GROUP BY` clauses.
      * `LIKE 'prefix%'` (but not `'%suffix'` or `'%substring%'`).
  * **Strengths:** General purpose, highly optimized, good for most common query patterns.
  * **Weaknesses:** Not ideal for full-text search, geometric data, or very large arrays/JSONB documents (unless you're indexing specific scalar fields within them).

**4.2. Hash Indexes**

  * **Syntax:** `CREATE INDEX [index_name] ON table_name USING HASH (column_name);`
  * **Primary Use Cases:** Only for **equality comparisons (`=`)**.
  * **How it Works:** Stores a hash value of the column content and a pointer to the row.
  * **Strengths:** Historically, could be faster than B-Tree for exact matches in specific scenarios, but generally, B-Trees are often faster or comparable.
  * **Weaknesses:**
      * **No range queries:** Cannot be used for `<`, `>`, `BETWEEN`.
      * **No ordering:** Cannot speed up `ORDER BY`.
      * **No uniqueness enforcement:** Cannot be used for `UNIQUE` constraints.
      * **Less common:** Due to their limitations and B-Tree's improvements, rarely recommended over B-Tree in modern PostgreSQL. Prior to PG10, they were not crash-safe.
  * **Ineffectiveness:** Do not use if you need anything other than simple equality checks or if you have older PostgreSQL versions. B-Tree is almost always a safer and more versatile choice.

**4.3. GIN (Generalized Inverted Index)**

  * **Syntax:** `CREATE INDEX [index_name] ON table_name USING GIN (column_name);`
  * **Primary Use Cases:** Indexing columns that contain multiple values within a single field.
      * **Arrays (`TEXT[]`, `INT[]`):** For operators like `@>` (contains), `&&` (overlaps).
      * **JSONB data:** For operators like `?` (key exists), `?&` (all keys exist), `?|` (any keys exist), `@>` (contains).
      * **Full-Text Search (`tsvector`):** For `@@` (matches) operator.
  * **How it Works:** For each *item* within the indexed value (e.g., each word in a document, each element in an array, each key/value in JSONB), the index stores a list of rows where that item appears.
  * **Strengths:** Extremely fast for "contains" type queries on complex data types.
  * **Weaknesses:** Slower to build and update than B-Tree, larger on disk.
  * **Example (JSONB):**
    ```sql
    -- GIN index on 'metadata' column for efficient JSONB querying
    CREATE INDEX idx_employees_metadata_gin ON employees USING GIN (metadata);

    -- Now, queries like this will be fast:
    SELECT employee_id, first_name, metadata
    FROM employees
    WHERE metadata ? 'is_manager'; -- Does the JSONB contain the key 'is_manager'?

    SELECT employee_id, first_name, metadata
    FROM employees
    WHERE metadata @> '{"preferred_contact": "email"}'; -- Does the JSONB contain this sub-object?
    ```
  * **Example (Arrays):**
    ```sql
    CREATE INDEX idx_projects_tags_gin ON projects USING GIN (assigned_tags);
    SELECT project_name FROM projects WHERE assigned_tags @> ARRAY['web', 'design'];
    ```
  * **Ineffectiveness:** Using B-Tree on `JSONB` or `TEXT[]` without specific `JSONB` operators or array operators won't use the index for content-based searches. Trying to use `LIKE '%value%'` on a `TEXT` column instead of `GIN` with `tsvector` for full-text search is significantly less performant and flexible.

**4.4. GiST (Generalized Search Tree)**

  * **Syntax:** `CREATE INDEX [index_name] ON table_name USING GIST (column_name);`
  * **Primary Use Cases:** Indexing specialized data types where B-Tree is not suitable.
      * **Geometric data:** (e.g., points, boxes, circles) for spatial queries (often with PostGIS extension).
      * **Range types:** (`DATERANGE`, `TSRANGE`) for overlap and containment queries.
      * **Full-Text Search:** As an alternative to GIN, with different performance characteristics.
  * **How it Works:** A balanced tree, but unlike B-Tree, it allows for "lossy" storage in internal nodes, meaning a node might point to a child that *could* contain the value, not necessarily *does* contain it. This flexibility supports complex data types and operators.
  * **Strengths:** Highly extensible, supports complex operators and non-linear data.
  * **Weaknesses:** Can be slower than B-Tree for simple scalar types.
  * **Example (Range Types):**
    ```sql
    -- GiST index on 'booking_period' for efficient overlap checks
    CREATE INDEX idx_bookings_period_gist ON bookings USING GIST (booking_period);

    -- Now, queries checking for overlaps will be fast:
    SELECT *
    FROM bookings
    WHERE booking_period && '[2025-08-01 11:00:00, 2025-08-01 13:00:00)'::TSRANGE;
    ```
  * **Ineffectiveness:** Not suitable for basic equality or range queries on scalar types.

**4.5. BRIN (Block Range Index)**

  * **Syntax:** `CREATE INDEX [index_name] ON table_name USING BRIN (column_name);`
  * **Primary Use Cases:** Very large tables where data is *naturally ordered* on the indexed column.
      * Time-series data, log tables, or tables with auto-incrementing primary keys where new data is appended.
  * **How it Works:** Stores summary information (like min/max values) for *ranges of physical data blocks* on disk, rather than for individual rows.
  * **Strengths:**
      * Extremely small index size (much smaller than B-Tree).
      * Very fast for queries that filter on the indexed column, provided the data is well-ordered.
      * Low maintenance overhead.
  * **Weaknesses:** Only effective if the data on disk is highly correlated with the indexed column's values. If data is randomly inserted, BRIN is useless.
  * **Example:**
    If `employees` were inserted purely by `hire_date` order:
    ```sql
    CREATE INDEX idx_employees_hire_date_brin ON employees USING BRIN (hire_date);

    -- This query would be efficient if hire_date is physically ordered
    SELECT * FROM employees WHERE hire_date BETWEEN '2023-01-01' AND '2023-12-31';
    ```
  * **Ineffectiveness:** On tables where the indexed column's values are randomly distributed across disk blocks, a BRIN index will be ineffective and lead to sequential scans. You cannot simply `CREATE INDEX USING BRIN` on any column; you must verify the data's physical order.

-----

#### **5. Partial Indexes**

  * **Definition:** An index that only includes a subset of rows from a table, defined by a `WHERE` clause during index creation.
  * **Syntax:** `CREATE INDEX [index_name] ON table_name (column) WHERE condition;`
  * **Advantages:**
      * **Smaller Size:** Consumes less disk space and memory.
      * **Faster Maintenance:** Updates, inserts, and deletes on rows *outside* the partial index's condition do not require updating the index.
      * **More Efficient Queries:** If most queries target the indexed subset of data, this index can be very effective.
  * **Use Cases:**
      * Columns with highly skewed data distribution (e.g., `is_active` column where 95% of records are `is_active = FALSE`). You'd index `WHERE is_active = TRUE`.
      * Tables with many `NULL` values where queries filter `IS NOT NULL`.
  * **Example:**
    Imagine `employee_email` can be `NULL` for temporary workers, but most queries filter for active emails.
    ```sql
    -- Index only employees who have an email
    CREATE UNIQUE INDEX uix_employees_active_email ON employees (employee_email) WHERE employee_email IS NOT NULL;

    -- This query will use the partial index
    SELECT * FROM employees WHERE employee_email = 'john.doe@example.com';
    ```
  * **Ineffectiveness:** The `WHERE` clause in your `SELECT` query *must* match or be logically covered by the `WHERE` clause of the partial index for it to be used. If you query `WHERE employee_email IS NULL`, the partial index above won't be used.

-----

#### **6. Expression Indexes**

  * **Definition:** An index created on the result of an expression or function, rather than directly on a column.
  * **Syntax:** `CREATE INDEX [index_name] ON table_name (expression);`
  * **Advantages:**
      * Allows indexing on transformed data that is frequently used in queries.
      * Enables use of indexes for queries that involve functions in the `WHERE` clause.
  * **Use Cases:**
      * **Case-insensitive search:** Indexing `LOWER(column_name)` allows case-insensitive lookups using `WHERE LOWER(column_name) = 'value'`.
      * **Concatenated fields:** Indexing `(first_name || ' ' || last_name)` to quickly search full names.
      * **Extracting parts of dates:** Indexing `EXTRACT(YEAR FROM hire_date)`.
  * **Example:**
    ```sql
    -- Create an index for case-insensitive last name search
    CREATE INDEX idx_employees_lower_last_name ON employees (LOWER(last_name));

    -- This query will now use the expression index
    SELECT * FROM employees WHERE LOWER(last_name) = 'smith';

    -- Create an index for full name search
    CREATE INDEX idx_employees_full_name ON employees ((first_name || ' ' || last_name));
    -- This query will use the index
    SELECT * FROM employees WHERE (first_name || ' ' || last_name) = 'John Doe';
    ```
  * **Ineffectiveness:** The expression in the `WHERE` clause of your `SELECT` query *must exactly match* the expression in the index definition for the index to be used. If you create an index on `LOWER(last_name)` but query `WHERE last_name = 'Smith'`, the index will not be used.

-----

#### **7. When to Use and When *Not* to Use Indexes**

**7.1. When to Use Indexes (Good Candidates):**

  * **Columns in `WHERE` clauses:** If a column is frequently used to filter rows.
  * **Columns in `JOIN` conditions:** Foreign key columns are prime candidates.
  * **Columns in `ORDER BY` or `GROUP BY` clauses:** Can speed up sorting and grouping, sometimes avoiding explicit sorts.
  * **Columns with High Cardinality:** Columns with many unique values (e.g., `email`, `user_id`). Indexes are less effective on columns with low cardinality (e.g., `gender`, `boolean` flags) unless used as partial indexes.
  * **Tables with High Read-to-Write Ratio:** Indexes primarily benefit reads.
  * **Primary Keys & Unique Constraints:** PostgreSQL automatically creates unique B-Tree indexes for these.
  * **Foreign Keys:** Strongly recommended to index foreign keys to speed up `JOIN`s and referential integrity checks.

**7.2. When *Not* to Use Indexes (Bad Candidates / Over-Indexing):**

  * **Very Small Tables:** For tables with only a few hundred or thousand rows, a sequential scan might be faster or comparable to an index scan, as the overhead of index lookup might negate the benefit.
  * **Tables with Very High Write-to-Read Ratio:** Every `INSERT`, `UPDATE`, or `DELETE` on an indexed table requires the index(es) to be updated, which adds write overhead. If your table is mostly written to and rarely read, indexes can slow it down.
  * **Columns with Very Low Cardinality (Many Duplicates):** E.g., a `gender` column with only 'M' and 'F' where data is evenly distributed. An index lookup here might not significantly narrow down the search, leading the optimizer to prefer a sequential scan. (Consider partial indexes if values are skewed).
  * **Columns with Frequent Updates:** If a column value is constantly changing, the index on that column will constantly need maintenance, adding overhead.
  * **Over-indexing:** Creating too many indexes or redundant indexes:
      * **Wastes Disk Space:** Indexes consume storage.
      * **Slows Down Writes:** More indexes mean more maintenance work for the database on writes.
      * **Optimizer Confusion:** The query planner might struggle to pick the best index if many are available, or might pick a suboptimal one.
  * **Columns where `LIKE '%suffix'` or `LIKE '%substring%'` is common:** B-Tree indexes cannot be used efficiently for leading wildcards. Consider full-text search (GIN) or specialized extensions.

-----

#### **8. Analyzing Index Usage (`EXPLAIN ANALYZE`)**

`EXPLAIN ANALYZE` is your debugger for query performance. It shows you the query execution plan (how PostgreSQL intends to run your query) and the *actual* execution statistics (how it *did* run it).

**Syntax:**

```sql
EXPLAIN ANALYZE SELECT ... FROM ... WHERE ...;
```

**Key Information in `EXPLAIN ANALYZE` Output:**

  * **`->` (Arrows):** Indicate nested operations. The innermost operation is executed first.
  * **Node Types (e.g., `Seq Scan`, `Index Scan`, `Bitmap Heap Scan`, `Hash Join`, `Merge Join`, `Sort`):** Describe the operation being performed.
  * **`cost`:** An estimate of the query's cost (arbitrary units, lower is better).
      * `{startup_cost}..{total_cost}`: Startup cost (time to return first row) and total cost (time to return all rows).
  * **`rows`:** Estimated number of rows processed by this operation.
  * **`width`:** Estimated average width (bytes) of rows processed.
  * **`actual time`:** The *actual* time taken for this node in milliseconds.
      * `{startup_time}..{total_time}`: Actual startup time and actual total time.
  * **`loops`:** Number of times this node was executed.
  * **`rows removed` / `rows filtered`:** How many rows were discarded at this step.
  * **`Buffers`:** (Very important for I/O analysis, requires `track_io_timing` to be on). Shows number of shared/local/temp buffers hit/read/dirtied.

**How to Interpret for Index Usage:**

  * **`Seq Scan`:** Indicates a full table scan. If this is on a large table for a selective query, it usually means an index is missing or not being used.
  * **`Index Scan`:** The query plan used a B-Tree (or other) index to retrieve rows directly. This is generally good.
  * **`Bitmap Heap Scan`:** Often seen when multiple indexes are used, or when an index returns a bitmap of block locations, and then the actual table rows are fetched from those blocks. It's an efficient way to combine index lookups.

**Example Demonstration:**

Let's test a query before and after creating an index on `salary`.

1.  **Run `EXPLAIN ANALYZE` without an index:**
    (Ensure no index exists on `salary`. You can drop it if you created one earlier: `DROP INDEX IF EXISTS idx_employees_salary;`)

    ```sql
    EXPLAIN ANALYZE SELECT * FROM employees WHERE salary > 70000;
    ```

      * **Expected Output Snippet (Look for this pattern):**
        ```
        Seq Scan on employees  (cost=0.00..X.XX rows=Y width=Z) (actual time=0.ZZZ..0.AAA rows=B loops=1)
        Filter: (salary > '70000'::numeric)
        Rows Removed by Filter: C
        Planning Time: D.EEE ms
        Execution Time: F.GGG ms
        ```
        Notice `Seq Scan` (meaning it scanned the whole table).

2.  **Create an index on `salary`:**

    ```sql
    CREATE INDEX idx_employees_salary ON employees (salary);
    ```

3.  **Run `EXPLAIN ANALYZE` again:**

    ```sql
    EXPLAIN ANALYZE SELECT * FROM employees WHERE salary > 70000;
    ```

      * **Expected Output Snippet (Look for this pattern):**
        ```
        Index Scan using idx_employees_salary on employees  (cost=0.XX..0.YY rows=Z width=A) (actual time=0.BBB..0.CCC rows=D loops=1)
        Index Cond: (salary > '70000'::numeric)
        Planning Time: E.FFF ms
        Execution Time: G.HHH ms
        ```
        Notice `Index Scan` (meaning it used the index) and hopefully a lower `actual time`.

By comparing the `EXPLAIN ANALYZE` output, you can visibly see how the database changes its execution plan from a slow sequential scan to a fast index scan after creating the index. This is a fundamental skill for debugging and optimizing database performance.