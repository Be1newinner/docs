<immersive type="text/markdown">

# 10-custom-decorators

## ✨ Custom Decorators: Extending NestJS Functionality

NestJS extensively uses decorators (`@Get()`, `@Body()`, `@UseGuards()`, etc.) to provide a declarative and readable way to define application structure and behavior. **Custom decorators** allow you to create your own specialized decorators, abstracting away common patterns and enhancing code clarity and reusability.

### What are Custom Decorators?

Custom decorators in NestJS typically fall into two categories:

1.  **Parameter Decorators:** Used to transform or extract data from the `ExecutionContext` and inject it directly into a route handler's parameters (e.g., `@Body()`, `@Param()`). You create these using `createParamDecorator`.
2.  **Class/Method Decorators:** Used to attach metadata to classes or methods, which can then be read by guards, interceptors, or other custom logic (e.g., our `@Roles()` decorator). You create these using `SetMetadata`.

### 🎯 Responsibility & Why Use Custom Decorators? (FAANG Perspective)

From a FAANG-level engineering perspective, custom decorators are valuable for:

1.  **Reducing Boilerplate:** Encapsulating repetitive logic (e.g., extracting user ID from the request) into a single, reusable decorator.
2.  **Improving Readability:** Making controller and service code cleaner and more semantic by clearly indicating what data is being injected or what metadata is applied.
3.  **Separation of Concerns:** Abstracting away common data extraction or metadata application logic, keeping controllers focused on handling requests.
4.  **Enforcing Conventions:** Encouraging consistent patterns across your codebase.
5.  **Enhanced Type Safety:** When combined with TypeScript, they can provide strong type inference for the injected data.

### ✅ Example 1: `CurrentUser` Parameter Decorator

A very common pattern in authenticated APIs is to access the currently authenticated user's information within a route handler. Instead of always doing `req.user` and casting it, we can create a `CurrentUser` decorator. This assumes our `AuthGuard` or `AuthTokenMiddleware` has already attached the user object to the request.

```bash
# From your project root
nest g decorator common/current-user
```

```typescript
// src/common/current-user/current-user.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';
import { Request } from 'express'; // Import Request type for better typing

// Define a simple User interface for type safety (you'd have a more complete one)
export interface AuthenticatedUser {
  id: string;
  username: string;
  email: string;
  role: string; // e.g., 'user', 'vendor', 'admin'
  // ... any other user properties
}

export const CurrentUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext): AuthenticatedUser => {
    const request = ctx.switchToHttp().getRequest<Request>();
    // Assuming AuthGuard or AuthTokenMiddleware has populated req.user
    // and it conforms to AuthenticatedUser interface.
    // 'data' argument can be used to pick a specific property, e.g., @CurrentUser('id')
    return data ? request.user?.[data as string] : request.user;
  },
);
```

**Using the `CurrentUser` Decorator in `ProductsController`:**

Now, let's modify our `ProductsController` to log who is creating a product.

```typescript
// src/products/products.controller.ts (updated)
import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { ProductsService } from './products.service';
import { CreateProductDto } from './dto/create-product.dto';
import { AuthGuard } from '../common/auth/auth.guard';
import { RolesGuard } from '../common/roles/roles.guard';
import { Roles, UserRole } from '../common/roles/roles.decorator';
import { CurrentUser, AuthenticatedUser } from '../common/current-user/current-user.decorator'; // Import our new decorator

@Controller('products')
@UseGuards(AuthGuard, RolesGuard) // Ensure AuthGuard runs first to populate req.user
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}

  @Post()
  @Roles(UserRole.ADMIN, UserRole.VENDOR)
  create(
    @Body() createProductDto: CreateProductDto,
    // Use the CurrentUser decorator to inject the authenticated user object
    @CurrentUser() user: AuthenticatedUser,
  ) {
    console.log(`[ProductsController] User ${user.username} (ID: ${user.id}) is creating a product.`);
    // In a real app, you might associate the product with the vendor user's ID
    return this.productsService.create(createProductDto);
  }

  // ... other methods
}
```

Now, your `create` method instantly gets the typed `user` object, making the code cleaner and less error-prone.

### ✅ Example 2: `IsPublic` Method Decorator (for skipping authentication)

Sometimes, you have a global guard (like `AuthGuard`) applied to your entire application or controller, but certain routes need to be publicly accessible (e.g., login, registration, public product listings). A custom decorator can mark these routes to be skipped by the guard.

This requires a combination of `SetMetadata` (for the decorator) and `Reflector` (for the guard to read the metadata).

#### 1\. Create the `IsPublic` Decorator

```bash
# From your project root
nest g decorator common/is-public
```

```typescript
// src/common/is-public/is-public.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const IS_PUBLIC_KEY = 'isPublic'; // Key to store metadata

// @IsPublic() decorator simply sets a boolean metadata flag
export const IsPublic = () => SetMetadata(IS_PUBLIC_KEY, true);
```

#### 2\. Update `AuthGuard` to Respect `IsPublic`

Our `AuthGuard` needs to use `Reflector` to check if the route it's protecting has the `IsPublic` metadata.

```typescript
// src/common/auth/auth.guard.ts (updated)
import { CanActivate, ExecutionContext, Injectable, UnauthorizedException } from '@nestjs/common';
import { Observable } from 'rxjs';
import { Reflector } from '@nestjs/core'; // Import Reflector
import { IS_PUBLIC_KEY } from '../is-public/is-public.decorator'; // Import our new key

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private reflector: Reflector) {} // Inject Reflector

  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    // Check if the route is public by looking for the IS_PUBLIC_KEY metadata
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(), // Check method metadata first
      context.getClass(),   // Then check class metadata
    ]);

    if (isPublic) {
      console.log('[AuthGuard] Route is public. Skipping authentication.');
      return true; // Allow access without authentication
    }

    const request = context.switchToHttp().getRequest();
    if (request.user) {
      console.log('[AuthGuard] User authenticated:', request.user);
      return true;
    } else {
      console.log('[AuthGuard] User not authenticated. Denying access.');
      throw new UnauthorizedException('Authentication required');
    }
  }
}
```

#### 3\. Apply `IsPublic` to a Route

Let's make our `findAll` products endpoint public, even if `AuthGuard` is applied to the controller.

```typescript
// src/products/products.controller.ts (updated with IsPublic)
import { Controller, Post, Body, UseGuards, Get, Delete, Param, Patch } from '@nestjs/common';
// ... other imports
import { IsPublic } from '../common/is-public/is-public.decorator'; // Import IsPublic

@Controller('products')
@UseGuards(AuthGuard, RolesGuard) // These guards still apply by default
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}

  @Post()
  @Roles(UserRole.ADMIN, UserRole.VENDOR)
  create(
    @Body() createProductDto: CreateProductDto,
    @CurrentUser() user: AuthenticatedUser,
  ) {
    console.log(`[ProductsController] User ${user.username} (ID: ${user.id}) is creating a product.`);
    return this.productsService.create(createProductDto);
  }

  @Get()
  @IsPublic() // This route is now public, AuthGuard will skip for it
  findAll() {
    console.log('[ProductsController] Accessing public products list.');
    return this.productsService.findAll();
  }

  // ... other methods which will still require authentication and roles
}
```

Now, the `findAll` endpoint (`GET /products`) can be accessed without an authentication token, while `POST /products` or `DELETE /products/:id` still require authentication and specific roles.

### 🧠 FAANG-Level Custom Decorator Best Practices:

1.  **Semantic Naming:** Give your decorators clear, self-explanatory names (e.g., `CurrentUser`, `IsPublic`, `Roles`).
2.  **Focus on Data Extraction/Metadata:** Custom decorators should primarily be for extracting data from the request/execution context or attaching metadata. Avoid putting complex business logic directly inside the decorator itself.
3.  **Leverage Existing NestJS Utilities:** Use `createParamDecorator` for parameter decorators and `SetMetadata` with `Reflector` for class/method decorators.
4.  **Type Safety:** Always provide type definitions (`AuthenticatedUser` interface) for the data your decorators extract, enhancing developer experience and preventing runtime errors.
5.  **Reusability:** Design decorators to be as generic as possible so they can be reused across different parts of your application.
6.  **Avoid Overuse:** While powerful, don't create decorators for every minor pattern. Use them when they genuinely reduce complexity and improve readability. If logic gets too complex, it might belong in a pipe, guard, or interceptor.
7.  **Order with Guards/Interceptors:** If your decorator is setting metadata for a guard or interceptor, ensure the decorator is applied *before* the guard/interceptor in the pipeline where the metadata needs to be read.

Custom decorators are a testament to NestJS's flexibility and allow you to build highly expressive and maintainable APIs by abstracting common concerns into declarative syntax.
