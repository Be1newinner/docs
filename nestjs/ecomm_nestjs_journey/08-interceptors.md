<immersive type="text/markdown">

# 07-guards

## 🛡️ Guards: Controlling Route Access (Authentication & Authorization)

In NestJS, **Guards** are classes decorated with `@Injectable()` that implement the `CanActivate` interface. Their primary purpose is to determine whether a request should proceed to the route handler based on specific conditions, typically **authorization** (who can do what) and **authentication** (who is the user).

Guards are executed **after** middleware and pipes, but **before** any interceptors or the controller's route handler method. This position in the pipeline makes them ideal for access control.

### What is a Guard?

A guard is a class that implements the `CanActivate` interface, which has a single `canActivate()` method. This method returns an `Observable<boolean>`, `Promise<boolean>`, or `boolean`, indicating whether the current request is allowed to proceed (`true`) or should be denied (`false`).

### 🎯 Responsibility & Why Use Guards? (FAANG Perspective)

For building secure and robust APIs at scale, Guards are paramount because they:

1.  **Enforce Access Control:** They are the definitive layer for deciding who is allowed to access specific resources or perform certain actions.
2.  **Separate Concerns:** They cleanly separate authorization logic from business logic (in services) and request handling (in controllers). This makes both controllers and services leaner and more focused.
3.  **Reusability:** A single guard can protect multiple routes, or even an entire controller, ensuring consistent security policies across the application.
4.  **Testability:** Authorization logic encapsulated in guards is easier to unit test independently.
5.  **Policy Enforcement:** At FAANG, security is paramount. Guards allow for declarative, policy-driven security, ensuring that access policies are enforced consistently at the API boundary.

### How Guards Work

When a guard's `canActivate()` method is called, it receives an `ExecutionContext` object. This powerful object provides access to the current request context, including:

  * `getClass()`: The controller class about to be activated.
  * `getHandler()`: The route handler method about to be activated.
  * `getArgs()`: The arguments that will be passed to the route handler.
  * `getType()`: The type of context (`http`, `ws`, `rpc`).
  * `switchToHttp()`: Returns an `HttpArgumentsHost` which can give you the `Request` and `Response` objects (`getRequest()`, `getResponse()`).

This rich context allows guards to make informed decisions based on the incoming request, the target controller, and even custom metadata.

### ✅ Example 1: Basic Authentication Guard (`AuthGuard`)

Before we implement role-based access, let's set up a simple `AuthGuard` that checks if a user is "authenticated" (for now, simply if `req.user` exists, assuming our `AuthTokenMiddleware` has populated it). Later, this will integrate with proper JWT authentication.

```bash
# From your project root
nest g guard common/auth
```

```typescript
// src/common/auth/auth.guard.ts
import { CanActivate, ExecutionContext, Injectable, UnauthorizedException } from '@nestjs/common';
import { Observable } from 'rxjs';

@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    const request = context.switchToHttp().getRequest();
    // For now, we're just checking if req.user exists (populated by AuthTokenMiddleware)
    // In a real app, this would involve validating JWTs, checking sessions, etc.
    if (request.user) {
      console.log('[AuthGuard] User authenticated:', request.user);
      return true; // Allow access
    } else {
      console.log('[AuthGuard] User not authenticated. Denying access.');
      throw new UnauthorizedException('Authentication required'); // Deny access with a 401
    }
  }
}
```

Now, apply this guard to a controller method or an entire controller:

```typescript
// src/products/products.controller.ts (excerpt)
import { Controller, Get, Post, Body, Param, Patch, Delete, UseGuards } from '@nestjs/common';
import { ProductsService } from './products.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { AuthGuard } from '../common/auth/auth.guard'; // Import our AuthGuard

@Controller('products')
// Apply AuthGuard to the entire controller, protecting all its routes
@UseGuards(AuthGuard)
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}

  // All methods in this controller will now require authentication
  // before being executed.
  @Post()
  create(@Body() createProductDto: CreateProductDto) {
    return this.productsService.create(createProductDto);
  }

  @Get()
  findAll() {
    return this.productsService.findAll();
  }

  // ... other methods
}
```

Now, if you try to access `/products` without a valid `req.user` (which our `AuthTokenMiddleware` would try to set), the `AuthGuard` will throw an `UnauthorizedException`.

### ✅ Example 2: Role-Based Access Control (RBAC) Guard

In our e-commerce app, we'll have users with different roles: `user`, `vendor`, and `admin`. Only `admin` or `vendor` might be able to create products, while `admin` might have full control.

This requires two parts:

1.  A custom decorator to attach required roles to a route.
2.  A guard that reads these roles and checks them against the authenticated user's roles.

#### 1\. Create a `Roles` Custom Decorator

This decorator will allow us to specify required roles on a controller method or class.

```bash
# From your project root
nest g decorator common/roles
```

```typescript
// src/common/roles/roles.decorator.ts
import { SetMetadata } from '@nestjs/common';

// Define an Enum for roles for type safety and consistency
export enum UserRole {
  USER = 'user',
  VENDOR = 'vendor',
  ADMIN = 'admin',
}

export const ROLES_KEY = 'roles'; // Key to retrieve metadata

// @Roles() decorator allows specifying an array of UserRole values
export const Roles = (...roles: UserRole[]) => SetMetadata(ROLES_KEY, roles);
```

#### 2\. Create a `RolesGuard`

This guard will use the `Reflector` (a NestJS utility) to read the metadata set by our `Roles` decorator and compare it with the user's role.

```bash
# From your project root
nest g guard common/roles
```

```typescript
// src/common/roles/roles.guard.ts
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core'; // Used to read metadata
import { Observable } from 'rxjs';
import { UserRole, ROLES_KEY } from './roles.decorator';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {} // Inject Reflector

  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    // 1. Get required roles from metadata
    const requiredRoles = this.reflector.getAllAndOverride<UserRole[]>(ROLES_KEY, [
      context.getHandler(), // Check method metadata first
      context.getClass(),   // Then check class metadata
    ]);

    // If no roles are specified for this route, allow access (or handle as per policy)
    if (!requiredRoles) {
      return true; // No specific roles required for this endpoint
    }

    // 2. Get the user from the request (assuming AuthGuard or AuthTokenMiddleware has set it)
    const { user } = context.switchToHttp().getRequest();

    // In a real app, `user.role` would come from decoded JWT payload or session
    // For this example, let's mock a user object
    // user = { username: 'admin_user', role: UserRole.ADMIN }
    // user = { username: 'vendor_user', role: UserRole.VENDOR }
    // user = { username: 'regular_user', role: UserRole.USER }

    if (!user || !user.role) {
      // If no user or role, deny access (though AuthGuard should ideally handle this first)
      return false;
    }

    // 3. Check if the user's role matches any of the required roles
    const hasRole = requiredRoles.some((role) => user.role === role);

    if (!hasRole) {
      console.warn(`[RolesGuard] User ${user.username} (role: ${user.role}) denied access to route requiring roles: ${requiredRoles.join(', ')}`);
    } else {
      console.log(`[RolesGuard] User ${user.username} (role: ${user.role}) granted access.`);
    }

    return hasRole;
  }
}
```

#### 3\. Apply the `RolesGuard` and `Roles` Decorator

Now, let's protect our `create` product endpoint so only `ADMIN` or `VENDOR` users can access it.

```typescript
// src/products/products.controller.ts (updated with Roles and UseGuards)
import { Controller, Post, Body, Param, Patch, Delete, UseGuards, Get } from '@nestjs/common';
import { ProductsService } from './products.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { AuthGuard } from '../common/auth/auth.guard'; // Our authentication guard
import { RolesGuard } from '../common/roles/roles.guard'; // Our new roles guard
import { Roles, UserRole } from '../common/roles/roles.decorator'; // Our custom Roles decorator

@Controller('products')
// Apply AuthGuard globally to the controller, then RolesGuard.
// The order matters: AuthGuard runs first to ensure user is authenticated,
// then RolesGuard runs to check user's role.
@UseGuards(AuthGuard, RolesGuard)
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}

  // Only users with ADMIN or VENDOR role can create products
  @Post()
  @Roles(UserRole.ADMIN, UserRole.VENDOR) // Apply our custom decorator
  create(@Body() createProductDto: CreateProductDto) {
    return this.productsService.create(createProductDto);
  }

  // All users (if authenticated by AuthGuard) can view all products
  @Get()
  findAll() {
    return this.productsService.findAll();
  }

  // Admin users can delete products
  @Delete(':id')
  @Roles(UserRole.ADMIN) // Only ADMIN can delete
  remove(@Param('id') id: string) {
    return this.productsService.remove(id);
  }

  // Other methods (findOne, update) will still be protected by AuthGuard but have no specific role requirements
  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.productsService.findOne(id.toString());
  }

  @Patch(':id')
  @Roles(UserRole.ADMIN, UserRole.VENDOR) // Both ADMIN and VENDOR can update
  update(@Param('id') id: string, @Body() updateProductDto: UpdateProductDto) {
    return this.productsService.update(id.toString(), updateProductDto);
  }
}
```

When applying multiple guards using `@UseGuards()`, they are executed in the order they are provided. If any guard returns `false` (or throws an exception), the subsequent guards and the route handler will not be executed.

### 🧠 FAANG-Level Guard Best Practices:

1.  **Separate Authentication & Authorization:** `AuthGuard` handles "who are you?", `RolesGuard` handles "what are you allowed to do?". Keep these concerns separate for clarity and reusability.
2.  **Granular Control:** Use `Roles` decorators (or similar policy decorators) to apply fine-grained access control at the method level.
3.  **Use `Reflector` for Metadata:** This is the standard NestJS way to read custom metadata attached to routes or controllers.
4.  **Inject Dependencies:** Guards can inject services (e.g., a `UserService` to fetch user roles from a database) just like any other provider.
5.  **Chain Guards:** Apply multiple guards sequentially with `@UseGuards(Guard1, Guard2, ...)`. The order matters.
6.  **Fail Fast:** If a guard determines that a request should not proceed, it should return `false` or throw an appropriate `HttpException` immediately.
7.  **Global vs. Controller/Method Level:** Apply guards globally (e.g., `app.useGlobalGuards(new AuthGuard())`) for policies that apply everywhere. Use `@UseGuards()` for specific routes or controllers.

Guards are a cornerstone of building secure and robust APIs. They provide a powerful and declarative way to enforce access policies, which is essential for any production-grade application, especially in large-scale systems.