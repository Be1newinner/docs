### **Chapter 7: Transactions and Concurrency Control**

This chapter covers the fundamental principles that allow relational databases to manage concurrent operations safely. You will learn about transactions and their crucial ACID properties, different isolation levels and the anomalies they prevent, PostgreSQL's MVCC mechanism, and how to deal with deadlocks and various locking strategies.

-----

Let's use our existing `employees` table for practical demonstrations.

```sql
-- Ensure we have some data
SELECT employee_id, first_name, last_name, salary FROM employees LIMIT 5;
```

-----

#### **1. Understanding Transactions: `BEGIN`, `COMMIT`, `ROLLBACK`**

A **transaction** is a single logical unit of work performed on a database. It consists of one or more SQL statements that are treated as a single, indivisible operation. Either all statements within the transaction are successfully completed and recorded in the database, or none of them are.

**The ACID Properties:**

Transactions are designed to guarantee **ACID** properties, which are fundamental to database reliability:

  * **Atomicity (All or Nothing):** A transaction is an indivisible unit. It either completes entirely (all its operations succeed and are committed) or it doesn't happen at all (all its operations are rolled back). If any part of the transaction fails, the entire transaction is aborted, and the database is returned to its state before the transaction began.
      * *Analogy:* Transferring money between bank accounts. You can't debit one account without crediting another.
  * **Consistency (Valid State):** A transaction brings the database from one valid state to another. It ensures that any data written to the database must comply with all defined rules (constraints, triggers, etc.). If a transaction violates a constraint, it is rolled back.
      * *Analogy:* After a money transfer, the total sum of money in all accounts remains consistent.
  * **Isolation (Concurrent Operations):** The execution of concurrent transactions produces the same result as if they were executed sequentially. Each transaction operates independently without interference from other concurrent transactions. This property is what we'll dive deeper into with isolation levels.
      * *Analogy:* Multiple people using ATMs simultaneously don't see each other's in-progress transactions.
  * **Durability (Permanent Changes):** Once a transaction has been committed, its changes are permanent and survive system failures (like power outages or crashes). The committed data is written to stable storage (disk).
      * *Analogy:* Once a bank transfer is confirmed, the money is permanently moved, even if the bank's system crashes immediately afterward.

**Transaction Commands:**

  * **`BEGIN;` (or `START TRANSACTION;`)**: Initiates a new transaction. All subsequent SQL statements will be part of this transaction until a `COMMIT` or `ROLLBACK` is issued.
  * **`COMMIT;`**: Saves all changes made within the current transaction to the database, making them permanent and visible to other transactions.
  * **`ROLLBACK;`**: Undoes all changes made within the current transaction, effectively reverting the database to its state before the transaction began.

**Example: Funds Transfer (Conceptual, assuming `accounts` table)**

```sql
-- Imagine an 'accounts' table with account_id INT PRIMARY KEY, balance NUMERIC.
-- CREATE TABLE accounts (account_id INT PRIMARY KEY, balance NUMERIC);
-- INSERT INTO accounts VALUES (1, 1000.00), (2, 500.00);

BEGIN; -- Start the transaction

-- Step 1: Debit sender's account
UPDATE accounts
SET balance = balance - 100.00
WHERE account_id = 1;

-- Step 2: Check for sufficient funds (a common consistency check in app logic)
-- If this check fails, the application would likely issue a ROLLBACK
-- SELECT balance FROM accounts WHERE account_id = 1;

-- Step 3: Credit receiver's account
UPDATE accounts
SET balance = balance + 100.00
WHERE account_id = 2;

COMMIT; -- If both updates succeed, make them permanent.
-- If any error occurred, we would issue ROLLBACK; to undo both changes.

-- Verify
-- SELECT * FROM accounts;
```

  * **Ineffectiveness of Not Using Transactions:**
      * **Data Corruption:** If a multi-step operation fails midway (e.g., power outage, application crash), the database could be left in an inconsistent state (e.g., money debited but not credited).
      * **Partial Updates:** Changes from one part of a logical unit of work might be saved while others are lost, leading to incorrect data.
      * **Concurrency Issues:** Without isolation, concurrent operations could interfere with each other, leading to incorrect reads or lost updates.

-----

#### **2. Isolation Levels**

The SQL standard defines four transaction isolation levels, which control the degree to which one transaction's uncommitted changes are visible to other concurrent transactions. Higher isolation provides more consistency but typically incurs higher overhead due to more stringent locking or versioning.

**Understanding Anomalies (What isolation levels prevent):**

  * **1. Dirty Read (Read Uncommitted):**
      * Occurs when a transaction reads data that has been modified by another transaction but has *not yet been committed*. If the modifying transaction later rolls back, the first transaction will have read "dirty" or invalid data.
      * *Analogy:* You read a draft document that someone is still editing. They then delete their changes, making your copy outdated and incorrect.
  * **2. Non-Repeatable Read:**
      * Occurs when a transaction reads the same row multiple times, but gets different values each time because another *committed* transaction modified that row *between* the reads.
      * *Analogy:* You look at a product's price, decide to buy it, but when you check out, the price has changed because another customer just completed a purchase at a different price.
  * **3. Phantom Read:**
      * Occurs when a transaction re-executes a query that returns a set of rows (e.g., `SELECT COUNT(*)` or `SELECT * WHERE some_condition`), and the set of rows changes because another *committed* transaction inserted or deleted rows that satisfy the `WHERE` clause *between* the reads.
      * *Analogy:* You count the number of available seats in a flight. You count again and find fewer seats because someone else just booked one.

**PostgreSQL's Isolation Levels:**

PostgreSQL implements `READ COMMITTED`, `REPEATABLE READ`, and `SERIALIZABLE`. Note that PostgreSQL does *not* implement `READ UNCOMMITTED`.

1.  **`READ COMMITTED` (Default in PostgreSQL)**

      * **How it works:** Each statement within a transaction sees only data that was committed *before that statement began*. It does not see any uncommitted changes from other concurrent transactions.
      * **Anomalies Prevented:** **Dirty Reads**.
      * **Anomalies Allowed:** **Non-Repeatable Reads**, **Phantom Reads**.
      * **When to use:** This is the default and generally suitable for most applications where high concurrency is desired and occasional inconsistencies due to Non-Repeatable or Phantom Reads are acceptable (e.g., simple web requests, reporting where exact consistency over long-running transactions isn't critical).
      * **Example Scenario (Non-Repeatable Read in `READ COMMITTED`):**
          * **Session A:**
            ```sql
            BEGIN;
            SELECT salary FROM employees WHERE employee_id = 1; -- (Reads 60000.00)
            -- ... some long processing ...
            ```
          * **Session B (Concurrent):**
            ```sql
            BEGIN;
            UPDATE employees SET salary = 65000.00 WHERE employee_id = 1;
            COMMIT;
            ```
          * **Session A (Continues):**
            ```sql
            SELECT salary FROM employees WHERE employee_id = 1; -- (Now reads 65000.00 - Non-Repeatable Read!)
            COMMIT;
            ```

2.  **`REPEATABLE READ`**

      * **How it works:** All statements within a transaction see a consistent snapshot of the data as it was *at the beginning of the transaction*. Changes committed by other transactions *after* this transaction began are not visible. If another transaction modifies a row that this transaction has read or written to, this transaction may fail with a serialization error (`could not serialize access due to concurrent update`) upon `COMMIT`.
      * **Anomalies Prevented:** **Dirty Reads**, **Non-Repeatable Reads**.
      * **Anomalies Allowed:** **Phantom Reads**. (PostgreSQL's `REPEATABLE READ` *does* prevent phantom reads in many common cases due to its MVCC implementation, but according to the SQL standard, it's still theoretically possible, and PostgreSQL's `SERIALIZABLE` is the truly iron-clad guarantee).
      * **When to use:** When you need a higher level of consistency for a transaction's reads, ensuring that if you query the same data multiple times, you always get the same result (e.g., complex reports, multi-step business processes where reads must be consistent).
      * **Example Scenario (No Non-Repeatable Read in `REPEATABLE READ`):**
          * **Session A:**
            ```sql
            BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
            SELECT salary FROM employees WHERE employee_id = 1; -- (Reads 60000.00)
            -- ... some long processing ...
            ```
          * **Session B (Concurrent):**
            ```sql
            BEGIN;
            UPDATE employees SET salary = 65000.00 WHERE employee_id = 1;
            COMMIT;
            ```
          * **Session A (Continues):**
            ```sql
            SELECT salary FROM employees WHERE employee_id = 1; -- (STILL reads 60000.00, as of transaction start)
            -- If Session A then tries to UPDATE this row, it might get a serialization error on COMMIT
            COMMIT;
            ```

3.  **`SERIALIZABLE`**

      * **How it works:** This is the highest isolation level. Transactions are executed in such a way that the final database state is the same as if the transactions had been executed sequentially (serially). PostgreSQL achieves this using a technique called Snapshot Isolation (SI) with additional checks to detect and prevent "serialization anomalies" (complex read/write dependencies that could lead to incorrect results even under `REPEATABLE READ`). If a serialization anomaly is detected, one of the conflicting transactions will be rolled back (the "victim" transaction).
      * **Anomalies Prevented:** **Dirty Reads**, **Non-Repeatable Reads**, **Phantom Reads**, and other **Serialization Anomalies**.
      * **When to use:** When data integrity is paramount and even rare, subtle concurrency issues cannot be tolerated (e.g., financial systems, complex inventory management, critical reporting where a perfectly consistent view of data across multiple queries is essential). You *must* implement retry logic in your application for `SERIALIZABLE` transactions, as they can fail due to serialization errors.
      * **Example Scenario (Preventing Phantom Read in `SERIALIZABLE`):**
          * **Session A:**
            ```sql
            BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
            SELECT COUNT(*) FROM employees WHERE department = 'Sales'; -- (Counts 3 employees)
            -- ...
            ```
          * **Session B (Concurrent):**
            ```sql
            BEGIN;
            INSERT INTO employees (first_name, last_name, salary, department) VALUES ('New', 'Salesperson', 50000, 'Sales');
            COMMIT;
            ```
          * **Session A (Continues):**
            ```sql
            SELECT COUNT(*) FROM employees WHERE department = 'Sales'; -- (Still counts 3 employees - no phantom read)
            -- When Session A tries to COMMIT, it might get a serialization error if it performs a write
            -- that conflicts with Session B's insert, causing Session A to roll back.
            COMMIT; -- Might fail here and require retry
            ```

-----

#### **3. Concurrency Control Mechanisms: Multi-Version Concurrency Control (MVCC) in PostgreSQL**

PostgreSQL's primary concurrency control mechanism is **Multi-Version Concurrency Control (MVCC)**. This is a fundamental concept for understanding PostgreSQL's performance characteristics.

  * **Core Idea:** Instead of using traditional read/write locks that block access, MVCC allows multiple versions of a row to exist concurrently. When a transaction modifies a row, it doesn't *overwrite* the existing data; instead, it creates a *new version* of that row.

  * **Visibility:** Each transaction gets a "snapshot" of the database at its starting point (or statement start for `READ COMMITTED`). When a transaction reads data, it only sees the versions of rows that were committed and visible according to its snapshot.

      * Readers never block writers.
      * Writers never block readers.
      * This vastly improves concurrency, as read-heavy workloads don't contend with write-heavy ones.

  * **Transaction IDs (XIDs):** Each transaction in PostgreSQL is assigned a unique Transaction ID (XID). Each row version stores the XID of the transaction that created it (`xmin`) and the XID of the transaction that deleted it (`xmax`) (or a null if not deleted).

  * **Garbage Collection (VACUUM):** Over time, as old row versions are superseded by newer ones and are no longer needed by any active transaction, they become "dead tuples." These dead tuples must be reclaimed to free up disk space and prevent table bloat. This process is handled by the `VACUUM` command (often automatically by the autovacuum daemon).

  * **Ineffectiveness of Non-MVCC (Traditional Locking Systems):**

      * **Reader-Writer Contention:** In systems that use traditional locking, a writer might place an exclusive lock on data, blocking all readers until the writer commits. Similarly, readers might place shared locks, preventing writers. This significantly reduces concurrency, especially in high-volume mixed workloads.
      * **Deadlock Prone:** More extensive locking inherently increases the likelihood of deadlocks.

-----

#### **4. Deadlocks and How to Handle Them**

A **deadlock** occurs when two or more transactions are in a circular waiting state, each holding a lock on a resource that another transaction needs, and waiting indefinitely for the other to release its lock.

**Example Scenario:**

  * **Session A:**
    ```sql
    BEGIN;
    UPDATE employees SET salary = salary * 1.05 WHERE employee_id = 1; -- Acquires lock on row 1
    -- ... (some delay) ...
    UPDATE employees SET salary = salary * 1.05 WHERE employee_id = 2; -- Tries to acquire lock on row 2, but Session B holds it
    ```
  * **Session B (Concurrent):**
    ```sql
    BEGIN;
    UPDATE employees SET salary = salary * 1.05 WHERE employee_id = 2; -- Acquires lock on row 2
    -- ... (some delay) ...
    UPDATE employees SET salary = salary * 1.05 WHERE employee_id = 1; -- Tries to acquire lock on row 1, but Session A holds it
    ```
    At this point, Session A is waiting for B, and B is waiting for A. A deadlock occurs.

**PostgreSQL's Deadlock Handling:**

PostgreSQL has an active **deadlock detection** mechanism. It periodically checks for deadlocks. If a deadlock is detected, PostgreSQL will automatically:

1.  Choose one of the transactions involved as the "victim."
2.  Rollback the victim transaction.
3.  Release the victim's locks, allowing the other transaction(s) to proceed.
    The rolled-back transaction will receive an error message (e.g., `ERROR: deadlock detected`).

**How to Handle Deadlocks as a Developer:**

  * **Application-Level Retry Logic (Crucial):** This is the most important strategy. When your application receives a deadlock error, it should catch the error and retry the entire transaction (with a small random backoff to avoid immediate re-deadlocking).

  * **Consistent Lock Order:** Design your application to always access and lock resources (tables, rows) in the same predefined order. For example, if you typically update `employee_id = 1` then `employee_id = 2`, always stick to that order.

  * **Keep Transactions Short:** Minimize the duration of transactions to reduce the time locks are held, thus reducing the window for deadlocks.

  * **Use Appropriate Isolation Levels:** `SERIALIZABLE` can reduce certain types of deadlocks by preventing anomalies at a higher level, but introduces serialization errors that also require retry logic.

  * **Index Usage:** Efficient queries (using indexes) reduce the time spent acquiring and holding locks by processing data faster.

  * **Ineffectiveness of Ignoring Deadlocks:** Leads to application failures, user frustration, and data inconsistencies if transactions are aborted mid-way without proper handling.

-----

#### **5. Locking Mechanisms**

While MVCC handles many concurrency issues by providing different data versions, locks are still necessary for write operations and to ensure data integrity during specific operations.

**5.1. Row-Level Locks (Tuple Locks):**

  * These are the most granular locks and are implicitly acquired by DML statements.
  * **Implicit Locks:**
      * `UPDATE`, `DELETE`, `INSERT` (on the affected rows). These acquire exclusive row-level locks on the specific rows being modified to prevent other transactions from simultaneously modifying the *exact same* row.
  * **Explicit Locks (for specific scenarios):**
      * **`SELECT ... FOR UPDATE`:**
          * **Purpose:** Acquires an exclusive lock on the selected rows. This prevents any other transaction from `UPDATE`ing, `DELETE`ing, or using `FOR UPDATE` on these rows until the current transaction commits or rolls back.
          * **Use Case:** Critical for "read-modify-write" patterns to prevent race conditions. E.g., check account balance, then debit. You need to ensure the balance doesn't change between your read and your write.
          * **Example:**
              * **Session A:**
                ```sql
                BEGIN;
                SELECT salary FROM employees WHERE employee_id = 1 FOR UPDATE; -- Locks row 1
                -- ... some application logic, calculate new salary ...
                UPDATE employees SET salary = new_calculated_salary WHERE employee_id = 1;
                COMMIT;
                ```
              * **Session B (Concurrent):**
                ```sql
                BEGIN;
                UPDATE employees SET salary = 70000 WHERE employee_id = 1; -- WILL WAIT until Session A commits/rolls back
                -- Or SELECT salary FROM employees WHERE employee_id = 1 FOR UPDATE; -- WILL WAIT
                COMMIT;
                ```
      * **`SELECT ... FOR SHARE`:**
          * **Purpose:** Acquires a shared lock on the selected rows. This allows other transactions to also acquire `FOR SHARE` locks on the same rows, but prevents `FOR UPDATE`, `UPDATE`, or `DELETE` operations on those rows.
          * **Use Case:** When you need to read data and ensure it doesn't change while your transaction is active, but you don't intend to modify it yourself (or you're part of a shared-read pattern).
          * **Example:**
              * **Session A:**
                ```sql
                BEGIN;
                SELECT * FROM projects WHERE project_id = 1 FOR SHARE;
                -- ... read consistent project data ...
                ```
              * **Session B (Concurrent):**
                ```sql
                BEGIN;
                SELECT * FROM projects WHERE project_id = 1 FOR SHARE; -- ALLOWED
                UPDATE projects SET budget = 200000 WHERE project_id = 1; -- WILL WAIT
                COMMIT;
                ```
  * **Ineffectiveness:** Not using explicit `FOR UPDATE` for read-modify-write cycles can lead to race conditions where concurrent transactions read outdated data and overwrite each other's changes, leading to lost updates.

**5.2. Table-Level Locks:**

  * These affect entire tables and are usually acquired implicitly by DDL (Data Definition Language) commands.
  * **Implicit Locks:**
      * `ALTER TABLE`, `DROP TABLE`, `TRUNCATE TABLE`, `VACUUM FULL`: Acquire strong (e.g., `ACCESS EXCLUSIVE`) table locks to ensure no concurrent operations are happening that could conflict with schema changes.
      * `SELECT`, `INSERT`, `UPDATE`, `DELETE`: Acquire weaker table locks (e.g., `ACCESS SHARE`, `ROW EXCLUSIVE`) that allow normal concurrent DML operations but prevent DDL.
  * **Explicit Locks (`LOCK TABLE`):**
      * **Syntax:** `LOCK TABLE table_name IN lock_mode;`
      * **`lock_mode`:** Various modes exist, from least restrictive (`ACCESS SHARE`) to most restrictive (`ACCESS EXCLUSIVE`).
      * **Use Case:** Rarely used by application developers. Primarily for database administrators or very specific scenarios where you need to guarantee no other activity on a table for a short period (e.g., preparing for a bulk load, running a complex migration script). Overuse leads to severe contention.
      * **Example (Highly Restrictive):**
        ```sql
        BEGIN;
        LOCK TABLE employees IN ACCESS EXCLUSIVE MODE; -- Prevents all other access (reads/writes/DDL)
        -- Perform sensitive, single-user operations
        -- ...
        COMMIT;
        ```
  * **Ineffectiveness:** Explicit table locks (especially strong ones) are very coarse-grained and severely limit concurrency. They should be used only when absolutely necessary and for the shortest possible duration.

**5.3. Advisory Locks:**

  * **Definition:** Application-level locks. PostgreSQL provides the mechanism, but the database system *does not enforce their meaning or apply them automatically*. It's up to the application developer to explicitly acquire and release them and to ensure all parts of the application adhere to the advisory lock protocol.
  * **Purpose:** For coordinating custom application logic that doesn't directly involve standard row or table modifications.
      * Ensuring only one instance of a batch job runs at a time.
      * Implementing a distributed mutex for non-database resources.
      * Protecting application-specific shared resources.
  * **Functions:**
      * `pg_advisory_lock(key_number)`: Acquires an exclusive advisory lock. Blocks if the lock is held.
      * `pg_advisory_unlock(key_number)`: Releases the lock.
      * `pg_try_advisory_lock(key_number)`: Attempts to acquire a lock immediately, returns `true` or `false` without blocking.
      * `pg_advisory_xact_lock(key_number)`: Acquires an exclusive advisory lock that is automatically released at the end of the transaction.
  * **Example (Ensuring single batch job instance):**
      * **Batch Job Process:**
        ```sql
        BEGIN;
        -- Try to acquire an advisory lock for this job (e.g., using a unique integer ID)
        SELECT pg_try_advisory_lock(123456) AS lock_acquired;
        -- If lock_acquired is TRUE, proceed with job
        -- Else, another instance is running, exit
        -- ... do job work ...
        SELECT pg_advisory_unlock(123456); -- Release the lock
        COMMIT;
        ```
  * **Ineffectiveness:** Advisory locks rely entirely on application code discipline. If parts of your application don't adhere to the locking protocol, data inconsistency or concurrent execution problems can occur silently. They don't provide automatic enforcement like standard SQL locks.