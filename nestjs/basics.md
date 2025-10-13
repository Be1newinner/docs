## *Create a nest app*

* $ npm i -g @nestjs/cli
* $ nest new project-name

## ✅ 1. **Controllers**

Controllers handle **incoming HTTP requests** and return **responses** to the client.

### 🎯 Responsibility

* Bind routes to logic
* Deal with request/response cycle

### ✅ Example

```ts
// trip.controller.ts
import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { TripService } from './trip.service';

@Controller('trips')
export class TripController {
  constructor(private readonly tripService: TripService) {}

  @Get()
  findAll() {
    return this.tripService.getAllTrips();
  }

  @Post()
  create(@Body() body: CreateTripDto) {
    return this.tripService.createTrip(body);
  }

  @Get(':id')
  findById(@Param('id') id: string) {
    return this.tripService.getTripById(id);
  }
}
```

---

## ✅ 2. **Providers**

Providers are **services** or classes with some business logic. They can be injected via **Dependency Injection (DI)**.

### 🎯 Responsibility

* Handle logic, DB operations, computations, etc.
* Reusable across controllers or other providers

### ✅ Example

```ts
// trip.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class TripService {
  private trips = [];

  getAllTrips() {
    return this.trips;
  }

  createTrip(trip: any) {
    this.trips.push(trip);
    return trip;
  }

  getTripById(id: string) {
    return this.trips.find(t => t.id === id);
  }
}
```

---

## ✅ 3. **Modules**

Modules are containers for **controllers, providers, and other modules**. Everything in Nest must belong to a module.

### 🎯 Responsibility

* Organize features
* Control scope of providers

### ✅ Example

```ts
// trip.module.ts
import { Module } from '@nestjs/common';
import { TripController } from './trip.controller';
import { TripService } from './trip.service';

@Module({
  controllers: [TripController],
  providers: [TripService],
})
export class TripModule {}
```

---

## ✅ 4. **Middleware**

Middleware are functions that are called **before route handlers**. You can use them for logging, authentication, etc.

### 🎯 Responsibility

* Preprocess requests
* Mutate `req`, `res`, or stop execution

### ✅ Example

```ts
// logger.middleware.ts
import { Injectable, NestMiddleware } from '@nestjs/common';

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: () => void) {
    console.log(`[${req.method}] ${req.url}`);
    next();
  }
}
```

### ✅ Apply Middleware

```ts
// in app.module.ts or any module
import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { LoggerMiddleware } from './logger.middleware';

@Module({...})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(LoggerMiddleware).forRoutes('*');
  }
}
```

---

## ✅ 5. **Exception Filters**

They catch and handle **exceptions thrown** in your app. You can use them to **customize error responses**.

### 🎯 Responsibility

* Centralized error handling
* Transform exceptions into HTTP responses

### ✅ Example

```ts
// http-exception.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
} from '@nestjs/common';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const status = exception.getStatus();

    response.status(status).json({
      statusCode: status,
      message: exception.message,
      timestamp: new Date().toISOString(),
    });
  }
}
```

### ✅ Usage

```ts
@UseFilters(HttpExceptionFilter)
@Get()
find() {
  throw new HttpException('Custom error', 400);
}
```

---

## ✅ 6. **Pipes**

Pipes are used for **validation**, **transformation**, and **sanitization** of input.

### 🎯 Responsibility

* Transform input data (e.g., string to number)
* Validate inputs (e.g., DTO validation)

### ✅ Example: Validation Pipe

```ts
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseIntPipe implements PipeTransform {
  transform(value: string) {
    const val = parseInt(value, 10);
    if (isNaN(val)) {
      throw new BadRequestException('Validation failed');
    }
    return val;
  }
}
```

### ✅ Usage

```ts
@Get(':id')
getById(@Param('id', ParseIntPipe) id: number) {
  return this.service.getById(id);
}
```

---

## ✅ 7. **Guards**

Guards control **route access** based on roles, permissions, or conditions.

### 🎯 Responsibility

* Implement authentication or authorization logic

### ✅ Example: AuthGuard

```ts
import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';

@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const req = context.switchToHttp().getRequest();
    return !!req.headers['authorization'];
  }
}
```

### ✅ Usage

```ts
@UseGuards(AuthGuard)
@Get()
getAllProtected() {
  return this.service.getAll();
}
```

---

## ✅ 8. **Interceptors**

Interceptors wrap around method execution — you can use them for **logging**, **caching**, **response shaping**, etc.

### 🎯 Responsibility

* Run code **before/after** request processing
* Modify result or handle errors

### ✅ Example: LoggingInterceptor

```ts
import {
  Injectable,
  NestInterceptor,
  ExecutionContext,
  CallHandler,
} from '@nestjs/common';
import { Observable, tap } from 'rxjs';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const now = Date.now();
    return next.handle().pipe(
      tap(() => console.log(`Response Time: ${Date.now() - now}ms`)),
    );
  }
}
```

### ✅ Usage

```ts
@UseInterceptors(LoggingInterceptor)
@Get()
getAll() {
  return this.service.getAll();
}
```

---

## ✅ 9. **Custom Decorators**

They are custom annotations to extract or inject logic/data from context.

### 🎯 Responsibility

* Abstract repeated logic
* Cleanly inject data like user, roles, etc.

### ✅ Example: GetUser Decorator

```ts
// get-user.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const GetUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const req = ctx.switchToHttp().getRequest();
    return req.user;
  },
);
```

### ✅ Usage

```ts
@Get('profile')
getProfile(@GetUser() user) {
  return user;
}
```

---

## 🧠 How FAANG engineers use these:

| Feature           | Used For                                           |
| ----------------- | -------------------------------------------------- |
| Controllers       | Route entry points                                 |
| Providers         | Business logic, services, adapters                 |
| Modules           | Feature grouping, lazy loading                     |
| Middleware        | Logging, token parsing, performance metrics        |
| Filters           | Global error response shaping                      |
| Pipes             | DTO validation, input transformation               |
| Guards            | AuthZ / Role-based access control                  |
| Interceptors      | Tracing, caching, metrics, modifying responses     |
| Custom Decorators | Injecting metadata, user info, request-scoped data |

---


## 🔍 Quick Comparison

| Aspect               | **Middleware**                                   | **Interceptor**                                          |
| -------------------- | ------------------------------------------------ | -------------------------------------------------------- |
| **Execution Phase**  | Before route handler (low-level)                 | Around route handler (high-level)                        |
| **Access To**        | `req`, `res`, `next` (raw HTTP request/response) | Request + Response + Handler Result (`ExecutionContext`) |
| **Use Case**         | Logging, CORS, token parsing, rate-limiting      | Response transformation, logging, timeout, caching       |
| **Return Control**   | Must call `next()` manually                      | Uses RxJS (`next.handle().pipe(...)`)                    |
| **Cannot access...** | Method return values                             | Raw `req/res` or modify request body before controller   |
| **Scope**            | Application or route level                       | Controller or method level                               |

---

## 📶 Execution Flow Diagram

```
Incoming Request
     ↓
[Middleware]      <- Pre-processing (low-level, before route logic)
     ↓
[Guards]          <- Can block access (auth, roles)
     ↓
[Interceptors]    <- Around controller method (before & after)
     ↓
[Pipes]           <- Transform/validate method inputs
     ↓
Controller Method <- Handles business logic
     ↓
[Interceptors]    <- Can modify the response
     ↓
[Exception Filter] <- Handle thrown errors (if any)
     ↓
Response
```

---

## 🧠 Mental Model

Think of it like this:

| Layer           | Analogy                       | Example                                                                 |
| --------------- | ----------------------------- | ----------------------------------------------------------------------- |
| Middleware      | Airport Security Check        | Check your ID, scan bags, verify token                                  |
| Interceptor     | Air Hostess / Flight Recorder | Records flight time, serves meal, logs journey, adjusts food (response) |
| Pipe            | Baggage Scanner               | Converts items to standard format (validation)                          |
| Guard           | Immigration Officer           | Rejects entry based on Visa or Passport                                 |
| ExceptionFilter | Airport Emergency Team        | Catches crash and handles recovery                                      |

---

## ✅ Real Use Case Example

### 👮 **Middleware Example (Logging)**

```ts
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: () => void) {
    console.log(`[MIDDLEWARE] ${req.method} ${req.url}`);
    next(); // important!
  }
}
```

### 🎯 **Interceptor Example (Timing & Response Manipulation)**

```ts
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const now = Date.now();
    console.log(`[INTERCEPTOR] Before...`);

    return next.handle().pipe(
      tap(() => console.log(`[INTERCEPTOR] After... ${Date.now() - now}ms`))
    );
  }
}
```

---

## 🧪 When to Use What?

| Situation                                                       | Use                   |
| --------------------------------------------------------------- | --------------------- |
| You need to log every request                                   | ✅ Middleware          |
| You want to validate a JWT token                                | ✅ Middleware or Guard |
| You want to transform API response                              | ✅ Interceptor         |
| You want to cache method result                                 | ✅ Interceptor         |
| You want to reject request based on role                        | ✅ Guard               |
| You want to modify response shape (e.g., wrap in `{data: ...}`) | ✅ Interceptor         |
| You want to run something **before and after** a method         | ✅ Interceptor         |
| You want to **pre-process `req/res`** (e.g., parse JSON)        | ✅ Middleware          |

---

## 🔥 Pro Tip

* **Middleware** is closer to Express layer
* **Interceptors** are closer to Nest's **Observable flow** (RxJS powered)

You typically use **Middleware once per app**, but **Interceptors can be method-specific, controller-specific, or global** — making them more powerful and Nest-native.

---

In NestJS, **decorators** are the **backbone of the framework’s declarative programming style** — they define how classes and methods behave in the Nest ecosystem.


## 🧱 1. **Class-level Decorators**

These define **Controllers**, **Services**, **Modules**, etc.

### `@Controller()`

Defines a controller and optionally sets a route prefix.

```ts
@Controller('users')
export class UserController {}
```

---

### `@Injectable()`

Marks a class as a **Provider** that can be injected elsewhere.

```ts
@Injectable()
export class UserService {}
```

---

### `@Module()`

Defines a Nest module — registers controllers, providers, imports.

```ts
@Module({
  imports: [],
  controllers: [UserController],
  providers: [UserService],
})
export class UserModule {}
```

---

## 🌐 2. **Route Handler Decorators**

Used inside controllers to map HTTP routes.

| Decorator   | Description           | Example                |
| ----------- | --------------------- | ---------------------- |
| `@Get()`    | Maps GET requests     | `@Get('profile')`      |
| `@Post()`   | Maps POST requests    | `@Post('register')`    |
| `@Put()`    | Maps PUT requests     | `@Put(':id')`          |
| `@Delete()` | Maps DELETE requests  | `@Delete(':id')`       |
| `@Patch()`  | Maps PATCH requests   | `@Patch(':id/status')` |
| `@All()`    | Maps all HTTP methods | `@All('health')`       |

---

## 📦 3. **Parameter Decorators**

Used to extract values from the request object.

| Decorator      | Description                             | Example                                |
| -------------- | --------------------------------------- | -------------------------------------- |
| `@Body()`      | Extracts the body of the request        | `@Post() create(@Body() dto)`          |
| `@Param()`     | Extracts route params                   | `@Get(':id') get(@Param('id'))`        |
| `@Query()`     | Extracts query params                   | `@Get() list(@Query('page'))`          |
| `@Headers()`   | Extracts headers                        | `@Get() check(@Headers('user-agent'))` |
| `@Req()`       | Gives full request object               | `@Get() get(@Req() req)`               |
| `@Res()`       | Gives full response object (manual res) | `@Get() get(@Res() res)`               |
| `@Ip()`        | Gets request IP                         | `@Get() get(@Ip() ip)`                 |
| `@HostParam()` | Gets hostname from subdomain routing    | For multi-tenancy setups               |

---

## 🛡 4. **Guards, Pipes, Interceptors, Filters**

| Decorator            | Applies Logic                            | Used On           |
| -------------------- | ---------------------------------------- | ----------------- |
| `@UseGuards()`       | Attach guards (Auth, Roles)              | Controller/method |
| `@UsePipes()`        | Attach input transformation              | Controller/method |
| `@UseInterceptors()` | Attach interceptors (logging, transform) | Controller/method |
| `@UseFilters()`      | Attach exception filters                 | Controller/method |

### ✅ Example:

```ts
@UseGuards(AuthGuard)
@UsePipes(ValidationPipe)
@Post()
create(@Body() dto: CreateUserDto) {}
```

---

## 🧑‍🏫 5. **Custom Decorators**

You can define your own decorators for DRY code — e.g., extract user from `req`.

### Example: `@GetUser()` Decorator

```ts
// get-user.decorator.ts
export const GetUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const req = ctx.switchToHttp().getRequest();
    return req.user;
  },
);
```

### Usage:

```ts
@Get('me')
getProfile(@GetUser() user: User) {
  return user;
}
```

---

## 🧪 6. **Lifecycle and Dependency Injection Decorators**

| Decorator                  | Description                               |
| -------------------------- | ----------------------------------------- |
| `@Inject()`                | Manual dependency injection (token-based) |
| `@Optional()`              | Makes an injected dependency optional     |
| `@OnModuleInit()`          | Runs logic after DI setup                 |
| `@OnApplicationShutdown()` | Cleanup logic (e.g., close DB)            |

### Example:

```ts
@Injectable()
export class DbService implements OnModuleInit {
  onModuleInit() {
    console.log('Connected to DB');
  }
}
```

---

## 🧙‍♂️ 7. **Swagger Decorators** (for API docs)

If you're using `@nestjs/swagger` for OpenAPI docs:

| Decorator          | Purpose                          |
| ------------------ | -------------------------------- |
| `@ApiTags()`       | Group endpoints                  |
| `@ApiOperation()`  | Describe endpoint                |
| `@ApiResponse()`   | Define success/failure responses |
| `@ApiBody()`       | Describe body schema             |
| `@ApiBearerAuth()` | Add bearer auth header           |

---

## 🔥 Summary Cheat Sheet

| Category         | Decorators                                                             |
| ---------------- | ---------------------------------------------------------------------- |
| Class            | `@Controller()`, `@Injectable()`, `@Module()`                          |
| Routes           | `@Get()`, `@Post()`, `@Put()`, `@Delete()`, `@Patch()`                 |
| Params           | `@Body()`, `@Param()`, `@Query()`, `@Headers()`, `@Req()`, `@Res()`    |
| Request Pipeline | `@UseGuards()`, `@UsePipes()`, `@UseFilters()`, `@UseInterceptors()`   |
| Lifecycle / DI   | `@Inject()`, `@Optional()`, `@OnModuleInit()`                          |
| Custom           | `@createParamDecorator`, `@SetMetadata()` for roles, permissions, etc. |

## 🧠 FAANG-Level Tips:

* Use `@SetMetadata()` with Guards for **role-based access**
* Combine `@UseInterceptors()` + `@ClassSerializerInterceptor` to hide sensitive fields like `password`
* Write reusable **custom decorators** for extracting `@Tenant()`, `@CurrentUser()`, etc.
* Use `@ApiTags()` + `@ApiBearerAuth()` to make Swagger beautiful and secured

---

## 🚀 What does `nest g` do?

The `nest g` command **automatically creates files** (controllers, services, modules, etc.) with proper **imports**, **decorators**, and **registration** inside the module.

### ✅ Syntax

```
nest g <schematic> <name>
```

Or the long form:

```
nest generate <schematic> <name>
```

---

## 🔧 Common Schematics (`<schematic>` options)

| Schematic                                        | Description                    | Files Created             |
| ------------------------------------------------ | ------------------------------ | ------------------------- |
| `module` (`mo`)                                  | Creates a new module           | `*.module.ts`             |
| `controller` (`co`)                              | Creates a new controller       | `*.controller.ts`         |
| `service` (`s`)                                  | Creates a new service          | `*.service.ts`            |
| `provider` (`p`)                                 | Creates a new provider         | `*.provider.ts`           |
| `middleware` (`mi`)                              | Creates a new middleware class | `*.middleware.ts`         |
| `interceptor` (`in`)                             | Creates a new interceptor      | `*.interceptor.ts`        |
| `guard` (`g`)                                    | Creates a new guard            | `*.guard.ts`              |
| `pipe` (`pi`)                                    | Creates a new pipe             | `*.pipe.ts`               |
| `filter` (`f`)                                   | Creates a new exception filter | `*.filter.ts`             |
| `gateway` (`ga`)                                 | Creates a WebSocket gateway    | `*.gateway.ts`            |
| `resolver` (`r`)                                 | Creates a GraphQL resolver     | `*.resolver.ts`           |
| `class`, `interface`, `enum`, `decorator`, `dto` | For raw boilerplate classes    | `*.ts` files as specified |

---

## 🛠️ Example Usages

### 1. **Generate a Module**

```bash
nest g module trips
```

🟢 Output:

```
src/trips/trips.module.ts
```

---

### 2. **Generate a Controller**

```bash
nest g controller trips
```

🟢 Output:

```
src/trips/trips.controller.ts
```

✅ It also **auto-registers the controller** inside `TripsModule` (if it exists).

---

### 3. **Generate a Service**

```bash
nest g service trips
```

🟢 Output:

```
src/trips/trips.service.ts
```

✅ It also **registers the service as a provider** inside `TripsModule`.

---

### 4. **Generate a Guard**

```bash
nest g guard auth/jwt
```

🟢 Output:

```
src/auth/jwt/jwt.guard.ts
```

---

### 5. **Generate DTO**

```bash
nest g class trips/dto/create-trip.dto --no-spec
```

🟢 Output:

```
src/trips/dto/create-trip.dto.ts
```

---

## 🎯 Flags

| Flag        | Description                           |
| ----------- | ------------------------------------- |
| `--flat`    | Avoids creating a folder for the file |
| `--no-spec` | Skips creating the `*.spec.ts` file   |
| `--spec`    | Forces test file generation           |
| `--path`    | Manually specify where to generate    |

---

## 📦 Best Practice: Generate a Feature with Module + Controller + Service

```bash
nest g resource trips
```

📦 It asks if it's REST or GraphQL and generates:

```
src/trips/
  ├── trips.module.ts
  ├── trips.controller.ts
  ├── trips.service.ts
  ├── dto/
  ├── entities/
```

---

## 🧠 FAANG-Level Tips

* ✅ Use CLI consistently to **enforce structure** and avoid human error
* ✅ Combine `nest g` with **Turborepo** or **monorepo** to generate inside sub-packages
* ✅ You can create **custom schematics** to generate boilerplate with your own standards
* ✅ Ideal for **team projects** to keep structure uniform

---

## 🔥 Summary

| You want to...                    | Use                         |
| --------------------------------- | --------------------------- |
| Create a feature module           | `nest g module feature`     |
| Add controller logic              | `nest g controller feature` |
| Write business logic in a service | `nest g service feature`    |
| Add input validation pipe         | `nest g pipe validation`    |
| Add route guards (AuthZ)          | `nest g guard auth/jwt`     |
| Catch exceptions globally         | `nest g filter http`        |