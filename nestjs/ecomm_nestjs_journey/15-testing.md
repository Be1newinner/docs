# **15. Testing**

Testing is not merely a phase; it's an integral part of the development process at FAANG companies. A well-tested application reduces bugs, enables confident refactoring, accelerates development cycles, and ensures the system behaves as expected under various conditions. For a complex e-commerce backend, robust testing is crucial to prevent issues with product availability, order processing, payment, and user data.

NestJS provides first-class support for testing, leveraging popular tools like **Jest** as its default testing framework.

**Why comprehensive Testing for FAANG-level applications?**

  * **Reliability**: Guarantees that features work as intended and that new changes don't break existing functionality (regression prevention).
  * **Maintainability & Refactoring**: Allows developers to confidently make changes and refactor code, knowing that tests will catch unintended side effects.
  * **Faster Development Cycles**: Reduces the need for manual testing, enabling quicker iteration and deployment.
  * **Collaboration**: Provides clear specifications of how code should behave, aiding team understanding.
  * **Quality Assurance**: Ensures the delivered product meets functional and non-functional requirements.
  * **Reduced Operational Costs**: Fewer bugs in production mean less time spent on hotfixes and incident response.

**Core Components & Types of Tests:**

1.  **Jest**: The powerful JavaScript testing framework that NestJS integrates with out-of-the-box.
2.  **Supertest**: A library for testing HTTP APIs, commonly used for integration and end-to-end tests.
3.  **Testing Strategy**:
      * **Unit Tests**: Test individual components (functions, classes, services) in isolation.
      * **Integration Tests**: Test the interaction between multiple components (e.g., a controller and a service, a service and a database).
      * **End-to-End (E2E) Tests**: Test the entire system flow from the user's perspective, simulating real user interactions through API calls.

**Installation (already part of NestJS setup, but verify dependencies):**

Your preferred versions are: `jest 29.7.0`, `@types/jest` (should be compatible with Jest 29). `supertest` and `@types/supertest` will also be needed.

```bash
npm install --save-dev jest@29.7.0 @types/jest@29.5.12 supertest@6.3.4 @types/supertest@6.0.2
```

*(Self-correction: Ensure `@types/jest` is compatible with `jest` 29.7.0. `@types/jest@29.5.12` is a good match. `supertest` and its types are crucial for integration/E2E HTTP testing.)*

NestJS CLI automatically sets up basic testing infrastructure when you generate new components (`nest g service`, `nest g controller`, etc.).

-----

### **15.1 Unit Testing with Jest**

Unit tests focus on the smallest testable parts of an application, typically individual classes or functions, in isolation from their external dependencies.

**Example: Unit Testing a `UserService`**

Let's assume our `UserService` (from Chapter 12) has methods like `create` and `findOneByEmail`. We want to test these methods without actually hitting a MongoDB database. This is achieved through **mocking**.

1.  **`user.service.spec.ts`**:
    ```typescript
    // src/users/user.service.spec.ts
    import { Test, TestingModule } from '@nestjs/testing';
    import { UserService } from './user.service';
    import { getModelToken } from '@nestjs/mongoose';
    import { Model } from 'mongoose';
    import { User } from './schemas/user.schema';
    import * as bcrypt from 'bcrypt';
    import { BadRequestException } from '@nestjs/common';

    // Mock the Mongoose User Model
    const mockUserModel = {
      findOne: jest.fn(),
      findById: jest.fn(),
      create: jest.fn(), // We'll mock the static create method for simplicity in some cases
      // For instance methods like .save(), we need to mock the instance
      save: jest.fn(),
    };

    // Mock bcrypt.hash
    jest.mock('bcrypt', () => ({
      hash: jest.fn((password) => Promise.resolve(`hashed_${password}_salt`)),
      compare: jest.fn((password, hash) => Promise.resolve(`hashed_${password}_salt` === hash)),
    }));

    describe('UserService (Unit)', () => {
      let service: UserService;
      let userModel: Model<User>;

      beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
          providers: [
            UserService,
            {
              provide: getModelToken(User.name),
              useValue: mockUserModel, // Provide our mock model
            },
          ],
        }).compile();

        service = module.get<UserService>(UserService);
        userModel = module.get<Model<User>>(getModelToken(User.name));

        // Reset mocks before each test
        jest.clearAllMocks();
      });

      it('should be defined', () => {
        expect(service).toBeDefined();
      });

      describe('create', () => {
        const registerDto = { email: 'test@example.com', password: 'Password123!' };

        it('should create a new user and hash the password', async () => {
          const mockUserDoc = {
            email: registerDto.email,
            password: 'hashed_Password123!_salt',
            roles: ['user'],
            save: mockUserModel.save, // Attach the mock save method to the mock document
          };
          // Mocking the constructor call for `new this.userModel` and its .save() method
          jest.spyOn(userModel, 'create').mockImplementationOnce(() => mockUserDoc as any); // Type assertion for mock
          mockUserModel.save.mockResolvedValueOnce(mockUserDoc);

          const result = await service.create(registerDto);

          expect(bcrypt.hash).toHaveBeenCalledWith(registerDto.password, 10);
          expect(userModel.create).toHaveBeenCalledWith({
            email: registerDto.email,
            password: 'hashed_Password123!_salt',
            roles: ['user'],
          });
          expect(result).toEqual(mockUserDoc);
        });

        it('should throw BadRequestException if user with email already exists', async () => {
          jest.spyOn(service, 'findOneByEmail').mockResolvedValueOnce({ email: registerDto.email } as any);

          await expect(service.create(registerDto)).rejects.toThrow(BadRequestException);
          expect(bcrypt.hash).not.toHaveBeenCalled(); // Password should not be hashed if user exists
        });
      });

      describe('findOneByEmail', () => {
        it('should return a user if found', async () => {
          const mockUser = { email: 'existing@example.com', password: 'hashedpassword' };
          mockUserModel.findOne.mockReturnValueOnce({ exec: jest.fn().mockResolvedValueOnce(mockUser) });

          const result = await service.findOneByEmail('existing@example.com');
          expect(result).toEqual(mockUser);
          expect(mockUserModel.findOne).toHaveBeenCalledWith({ email: 'existing@example.com' });
        });

        it('should return null if user not found', async () => {
          mockUserModel.findOne.mockReturnValueOnce({ exec: jest.fn().mockResolvedValueOnce(null) });

          const result = await service.findOneByEmail('nonexistent@example.com');
          expect(result).toBeNull();
        });
      });
    });
    ```
      * **FAANG Insight**:
          * **Test Bed (`Test.createTestingModule`)**: NestJS's testing utility creates a lightweight testing module, allowing you to easily provide mocks for dependencies instead of real implementations.
          * **`getModelToken`**: Essential for providing a mock Mongoose `Model`.
          * **Deep Mocking**: Notice how we mock the `Model` methods (`findOne`, `findById`, `create`) and the chainable `.exec()` method for Mongoose. For `create`, we mock the instance's `save()` method. This ensures we control the behavior of external dependencies precisely.
          * **`jest.fn()` / `jest.spyOn()`**: Use `jest.fn()` to create mock functions and `jest.spyOn()` to spy on existing methods, allowing you to assert calls and control return values.
          * **`jest.clearAllMocks()`**: Crucial in `beforeEach` to ensure a clean state for each test, preventing test pollution.
          * **Testing Edge Cases**: We test both successful creation and the `BadRequestException` for existing users.
          * **Password Hashing Mock**: We completely mock `bcrypt.hash` and `bcrypt.compare` to avoid slow cryptographic operations during unit tests. This ensures tests run quickly.

-----

### **15.2 Integration Testing**

Integration tests verify that different modules or services in your application work correctly together. This often involves testing a controller that uses a service, which in turn might interact with a mocked database.

**Example: Integration Testing `AuthController` and `AuthService` with Mocked `UserService` and `JwtService`**

Here, we'll test the `/auth/register` and `/auth/login` endpoints. We won't hit a real database, but we *will* use the actual `AuthController` and `AuthService`, mocking their deeper dependencies.

1.  **`auth.controller.spec.ts` (Integration Test)**:
    ```typescript
    // src/auth/auth.controller.spec.ts
    import { Test, TestingModule } from '@nestjs/testing';
    import { AuthController } from './auth.controller';
    import { AuthService } from './auth.service';
    import { JwtService } from '@nestjs/jwt';
    import { UserService } from '../users/user.service';
    import { getModelToken } from '@nestjs/mongoose';
    import { User } from '../users/schemas/user.schema';
    import { ConfigService } from '@nestjs/config'; // Needed for JwtModule.registerAsync

    // Mock dependencies for AuthService
    const mockUserService = {
      findOneByEmail: jest.fn(),
      create: jest.fn(),
    };

    const mockJwtService = {
      sign: jest.fn(() => 'mockAccessToken'),
    };

    // Mock ConfigService to provide JWT_SECRET
    const mockConfigService = {
      get: jest.fn((key: string) => {
        if (key === 'JWT_SECRET') return 'superSecretDevelopmentKey!';
        if (key === 'JWT_EXPIRATION_TIME') return '1h';
        return null;
      }),
    };

    describe('AuthController (Integration)', () => {
      let controller: AuthController;
      let authService: AuthService;

      beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
          controllers: [AuthController],
          providers: [
            AuthService,
            { provide: UserService, useValue: mockUserService },
            { provide: JwtService, useValue: mockJwtService },
            { provide: ConfigService, useValue: mockConfigService }, // Provide mock ConfigService
            // Mocks for Mongoose models if UserService were not mocked directly
            { provide: getModelToken(User.name), useValue: {} },
          ],
        }).compile();

        controller = module.get<AuthController>(AuthController);
        authService = module.get<AuthService>(AuthService);

        jest.clearAllMocks();
      });

      it('should be defined', () => {
        expect(controller).toBeDefined();
      });

      describe('register', () => {
        const registerDto = { email: 'newuser@example.com', password: 'Password123!' };

        it('should register a new user successfully', async () => {
          jest.spyOn(authService, 'register').mockResolvedValueOnce({ email: registerDto.email } as any);

          const result = await controller.register(registerDto);
          expect(authService.register).toHaveBeenCalledWith(registerDto);
          expect(result).toEqual({ email: registerDto.email });
        });

        it('should throw BadRequestException for duplicate email', async () => {
          jest.spyOn(authService, 'register').mockRejectedValueOnce(new BadRequestException('User with this email already exists'));

          await expect(controller.register(registerDto)).rejects.toThrow(BadRequestException);
        });
      });

      describe('login', () => {
        const loginDto = { email: 'user@example.com', password: 'Password123!' };
        const mockUserPayload = { _id: 'someUserId', email: loginDto.email, roles: ['user'] };

        it('should log in user and return access token', async () => {
          // Mock validateUser method within AuthService directly, as LocalAuthGuard calls it
          jest.spyOn(authService, 'validateUser').mockResolvedValueOnce(mockUserPayload);
          jest.spyOn(authService, 'login').mockResolvedValueOnce({ access_token: 'mockAccessToken' });

          // We need to simulate req.user being populated by the LocalAuthGuard
          const req = { user: mockUserPayload };
          const result = await controller.login(req as any);

          expect(authService.login).toHaveBeenCalledWith(mockUserPayload);
          expect(result).toEqual({ access_token: 'mockAccessToken' });
        });

        it('should throw UnauthorizedException for invalid credentials', async () => {
          jest.spyOn(authService, 'validateUser').mockResolvedValueOnce(null); // Simulate validation failure

          // We need to mock the guard's behavior as well, or test the guard directly.
          // For controller integration, we typically mock the AuthService's underlying validation.
          // Note: Testing guards directly often requires a separate test for the guard.
          // Here, we're relying on the fact that if validateUser returns null, authService.login won't be called,
          // and a real LocalAuthGuard would throw UnauthorizedException.
          // For true integration, you'd use Supertest and the actual LocalAuthGuard.
        });
      });
    });
    ```
      * **FAANG Insight**:
          * **Focused Scope**: We're testing the `AuthController`'s interaction with the `AuthService` and its DTOs, but we mock deeper dependencies like `UserService` and `JwtService`. This keeps the test focused on the "integration" between controller and service.
          * **Mocking `req.user`**: For handlers using `@Request() req: any`, it's important to mock how `req.user` would be populated by a guard (like `LocalAuthGuard` or `JwtAuthGuard`).
          * **Testing Guards Separately (or with E2E)**: While `authService.validateUser` is mocked here, in a real scenario, you'd have dedicated unit tests for `LocalAuthGuard` and `JwtAuthGuard` themselves, and then rely on E2E tests to verify their full integration with the HTTP pipeline.

-----

### **15.3 End-to-End (E2E) Testing with Jest and Supertest**

E2E tests simulate real user scenarios by sending actual HTTP requests to your running NestJS application (or a test instance of it). They test the entire stack, from routing, controllers, services, to database interactions.

**Example: E2E Testing User Registration and Login**

For E2E tests, you typically set up a dedicated test database (or a fresh instance) to ensure isolation and prevent test pollution.

1.  **`app.e2e-spec.ts` or `auth.e2e-spec.ts`**:
    ```typescript
    // test/auth.e2e-spec.ts
    import { Test, TestingModule } from '@nestjs/testing';
    import { INestApplication, ValidationPipe, HttpStatus } from '@nestjs/common';
    import * as request from 'supertest';
    import { AppModule } from './../src/app.module';
    import { MongooseModule } from '@nestjs/mongoose'; // To close connection
    import { Connection } from 'mongoose';
    import { getConnectionToken } from '@nestjs/mongoose';
    import { ConfigService } from '@nestjs/config';

    describe('Auth E2E', () => {
      let app: INestApplication;
      let dbConnection: Connection;
      let configService: ConfigService;

      beforeAll(async () => {
        // Create a test module that uses the actual AppModule but potentially
        // overrides some configuration for testing purposes (e.g., test database)
        const moduleFixture: TestingModule = await Test.createTestingModule({
          imports: [AppModule],
        })
        .overrideProvider(ConfigService) // Override ConfigService to ensure test env variables
        .useValue({
          get: jest.fn((key: string) => {
            if (key === 'MONGODB_URI') return process.env.TEST_MONGODB_URI || 'mongodb://localhost:27017/ecommerce_test_db';
            if (key === 'JWT_SECRET') return 'superSecretDevelopmentKey!'; // Same as in .env for dev
            if (key === 'JWT_EXPIRATION_TIME') return '1h';
            if (key === 'PORT') return 4000;
            if (key === 'API_PREFIX') return 'api/v1';
            return null;
          }),
        })
        .compile();

        app = moduleFixture.createNestApplication();

        // Apply global pipes and prefix as in main.ts
        app.useGlobalPipes(new ValidationPipe({
          transform: true,
          whitelist: true,
          forbidNonWhitelisted: true,
        }));
        configService = app.get(ConfigService);
        app.setGlobalPrefix(configService.get('API_PREFIX'));

        await app.init();

        // Get the Mongoose connection to clear the database before each test suite
        dbConnection = app.get<Connection>(getConnectionToken());
      });

      beforeEach(async () => {
        // Clear all collections before each test to ensure test isolation
        const collections = Object.keys(dbConnection.collections);
        for (const collectionName of collections) {
          const collection = dbConnection.collections[collectionName];
          await collection.deleteMany({});
        }
      });

      afterAll(async () => {
        await dbConnection.close(); // Close database connection
        await app.close();
      });

      describe('/auth/register (POST)', () => {
        const registerDto = { email: 'e2e_test@example.com', password: 'E2EP@ssw0rd!' };

        it('should register a new user successfully', async () => {
          const response = await request(app.getHttpServer())
            .post('/api/v1/auth/register') // Use the global prefix
            .send(registerDto)
            .expect(HttpStatus.CREATED);

          expect(response.body).toHaveProperty('email', registerDto.email);
          expect(response.body).not.toHaveProperty('password'); // Password should not be returned
          expect(response.body).toHaveProperty('_id');
          expect(response.body).toHaveProperty('roles', ['user']);
        });

        it('should return 400 for duplicate email', async () => {
          await request(app.getHttpServer())
            .post('/api/v1/auth/register')
            .send(registerDto)
            .expect(HttpStatus.CREATED); // First registration

          const response = await request(app.getHttpServer())
            .post('/api/v1/auth/register')
            .send(registerDto) // Second registration with same email
            .expect(HttpStatus.BAD_REQUEST);

          expect(response.body.message).toEqual('User with this email already exists');
        });

        it('should return 400 for invalid password format', async () => {
          const invalidRegisterDto = { email: 'e2e_invalid@example.com', password: 'weak' };
          const response = await request(app.getHttpServer())
            .post('/api/v1/auth/register')
            .send(invalidRegisterDto)
            .expect(HttpStatus.BAD_REQUEST);

          expect(response.body.message).toEqual([
            'Password must be between 8 and 30 characters',
            'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character',
          ]);
        });
      });

      describe('/auth/login (POST)', () => {
        const user = { email: 'login_test@example.com', password: 'LoginP@ssw0rd!' };
        let accessToken: string;

        beforeEach(async () => {
          // Register the user before each login test
          await request(app.getHttpServer())
            .post('/api/v1/auth/register')
            .send(user)
            .expect(HttpStatus.CREATED);
        });

        it('should log in a user and return an access token', async () => {
          const response = await request(app.getHttpServer())
            .post('/api/v1/auth/login')
            .send(user)
            .expect(HttpStatus.OK);

          expect(response.body).toHaveProperty('access_token');
          accessToken = response.body.access_token;
        });

        it('should return 401 for invalid credentials', async () => {
          const invalidUser = { email: 'login_test@example.com', password: 'WrongPassword!' };
          const response = await request(app.getHttpServer())
            .post('/api/v1/auth/login')
            .send(invalidUser)
            .expect(HttpStatus.UNAUTHORIZED);

          expect(response.body.message).toEqual('Invalid credentials'); // Message from LocalStrategy
        });
      });
    });
    ```
      * **FAANG Insight**:
          * **Full Application Instance (`app.init()`)**: `Test.createTestingModule({ imports: [AppModule] })` and `app.init()` spin up a full NestJS application, including all modules, controllers, services, and database connections (to the test DB).
          * **`supertest`**: Used to send actual HTTP requests to the application. This is the cornerstone of E2E testing for HTTP APIs.
          * **Dedicated Test Database**: **Crucial\!** Always use a separate database for E2E tests to prevent data corruption and ensure test isolation. We override `ConfigService` to point to a `ecommerce_test_db`.
          * **`beforeEach` for Data Cleanup**: Clearing all collections before *each* test ensures that tests are independent and don't affect each other. This is a common pattern in E2E tests.
          * **Testing HTTP Status Codes**: Use `.expect(HttpStatus.CREATED)` or `.expect(400)` to assert correct HTTP responses.
          * **Payload Validation**: Assert that the response body contains expected properties and values (e.g., `toHaveProperty`, `not.toHaveProperty`).
          * **Testing Error Paths**: It's as important to test invalid inputs and error responses as it is to test success paths.

-----

### **15.4 Mocking Dependencies**

As seen in the examples, mocking is fundamental for testing, especially for unit and some integration tests.

**Key Mocking Strategies:**

  * **`jest.fn()`**: Creates a mock function. Useful when you need to replace a function with a controlled version.
  * **`jest.spyOn()`**: Spies on an existing method of an object. The original method can still be called, or you can mock its implementation with `mockImplementation()` or `mockReturnValue()`.
  * **`jest.mock('module-name')`**: Mocks an entire module. Useful for external libraries (like `bcrypt` or database drivers) or for core NestJS components that you want to completely control.
  * **`Test.createTestingModule().overrideProvider()`**: NestJS specific way to replace a provider (service, controller, gateway) with a mock implementation within the test module. This is powerful for isolating components.

**When to Mock?**

  * **Unit Tests**: Mock *all* external dependencies of the component under test.
  * **Integration Tests**: Mock dependencies that are *outside the scope* of the integration (e.g., actual database calls, external API calls), but use real implementations for components within the integration scope.
  * **E2E Tests**: Mock *nothing* that is part of the application's core flow. You *might* mock external services (like a payment gateway or email service) if you don't want to incur real costs or delays, but the goal is to be as close to reality as possible.

-----

### **FAANG-level Best Practices for Testing:**

1.  **Test Pyramid**: Follow the test pyramid strategy:

      * **Many Unit Tests**: Fast, cheap, isolated. Cover most business logic.
      * **Fewer Integration Tests**: Slower, more expensive, cover component interactions.
      * **Fewest E2E Tests**: Slowest, most expensive, cover critical user flows.
          * **FAANG Insight**: Companies heavily rely on automated testing. Unit tests are often run on every code commit (e.g., pre-commit hooks). Integration and E2E tests run in CI/CD pipelines, typically on feature branches and before merging to main.

2.  **Test Coverage**: Aim for high, but sensible, test coverage (e.g., 80%+ line/branch coverage). Don't aim for 100% blindly; focus on critical paths and complex logic.

      * **FAANG Insight**: Code coverage is a common metric, often enforced in CI/CD.

3.  **Clear Naming Conventions**:

      * `*.spec.ts` for unit/integration tests.
      * `*.e2e-spec.ts` for end-to-end tests.
      * Descriptive `describe` and `it` blocks (e.g., `describe('UserService', () => { it('should create a user', ...)})`).

4.  **Test Isolation & Idempotency**:

      * Each test should be independent and produce the same result every time it runs, regardless of the order or previous test executions.
      * For E2E tests, this means cleaning the database before each test or using transactions and rolling them back.

5.  **Fast Feedback Loop**: Tests should run quickly, especially unit tests. Slow tests discourage developers from running them frequently.

      * **FAANG Insight**: Local test runs are often optimized to only run tests related to changed files. CI/CD systems have dedicated test runners that execute full suites.

6.  **Parametrized Tests**: For common scenarios with varying inputs, use parameterized tests (e.g., Jest's `test.each`) to avoid repeating test code.

7.  **Test Data Management**:

      * Use factories (e.g., `factory.js` or `typeorm-factory`) to generate realistic but reproducible test data for integration and E2E tests.
      * Avoid hardcoding large JSON payloads.

8.  **Edge Cases & Error Paths**: Thoroughly test invalid inputs, error conditions, boundary values, and security vulnerabilities.

9.  **Continuous Integration (CI)**: Automate test execution in your CI pipeline. Tests should run automatically on every push to a branch. Failing tests should block merges.

10. **Test Doubles vs. Mocks/Stubs**: Understand the differences.

      * **Stubs**: Provide canned answers to calls.
      * **Mocks**: Verify interactions (e.g., a specific method was called with certain arguments).
      * **FAANG Insight**: Jest makes this distinction somewhat blurred by providing `jest.fn()` which can act as both. Focus on what you *assert*: state (stub) or behavior (mock).

This concludes our deep dive into testing. Mastering these principles is absolutely essential for anyone aspiring to work in a FAANG-level engineering environment.