### **Chapter 12: Backup and Recovery Strategies**

This chapter covers the essential practices for protecting your PostgreSQL data. You will learn about different types of backups (logical vs. physical), how to implement Point-in-Time Recovery (PITR), establish High Availability (HA) through replication, and leverage specialized tools to automate and enhance your backup and recovery processes.

-----

#### **1. The Importance of a Robust Backup Strategy**

A well-defined backup and recovery strategy is non-negotiable for any critical database system. Its importance stems from various data loss scenarios and business imperatives:

  * **Disaster Recovery:** Protection against catastrophic events like hardware failures (disk crashes, server loss), natural disasters, or data center outages.

  * **Data Corruption:** Safeguarding against logical data corruption caused by software bugs, faulty application code, or even PostgreSQL bugs (rare, but possible).

  * **Human Error:** The most common cause of data loss. Accidental `DROP TABLE`, `DELETE` without `WHERE`, incorrect `UPDATE`s, or misconfigurations can be devastating. Backups allow you to revert to a state before the error.

  * **Malicious Activity:** Protection against ransomware, unauthorized data deletion, or tampering.

  * **Compliance & Audit:** Many regulatory frameworks (e.g., GDPR, HIPAA, PCI DSS) mandate data retention and recovery capabilities.

  * **Business Continuity (RTO/RPO):**

      * **RTO (Recovery Time Objective):** The maximum tolerable downtime. How quickly can you get the system back online?
      * **RPO (Recovery Point Objective):** The maximum tolerable data loss. How much data are you willing to lose?
        A good backup strategy minimizes both RTO and RPO.

  * **Ineffectiveness of No Strategy:** No backups equals no business. It's not a matter of *if* you'll need a backup, but *when*.

-----

#### **2. Logical Backups: `pg_dump`, `pg_dumpall`**

Logical backups export the database contents as a set of SQL commands or a custom archive format, which can then be used to recreate the database objects and data.

  * **`pg_dump`:**

      * **Purpose:** Backs up a single PostgreSQL database.
      * **Output Formats:**
          * **Plain-text (`-Fp` or no option):** Generates a `.sql` file with SQL commands (`CREATE TABLE`, `INSERT`, etc.). Human-readable, easy to modify, but can be slow to restore and locks tables during backup for consistency.
          * **Custom (`-Fc`):** **(Recommended)** PostgreSQL's proprietary binary format. More flexible, allows selective restore of tables/data, parallel restore, and compression.
          * **Directory (`-Fd`):** Creates a directory with one file per table/object. Good for large databases and parallel backups/restores.
          * **Tar (`-Ft`):** Creates a standard tar archive.
      * **Example (Custom Format):**
        ```bash
        # Backup a database named 'my_app_db' to a custom format file
        pg_dump -Fc -Z 9 -f /path/to/backups/my_app_db_$(date +%Y%m%d_%H%M%S).dump my_app_db
        # -Z 9: Compress the output (level 9)
        # -f: Output file path

        # To restore from custom format:
        pg_restore -d new_db_name /path/to/backups/my_app_db_latest.dump
        # -d: Target database
        ```
      * **Use Cases:**
          * Migrating small-to-medium databases.
          * Creating development/testing environments.
          * Backing up specific schemas or tables.
          * Getting a human-readable schema backup.

  * **`pg_dumpall`:**

      * **Purpose:** Backs up an entire PostgreSQL cluster, including all databases, global objects (roles/users, tablespaces), and database-specific data.
      * **Output Format:** Only plain-text SQL.
      * **Example:**
        ```bash
        # Backup entire cluster to a single SQL file
        pg_dumpall > /path/to/backups/all_databases_$(date +%Y%m%d_%H%M%S).sql

        # To restore (must be done by a superuser on an empty cluster):
        psql -f /path/to/backups/all_databases_latest.sql postgres
        ```
      * **Use Cases:** Full cluster migration, backing up roles and tablespaces.

  * **Limitations of Logical Backups:**

      * **Speed:** Can be very slow for large databases, as they involve reading all data and converting it to SQL statements.
      * **Locking:** Plain-text `pg_dump` locks tables to ensure consistency.
      * **No Point-in-Time Recovery (PITR):** A logical backup is a snapshot at a single point in time. You cannot recover to an arbitrary moment between two logical backups.
      * **WAL Management:** They don't include or interact with the Write-Ahead Log (WAL).

-----

#### **3. Physical Backups: Base Backups and Write-Ahead Log (WAL) Archiving**

Physical backups involve copying the actual data files from the PostgreSQL data directory. This is the foundation for Point-in-Time Recovery (PITR) and is essential for large, critical databases.

  * **Base Backups:**

      * **Concept:** A consistent snapshot of the entire PostgreSQL data directory. It captures all data files (table data, indexes, configuration files) at a specific moment.
      * **How to Create:**
          * **`pg_basebackup` (Recommended):** The official tool. It's easy to use, creates a consistent backup, and automatically handles the necessary internal PostgreSQL commands (`pg_start_backup()`, `pg_stop_backup()`).
            ```bash
            # Create a base backup
            pg_basebackup -h localhost -p 5432 -U postgres -D /path/to/physical_backups/base_$(date +%Y%m%d_%H%M%S) -F t -Xs -P -R -v
            # -D: Destination directory
            # -F t: Tar format (or -F p for plain)
            # -Xs: Include WAL files in the backup (stream WAL while taking backup)
            # -P: Show progress
            # -R: Create 'standby.signal' file for easier standby setup
            # -v: Verbose output
            ```
          * **Filesystem Copy (`pg_start_backup()` / `pg_stop_backup()`):** Manual method where you issue `SELECT pg_start_backup('label');` copy the data directory, then `SELECT pg_stop_backup();`. Less recommended than `pg_basebackup` due to manual steps.
      * **Role:** Provides the initial state from which recovery begins.

  * **Write-Ahead Log (WAL) Archiving:**

      * **Concept:** PostgreSQL uses a Write-Ahead Log (WAL) for durability. Every change (transaction) is first written to the WAL before being applied to the actual data files. By continuously archiving these WAL segments, you create a log of every change that has occurred since your last base backup.
      * **Configuration (`postgresql.conf`):**
          * `wal_level = replica` (or `logical`): Ensures enough information is written to WAL for recovery/replication.
          * `archive_mode = on`: Enables WAL archiving.
          * `archive_command = 'cp %p /path/to/wal_archive/%f'`: The shell command to copy a completed WAL segment (`%p` is source path, `%f` is filename) to a safe, persistent archive location (e.g., S3, NFS). **This command must succeed.**
      * **Importance:** WAL archiving is what enables Point-in-Time Recovery. Without it, you can only recover to the point of your last base backup.

  * **Pros of Physical Backups:**

      * **Speed:** Much faster for large databases than logical backups, as it's a block-level copy.
      * **Point-in-Time Recovery (PITR):** Enables highly granular recovery.
      * **Efficiency:** Restores are typically faster.
      * **Replication:** Forms the basis for streaming replication.

  * **Cons of Physical Backups:**

      * **Not Human-Readable:** The data files are in PostgreSQL's internal format.
      * **Version Specific:** A physical backup from one major PostgreSQL version cannot be restored to another.
      * **Larger Size:** Often larger than compressed logical backups for the same data.

-----

#### **4. Point-in-Time Recovery (PITR)**

PITR is the ability to restore your database to *any specific point in time* within your WAL archive, not just to the moment the last base backup was taken. This is invaluable for recovering from accidental data deletions or corruptions.

  * **How it Works:**

    1.  **Start with a Base Backup:** Restore the chosen physical base backup to a new data directory.
    2.  **Replay WAL Segments:** PostgreSQL then applies all archived WAL segments that were generated *after* that base backup.
    3.  **Stop at Target:** The recovery process stops when it reaches your specified `recovery_target` (e.g., a specific timestamp, transaction ID, or named recovery point).

  * **Configuration for Recovery (`postgresql.conf` of the *recovering* instance):**

      * Ensure the data directory is empty or a fresh cluster.
      * Copy the base backup into the new data directory.
      * Create a `recovery.signal` file in the data directory (for PostgreSQL 12+).
      * Configure `restore_command` in `postgresql.conf` to tell PostgreSQL how to retrieve archived WAL files:
        ```ini
        # Example: if WALs are in /mnt/wal_archive/
        restore_command = 'cp /mnt/wal_archive/%f %p'
        # %f is the WAL file name, %p is the destination path in PG's wal_log directory
        ```
      * Set your `recovery_target` parameters:
          * `recovery_target_time = '2025-07-26 10:00:00 IST'`
          * `recovery_target_xid = '12345'` (a specific transaction ID)
          * `recovery_target_name = 'my_recovery_point'` (a named point created via `pg_create_restore_point('my_recovery_point')`)
          * `recovery_target_action = 'pause'` (pause recovery at target) or `'promote'` (promote to primary) or `'shutdown'` (default).

  * **Benefits:**

      * **Minimal Data Loss (Low RPO):** You can recover to just seconds before a disaster or human error.
      * **Granular Recovery:** Offers precise control over the recovery point.
      * **Disaster Recovery:** A cornerstone of any serious DR plan.

-----

#### **5. High Availability Concepts: Streaming Replication, Logical Replication**

High Availability (HA) refers to systems designed to operate continuously without failure for long periods, minimizing downtime in case of a component failure. Replication is key to achieving HA in PostgreSQL.

  * **5.1. Streaming Replication (Physical Replication):**

      * **Concept:** Creates a primary-standby architecture where a replica (standby) server continuously receives and applies the WAL stream directly from the primary server. This keeps the standby almost perfectly in sync with the primary.
      * **Architecture:**
          * **Primary (Master):** The active server accepting reads and writes.
          * **Standby (Replica/Slave):** One or more servers receiving WAL. Can be used for read-only queries.
      * **How it Works:**
          * The primary continuously sends WAL records (as they are generated) to the standbys over a dedicated connection.
          * Standbys apply these WAL records, keeping their data synchronized with the primary.
      * **Modes:**
          * **Asynchronous Replication (Default):** The primary commits transactions immediately without waiting for the standby to confirm receipt or application of WAL.
              * **Pros:** Fastest commits on the primary.
              * **Cons:** Potential for minimal data loss on primary failure (transactions might be committed on primary but not yet replicated to standby).
          * **Synchronous Replication:** The primary waits for the standby (or a configurable number of standbys) to confirm that it has received and written the WAL data to disk before committing the transaction on the primary.
              * **Pros:** Zero data loss guarantee on primary failure.
              * **Cons:** Slower commits on the primary (latency of network + standby I/O).
      * **Benefits:**
          * **High Availability:** In case of primary failure, a standby can be quickly promoted to become the new primary, minimizing downtime (low RTO).
          * **Read Scaling:** Standby servers can serve read-only queries, offloading the primary and improving application performance.
          * **Disaster Recovery:** Standbys can be in different geographical locations for regional disaster recovery.
      * **Failover/Switchover:**
          * **Failover:** The process of manually or automatically promoting a standby to primary in response to a primary failure.
          * **Switchover:** A planned promotion of a standby to primary, usually for maintenance or upgrades, with careful coordination to minimize downtime.

  * **5.2. Logical Replication (PostgreSQL 10+):**

      * **Concept:** A publisher-subscriber model that replicates *data changes at the row level* rather than physical WAL segments. It uses logical decoding to extract changes from the WAL.
      * **Architecture:** A "publisher" database publishes changes for specific tables/databases, and "subscribers" consume these changes.
      * **How it Works:** The publisher generates logical WAL records for DML operations. Subscribers connect to the publisher and apply these changes.
      * **Use Cases:**
          * **Selective Replication:** Replicate only specific tables or schemas.
          * **Cross-Version Upgrades:** Replicate from an older PostgreSQL version to a newer one (allows for minimal downtime upgrades).
          * **Data Distribution:** Distribute data to multiple downstream systems (including non-PostgreSQL databases via custom decoders).
          * **Zero-Downtime Migrations:** Move data between different infrastructures.
      * **Benefits:**
          * **Flexibility:** Granular control over what data is replicated.
          * **Heterogeneous Environments:** Can replicate between different PostgreSQL versions or even different database types (with custom decoders).
          * **Lower Overhead for Specific Cases:** Can be less resource-intensive than physical replication if only a small subset of data needs to be replicated.
      * **Limitations:**
          * **No DDL Replication:** Schema changes (like `ALTER TABLE`) are *not* automatically replicated. You must manually apply DDL on both publisher and subscriber.
          * **No Sequence Replication:** Sequence states are not replicated.
          * **No Large Objects:** Large object changes are not replicated.
          * Not suitable for complete high availability requiring exact physical consistency (streaming replication is better here).

  * **Ineffectiveness of No HA:** A single point of failure means any outage (planned or unplanned) leads to application downtime. This is unacceptable for mission-critical systems.

-----

#### **6. Tools for Backup and Recovery (Barman, pgBackRest)**

While PostgreSQL provides native tools (`pg_dump`, `pg_basebackup`, WAL archiving), managing these manually in a complex production environment can be error-prone and time-consuming. Dedicated tools automate and enhance the process.

  * **Barman (Backup and Recovery Manager):**

      * **Features:**
          * **Centralized Management:** Manage backups for multiple PostgreSQL servers from a single control machine.
          * **Continuous Archiving:** Automates WAL archiving.
          * **Base Backups:** Integrates `pg_basebackup`.
          * **Point-in-Time Recovery (PITR):** Simplifies restoring to any point.
          * **Compression & Deduplication:** Reduces storage space.
          * **Retention Policies:** Automatically manages old backups.
          * **Recovery Operations:** Streamlines full restores and disaster recovery scenarios.
          * **Monitoring:** Provides status of backups and archiving.
      * **Why use it:** Provides a comprehensive, enterprise-grade solution for backup and recovery with a strong focus on disaster recovery.

  * **pgBackRest:**

      * **Features:**
          * **Reliability:** Designed for high reliability and data integrity.
          * **Parallel Processing:** Uses parallel jobs for faster backups and restores.
          * **Incremental/Differential Backups:** Efficiently backs up only changed data.
          * **Delta Restores:** Restores only required changes, significantly speeding up recovery.
          * **Asynchronous Archiving:** Efficient WAL archiving.
          * **Archive Integrity Checking:** Verifies WAL segments.
          * **Cloud Storage Integration:** Supports S3, Azure, Google Cloud Storage.
      * **Why use it:** Excellent for large databases, focusing on performance, robustness, and flexibility in backup/restore types.

  * **Ineffectiveness of Manual Backup Scripts:**

      * **Error-Prone:** Easy to make mistakes in shell scripts (permissions, paths, cleanup).
      * **Lack of Features:** No built-in compression, parallelization, proper retention policies, or robust monitoring.
      * **Complexity for PITR:** Manually tracking and managing WAL segments for PITR is extremely complex and risky.
      * **Hard to Scale:** Difficult to manage backups for dozens or hundreds of databases manually.
