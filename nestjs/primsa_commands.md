## MOST USED PRISMA COMMANDS

### 1\. `npx prisma init`

  * **Purpose:** This command initializes Prisma in your project. It creates a `prisma` directory with a `schema.prisma` file and a `.env` file to store your database connection string.
  * **When to use it:** At the very beginning of a new project where you're setting up Prisma for the first time.
  * **Example (for PostgreSQL):**
    ```bash
    npx prisma init --datasource-provider postgresql
    ```
    This specifically sets up your `schema.prisma` to use PostgreSQL as the database provider.

### 2\. `npx prisma migrate dev`

  * **Purpose:** This is your go-to command for managing database schema changes during development. It does three crucial things:
    1.  It creates a new migration file in the `prisma/migrations` folder based on the changes you've made to your `schema.prisma`.
    2.  It applies these changes to your database.
    3.  It automatically generates or updates the Prisma Client (which is the TypeScript code you'll use to interact with your database).
  * **When to use it:** Every time you modify your `schema.prisma` file (e.g., add a new model, change a field, add a new relation) and want to sync these changes with your PostgreSQL database.
  * **Example:**
    ```bash
    npx prisma migrate dev --name init_database # For your initial migration
    npx prisma migrate dev --name add_user_profile # For subsequent changes
    ```
    The `--name` flag is important for giving your migration a descriptive name.

### 3\. `npx prisma db push`

  * **Purpose:** This command pushes the current state of your `schema.prisma` directly to your database, without creating a migration history.
  * **When to use it:** Primarily for rapid prototyping or during early development stages when you're quickly iterating on your schema and don't need to maintain a detailed migration history. **Use with caution in production, as it can lead to data loss if not used correctly.**
  * **Example:**
    ```bash
    npx prisma db push
    ```

### 4\. `npx prisma generate`

  * **Purpose:** This command generates the Prisma Client based on your `schema.prisma` file. The Prisma Client is the type-safe API that allows your NestJS application to interact with your PostgreSQL database.
  * **When to use it:**
      * After making any changes to your `schema.prisma` (although `prisma migrate dev` automatically calls this).
      * If you're using `prisma db push` and need to regenerate the client.
      * If you manually delete the `node_modules/@prisma/client` folder or have issues with your generated client.
  * **Example:**
    ```bash
    npx prisma generate
    ```

### 5\. `npx prisma studio`

  * **Purpose:** This command opens a graphical user interface (GUI) in your browser that allows you to view, explore, and manipulate the data in your PostgreSQL database. It's incredibly useful for development and debugging.
  * **When to use it:** To inspect your database data, manually add or modify records, or verify that your migrations have applied correctly.
  * **Example:**
    ```bash
    npx prisma studio
    ```

### 6\. `npx prisma migrate reset` (Use with extreme caution\!)

  * **Purpose:** This command deletes all data and tables in your database and then re-applies all your migrations from scratch.
  * **When to use it:** Only in development environments when you need a completely clean slate for your database, perhaps to resolve complex migration issues or when starting a feature from scratch. **Never use this in a production environment.**
  * **Example:**
    ```bash
    npx prisma migrate reset
    ```

### Best Practices for an SDE 1:

  * **Always use `npx`:** It ensures you're running the locally installed version of the Prisma CLI.
  * **Understand `migrate dev` vs. `db push`:** For most team-based or production-focused development, `prisma migrate dev` is preferred as it maintains a clear history of schema changes. `db push` is for quick, local iterations.
  * **Commit your migrations:** The `prisma/migrations` folder should always be committed to version control.
  * **Regularly regenerate the client:** Ensure your Prisma Client is always up-to-date with your `schema.prisma` to leverage type safety.
  * **Use `.env` for database URLs:** Keep your database credentials out of your code and in environment variables.