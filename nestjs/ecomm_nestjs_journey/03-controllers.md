<immersive type="text/markdown">

# 3rd chapter: controllers

## 📡 Controllers: The Entry Point for HTTP Requests

In NestJS, **Controllers are responsible for handling incoming HTTP requests and returning responses to the client**. They act as the entry points for your API, defining the specific routes (endpoints) that clients can interact with. Controllers are essentially the `C` in the MVC (Model-View-Controller) pattern, but in a backend-only context, they manage the interaction layer.

### What is a Controller?

A controller is a class decorated with `@Controller()`. This decorator can optionally take a string argument, which serves as a **route prefix** for all routes defined within that controller. This helps organize endpoints and avoid repetition.

### 🎯 Responsibility & Why Use Controllers? (FAANG Perspective)

From a FAANG-level system design perspective, controllers have very specific responsibilities:

1.  **Route Definition & Binding:** Their primary job is to map incoming HTTP requests (e.g., `GET /products`, `POST /products`) to specific handler methods within the controller class.
2.  **Request Input Handling:** They are responsible for extracting data from the incoming request (e.g., request body, URL parameters, query parameters, headers).
3.  **Response Generation:** They return the appropriate HTTP response to the client.

**Crucially, controllers should be "thin" (or "dumb").** This means they should **not** contain complex business logic, database interactions, or intensive computations. Instead, they should delegate these responsibilities to **Providers (Services)**. This separation of concerns is fundamental for:

  * **Testability:** Isolating business logic in services makes them easier to unit test.
  * **Maintainability:** Changes in business rules don't require changes in the controller's routing logic.
  * **Reusability:** Services can be reused by multiple controllers or even other services.
  * **Scalability:** Clear responsibilities make it easier to understand and scale different layers of the application.

### ✅ Example: `ProductsController` (E-commerce Context)

Let's continue with our e-commerce application. We generated a `ProductsController` in the previous chapter using `nest g resource products`. Now, let's flesh it out with some basic CRUD (Create, Read, Update, Delete) operations for our products.

Recall the file structure from the `nest g resource` command:

```
src/
└── products/
    ├── products.module.ts
    ├── products.controller.ts
    ├── products.service.ts # This is where business logic will go
    ├── dto/
    │   ├── create-product.dto.ts
    │   └── update-product.dto.ts
    └── entities/
        └── product.entity.ts
```

#### 1\. Defining the Controller

```typescript
// src/products/products.controller.ts
import {
  Controller,
  Get,
  Post,
  Body,
  Param,
  Patch,
  Delete,
  HttpCode, // For explicit status codes
  HttpStatus, // For explicit status codes
} from '@nestjs/common';
import { ProductsService } from './products.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';

// @Controller('products') sets the base route for all endpoints in this controller to /products
@Controller('products')
export class ProductsController {
  // Dependency Injection: ProductsService is injected into the controller
  // This allows the controller to delegate business logic to the service
  constructor(private readonly productsService: ProductsService) {}

  // POST /products
  @Post()
  // @HttpCode(HttpStatus.CREATED) explicitly sets the HTTP status code for successful creation
  @HttpCode(HttpStatus.CREATED)
  create(@Body() createProductDto: CreateProductDto) {
    // Delegate creation logic to ProductsService
    return this.productsService.create(createProductDto);
  }

  // GET /products
  @Get()
  // @HttpCode(HttpStatus.OK) is default, but good for clarity
  @HttpCode(HttpStatus.OK)
  findAll() {
    // Delegate finding all products logic to ProductsService
    return this.productsService.findAll();
  }

  // GET /products/:id
  @Get(':id')
  @HttpCode(HttpStatus.OK)
  // @Param('id') extracts the 'id' parameter from the URL
  findOne(@Param('id') id: string) {
    // Delegate finding a single product by ID to ProductsService
    return this.productsService.findOne(id);
  }

  // PATCH /products/:id
  @Patch(':id')
  @HttpCode(HttpStatus.OK)
  // @Param('id') extracts 'id', @Body() extracts the request body
  update(@Param('id') id: string, @Body() updateProductDto: UpdateProductDto) {
    // Delegate update logic to ProductsService
    return this.productsService.update(id, updateProductDto);
  }

  // DELETE /products/:id
  @Delete(':id')
  // @HttpCode(HttpStatus.NO_CONTENT) explicitly sets 204 for successful deletion with no body
  @HttpCode(HttpStatus.NO_CONTENT)
  remove(@Param('id') id: string) {
    // Delegate deletion logic to ProductsService
    return this.productsService.remove(id);
  }
}
```

#### 2\. Placeholder Service Methods

For the above controller to work, our `ProductsService` needs placeholder methods. We'll implement the actual business logic and database interactions in a later chapter. For now, they'll return simple mock data or confirmations.

```typescript
// src/products/products.service.ts (updated for controller interaction)
import { Injectable, NotFoundException } from '@nestjs/common';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { Product } from './entities/product.entity'; // Assuming this entity exists

@Injectable()
export class ProductsService {
  private products: Product[] = []; // Simple in-memory array for now

  // Simulate unique ID generation
  private generateId(): string {
    return (this.products.length + 1).toString();
  }

  create(createProductDto: CreateProductDto): Product {
    // In a real app, this would save to DB and return the created entity
    const newProduct: Product = { id: this.generateId(), ...createProductDto };
    this.products.push(newProduct);
    console.log(`Product created: ${JSON.stringify(newProduct)}`);
    return newProduct;
  }

  findAll(): Product[] {
    return this.products;
  }

  findOne(id: string): Product {
    const product = this.products.find(p => p.id === id);
    if (!product) {
      throw new NotFoundException(`Product with ID "${id}" not found.`);
    }
    return product;
  }

  update(id: string, updateProductDto: UpdateProductDto): Product {
    const index = this.products.findIndex(p => p.id === id);
    if (index === -1) {
      throw new NotFoundException(`Product with ID "${id}" not found.`);
    }
    this.products[index] = { ...this.products[index], ...updateProductDto, id };
    console.log(`Product updated: ${JSON.stringify(this.products[index])}`);
    return this.products[index];
  }

  remove(id: string): void {
    const initialLength = this.products.length;
    this.products = this.products.filter(p => p.id !== id);
    if (this.products.length === initialLength) {
      throw new NotFoundException(`Product with ID "${id}" not found.`);
    }
    console.log(`Product with ID "${id}" removed.`);
  }
}
```

#### 3\. Minimal DTOs (Data Transfer Objects)

We'll cover DTOs in detail in a later chapter, but for now, let's define their basic structure.

```typescript
// src/products/dto/create-product.dto.ts
export class CreateProductDto {
  name: string;
  description?: string; // Optional field
  price: number;
  stock: number;
}
```

```typescript
// src/products/dto/update-product.dto.ts
// A partial type is often used for update DTOs to allow only sending fields to update
import { PartialType } from '@nestjs/mapped-types'; // Or '@nestjs/swagger' for OpenAPI generation
import { CreateProductDto } from './create-product.dto';

export class UpdateProductDto extends PartialType(CreateProductDto) {
  // Additional fields specific to update if needed
}
```

```typescript
// src/products/entities/product.entity.ts
export class Product {
  id: string;
  name: string;
  description?: string;
  price: number;
  stock: number;
}
```

### 🧠 FAANG-Level Controller Best Practices:

1.  **Thin Controllers:** As emphasized, controllers should be lean. Their job is to parse requests, delegate to services, and format responses. Any business logic or data manipulation belongs in services.
2.  **Clear Route Prefixes:** Use the `@Controller('prefix')` decorator to organize related endpoints logically (e.g., `/users`, `/products`, `/orders`). This improves API readability and maintainability.
3.  **Explicit HTTP Status Codes:** While NestJS often infers status codes (e.g., 200 for GET, 201 for POST), explicitly using `@HttpCode(HttpStatus.CREATED)` or `@HttpCode(HttpStatus.NO_CONTENT)` enhances code clarity and ensures correct behavior, especially for edge cases.
4.  **Parameter Validation:** Don't validate parameters directly in controllers. This responsibility is delegated to **Pipes** (which we'll cover soon), ensuring clean separation of concerns and reusability.
5.  **Exception Handling:** Controllers should not have `try-catch` blocks for business logic errors. Instead, throw standard NestJS `HttpException` classes (like `NotFoundException`, `BadRequestException`) or custom exceptions, and let **Exception Filters** handle them globally.
6.  **Dependency Injection:** Always inject services via the constructor. This is the NestJS way and aligns with testability best practices.
7.  **Single Responsibility:** Each controller should ideally handle requests for a single resource (e.g., `ProductsController` for products, not users or orders).

By adhering to these principles, our controllers remain focused on request handling, allowing services to manage the complex business rules and data interactions, a pattern highly favored in large-scale system development.