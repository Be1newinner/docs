<immersive type="text/markdown">

# 09-exception-filters

## 🚨 Exception Filters: Centralized Error Handling

In any robust application, proper error handling is paramount. NestJS provides **Exception Filters** as a dedicated layer to catch unhandled exceptions (thrown by controllers, services, guards, pipes, or interceptors) and transform them into appropriate HTTP responses. This ensures a consistent error contract for your API consumers, preventing sensitive internal error details from leaking.

### What is an Exception Filter?

An exception filter is a class decorated with `@Catch()` that implements the `ExceptionFilter` interface. The `@Catch()` decorator specifies which type of exception(s) the filter should handle.

### 🎯 Responsibility & Why Use Exception Filters? (FAANG Perspective)

From a FAANG-level system design perspective, Exception Filters are critical for:

1.  **Consistent Error Responses:** Ensuring all error responses adhere to a predefined format, making your API predictable and easier for clients to consume.
2.  **Information Hiding:** Preventing sensitive stack traces or internal server errors from being exposed to the client, enhancing security.
3.  **User-Friendly Messages:** Transforming technical error messages into more understandable and actionable messages for API consumers.
4.  **Centralized Logging:** Providing a single point to log all unhandled exceptions, crucial for monitoring and debugging in production.
5.  **Separation of Concerns:** Decoupling error handling logic from business logic and request processing, keeping controllers and services clean.
6.  **Fault Tolerance:** Contributing to a more resilient system by gracefully handling unexpected errors.

### How Exception Filters Work

When an unhandled exception occurs within your NestJS application (after middleware, pipes, and guards, but before the response is sent), the exception filter chain is invoked.

  * The `catch()` method of an exception filter receives two arguments:
      * `exception: unknown`: The actual exception object that was thrown.
      * `host: ArgumentsHost`: An object providing utilities to access the `ExecutionContext` (HTTP, WebSockets, RPC context). You'll typically use `host.switchToHttp().getRequest()` and `host.switchToHttp().getResponse()`.

### ✅ Example 1: Catching `HttpException` and its Descendants

NestJS provides a built-in `HttpException` class and a set of standard exceptions (e.g., `BadRequestException`, `UnauthorizedException`, `NotFoundException`). It's good practice to create a filter that handles these in a consistent way.

```bash
# From your project root
nest g filter common/http-exception
```

```typescript
// src/common/http-exception/http-exception.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { Request, Response } from 'express';
import { LoggerService } from '../../shared/logger/logger.service'; // Our custom logger

@Catch(HttpException) // This filter will catch all instances of HttpException and its subclasses
export class HttpExceptionFilter implements ExceptionFilter {
  constructor(private readonly logger: LoggerService) {
    this.logger.setContext('HttpExceptionFilter');
  }

  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();
    const status = exception.getStatus();
    const exceptionResponse = exception.getResponse(); // Get the response object/string from the exception

    // Determine if it's a validation error (from ValidationPipe)
    const isValidationError = typeof exceptionResponse === 'object' && 'message' in exceptionResponse && Array.isArray(exceptionResponse.message);

    const errorResponse = {
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      // If it's a validation error, provide specific messages, otherwise default to exception message
      message: isValidationError
        ? 'Validation failed'
        : (typeof exceptionResponse === 'string'
            ? exceptionResponse
            : (exceptionResponse as any).message || 'An unexpected error occurred'),
      errors: isValidationError ? (exceptionResponse as any).message : undefined, // Include detailed validation errors
    };

    // Log the error (optional, but highly recommended for all exceptions)
    this.logger.error(
      `[HTTP Error] ${request.method} ${request.url} - Status: ${status} - Message: ${errorResponse.message}`,
      exception.stack, // Log stack trace for debugging
    );

    response.status(status).json(errorResponse);
  }
}
```

#### Applying the Filter:

Like pipes and interceptors, exception filters can be applied globally, controller-level, or method-level. For consistent error handling, a global filter for `HttpException` is almost always recommended.

```typescript
// src/main.ts (updated)
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { TransformInterceptor } from './common/transform/transform.interceptor';
import { LoggingInterceptor } from './common/logging/logging.interceptor';
import { LoggerService } from './shared/logger/logger.service';
import { HttpExceptionFilter } from './common/http-exception/http-exception.filter'; // Import our filter

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(new ValidationPipe({ /* ... */ }));

  app.useGlobalInterceptors(
    new LoggingInterceptor(app.get(LoggerService)), // Use app.get() to resolve LoggerService from DI
    new TransformInterceptor(),
  );

  // Apply HttpExceptionFilter globally
  // Note: For global filters that have dependencies (like LoggerService),
  // it's best to retrieve them from the app context or use `APP_FILTER` token.
  // For simplicity here, if LoggerService is globally provided in AppModule.
  // A better way is using APP_FILTER token: see below.
  // app.useGlobalFilters(new HttpExceptionFilter(app.get(LoggerService)));

  // More robust way to register global filters with dependencies:
  app.useGlobalFilters(new HttpExceptionFilter(new LoggerService())); // If LoggerService has no dependencies, or it's a simple instance.
                                                                    // For services that themselves have complex dependencies,
                                                                    // provide them via `APP_FILTER` in a module (see below).

  app.enableCors({ /* ... */ });

  const PORT = process.env.PORT || 3000;
  await app.listen(PORT);
  console.log(`Application is running on: ${await app.getUrl()}`);
}
bootstrap();
```

**Alternative for Global Filter with Dependencies (`APP_FILTER` token):**
If `HttpExceptionFilter` needs dependencies that need to be resolved by NestJS's DI, register it as a provider using the `APP_FILTER` token:

```typescript
// src/app.module.ts (updated to provide global filter)
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ProductsModule } from './products/products.module';
import { LoggerMiddleware } from './common/logger/logger.middleware';
import { AuthTokenMiddleware } from './common/auth-token/auth-token.middleware';
import { APP_FILTER } from '@nestjs/core'; // Import APP_FILTER token
import { HttpExceptionFilter } from './common/http-exception/http-exception.filter';
import { SharedModule } from './shared/shared.module'; // Ensure SharedModule is imported for LoggerService

@Module({
  imports: [
    ProductsModule,
    SharedModule, // Make sure SharedModule (with LoggerService) is imported
  ],
  controllers: [AppController],
  providers: [
    AppService,
    {
      provide: APP_FILTER, // This token makes HttpExceptionFilter global
      useClass: HttpExceptionFilter,
    },
  ],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(LoggerMiddleware, AuthTokenMiddleware)
      .forRoutes('*');
  }
}
```

*Now, `app.useGlobalFilters()` in `main.ts` is no longer needed for `HttpExceptionFilter`.*

### ✅ Example 2: Catching All Unhandled Exceptions (Generic Fallback)

It's crucial to have a fallback filter that catches *any* unhandled exception (e.g., database connection errors, uncaught `ReferenceError`s, etc.) that aren't specifically caught by other filters. This prevents your server from crashing or returning generic, unhelpful error messages.

```bash
# From your project root
nest g filter common/all-exceptions
```

```typescript
// src/common/all-exceptions/all-exceptions.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { Request, Response } from 'express';
import { LoggerService } from '../../shared/logger/logger.service';

@Catch() // Without arguments, this catches all exceptions
export class AllExceptionsFilter implements ExceptionFilter {
  constructor(private readonly logger: LoggerService) {
    this.logger.setContext('AllExceptionsFilter');
  }

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    const message =
      exception instanceof HttpException
        ? (exception.getResponse() as any).message || exception.message
        : 'Internal server error';

    // Log the original exception for debugging purposes.
    // In production, you might send this to a dedicated error tracking service (Sentry, New Relic).
    this.logger.error(
      `[Unhandled Error] ${request.method} ${request.url} - Status: ${status} - Message: ${message}`,
      (exception as Error).stack || exception, // Log stack trace for non-HttpException errors too
    );

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message: status === HttpStatus.INTERNAL_SERVER_ERROR
        ? 'Internal server error' // Mask generic server errors from client
        : message,
      // For INTERNAL_SERVER_ERROR, avoid exposing `errors` array from original exception
      errors: status !== HttpStatus.INTERNAL_SERVER_ERROR && exception instanceof HttpException
        ? (exception.getResponse() as any).errors
        : undefined,
    });
  }
}
```

**Applying the `AllExceptionsFilter` (Globally):**

This filter should be registered **after** your more specific `HttpExceptionFilter` because NestJS applies filters in the order they are provided, and the first one that matches the exception type will handle it.

```typescript
// src/app.module.ts (updated to provide multiple global filters)
import { Module, NestModule, MiddlewareConsumer } from '@nestjs/common';
import { APP_FILTER } from '@nestjs/core';
import { HttpExceptionFilter } from './common/http-exception/http-exception.filter';
import { AllExceptionsFilter } from './common/all-exceptions/all-exceptions.filter'; // Import our new filter
// ... other imports

@Module({
  imports: [
    ProductsModule,
    SharedModule,
  ],
  controllers: [AppController],
  providers: [
    AppService,
    // Order matters for filters! More specific (HttpExceptionFilter) before general (AllExceptionsFilter)
    {
      provide: APP_FILTER,
      useClass: HttpExceptionFilter,
    },
    {
      provide: APP_FILTER, // This will catch anything not caught by HttpExceptionFilter
      useClass: AllExceptionsFilter,
    },
  ],
})
export class AppModule implements NestModule { /* ... */ }
```

### 🧠 FAANG-Level Exception Handling Best Practices:

1.  **Consistent Error Contract:** Define a standard JSON structure for all your API error responses (e.g., `statusCode`, `message`, `timestamp`, `path`, `errorCode` if applicable, `details` or `errors` array for validation). This greatly simplifies client-side error handling.
2.  **Information Hiding in Production:** **Never expose raw stack traces or internal error messages to clients in a production environment.** Use `HttpStatus.INTERNAL_SERVER_ERROR` with a generic message for unexpected server errors. Log full details internally.
3.  **Distinguish Client vs. Server Errors:**
      * **Client Errors (4xx):** Result from invalid client input (e.g., `BadRequestException` for validation, `NotFoundException` for missing resource, `UnauthorizedException` for missing auth). These should provide clear, actionable messages to the client.
      * **Server Errors (5xx):** Result from issues on the server side (e.g., database down, external service error, uncaught code bug). Clients should get a generic `500 Internal Server Error` message and you log the full details.
4.  **Custom Exceptions:** For specific business logic errors, create your own custom exceptions that extend `HttpException` (or a base custom exception) to provide more semantic clarity (e.g., `InsufficientStockException`).
5.  **Global Filters:** Use global filters for common exception types (`HttpException`) and a fallback (`@Catch()`) to ensure comprehensive coverage.
6.  **Logging Integration:** Integrate your exception filters with your logging system. Every unhandled exception should be logged with sufficient detail (including stack traces) for debugging and monitoring.
7.  **Alerting:** For production systems, integrate your error logging with alerting systems (e.g., PagerDuty, Slack, email) to notify your team of critical unhandled errors.

Exception filters are essential for building a resilient, maintainable, and consumer-friendly API. They are a core part of a robust backend system's "observability" and "reliability" pillars.