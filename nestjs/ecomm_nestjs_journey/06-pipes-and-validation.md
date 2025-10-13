<immersive type="text/markdown">

# 06-pipes-and-validation

## 🧱 Pipes & Validation: Ensuring Data Integrity

In NestJS, **Pipes** are powerful classes that operate on the arguments of route handlers. They have two main purposes:

1.  **Transformation:** To transform input data to the desired format (e.g., string to number, string to boolean).
2.  **Validation:** To validate input data against predefined rules. If validation fails, a `BadRequestException` is thrown.

Pipes are executed **after** middleware and **before** guards and the actual controller method execution. This position in the pipeline makes them ideal for ensuring that incoming data is in the correct shape and format before any business logic is applied.

### What is a Pipe?

A pipe is a class that implements the `PipeTransform` interface, containing a `transform()` method.

### 🎯 Responsibility & Why Use Pipes? (FAANG Perspective)

For building reliable and secure applications at scale, Pipes are indispensable for:

1.  **Input Validation:** Ensuring that all incoming data adheres to the expected format and constraints. This is a critical security and data integrity measure.
2.  **Input Transformation:** Automatically converting data types or structuring complex inputs, reducing boilerplate code in controllers.
3.  **Separation of Concerns:** Keeping validation and transformation logic out of controllers and services. Controllers focus on routing, services on business logic, and pipes on input processing.
4.  **Reusability:** A single pipe can be applied to multiple routes or even globally, ensuring consistent data handling across the API.

### ✅ Example 1: Transformation Pipe (`ParseIntPipe`)

NestJS provides several built-in pipes. One common example is `ParseIntPipe`, which transforms a string (from a URL parameter or query) into a number. If the transformation fails (e.g., "abc" cannot be parsed as a number), it throws a `BadRequestException`.

```typescript
// src/products/products.controller.ts (excerpt from earlier)
import { Controller, Get, Param, ParseIntPipe } from '@nestjs/common';
import { ProductsService } from './products.service';

@Controller('products')
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}

  // GET /products/:id
  // Usage of ParseIntPipe directly on the parameter
  // NestJS will try to parse 'id' as an integer. If it fails, it throws a 400 Bad Request.
  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) {
    // Note: The service expects string IDs in our current setup, so this is illustrative.
    // If your service (and DB) uses numeric IDs, this is perfect.
    // For our current string-based service: return this.productsService.findOne(id.toString());
    return this.productsService.findOne(id.toString()); // Adapt for our current string-based ID service
  }
}
```

### ✅ Example 2: Validation Pipes with Data Transfer Objects (DTOs)

This is arguably the most powerful use case for pipes. **Data Transfer Objects (DTOs)** are plain TypeScript classes that define the shape of data sent over the network. When combined with the `ValidationPipe` and the `class-validator` library, they provide robust, automatic input validation.

#### Why DTOs and `class-validator`? (FAANG Perspective)

  * **Clear API Contracts:** DTOs explicitly define what data your API expects, acting as documentation.
  * **Strong Typing:** Leverages TypeScript for compile-time safety and better developer experience.
  * **Automatic Validation:** The `ValidationPipe` automatically validates incoming request bodies against the DTO's schema.
  * **Reduced Boilerplate:** No more manual if-else validation checks in controllers.
  * **Maintainability:** Validation rules are declared declaratively using decorators, making them easy to read and update.

#### Setup for DTOs and Validation:

First, ensure you have the necessary packages installed (as per your preferred stack):

```bash
npm install class-validator@0.14.2 class-transformer@0.5.1
npm install --save-dev @types/express # Ensure Express types are installed for middleware/pipes
```

#### 1\. Define DTOs with `class-validator` Decorators

Let's refine our `CreateProductDto` and `UpdateProductDto` using validation decorators.

```typescript
// src/products/dto/create-product.dto.ts
import { IsString, IsNumber, IsOptional, Min, MaxLength, IsNotEmpty } from 'class-validator';

export class CreateProductDto {
  @IsNotEmpty() // Ensures the string is not empty
  @IsString()
  @MaxLength(100) // Max length for product names
  name: string;

  @IsOptional() // The field is optional
  @IsString()
  description?: string;

  @IsNumber()
  @Min(0.01) // Price must be at least 0.01
  price: number;

  @IsNumber()
  @Min(0) // Stock cannot be negative
  stock: number;
}
```

```typescript
// src/products/dto/update-product.dto.ts
import { PartialType } from '@nestjs/mapped-types'; // Used for convenience with DTO inheritance
// Alternatively, if not installing @nestjs/mapped-types, you can manually make fields optional.
import { CreateProductDto } from './create-product.dto';

// PartialType makes all properties of CreateProductDto optional for updates.
export class UpdateProductDto extends PartialType(CreateProductDto) {}
```

#### 2\. Apply the `ValidationPipe`

You can apply `ValidationPipe` at different levels:

  * **Method-level:** Apply to a specific route handler.
  * **Controller-level:** Apply to all route handlers in a controller.
  * **Global-level (Recommended for FAANG):** Apply to the entire application. This is the best practice as it ensures all incoming data is validated consistently.

Let's apply it globally in `main.ts`:

```typescript
// src/main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common'; // Import ValidationPipe

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Apply ValidationPipe globally
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true, // Strips away properties that are not defined in the DTO
    forbidNonWhitelisted: true, // Throws an error if non-whitelisted properties are present
    transform: true, // Automatically transforms payload objects to DTO instances
    // Forbid unknown values in nested objects, useful for strict API contracts
    // disableErrorMessages: false, // Set to true in production for security
  }));

  // Enable CORS for our e-commerce frontend
  app.enableCors({
    origin: ['http://localhost:4200', 'http://localhost:3001'], // Allow specific origins
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    credentials: true,
  });


  const PORT = process.env.PORT || 3000;
  await app.listen(PORT);
  console.log(`Application is running on: ${await app.getUrl()}`);
}
bootstrap();
```

With the global `ValidationPipe` enabled, any `CreateProductDto` or `UpdateProductDto` passed to a controller method decorated with `@Body()` will automatically be validated against its `class-validator` rules. If validation fails, NestJS will automatically throw a `BadRequestException` with detailed error messages.

#### 3\. Update `ProductsController` to Use DTOs

Our `ProductsController` already uses these DTOs. Now, with the global pipe, it gets automatic validation for free:

```typescript
// src/products/products.controller.ts (no changes needed from before, just showing context)
import { Controller, Post, Body } from '@nestjs/common';
import { ProductsService } from './products.service';
import { CreateProductDto } from './dto/create-product.dto';

@Controller('products')
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}

  @Post()
  create(@Body() createProductDto: CreateProductDto) {
    // No manual validation needed here! The ValidationPipe handled it.
    return this.productsService.create(createProductDto);
  }

  // ... other methods
}
```

### 🧠 FAANG-Level Pipes & Validation Best Practices:

1.  **Global `ValidationPipe` with `whitelist: true` and `forbidNonWhitelisted: true`:** This is the gold standard for robust API inputs. It ensures that only expected data passes through and prevents malicious or unintended extra properties from reaching your business logic.
2.  **DTOs for Every Input:** Use DTOs for all incoming request bodies (`@Body()`), query parameters (`@Query()`), and route parameters (`@Param()`). Even if a DTO seems trivial, it provides a clear contract.
3.  **Strict Type Definitions:** Leverage TypeScript to its fullest. DTOs should reflect the exact shape of your data.
4.  **`class-validator` for Expressive Rules:** Use `class-validator`'s rich set of decorators (`@IsString()`, `@IsNumber()`, `@IsEmail()`, `@IsUUID()`, `@IsEnum()`, `@ValidateNested()`, etc.) to define precise validation rules.
5.  **`class-transformer` for Type Coercion:** The `transform: true` option in `ValidationPipe` automatically uses `class-transformer` to convert plain JavaScript objects into instances of your DTO classes. This is crucial for working with types (e.g., ensuring `price` is a `number`, not a `string`).
6.  **Custom Validation Rules:** For complex or unique validation logic, create custom validation decorators or custom pipes.
7.  **Zod as an Alternative (FAANG insight):** While `class-validator` is the default and well-integrated, companies like Google often favor schema validation libraries that can also be used for runtime validation *and* static type inference, such as **Zod** (which is in your preferred stack). You can integrate Zod with NestJS by writing a custom pipe that uses a Zod schema to validate the input. This provides a single source of truth for your data shapes and validates at runtime, while also giving you strong TypeScript types. We are sticking to `class-validator` here for the default NestJS learning path, but keep Zod in mind for advanced schema management.

Pipes, especially in conjunction with DTOs and `class-validator`, form a powerful and declarative system for managing incoming data, a cornerstone of building secure and stable APIs at scale.