<immersive type="text/markdown">

# 5th chapter: middleware

## 🛣️ Middleware: Global Request Pre-processing

Middleware in NestJS operates at the **Express/Fastify layer**, meaning it runs **before** the request reaches any NestJS-specific components like Guards, Interceptors, or your Controller's route handlers. This makes it ideal for handling general-purpose tasks that apply to many or all incoming requests.

### What is Middleware?

A middleware function is simply a function that has access to the request (`req`), response (`res`), and the next middleware function in the application's request-response cycle (`next`). NestJS middleware are typically classes implementing the `NestMiddleware` interface.

### 🎯 Responsibility & Why Use Middleware? (FAANG Perspective)

Middleware's responsibilities revolve around pre-processing requests and potentially modifying them before they proceed further down the pipeline. From a FAANG-level perspective, middleware is used for:

1.  **Cross-Cutting Concerns:** Handling operations that affect a wide range of endpoints and don't require access to NestJS's rich execution context (like the controller method or arguments).
2.  **Request Transformation/Augmentation:** Modifying the request or response objects (e.g., adding properties, parsing data).
3.  **Basic Security Checks:** Initial authentication token parsing, CORS handling, basic rate-limiting.
4.  **Logging & Monitoring:** Recording details about incoming requests, response times (though interceptors are often better for after-handler logging).
5.  **Performance Metrics:** Capturing high-level request metrics.
6.  **Early Exits:** Stopping the request-response cycle early if certain conditions are not met (e.g., invalid API key).

**Key Distinction:** Middleware operates at a lower level, closer to the raw HTTP request/response. It doesn't have direct access to the NestJS execution context (like the handler method, arguments, or DI container beyond its own injected dependencies) as Interceptors do.

### ✅ Example: A Simple Logging Middleware

Let's create a middleware that logs every incoming request. This is a common pattern for high-level request tracking.

**1. Create the Middleware Class:**

```bash
# From your project root (ecommerce-backend)
nest g middleware common/logger
```

This will create `src/common/logger/logger.middleware.ts`.

```typescript
// src/common/logger/logger.middleware.ts
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express'; // Using Express types for clarity

@Injectable() // Mark as injectable if it needs dependencies
export class LoggerMiddleware implements NestMiddleware {
  // You could inject a LoggerService here if needed:
  // constructor(private readonly loggerService: LoggerService) {}

  use(req: Request, res: Response, next: NextFunction) {
    const startTime = Date.now();

    // Log request details
    console.log(`[HTTP Request] ${req.method} ${req.originalUrl}`);
    console.log(`  IP: ${req.ip}`);
    console.log(`  User-Agent: ${req.get('User-Agent') || 'N/A'}`);

    // Attach listener for when response finishes
    res.on('finish', () => {
      const duration = Date.now() - startTime;
      console.log(
        `[HTTP Response] ${req.method} ${req.originalUrl} - Status: ${res.statusCode} - Duration: ${duration}ms`,
      );
    });

    // IMPORTANT: Call next() to pass control to the next middleware or route handler
    next();
  }
}
```

**2. Apply the Middleware in a Module:**

Middleware is applied using the `configure()` method of a module that implements the `NestModule` interface. This is typically done in the `AppModule` for global middleware, or in feature modules for module-specific middleware.

```typescript
// src/app.module.ts (updated)
import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ProductsModule } from './products/products.module';
import { LoggerMiddleware } from './common/logger/logger.middleware'; // Import our middleware

@Module({
  imports: [ProductsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule implements NestModule {
  // The configure method is where you apply middleware
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(LoggerMiddleware) // Apply our LoggerMiddleware
      .forRoutes('*'); // Apply to all routes in the application
    // Alternatively: .forRoutes('products'); // Apply only to /products routes
    // Or: .forRoutes({ path: 'products/:id', method: RequestMethod.GET }); // Specific route and method
  }
}
```

Now, every request to your e-commerce backend will be logged by `LoggerMiddleware` before it reaches its intended controller.

### ✅ Example: Basic Authentication Token Parsing Middleware

For an initial pass at authentication (before Guards take over for actual authorization), middleware can parse a JWT token from the header and attach the decoded payload to the request object.

```bash
# From your project root
nest g middleware common/auth-token
```

```typescript
// src/common/auth-token/auth-token.middleware.ts
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import * as jwt from 'jsonwebtoken'; // You'd use @nestjs/jwt later for proper JWT handling

// Extend Express Request interface for custom properties
declare global {
  namespace Express {
    interface Request {
      user?: any; // To attach decoded user info
      token?: string; // To attach the raw token
    }
  }
}

@Injectable()
export class AuthTokenMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    const authHeader = req.headers.authorization;

    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.split(' ')[1];
      req.token = token; // Store raw token

      try {
        // In a real app, replace 'YOUR_SECRET_KEY' with process.env.JWT_SECRET
        const decoded = jwt.verify(token, 'YOUR_SECRET_KEY');
        req.user = decoded; // Attach decoded payload to request
        console.log(`[AuthTokenMiddleware] Token decoded for user: ${JSON.stringify(decoded)}`);
      } catch (error) {
        console.warn('[AuthTokenMiddleware] Invalid or expired token:', error.message);
        // Do not throw error here unless you want to stop processing immediately.
        // Guards will handle actual access denial later.
      }
    } else {
      console.log('[AuthTokenMiddleware] No authorization header found.');
    }

    next(); // Pass control to the next handler
  }
}
```

**Applying the Auth Token Middleware:**

Add it to `AppModule`'s `configure` method, likely *before* other specific route handling middleware if it's broadly needed.

```typescript
// src/app.module.ts (updated for multiple middleware)
import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
// ... other imports
import { LoggerMiddleware } from './common/logger/logger.middleware';
import { AuthTokenMiddleware } from './common/auth-token/auth-token.middleware';

@Module({ /* ... */ })
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(LoggerMiddleware, AuthTokenMiddleware) // Apply multiple middleware in order
      .forRoutes('*'); // Apply to all routes
  }
}
```

The order of `apply()` matters. Middleware functions are executed in the order they are listed.

### 🧠 FAANG-Level Middleware Best Practices:

1.  **Keep it Focused:** Each middleware should ideally have a single, well-defined responsibility.
2.  **Stateless Where Possible:** Middleware should generally be stateless to avoid concurrency issues and simplify scaling.
3.  **Early Exit for Broad Security:** Use middleware for coarse-grained security checks (e.g., API key validation, basic rate-limiting, CORS) that can stop the request early if requirements aren't met.
4.  **Enriching Request Context:** Middleware is excellent for enriching the `req` object with data that will be used by subsequent pipeline elements (like the `user` object after token parsing).
5.  **Use for Low-Level Concerns:** Reserve middleware for tasks that operate directly on the `req` and `res` objects and don't require the full NestJS execution context or dependency injection beyond basic services.
6.  **Global vs. Route-Specific:** Apply middleware globally in `AppModule` for concerns that affect the entire application. Use `.forRoutes()` with specific paths or methods when middleware is only relevant to a subset of endpoints.
7.  **Avoid Business Logic:** Do not put complex business logic or database operations in middleware. Delegate these to services that are injected into your controllers.

Middleware provides a powerful way to manage cross-cutting concerns effectively. While its role might seem similar to Interceptors, their fundamental difference in execution phase and access to the NestJS DI container makes them suitable for distinct use cases.