### **Chapter 15: Monitoring and Observability**

This chapter focuses on gaining insights into your PostgreSQL database's operations. You will learn about key metrics to track, how to leverage PostgreSQL's built-in statistics, configure effective logging, utilize popular monitoring tools, establish robust alerting, and practice proactive performance management to keep your database running smoothly.

-----

#### **1. Key Metrics to Monitor**

Monitoring involves collecting and analyzing various data points to understand the state and performance of your database server and the database instances running on it.

  * **System-Level Metrics:** These reflect the overall health of the server machine.

      * **CPU Utilization:** High CPU often indicates intensive query processing, complex calculations, or excessive connections. Monitor `user`, `system`, `iowait` CPU.
      * **Memory Usage:** Track available RAM, swap usage. High swap usage severely degrades performance. Monitor PostgreSQL's memory (`shared_buffers`, `work_mem`) vs. OS memory.
      * **Disk I/O (Input/Output):**
          * **Reads/Writes per second (IOPS):** How many read/write operations are occurring.
          * **Throughput (MB/s):** The volume of data being read/written.
          * **I/O Latency:** How long disk operations take. High latency is a major bottleneck.
          * **Disk Space Usage:** Critical for preventing outages due to full disks (data, WAL, logs, temporary files).
      * **Network Utilization:** Bandwidth usage, packet errors. Relevant for replication, client connections, and data transfer.

  * **Database-Level Metrics:** These provide insights into PostgreSQL's internal operations and workload.

      * **Connections:**
          * `Active Connections`: Number of clients currently connected.
          * `Idle in Transaction Connections`: Connections holding open transactions but not currently executing queries (potential for locks, resource waste).
          * `Max Connections Reached`: Alert if approaching `max_connections` limit.
      * **Query Latency:**
          * Average, 95th percentile, 99th percentile of query execution times. High latency directly impacts user experience.
          * Specific slow queries (identified via `log_min_duration_statement` or `pg_stat_statements`).
      * **Lock Contention:**
          * Number of active locks, types of locks (e.g., `AccessExclusiveLock`, `RowExclusiveLock`).
          * Blocking queries: Queries holding locks that prevent other queries from progressing.
      * **Transaction/WAL Activity:**
          * `Transactions per second (TPS)`: Overall database activity.
          * `WAL write activity`: Rate of WAL segment generation. High activity can indicate heavy writes and potential for I/O bottleneck on WAL disk.
          * `Checkpoints`: Frequency and duration of checkpoints. Too frequent can be bad.
      * **Replication Lag:** For HA setups, monitor the delay between primary and standby(s) (in bytes or time). High lag means higher RPO during failover.
      * **Cache Hit Ratio:** `shared_buffers` hit ratio. High hit ratio means data is served from memory, low means more disk I/O.
      * **Table/Index Statistics:** Number of sequential scans vs. index scans, dead tuples, bloat, index usage.

-----

#### **2. PostgreSQL Statistics Views (`pg_stat_activity`, `pg_stat_database`, etc.)**

PostgreSQL provides a rich set of built-in statistics views that expose detailed information about database activity, performance, and object usage. These views are the primary source for collecting database-specific metrics.

  * **`pg_stat_activity`:**

      * **Purpose:** Shows one row for each backend process (client connection), providing details on its current activity.
      * **Key Columns:** `pid`, `datname` (database name), `usename` (username), `client_addr`, `application_name`, `backend_start` (when connection established), `xact_start` (when current transaction started), `query_start` (when current query started), `state` (active, idle, idle in transaction), `wait_event_type`, `wait_event` (what the process is waiting on, e.g., `Lock`, `IO`), `query` (the query being executed).
      * **Use Cases:** Identifying long-running queries, blocking queries, idle-in-transaction connections, and overall active connections.

    <!-- end list -->

    ```sql
    -- Find active queries longer than 1 minute
    SELECT pid, usename, datname, client_addr, application_name, backend_start,
           xact_start, query_start, state, wait_event_type, wait_event, query
    FROM pg_stat_activity
    WHERE state = 'active' AND (now() - query_start) > INTERVAL '1 minute'
    ORDER BY query_start ASC;

    -- Find blocking queries (requires pg_locks)
    SELECT
        a.pid AS blocking_pid,
        a.usename AS blocking_user,
        a.application_name AS blocking_app,
        a.query AS blocking_query,
        b.pid AS blocked_pid,
        b.usename AS blocked_user,
        b.application_name AS blocked_app,
        b.query AS blocked_query
    FROM pg_stat_activity a
    JOIN pg_locks l1 ON a.pid = l1.pid AND l1.granted
    JOIN pg_locks l2 ON l1.relation = l2.relation AND l1.locktype = l2.locktype AND NOT l2.granted
    JOIN pg_stat_activity b ON l2.pid = b.pid;
    ```

  * **`pg_stat_database`:**

      * **Purpose:** Provides database-wide statistics.
      * **Key Columns:** `datname`, `numbackends` (active connections), `xact_commit`, `xact_rollback`, `blks_read` (disk reads), `blks_hit` (shared buffer hits), `tup_returned`, `tup_fetched`, `tup_inserted`, `tup_updated`, `tup_deleted`.
      * **Use Cases:** Calculating cache hit ratio (`blks_hit / (blks_hit + blks_read)`), overall transaction rate, and I/O activity per database.

    <!-- end list -->

    ```sql
    -- Check cache hit ratio and I/O for all databases
    SELECT datname,
           blks_read,
           blks_hit,
           CASE WHEN (blks_read + blks_hit) > 0 THEN ROUND((blks_hit::numeric / (blks_hit + blks_read)) * 100, 2) ELSE 0 END AS hit_ratio_pct,
           xact_commit,
           xact_rollback
    FROM pg_stat_database;
    ```

  * **`pg_stat_user_tables`:**

      * **Purpose:** Statistics specific to user tables.
      * **Key Columns:** `relname` (table name), `n_live_tup` (live tuples), `n_dead_tup` (dead tuples - indicates bloat/vacuum need), `n_mod_since_analyze` (changes since last analyze), `seq_scan` (sequential scans), `idx_scan` (index scans), `n_tup_ins`, `n_tup_upd`, `n_tup_del`.
      * **Use Cases:** Identifying bloated tables, tables that need `VACUUM` or `ANALYZE`, tables undergoing heavy DML, or tables that are unexpectedly being `Seq Scan`ned.

    <!-- end list -->

    ```sql
    -- Identify potentially bloated tables or those needing vacuum/analyze
    SELECT relname, n_live_tup, n_dead_tup,
           ROUND(n_dead_tup::numeric / (n_live_tup + n_dead_tup) * 100, 2) AS dead_tup_ratio_pct,
           n_mod_since_analyze,
           last_autovacuum, last_autoanalyze
    FROM pg_stat_user_tables
    WHERE n_live_tup > 0 AND n_dead_tup > 0
    ORDER BY dead_tup_ratio_pct DESC
    LIMIT 10;
    ```

  * **`pg_stat_user_indexes`:**

      * **Purpose:** Statistics specific to user-defined indexes.
      * **Key Columns:** `relname` (table name), `indexrelname` (index name), `idx_scan` (index scans), `idx_tup_fetch` (tuples fetched via index), `idx_tup_read` (index entries read).
      * **Use Cases:** Identifying unused indexes (low `idx_scan`), or indexes that are scanned but not effectively fetching tuples.

    <!-- end list -->

    ```sql
    -- Find potentially unused indexes (if idx_scan is very low/zero for active tables)
    SELECT relname, indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
    FROM pg_stat_user_indexes
    ORDER BY idx_scan ASC;
    ```

  * **`pg_locks`:** Shows current lock information. Useful in conjunction with `pg_stat_activity` to find blocking queries.

  * **`pg_stat_replication`:** (On primary) Shows status of replication standbys (e.g., `replay_lag`).

-----

#### **3. Logging Configuration (`postgresql.conf`)**

PostgreSQL's logging is invaluable for monitoring, auditing, and troubleshooting. Correct configuration ensures you capture the right information without overwhelming your system.

  * **Review from Chapter 11 (Security & Auditing):**

      * `log_destination = 'csvlog'`: (Highly recommended) Logs in CSV format, which is easy for automated tools and scripts to parse.
      * `logging_collector = on`: Enables the background process to capture log messages to files.
      * `log_directory`, `log_filename`, `log_rotation_age`, `log_rotation_size`: Manage log file location and rotation.
      * `log_connections = on`, `log_disconnections = on`: Track client connections.

  * **Key Parameters for Performance Monitoring:**

      * **`log_min_duration_statement = 500ms`:** (Crucial) Logs any statement that runs for longer than the specified duration (e.g., 500 milliseconds). Setting this to `0` logs *all* statements, which is useful for short-term debugging but usually too verbose for production. This is your primary source for identifying slow queries.
      * `log_temp_files = 0`: Logs creation of temporary files larger than the specified size (0 for all). Large temp files indicate queries spilling to disk due to insufficient `work_mem`.
      * `log_lock_waits = on`: Logs when a session waits longer than `deadlock_timeout` for a lock. Helps identify lock contention.
      * `log_autovacuum_min_duration = 0`: Logs all autovacuum actions. Helps understand autovacuum's behavior.

  * **Best Practices:**

      * Direct logs to a central logging system (Splunk, ELK stack, Datadog) for aggregation, analysis, alerting, and long-term retention.
      * Monitor disk space for log directories.
      * Avoid `log_statement = 'all'` in production unless explicitly debugging a short, critical period, as it generates enormous log volumes.

-----

#### **4. Tools for Monitoring**

While `psql` and direct queries to `pg_stat_*` views are useful for ad-hoc checks, dedicated monitoring tools provide continuous collection, visualization, and alerting.

  * **Prometheus & Grafana:**

      * **Prometheus:** An open-source monitoring system and time-series database. It "pulls" metrics from configured targets (PostgreSQL exporter, Node exporter for OS metrics).
      * **Grafana:** An open-source analytics and visualization platform. It connects to Prometheus (or other data sources) to create dynamic dashboards with graphs and alerts.
      * **PostgreSQL Exporter:** A community-maintained Prometheus exporter that scrapes metrics from `pg_stat_*` views and other sources, exposing them in a Prometheus-readable format.
      * **Benefits:** Powerful, flexible, highly customizable, open-source, and widely adopted in cloud-native environments.
      * **Architecture:** `PostgreSQL -> PostgreSQL Exporter -> Prometheus Server -> Grafana`

  * **Datadog / New Relic / Dynatrace:**

      * **Concept:** Commercial Application Performance Monitoring (APM) and infrastructure monitoring platforms.
      * **How they work:** Deploy agents on your database server that collect system metrics and integrate directly with PostgreSQL to pull database-specific metrics. They also offer APM for your application code.
      * **Benefits:** Comprehensive (full stack visibility), easy setup, pre-built dashboards, advanced alerting, AI-driven insights.
      * **Cons:** Commercial cost.

  * **pganalyze:**

      * **Concept:** A commercial monitoring service specifically designed for PostgreSQL.
      * **How it works:** Connects to your PostgreSQL instance, collects metrics (including query plans via `EXPLAIN`), and provides in-depth analysis, performance recommendations, and intelligent alerting.
      * **Benefits:** PostgreSQL-centric expertise, automated insights, focuses on actionable advice.
      * **Cons:** Commercial cost, a SaaS solution.

  * **`pg_activity`:**

      * A command-line tool (like `top` for PostgreSQL) that displays real-time activity, connections, queries, and various statistics.
      * **Benefits:** Quick, interactive view for immediate troubleshooting.

-----

#### **5. Alerting Strategies for Critical Events**

Monitoring is about seeing; alerting is about *being notified* when something needs attention. Effective alerting is crucial for proactive incident response.

  * **Why Alert?**

      * **Early Detection:** Catch problems before they become critical or impact users.
      * **Reduced Downtime:** Faster response means faster resolution.
      * **Proactive Maintenance:** Identify trends (e.g., slow disk usage growth) that indicate future issues.
      * **Security:** Detect suspicious activity (e.g., unusual number of failed login attempts).

  * **What to Alert On (Examples):**

      * **Availability:**
          * PostgreSQL process down.
          * Database connection failures.
      * **Performance:**
          * High CPU utilization (e.g., \>80% for 5 minutes).
          * Low free memory / High swap usage.
          * High disk I/O latency.
          * Disk space usage approaching critical thresholds (e.g., \>80%, \>90%).
          * `max_connections` limit approaching.
          * High query latency (e.g., average query time \> X ms or 99th percentile \> Y ms).
          * High number of `idle in transaction` connections.
          * Blocking queries lasting longer than a threshold.
          * High replication lag.
      * **Health:**
          * Excessive WAL file generation.
          * Autovacuum activity: Not running, or running too slowly on critical tables.
          * Critical errors in PostgreSQL logs.
      * **Security (from logs or `pgAudit`):**
          * Repeated failed login attempts.
          * Unauthorized privilege grants/revokes.
          * Suspicious DDL changes.

  * **How to Alert:**

      * **Define Thresholds:** Set clear thresholds for metrics (e.g., warning at 80% CPU, critical at 95%).
      * **Notification Channels:** PagerDuty (for on-call rotations), Slack, Email, SMS, VictorOps.
      * **Alert Fatigue:** Avoid over-alerting. Tune thresholds carefully and group related alerts to prevent engineers from ignoring notifications. Ensure alerts are actionable.
      * **Runbooks:** For every critical alert, have a documented runbook describing the problem, common causes, and initial troubleshooting steps.

-----

#### **6. Proactive Performance Management**

Monitoring isn't just about reacting to alerts; it's about continuous improvement and foresight.

  * **Regular Review of Top Queries:**
      * Periodically analyze `pg_stat_statements` for the most time-consuming queries (`total_time`, `mean_time`).
      * Use `EXPLAIN ANALYZE` on these queries to identify and optimize bottlenecks.
      * Check for changes in execution plans over time.
  * **Capacity Planning:**
      * Analyze historical trends of key metrics (CPU, Memory, Disk I/O, connections, TPS, data growth).
      * Forecast future resource needs based on application growth.
      * Plan hardware upgrades or scaling initiatives before resource exhaustion.
  * **Indexing Strategy Review:**
      * Regularly check `pg_stat_user_indexes` for unused or inefficient indexes.
      * Evaluate new queries for index opportunities.
  * **`VACUUM`/`ANALYZE` Monitoring:**
      * Ensure `autovacuum` is effectively managing dead tuples and statistics.
      * Monitor `n_dead_tup` and `n_mod_since_analyze` in `pg_stat_user_tables`.
      * Address table bloat proactively.
  * **Stay Updated:** Keep abreast of new PostgreSQL versions and features that can offer performance improvements or new monitoring capabilities.
  * **Stress Testing/Benchmarking:** Periodically simulate peak loads to understand system behavior under stress and identify new bottlenecks.