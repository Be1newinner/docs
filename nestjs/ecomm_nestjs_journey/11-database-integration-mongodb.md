<immersive type="text/markdown">

# 11-database-integration-mongodb

## 💾 Database Integration: MongoDB with Mongoose

For our e-commerce application, we need a robust way to store and retrieve data. **MongoDB** is a popular NoSQL document database, and **Mongoose** is an elegant ODM (Object Data Modeling) library for Node.js that provides a schema-based solution to model your application data. NestJS has excellent integration with Mongoose.

### Why MongoDB and Mongoose? (FAANG Perspective)

While FAANG companies often use a mix of relational (Postgres, MySQL) and NoSQL (Cassandra, DynamoDB, MongoDB) databases depending on the use case, MongoDB with Mongoose is a solid choice for many modern applications due to:

1.  **Flexibility (Schema-less Nature):** MongoDB's document model allows for flexible schemas, which can be advantageous in rapidly evolving applications or when dealing with diverse data structures. Mongoose, however, brings schema enforcement to MongoDB, providing a balance between flexibility and data integrity.
2.  **Scalability:** MongoDB is designed for horizontal scaling, making it suitable for high-volume, high-traffic applications.
3.  **Developer Experience:** Mongoose provides a powerful and intuitive API for interacting with MongoDB, including strong typing, validation, and query building, which significantly enhances developer productivity.
4.  **JSON-like Documents:** Data is stored in BSON (Binary JSON) format, which maps naturally to JavaScript objects, simplifying data manipulation in Node.js applications.
5.  **NestJS Integration:** NestJS provides a dedicated `@nestjs/mongoose` package, making integration seamless and idiomatic.

### Setting up MongoDB and Mongoose

First, ensure you have MongoDB running (locally or via a cloud provider like MongoDB Atlas).

#### 1\. Install Dependencies

```bash
npm install @nestjs/mongoose mongoose@8.15.0
npm install --save-dev @types/mongoose # For TypeScript types
```

#### 2\. Configure the Root Module (`AppModule`)

We'll use `MongooseModule.forRoot()` in our `AppModule` to establish the database connection.

```typescript
// src/app.module.ts (updated)
import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose'; // Import MongooseModule
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ProductsModule } from './products/products.module';
import { LoggerMiddleware } from './common/logger/logger.middleware';
import { AuthTokenMiddleware } from './common/auth-token/auth-token.middleware';
import { APP_FILTER } from '@nestjs/core';
import { HttpExceptionFilter } from './common/http-exception/http-exception.filter';
import { AllExceptionsFilter } from './common/all-exceptions/all-exceptions.filter';
import { SharedModule } from './shared/shared.module';

@Module({
  imports: [
    // Connect to MongoDB. Replace with your actual connection string.
    // For local MongoDB: 'mongodb://localhost/ecommerce'
    // For MongoDB Atlas: 'mongodb+srv://<user>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority'
    MongooseModule.forRoot('mongodb://localhost/ecommerce', {
      // Mongoose 8.15.0 options:
      // No need for useNewUrlParser, useUnifiedTopology, useCreateIndex, useFindAndModify as they are default in Mongoose 6+
    }),
    ProductsModule,
    SharedModule,
  ],
  controllers: [AppController],
  providers: [
    AppService,
    {
      provide: APP_FILTER,
      useClass: HttpExceptionFilter,
    },
    {
      provide: APP_FILTER,
      useClass: AllExceptionsFilter,
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

**Important Note on Connection String:**

  * `mongodb://localhost/ecommerce`: Connects to a local MongoDB instance on the default port (27017) and uses a database named `ecommerce`.
  * For production, you'd typically use environment variables for your connection string (e.g., `process.env.MONGO_URI`) and connect to a cloud-hosted MongoDB (like MongoDB Atlas).

### Defining Schemas and Models

Mongoose uses **Schemas** to define the structure of your documents and **Models** to interact with the MongoDB collection.

#### 1\. Define the Product Schema and Interface

We'll create a `product.schema.ts` file alongside our `product.entity.ts`. The entity defines the TypeScript type, while the schema defines the Mongoose structure.

```bash
# No need to generate, just create these files
# src/products/schemas/product.schema.ts
# src/products/interfaces/product.interface.ts (optional, but good practice for Mongoose Document type)
```

```typescript
// src/products/schemas/product.schema.ts
import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument } from 'mongoose';

// Export the Mongoose Document type for Product
export type ProductDocument = HydratedDocument<Product>;

@Schema({ timestamps: true }) // Adds createdAt and updatedAt fields automatically
export class Product {
  @Prop({ required: true, unique: true }) // 'name' is required and must be unique
  name: string;

  @Prop()
  description: string;

  @Prop({ required: true, min: 0 }) // 'price' is required and must be non-negative
  price: number;

  @Prop({ required: true, min: 0 }) // 'stock' is required and must be non-negative
  stock: number;

  // You can add more fields here, e.g., category: string, imageUrl: string[]
}

export const ProductSchema = SchemaFactory.createForClass(Product);
```

```typescript
// src/products/entities/product.entity.ts (Existing, but now can derive from schema)
// This file can now represent the plain DTO/interface for a Product
// and the Mongoose Document type can be used for actual DB interactions.
// For consistency, let's keep it simple and align it with the schema.
export class Product {
  id: string; // Mongoose adds _id, which we often map to 'id' in DTOs
  name: string;
  description?: string;
  price: number;
  stock: number;
  createdAt?: Date; // Added by timestamps: true
  updatedAt?: Date; // Added by timestamps: true
}
```

#### 2\. Register the Schema in `ProductsModule`

Each feature module that interacts with a database needs to register its own schemas using `MongooseModule.forFeature()`.

```typescript
// src/products/products.module.ts (updated)
import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose'; // Import MongooseModule
import { ProductsService } from './products.service';
import { ProductsController } from './products.controller';
import { Product, ProductSchema } from './schemas/product.schema'; // Import our schema and class
import { SharedModule } from '../shared/shared.module';

@Module({
  imports: [
    // Register the Product schema for this module
    MongooseModule.forFeature([{ name: Product.name, schema: ProductSchema }]),
    SharedModule, // For LoggerService
  ],
  controllers: [ProductsController],
  providers: [ProductsService],
  // If ProductsService needs to be used by other modules, it should be exported here.
  // exports: [ProductsService],
})
export class ProductsModule {}
```

### Interacting with the Database (`ProductsService`)

Now, we can inject the Mongoose `Model` into our `ProductsService` and use it for CRUD operations.

```typescript
// src/products/products.service.ts (updated to use Mongoose)
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose'; // Import InjectModel
import { Model } from 'mongoose'; // Import Mongoose Model type
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { Product, ProductDocument } from './schemas/product.schema'; // Import Mongoose Product and ProductDocument
import { LoggerService } from '../shared/logger/logger.service';

@Injectable()
export class ProductsService {
  // Inject the Mongoose Product Model
  constructor(
    @InjectModel(Product.name) private productModel: Model<ProductDocument>,
    private readonly logger: LoggerService,
  ) {
    this.logger.setContext('ProductsService');
  }

  async create(createProductDto: CreateProductDto): Promise<Product> {
    const createdProduct = new this.productModel(createProductDto);
    const savedProduct = await createdProduct.save();
    this.logger.log(`Created product: ${savedProduct.name} (ID: ${savedProduct._id})`);
    // Map Mongoose _id to id for consistency with DTOs/API responses
    return { id: savedProduct._id.toString(), ...savedProduct.toObject() };
  }

  async findAll(): Promise<Product[]> {
    this.logger.debug('Fetching all products from DB');
    const products = await this.productModel.find().exec();
    // Map _id to id for each product
    return products.map(p => ({ id: p._id.toString(), ...p.toObject() }));
  }

  async findOne(id: string): Promise<Product> {
    this.logger.debug(`Fetching product with ID: ${id}`);
    const product = await this.productModel.findById(id).exec();
    if (!product) {
      this.logger.warn(`Product with ID "${id}" not found.`);
      throw new NotFoundException(`Product with ID "${id}" not found.`);
    }
    return { id: product._id.toString(), ...product.toObject() };
  }

  async update(id: string, updateProductDto: UpdateProductDto): Promise<Product> {
    this.logger.log(`Updating product ID: ${id}`);
    const updatedProduct = await this.productModel.findByIdAndUpdate(id, updateProductDto, { new: true }).exec();
    if (!updatedProduct) {
      this.logger.warn(`Attempted to update non-existent product with ID "${id}".`);
      throw new NotFoundException(`Product with ID "${id}" not found.`);
    }
    return { id: updatedProduct._id.toString(), ...updatedProduct.toObject() };
  }

  async remove(id: string): Promise<void> {
    this.logger.log(`Removing product ID: ${id}`);
    const result = await this.productModel.deleteOne({ _id: id }).exec();
    if (result.deletedCount === 0) {
      this.logger.warn(`Attempted to remove non-existent product with ID "${id}".`);
      throw new NotFoundException(`Product with ID "${id}" not found.`);
    }
  }
}
```

**Note on `_id` to `id` mapping:**
MongoDB uses `_id` as its primary key. When returning data to clients, it's common practice to map `_id` to `id` for consistency with REST API conventions. `toObject()` converts the Mongoose document to a plain JavaScript object, making it easier to destructure and add `id`.

### 🧠 FAANG-Level Database Integration Best Practices:

1.  **Configuration Management:** Never hardcode database credentials. Use environment variables (`process.env.MONGO_URI`) and a dedicated configuration module (like `@nestjs/config`) to manage sensitive settings.
2.  **Connection Pooling:** Mongoose handles connection pooling automatically, which is crucial for performance at scale. Ensure your connection options are optimized for your environment.
3.  **Schema Design & Validation:** While NoSQL is flexible, enforce schemas with Mongoose. Use Mongoose schema types, validation rules, and indexes (`@Prop({ unique: true })`) to maintain data integrity and optimize query performance.
4.  **Error Handling:** Implement robust error handling for database operations. Catch Mongoose-specific errors (e.g., validation errors, duplicate key errors) and translate them into appropriate `HttpException` responses.
5.  **Asynchronous Operations:** All database operations are asynchronous. Always use `async/await` or Promises (`.exec()`) for clean, readable code.
6.  **Performance Optimization:**
      * **Indexing:** Define appropriate indexes on your Mongoose schemas (`ProductSchema.index({ name: 1 })`) for frequently queried fields to speed up read operations.
      * **Projection:** Retrieve only the fields you need using `.select()` to reduce network overhead.
      * **Pagination:** Implement pagination for large datasets to avoid returning too much data at once.
      * **Aggregation:** Use MongoDB's aggregation pipeline for complex data transformations and analytics on the database side.
7.  **Transactions (for MongoDB 4.0+):** For operations involving multiple documents that require atomicity, use MongoDB's multi-document transactions with Mongoose sessions.
8.  **Repository Pattern (Advanced):** For very large applications, consider abstracting Mongoose models behind a custom repository layer. This further decouples your services from the specific ORM/ODM implementation, making it easier to swap databases or testing.
9.  **Data Consistency:** Understand MongoDB's eventual consistency model and when strong consistency might be required (e.g., using transactions, write concerns).

Integrating MongoDB with Mongoose provides a powerful and flexible data layer for our NestJS e-commerce application. This setup is scalable and developer-friendly, aligning with modern backend development practices.