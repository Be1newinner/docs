### **Chapter 13: High Availability and Replication**

This chapter explores how to design and implement resilient PostgreSQL deployments that can withstand failures and continue serving requests. We will deepen our understanding of PostgreSQL's replication capabilities, discuss the crucial mechanisms of failover and switchover, strategies for load balancing, and introduce the leading tools and frameworks that automate these complex HA setups.

---

#### **1. Understanding High Availability (HA) and Disaster Recovery (DR)**

While often used interchangeably, High Availability (HA) and Disaster Recovery (DR) address different aspects of system resilience:

* **High Availability (HA):**
    * **Goal:** To minimize service interruption due to *local* failures (e.g., server crash, network interface failure, database process dying).
    * **Focus:** Achieves rapid recovery (low RTO – Recovery Time Objective, often measured in seconds to a few minutes). Aims for continuous operation or very short downtime.
    * **Scope:** Typically within a single data center or availability zone.
    * **Mechanisms:** Redundancy (multiple servers), automatic failover, health checks, monitoring.

* **Disaster Recovery (DR):**
    * **Goal:** To recover from *catastrophic, widespread failures* (e.g., entire data center outage, major natural disaster, regional network collapse).
    * **Focus:** Restoring operations at an alternative, geographically separate location. RTO and RPO (Recovery Point Objective) are typically higher than HA (minutes to hours for RTO, minutes to hours for RPO).
    * **Scope:** Across different geographical regions or data centers.
    * **Mechanisms:** Offsite backups, cross-region replication, pre-provisioned infrastructure in secondary locations.

* **Interplay:** HA is often a component of a broader DR strategy. A highly available cluster within one region can also serve as the source for replication to a disaster recovery site in another region. You need both for robust systems.

---

#### **2. PostgreSQL Replication Architectures**

PostgreSQL offers two primary built-in replication methods: **Physical Replication** and **Logical Replication**, each with distinct use cases and characteristics.

* **2.1. Physical Replication (Streaming Replication)**
    * **Concept:** This is the most common form of replication for HA and DR. It works by continuously shipping or streaming the Write-Ahead Log (WAL) records from a primary server to one or more standby servers. The standbys apply these WAL records, effectively keeping a byte-for-byte identical copy of the primary's data.
    * **Architecture:** Typically involves one **Primary** (master) server that accepts all reads and writes, and one or more **Standby** (replica/slave) servers that only accept reads (if configured as "hot standby").
    * **Modes:**
        * **Asynchronous Streaming Replication (Default):**
            * **How it works:** The primary commits transactions as soon as the WAL record is written to its local disk. It does *not* wait for the standby to receive or apply the WAL.
            * **Configuration:** `synchronous_standby_names = ''` (or omit).
            * **Pros:** Fastest commit times on the primary.
            * **Cons:** Potential for minimal data loss on primary failure (transactions committed on primary might not have reached the standby yet).
            * **Use Cases:** Most common setup. Suitable when slightly higher RPO (a few seconds of potential data loss) is acceptable in favor of lower write latency.
        * **Synchronous Streaming Replication:**
            * **How it works:** The primary waits for a configured number of standbys to confirm that they have *received and written* the WAL records to their disk before the primary reports the transaction as committed.
            * **Configuration:** `synchronous_standby_names = 'ANY 1 (standby_name)'` (requires at least one named standby to confirm).
            * **Pros:** Zero data loss guarantee (RPO = 0) on primary failure, as all committed transactions are guaranteed to be on at least one standby.
            * **Cons:** Higher write latency on the primary (due to network round trip and standby's disk I/O). If the designated synchronous standby fails, the primary will halt until it reconnects or configuration is changed.
            * **Use Cases:** Mission-critical applications where data integrity is paramount, and any data loss is unacceptable.
            * **Quorum Synchronous Replication:** By listing multiple standbys in `synchronous_standby_names` (e.g., `ANY 2 (standby1, standby2, standby3)`), the primary can wait for any two standbys to confirm, offering a balance between performance and availability.
    * **Cascading Replication:**
        * A standby server can itself act as a primary for other standbys (Primary -> Standby1 -> Standby2 -> Standby3...).
        * **Benefits:** Reduces the WAL streaming load on the primary, allowing more standbys without overwhelming the primary. Useful for large clusters or geo-distributed standbys.
    * **Hot Standby:**
        * Allows read-only queries to be executed on the standby server while WAL records are being applied. Requires `hot_standby = on` (default in recent versions).
        * **Benefits:** Enables read scaling by distributing read traffic across multiple replicas.
    * **Setting Up (Key Parameters):**
        * On Primary: `wal_level = replica`, `archive_mode = on`, `max_wal_senders` (number of concurrent WAL sender processes).
        * On Standby: `primary_conninfo` (connection string to primary), `restore_command` (for archive recovery), `hot_standby = on`, `standby.signal` file (PostgreSQL 12+).
        * `hot_standby_feedback = on`: (on standby) Sends information back to the primary about the oldest active query on the standby, preventing the primary from prematurely removing old data versions required by standby queries (avoids "query canceled because of conflict with recovery").
    * **Ineffectiveness:** Physical replication creates an exact copy. It cannot selectively replicate subsets of tables, nor can it replicate across different major PostgreSQL versions (e.g., Postgres 14 to Postgres 16 directly).

* **2.2. Logical Replication (Publication/Subscription)**
    * **Concept:** Introduced in PostgreSQL 10, logical replication provides a more flexible, row-based replication system. Instead of byte-level WAL segments, it decodes and streams logical changes (INSERTs, UPDATEs, DELETEs) from the WAL.
    * **Architecture:** `Publisher` (source database) creates `Publication`s for tables. `Subscriber` (destination database) creates `Subscription`s to consume these publications.
    * **How it Works:**
        * **Publisher:** Configures tables to be part of a `PUBLICATION`. Uses `pg_logical_replication_slot` to retain WAL records for the subscriber.
        * **Subscriber:** Creates a `SUBSCRIPTION` that connects to the publisher. It applies the logical changes to its own tables.
    * **Replication Slots:**
        * Crucial for both physical and logical replication. A replication slot ensures that the primary/publisher will *not* remove WAL segments required by a standby/subscriber until those segments have been consumed by the replica.
        * **Benefits:** Prevents WAL segment loss, even if the standby/subscriber is temporarily disconnected.
        * **Caution:** If a slot is not consumed by a replica, it will cause WAL accumulation on the primary, potentially filling up disk space. Monitor `pg_replication_slots` (`active`, `wal_status`, `restart_lsn`).
    * **Use Cases:**
        * **Selective Replication:** Replicate only specific tables or schemas.
        * **Cross-Version Upgrades:** Facilitates upgrading between major PostgreSQL versions with minimal downtime.
        * **Data Distribution:** Distribute data to multiple downstream systems, including potentially non-PostgreSQL databases (via custom decoders).
        * **Consolidating Data:** Merge data from multiple sources into a central data warehouse.
        * **Zero-Downtime Migrations:** Moving databases between different cloud providers or environments.
    * **Limitations:**
        * **No DDL Replication:** Schema changes (`ALTER TABLE`, `CREATE INDEX`) are *not* automatically replicated. You must manually apply DDL on both publisher and subscriber.
        * **No Sequence Replication:** Sequence states (`nextval()`) are not replicated.
        * **No Large Objects:** Changes to `oid` columns (large objects) are not replicated.
        * Less efficient for full database replication compared to physical replication due to the overhead of logical decoding and row-by-row application.
    * **Ineffectiveness:** Logical replication is not a drop-in replacement for physical replication when full database consistency (including DDL) or an exact binary copy is needed for HA/DR.

---

#### **3. Failover and Switchover Mechanisms**

These are the processes of shifting the primary role from one server to another within a replication cluster.

* **Failover (Unplanned):**
    * **Scenario:** The active primary server unexpectedly crashes or becomes unavailable.
    * **Process:**
        1.  **Failure Detection:** Monitoring tools detect the primary's failure.
        2.  **Election/Promotion:** A standby is elected (or manually chosen) and promoted to become the new primary. (`pg_ctl promote` or `SELECT pg_promote()`).
        3.  **Client Redirection:** Applications must be redirected to connect to the new primary.
        4.  **Old Primary Recovery:** The old primary, if it comes back online, must be reconfigured as a standby of the new primary to avoid a "split-brain" scenario.
    * **Challenges:**
        * **Split-Brain:** If both the original primary and a promoted standby believe they are the primary, they can both accept writes, leading to data divergence and corruption. Proper fencing/quorum mechanisms are vital.
        * **Data Loss:** If using asynchronous replication, some committed transactions on the failed primary might be lost.
        * **Client Redirection:** How quickly and reliably can clients find the new primary?
    * **Role of HA Tools:** Automated failover is complex and prone to errors if done manually. HA frameworks like Patroni automate detection, election, promotion, and redirection, mitigating split-brain risks.

* **Switchover (Planned):**
    * **Scenario:** A controlled, graceful change of the primary for scheduled maintenance, hardware upgrades, or version upgrades.
    * **Process:**
        1.  **Prepare Standby:** Ensure a standby is fully caught up and healthy.
        2.  **Graceful Shutdown/Demotion:** The current primary is gracefully shut down or demoted to a standby role.
        3.  **Promotion:** The chosen standby is promoted to be the new primary.
        4.  **Client Redirection:** Applications are redirected.
        5.  **Old Primary Reconfiguration:** The old primary is configured to follow the new primary.
    * **Goal:** Zero data loss and minimal (ideally zero) downtime. Much safer than a failover.

---

#### **4. Load Balancing for Read Replicas**

When using hot standbys for read scaling, you need a strategy to distribute read queries across multiple replicas effectively.

* **Why Needed:**
    * Scales read throughput beyond what a single primary can handle.
    * Offloads read traffic from the primary, improving its write performance.
    * Provides redundancy for read queries.

* **Methods:**
    1.  **Application-Level Load Balancing:**
        * **How it works:** The application code is aware of all primary and replica endpoints and directs read queries to replicas, and write queries to the primary.
        * **Pros:** Granular control, can implement complex routing logic.
        * **Cons:** Increases application complexity, requires manual endpoint updates on topology changes.
    2.  **DNS-based Load Balancing (e.g., Round-Robin DNS):**
        * **How it works:** Create multiple `A` records for a single hostname, each pointing to a different replica IP. DNS servers rotate through these IPs.
        * **Pros:** Simple to set up.
        * **Cons:** Very poor for HA (slow to remove failed replicas from rotation, no health checks), uneven distribution, client-side caching of DNS can lead to stale connections.
    3.  **Dedicated Load Balancers / Proxies (e.g., Pgpool-II, HAProxy, Nginx):**
        * **How it works:** A separate proxy layer sits between the application and the database servers. It performs health checks on all replicas and intelligently routes read queries to available replicas.
        * **Pgpool-II:** A PostgreSQL-specific middleware that offers connection pooling, load balancing, query routing, and even HA features for the pooler itself.
        * **HAProxy / Nginx:** General-purpose TCP/HTTP load balancers that can be configured to distribute PostgreSQL connections based on health checks.
        * **Pros:** Robust health checks, automatic failover detection (for routing), connection pooling, centralized configuration.
        * **Cons:** Adds another component to manage, potential single point of failure if the load balancer itself isn't redundant.

* **Challenges with Read Replicas:**
    * **Read Consistency (Stale Reads):** With asynchronous replication, there will be a replication lag. A read on a replica might return slightly stale data compared to the primary. Applications must be designed to tolerate this or use synchronous replication for critical reads.
    * **Session Stickiness:** For applications that rely on multiple statements within a session where later statements depend on earlier ones, ensuring all statements in a "read-only transaction" go to the *same* replica can be challenging.

---

#### **5. Introduction to Connection Pooling for HA Setups**

Connection poolers (like PgBouncer or Odyssey, which we discussed in Chapter 10) are crucial for HA setups, even beyond their basic function of reducing connection overhead.

* **How Connection Pooling Helps in HA:**
    * **Hides Failover from Applications:** When a failover occurs and the primary endpoint changes, the connection pooler can detect this change and seamlessly redirect new (or even existing, in `transaction` or `statement` mode) client connections to the new primary. Applications remain unaware of the underlying database topology change, reducing client-side reconnection logic.
    * **Reduces Reconnection Storms:** Instead of all application instances simultaneously trying to reconnect to the new primary after a failover (potentially overwhelming it), the pooler handles the limited number of backend connections, mitigating connection storms.
    * **Centralized Endpoint:** Applications always connect to the fixed address of the pooler, simplifying application configuration.
    * **Session/Transaction/Statement Pooling:**
        * `Session Pooling`: Client holds connection to pooler for session, pooler holds connection to DB for session. Failover means all DB connections for that pooler need to reconnect.
        * `Transaction Pooling`: Client holds connection to pooler for session, but pooler assigns a DB connection per *transaction*. This is excellent for failover, as new transactions will automatically go to the new primary.
        * `Statement Pooling`: Most aggressive. Connection assigned per *statement*.

* **Best Practice:** Always deploy a connection pooler (and ensure the pooler itself is highly available) in front of your PostgreSQL cluster in any production HA setup.

---

#### **6. Tools and Frameworks for HA (Patroni, Repmgr)**

Managing a PostgreSQL HA cluster manually (failover, replica creation, monitoring) is complex and error-prone. Dedicated tools automate these tasks.

* **Patroni:**
    * **Concept:** A highly robust, Python-based framework for building and managing PostgreSQL HA clusters. It uses a distributed consensus store (like etcd, Consul, or Apache Zookeeper) to maintain cluster state, elect a primary, and coordinate failovers.
    * **Features:**
        * **Automatic Failover:** Detects primary failures and automatically promotes a healthy standby.
        * **Automatic Switchover:** Facilitates controlled primary changes.
        * **Self-Healing:** Monitors cluster health and attempts to bring unhealthy nodes back into service.
        * **Replica Creation:** Can automate the creation of new standbys using `pg_basebackup`.
        * **WAL Archiving Integration:** Manages WAL archiving and retrieval.
        * **REST API:** For management and monitoring.
        * **Configuration Management:** Manages `postgresql.conf` for the cluster.
    * **Why use it:** Patroni is the de facto standard for fully automated, production-grade PostgreSQL HA. It significantly reduces operational burden and human error. It handles the full lifecycle of a PostgreSQL HA cluster.

* **Repmgr:**
    * **Concept:** A suite of open-source tools for managing PostgreSQL replication and failover. It's more of a replication management tool than a full HA solution, often used in conjunction with external cluster managers like Pacemaker for full automation.
    * **Features:**
        * **Clone Standby:** Simplifies creating new replicas from a primary.
        * **Monitor Replication:** Provides tools to monitor the health and status of replication.
        * **Manual/Assisted Failover:** Guides or automates the failover process (but requires external fencing for true safety in automatic mode).
        * **Switchover:** Facilitates planned primary changes.
        * **Witness Server:** Can use a witness server to help prevent split-brain.
    * **Why use it:** Good for users who want more direct control over replication management and are comfortable integrating it with other HA components (e.g., Pacemaker + Corosync) for full automation. Can be simpler to set up for smaller, less complex HA needs than Patroni if full automation isn't the primary goal.

* **Comparison:**
    * **Patroni:** More comprehensive, fully automated (including primary election and self-healing), leverages distributed consensus. Generally preferred for modern, highly available cloud-native deployments.
    * **Repmgr:** Focuses more on replication management, requires more external tooling for full automation (especially robust split-brain prevention). Can be easier for initial setup and manual control.