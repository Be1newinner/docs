# **14. Configuration Management**

In any production-grade application, managing configuration is paramount. This includes environment-specific settings (database URLs, API keys, service endpoints), sensitive credentials (secrets), and various application parameters that change between development, testing, staging, and production environments. Hardcoding these values is a massive anti-pattern and a significant security risk.

NestJS provides the `@nestjs/config` module, which is built on top of the popular `dotenv` package, offering a robust and type-safe way to manage configurations.

**Why comprehensive Configuration Management for FAANG-level applications?**

  * **Security**: Prevents sensitive data (like database passwords, API keys, JWT secrets) from being committed to source control.
  * **Flexibility & Portability**: Allows the same codebase to run in different environments (dev, test, prod) without modification, simply by changing environment variables.
  * **Maintainability**: Centralizes configuration, making it easier to manage and update.
  * **Scalability**: Critical for containerized environments (Docker, Kubernetes) where configurations are injected at runtime.
  * **Observability**: Well-managed configurations are easier to audit and troubleshoot.
  * **Developer Experience**: With type-safe configuration, developers get IntelliSense and compile-time checks for configuration access, reducing runtime errors.

**Core Components:**

1.  **`@nestjs/config`**: The main module providing configuration utilities.
2.  **`dotenv`**: The underlying library for loading environment variables from `.env` files.
3.  **Environment Variables**: Key-value pairs stored outside the codebase, typically in `.env` files locally and injected by the hosting environment in production.
4.  **Configuration Schemas (e.g., with Zod)**: For type-safe validation and definition of configuration shape.

**Installation:**

```bash
npm install @nestjs/config zod
```

  * `@nestjs/config`: The NestJS configuration module.
  * `zod`: A TypeScript-first schema declaration and validation library, which we'll use for robust configuration validation.

-----

### **14.1 Managing Environment Variables and Secrets**

The primary mechanism for managing environment variables and secrets in a local development environment is through `.env` files. In production, these are typically injected directly into the container or server process by your CI/CD pipeline or orchestration platform (e.g., Kubernetes Secrets, AWS Secrets Manager, Google Secret Manager).

**`.env` File (Local Development Example):**

Create a `.env` file in the root of your project. **Crucially, add `.env` to your `.gitignore` file to prevent it from being committed to your repository.**

```ini
# .env
# --- Application Settings ---
NODE_ENV=development
PORT=3000
API_PREFIX=api/v1
CORS_ORIGIN=* # Be specific in production, e.g., https://yourfrontend.com

# --- Database Settings (MongoDB) ---
MONGODB_URI=mongodb://localhost:27017/ecommerce_db_dev

# --- JWT Settings ---
JWT_SECRET=superSecretDevelopmentKey!_Change_In_Prod_12345
JWT_EXPIRATION_TIME=1h

# --- Third-party Service Keys (Example) ---
STRIPE_SECRET_KEY=sk_test_some_random_key
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USER=your_mailtrap_user
SMTP_PASS=your_mailtrap_password
```

**`.gitignore` Entry:**

```gitignore
# Environment variables
.env
.env.production
.env.staging
```

**Accessing Variables with `@nestjs/config`:**

The `ConfigModule` loads these variables and makes them accessible throughout your application via the `ConfigService`.

1.  **Import `ConfigModule`**:
    Ensure `ConfigModule` is imported and configured in your `AppModule` (or a dedicated `ConfigModule` if you prefer). It's best practice to make it global.

      * **`app.module.ts`**:
        ```typescript
        // src/app.module.ts
        import { Module } from '@nestjs/common';
        import { ConfigModule } from '@nestjs/config'; // Import ConfigModule
        import { MongooseModule } from '@nestjs/mongoose';
        // ... other imports ...

        @Module({
          imports: [
            ConfigModule.forRoot({
              isGlobal: true, // Makes ConfigModule available throughout the app
              envFilePath: '.env', // Specifies the path to your .env file
              // You can also load multiple files: envFilePath: ['.env.development', '.env'],
            }),
            MongooseModule.forRootAsync({
              imports: [ConfigModule], // Make sure ConfigModule is imported if you use ConfigService here
              useFactory: async (configService) => ({
                uri: configService.get<string>('MONGODB_URI'),
                // ... other Mongoose options ...
              }),
              inject: [ConfigService], // Inject ConfigService
            }),
            // ... other modules like AuthModule, UserModule, ProductsModule, OrdersModule, OrderStatusModule
          ],
          controllers: [],
          providers: [],
        })
        export class AppModule {}
        ```
          * **FAANG Insight**: `isGlobal: true` simplifies usage as you don't need to import `ConfigModule` in every module where you need `ConfigService`. For larger applications, sometimes a dedicated `SharedConfigModule` is used, but for most NestJS projects, `isGlobal` is fine. `envFilePath` is critical for local development; in production, environment variables are typically injected directly and `dotenv` may not even be needed.

2.  **Using `ConfigService`**:
    Inject `ConfigService` into any provider or controller where you need configuration values.

    ```typescript
    // src/auth/strategies/jwt.strategy.ts (Example from Chapter 12)
    import { Injectable, UnauthorizedException } from '@nestjs/common';
    import { PassportStrategy } from '@nestjs/passport';
    import { ExtractJwt, Strategy } from 'passport-jwt';
    import { ConfigService } from '@nestjs/config'; // Import ConfigService
    import { UserService } from '../../users/user.service';

    @Injectable()
    export class JwtStrategy extends PassportStrategy(Strategy) {
      constructor(
        private configService: ConfigService, // Inject ConfigService
        private userService: UserService,
      ) {
        super({
          jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
          ignoreExpiration: false,
          secretOrKey: configService.get<string>('JWT_SECRET'), // Access JWT_SECRET
        });
      }

      // ... validate method ...
    }
    ```

    ```typescript
    // src/main.ts (Example from Chapter 13)
    import { NestFactory } from '@nestjs/core';
    import { AppModule } from './app.module';
    import { ValidationPipe } from '@nestjs/common';
    import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
    import { ConfigService } from '@nestjs/config'; // Import ConfigService

    async function bootstrap() {
      const app = await NestFactory.create(AppModule);

      const configService = app.get(ConfigService); // Get ConfigService instance
      const port = configService.get<number>('PORT') || 3000;
      const apiPrefix = configService.get<string>('API_PREFIX') || 'api/v1';
      const corsOrigin = configService.get<string>('CORS_ORIGIN') || '*';

      // ... global pipes, prefix, swagger setup ...

      app.enableCors({
        origin: corsOrigin, // Use configured CORS origin
        methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
        credentials: true,
      });

      await app.listen(port);
      console.log(`Application is running on: ${await app.getUrl()}/${apiPrefix}`);
      console.log(`Swagger UI available at: ${await app.getUrl()}/api-docs`);
    }
    bootstrap();
    ```

-----

### **14.2 Type-Safe Configuration using `@nestjs/config` and Zod**

While accessing environment variables directly using `configService.get<string>('KEY')` works, it's prone to runtime errors if a key is missing or has an unexpected type. For FAANG-level reliability, we need **type safety and robust validation** for our configuration. Zod is an excellent choice for this.

**Steps for Type-Safe Configuration:**

1.  **Define Configuration Schema with Zod**:
    Create a Zod schema that defines the shape and validation rules for your environment variables.

      * **`config.schema.ts`**:
        ```typescript
        // src/config/config.schema.ts
        import { z } from 'zod';

        export const configSchema = z.object({
          NODE_ENV: z.enum(['development', 'production', 'test', 'staging']).default('development'),
          PORT: z.coerce.number().int().positive().default(3000),
          API_PREFIX: z.string().min(1).default('api/v1'),
          CORS_ORIGIN: z.string().min(1).default('*'), // Be more specific in prod

          MONGODB_URI: z.string().url('Invalid MongoDB URI format'),

          JWT_SECRET: z.string().min(16, 'JWT_SECRET must be at least 16 characters long'),
          JWT_EXPIRATION_TIME: z.string().default('1h'), // e.g., '1h', '7d'

          // Optional: Add more specific validation for third-party services
          STRIPE_SECRET_KEY: z.string().optional(),
          SMTP_HOST: z.string().optional(),
          SMTP_PORT: z.coerce.number().int().positive().optional(),
          SMTP_USER: z.string().optional(),
          SMTP_PASS: z.string().optional(),
        });

        export type AppConfig = z.infer<typeof configSchema>;
        ```
          * **FAANG Insight**:
              * `z.object({...})`: Defines the expected structure of your configuration.
              * `z.enum()`: Ensures `NODE_ENV` is one of the allowed values.
              * `z.coerce.number()`: Automatically converts string environment variables to numbers.
              * `.int().positive()`: Adds numerical constraints.
              * `.default()`: Provides fallback values if the variable is not set.
              * `z.string().url()`: Validates that `MONGODB_URI` is a valid URL.
              * `.min(16)`: Enforces minimum length for secrets.
              * `.optional()`: Marks fields as optional, meaning they don't have to be present.
              * `export type AppConfig = z.infer<typeof configSchema>;`: This is the magic\! Zod infers the TypeScript type from your schema, giving you full type safety when accessing configuration.

2.  **Load and Validate Configuration with `ConfigModule`**:
    Use the `validationSchema` option in `ConfigModule.forRoot()`.

      * **`app.module.ts` (updated):**
        ```typescript
        // src/app.module.ts
        import { Module } from '@nestjs/common';
        import { ConfigModule } from '@nestjs/config';
        import { MongooseModule } from '@nestjs/mongoose';
        import { configSchema } from './config/config.schema'; // Import your Zod schema
        // ... other imports ...

        @Module({
          imports: [
            ConfigModule.forRoot({
              isGlobal: true,
              envFilePath: '.env',
              validationSchema: configSchema, // <--- Add your Zod schema here
              // Optional: Provide custom validation options, e.g., validationOptions: { abortEarly: false }
            }),
            MongooseModule.forRootAsync({
              imports: [ConfigModule],
              useFactory: async (configService) => ({
                uri: configService.get<string>('MONGODB_URI'),
                // ... other Mongoose options ...
              }),
              inject: [ConfigService],
            }),
            // ... other modules
          ],
          controllers: [],
          providers: [],
        })
        export class AppModule {}
        ```
          * **FAANG Insight**: When `validationSchema` is provided, `ConfigModule` will automatically validate your environment variables against this schema during application startup. If validation fails (e.g., a required variable is missing, or a type is incorrect), the application will **fail to start immediately**, preventing deployment of misconfigured applications. This "fail-fast" approach is crucial for production systems.

3.  **Accessing Type-Safe Configuration**:
    Now, when you inject `ConfigService`, you can specify the `AppConfig` type for improved type safety.

    ```typescript
    // src/auth/strategies/jwt.strategy.ts (Updated for type safety)
    import { Injectable, UnauthorizedException } from '@nestjs/common';
    import { PassportStrategy } from '@nestjs/passport';
    import { ExtractJwt, Strategy } from 'passport-jwt';
    import { ConfigService } from '@nestjs/config';
    import { UserService } from '../../users/user.service';
    import { AppConfig } from '../../config/config.schema'; // Import the inferred type

    @Injectable()
    export class JwtStrategy extends PassportStrategy(Strategy) {
      constructor(
        private configService: ConfigService<AppConfig>, // <--- Now type-safe!
        private userService: UserService,
      ) {
        super({
          jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
          ignoreExpiration: false,
          secretOrKey: this.configService.get('JWT_SECRET'), // No need for <string> here
        });
      }

      // ... validate method ...
    }
    ```

      * **FAANG Insight**: By declaring `configService: ConfigService<AppConfig>`, you get compile-time checks and IntelliSense for all your environment variables. If you try to access `configService.get('NON_EXISTENT_VAR')`, TypeScript will immediately flag it, catching errors before runtime. This is a huge win for developer productivity and system reliability.

-----

### **FAANG-level Configuration Best Practices:**

1.  **Environment-Specific Files**: For different environments, you can specify different `.env` files. E.g., `.env.development`, `.env.test`, `.env.production`. You can load them conditionally:

    ```typescript
    ConfigModule.forRoot({
      envFilePath: `.env.${process.env.NODE_ENV || 'development'}`,
      // ...
    }),
    ```

      * **FAANG Insight**: While this is useful for managing distinct local environments, in actual production deployments, environments variables are rarely managed via physical files on the server. They are injected by the deployment platform.

2.  **External Secrets Management**:

      * **Cloud Providers**: AWS Secrets Manager, Google Secret Manager, Azure Key Vault.
      * **Dedicated Tools**: HashiCorp Vault.
      * **Kubernetes Secrets**: Encrypted at rest, but generally not encrypted in transit or memory. Requires careful access control.
      * **FAANG Insight**: This is paramount for production. Never store secrets directly in `.env` files on production servers or commit them to source control. Your CI/CD pipeline should retrieve secrets from a secure store and inject them as environment variables into your application containers at runtime.

3.  **Sensitive Data Handling**:

      * **No logging of secrets**: Ensure secrets are never logged (even truncated or masked).
      * **Encryption at Rest/In Transit**: Databases and inter-service communication should use encryption.
      * **Rotation**: Implement a strategy for regularly rotating secrets (e.g., database passwords, API keys).

4.  **Runtime Configuration (Advanced)**:
    Sometimes, configuration needs to be fetched at runtime from a centralized configuration service (e.g., AWS AppConfig, Consul, Spring Cloud Config). This is more common in large microservices architectures where services dynamically update their configuration without a full restart.

      * **FAANG Insight**: For the scale of a single e-commerce backend, injecting via environment variables is sufficient. For 100s or 1000s of microservices, dynamic configuration management becomes more critical.

5.  **Configuration as Code**:
    Treat your configuration (especially the Zod schema) as code that is version-controlled and peer-reviewed.

6.  **Immutable Deployments**:
    The application package (Docker image) should be immutable. All environment-specific parameters should be externalized as configuration, allowing the same image to be deployed across environments.

This chapter equips you with the knowledge to handle application configuration like a seasoned professional, ensuring your application is secure, flexible, and ready for deployment across various environments.