# **13. Web Sockets (Real-time Communication)**

In an e-commerce application, real-time communication can significantly enhance the user experience and internal operational efficiency. Think about features like:

  * **Order Status Updates**: Notifying users instantly when their order status changes (e.g., "Processing" to "Shipped" to "Delivered").
  * **Live Chat Support**: Enabling real-time communication between customers and support agents.
  * **Product Availability Alerts**: Notifying users when an out-of-stock item becomes available.
  * **Auction Bidding**: For an auction-based e-commerce platform, real-time bidding updates are crucial.
  * **Admin Dashboards**: Live updates on new orders, sales metrics, or inventory changes for administrators.

NestJS provides excellent support for Web Sockets using the `@nestjs/platform-socket.io` and `@nestjs/websockets` packages, leveraging the popular `Socket.IO` library.

**Why Web Sockets (Socket.IO) for FAANG-level applications?**

  * **Bidirectional Communication**: Unlike traditional HTTP where communication is client-initiated, Web Sockets allow for full-duplex communication, meaning both the client and server can send messages independently at any time.
  * **Low Latency**: Once a connection is established, data transfer is very fast, making it ideal for real-time applications.
  * **Reduced Overhead**: After the initial handshake, Web Socket frames are much smaller than HTTP requests, leading to less overhead.
  * **Automatic Reconnection**: Socket.IO handles connection drops and automatic re-connection gracefully, improving reliability.
  * **Room-based Messaging**: Socket.IO's concept of "rooms" allows for broadcasting messages to specific groups of clients, which is invaluable for features like order-specific updates or group chat.
  * **Scalability**: While Socket.IO itself provides basic pub/sub capabilities, it can be integrated with external message brokers (like Redis) for scaling across multiple instances.

**Core Components:**

1.  **Gateways (`@WebSocketGateway`)**: These are NestJS classes that act as entry points for incoming Web Socket connections and messages. They are similar to controllers but for Web Sockets.
2.  **Socket.IO Server**: NestJS abstracts the underlying `Socket.IO` server, allowing you to interact with it via decorators and methods.
3.  **Client-side Integration**: While this chapter focuses on the backend, remember that you'll need a corresponding client-side library (e.g., `socket.io-client` in a React/Angular/Vue frontend) to connect and interact with the Web Socket server.

**Installation:**

First, install the necessary packages:

```bash
npm install @nestjs/platform-socket.io @nestjs/websockets socket.io
npm install --save-dev @types/socket.io
```

  * `@nestjs/platform-socket.io`: Provides the platform adapter for Socket.IO.
  * `@nestjs/websockets`: Contains the core NestJS Web Socket functionalities and decorators.
  * `socket.io`: The underlying Socket.IO library.

-----

### **13.1 Basic Web Socket Gateway Setup**

Let's start by creating a simple gateway to handle real-time order status updates.

1.  **Create a Gateway Module**: It's good practice to encapsulate your gateway logic within a feature module.

      * **`order-status.module.ts`**:
        ```typescript
        // src/order-status/order-status.module.ts
        import { Module } from '@nestjs/common';
        import { OrderStatusGateway } from './order-status.gateway';
        import { OrderService } from '../orders/order.service'; // Assuming you have an OrderService
        import { MongooseModule } from '@nestjs/mongoose';
        import { Order, OrderSchema } from '../orders/schemas/order.schema'; // Assuming order schema

        @Module({
          imports: [
            MongooseModule.forFeature([{ name: Order.name, schema: OrderSchema }]),
          ],
          providers: [OrderStatusGateway, OrderService], // Provide the gateway and any necessary services
          exports: [OrderStatusGateway], // Export if other modules need to interact with it
        })
        export class OrderStatusModule {}
        ```
          * **FAANG Insight**: Even for real-time features, maintain modularity. The `OrderStatusGateway` needs access to the `OrderService` (and its underlying Mongoose model) to fetch and update order data, just like a regular controller.

2.  **Create the Gateway**:

      * **`order-status.gateway.ts`**:

        ```typescript
        // src/order-status/order-status.gateway.ts
        import {
          WebSocketGateway,
          SubscribeMessage,
          MessageBody,
          WebSocketServer,
          ConnectedSocket,
        } from '@nestjs/websockets';
        import { Server, Socket } from 'socket.io';
        import { Logger } from '@nestjs/common';
        import { OrderService } from '../orders/order.service'; // Assuming this service exists
        import { UpdateOrderStatusDto } from './dto/update-order-status.dto'; // Will create

        @WebSocketGateway(8000, {
          cors: {
            origin: '*', // Allow all origins for development, restrict in production
            methods: ['GET', 'POST'],
          },
        })
        export class OrderStatusGateway {
          @WebSocketServer()
          server: Server; // This property will hold the Socket.IO server instance

          private readonly logger = new Logger(OrderStatusGateway.name);

          constructor(private orderService: OrderService) {}

          // Handles client connection
          afterInit(server: Server) {
            this.logger.log('WebSocket Gateway Initialized');
          }

          handleConnection(client: Socket, ...args: any[]) {
            this.logger.log(`Client connected: ${client.id}`);
            // You can also authenticate clients here based on JWT from handshake
            // Example: const token = client.handshake.query.token;
            // if (!this.authService.validateToken(token)) client.disconnect();
          }

          handleDisconnect(client: Socket) {
            this.logger.log(`Client disconnected: ${client.id}`);
          }

          // Subscribe to a message named 'updateOrderStatus' from the client
          @SubscribeMessage('updateOrderStatus')
          async handleOrderStatusUpdate(
            @MessageBody() data: UpdateOrderStatusDto,
            @ConnectedSocket() client: Socket,
          ): Promise<void> {
            this.logger.debug(`Received updateOrderStatus message from ${client.id}: ${JSON.stringify(data)}`);

            try {
              // 1. Authenticate and Authorize (e.g., only Admin/Vendor can update status)
              // This is a crucial step for production systems!
              // For simplicity, we'll skip the full auth here, but note it's required.
              // Example: if (!client.data.user || !client.data.user.roles.includes('admin')) {
              //   client.emit('error', 'Unauthorized to update order status');
              //   return;
              // }

              // 2. Update the order in the database
              const updatedOrder = await this.orderService.updateOrderStatus(data.orderId, data.status);

              if (updatedOrder) {
                // 3. Emit the update to all clients in the specific order room
                this.server.to(`order-${data.orderId}`).emit('orderStatusUpdated', updatedOrder);
                this.logger.log(`Order ${data.orderId} status updated to ${data.status}`);
              } else {
                client.emit('error', `Order ${data.orderId} not found or status not updated.`);
              }
            } catch (error) {
              this.logger.error(`Error updating order status: ${error.message}`);
              client.emit('error', `Failed to update order status: ${error.message}`);
            }
          }

          // New method for clients to join an order room
          @SubscribeMessage('joinOrderRoom')
          handleJoinOrderRoom(
            @MessageBody() orderId: string,
            @ConnectedSocket() client: Socket,
          ): void {
            client.join(`order-${orderId}`);
            this.logger.log(`Client ${client.id} joined room: order-${orderId}`);
            client.emit('joinedRoom', `Successfully joined order-${orderId}`);
          }

          // New method for clients to leave an order room
          @SubscribeMessage('leaveOrderRoom')
          handleLeaveOrderRoom(
            @MessageBody() orderId: string,
            @ConnectedSocket() client: Socket,
          ): void {
            client.leave(`order-${orderId}`);
            this.logger.log(`Client ${client.id} left room: order-${orderId}`);
            client.emit('leftRoom', `Successfully left order-${orderId}`);
          }

          /**
           * FAANG-level consideration: Example of server-initiated message
           * This method could be called from any part of your application (e.g., from an order processing service)
           * to push updates to connected clients.
           */
          emitOrderStatusChange(orderId: string, newStatus: string, orderDetails: any) {
            this.server.to(`order-${orderId}`).emit('orderStatusUpdated', {
              orderId,
              status: newStatus,
              ...orderDetails
            });
            this.logger.log(`Emitted status change for order ${orderId} to ${newStatus}`);
          }
        }
        ```

      * **`update-order-status.dto.ts`**:

        ```typescript
        // src/order-status/dto/update-order-status.dto.ts
        import { IsString, IsNotEmpty } from 'class-validator';
        import { ApiProperty } from '@nestjs/swagger';

        export class UpdateOrderStatusDto {
          @ApiProperty({ description: 'ID of the order to update', example: '60c72b2f9f1b2c001c8e4d6a' })
          @IsString()
          @IsNotEmpty()
          orderId: string;

          @ApiProperty({ description: 'New status for the order', example: 'shipped' })
          @IsString()
          @IsNotEmpty()
          status: string; // Consider using an Enum for predefined statuses
        }
        ```

          * **FAANG Insight**:
              * **`@WebSocketGateway(8000, { cors: { ... } })`**: Defines the gateway and its port. CORS settings are crucial for frontend connectivity; always restrict `origin` in production.
              * **`@WebSocketServer() server: Server;`**: Injects the `Socket.IO` server instance, allowing you to emit events globally or to specific rooms/clients.
              * **`afterInit`, `handleConnection`, `handleDisconnect`**: These are lifecycle hooks for the gateway, useful for logging, authentication, and cleanup.
              * **`@SubscribeMessage('eventName')`**: Decorator to listen for specific messages from clients.
              * **`@MessageBody()`**: Extracts the data sent by the client.
              * **`@ConnectedSocket()`**: Provides access to the client's `Socket` instance.
              * **Room-based Messaging**: We've implemented `joinOrderRoom` and `leaveOrderRoom` methods. This allows clients interested in a specific order's updates to "subscribe" to that order's room. When the status changes, only clients in that room receive the update. This is vital for scalability as you're not broadcasting all updates to all clients.
              * **Server-initiated Messages**: The `emitOrderStatusChange` method demonstrates how your backend logic (e.g., a cron job, another microservice, or even a REST endpoint call) can trigger a real-time update to clients. This is critical for event-driven architectures.
              * **Authentication and Authorization**: **Crucially**, the comments highlight the need for authentication and authorization within the gateway. Just like REST endpoints, Web Socket messages must be secured. You'd typically authenticate the client on connection (e.g., by validating a JWT passed in the handshake query or a custom header) and then authorize specific `SubscribeMessage` handlers based on the authenticated user's roles.
              * **Error Handling**: Emitting `error` events back to the client on failures is good practice.

3.  **Integrate with Main Application**:

      * **`main.ts`**:

        ```typescript
        // src/main.ts
        import { NestFactory } from '@nestjs/core';
        import { AppModule } from './app.module';
        import { ValidationPipe } from '@nestjs/common';
        import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
        import { ConfigService } from '@nestjs/config'; // Import ConfigService

        async function bootstrap() {
          const app = await NestFactory.create(AppModule);

          // Get ConfigService to access environment variables
          const configService = app.get(ConfigService);
          const port = configService.get<number>('PORT') || 3000;
          const apiPrefix = configService.get<string>('API_PREFIX') || 'api/v1';

          // Global validation pipe
          app.useGlobalPipes(new ValidationPipe({
            transform: true, // Automatically transform payloads to DTO instances
            whitelist: true, // Remove properties not defined in DTOs
            forbidNonWhitelisted: true, // Throw error if non-whitelisted properties are present
          }));

          // Set global API prefix
          app.setGlobalPrefix(apiPrefix);

          // Configure Swagger
          const config = new DocumentBuilder()
            .setTitle('E-commerce API')
            .setDescription('FAANG-Optimized NestJS E-commerce Backend API Documentation')
            .setVersion('1.0')
            .addBearerAuth() // Add bearer token support for JWT authentication
            .build();
          const document = SwaggerModule.createDocument(app, config);
          SwaggerModule.setup('api-docs', app, document); // Setup Swagger UI at /api-docs

          // Enable CORS
          app.enableCors({
            origin: configService.get<string>('CORS_ORIGIN') || '*', // Restrict this in production
            methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
            credentials: true,
          });

          await app.listen(port);
          console.log(`Application is running on: ${await app.getUrl()}/${apiPrefix}`);
          console.log(`Swagger UI available at: ${await app.getUrl()}/api-docs`);
        }
        bootstrap();
        ```

          * **No specific changes needed in `main.ts` for Web Sockets beyond enabling CORS for your HTTP server (which also applies to WebSocket handshakes if on the same origin). NestJS automatically hooks up gateways when their modules are imported.**

      * **`app.module.ts`**:

        ```typescript
        // src/app.module.ts
        import { Module } from '@nestjs/common';
        import { ConfigModule } from '@nestjs/config';
        import { MongooseModule } from '@nestjs/mongoose';
        import { AppController } from './app.controller';
        import { AppService } from './app.service';
        import { AuthModule } from './auth/auth.module';
        import { UserModule } from './users/user.module';
        import { ProductsModule } from './products/products.module'; // Assuming products module
        import { OrdersModule } from './orders/orders.module'; // Assuming orders module
        import { OrderStatusModule } from './order-status/order-status.module'; // Import your new module

        @Module({
          imports: [
            ConfigModule.forRoot({
              isGlobal: true, // Makes ConfigModule available throughout the app
              envFilePath: '.env', // Specify your environment file
            }),
            MongooseModule.forRootAsync({
              imports: [ConfigModule],
              useFactory: async (configService) => ({
                uri: configService.get<string>('MONGODB_URI'),
                // Other Mongoose options for production:
                // useNewUrlParser: true,
                // useUnifiedTopology: true,
                // serverSelectionTimeoutMS: 5000, // Keep trying to send operations for 5 seconds
                // socketTimeoutMS: 45000, // Close sockets after 45 seconds of inactivity
              }),
              inject: [ConfigService],
            }),
            AuthModule,
            UserModule,
            ProductsModule, // Ensure this and other relevant modules are imported
            OrdersModule,
            OrderStatusModule, // <--- Add your OrderStatusModule here
          ],
          controllers: [AppController],
          providers: [AppService],
        })
        export class AppModule {}
        ```

          * **FAANG Insight**: Ensure your `OrderStatusModule` is imported into your `AppModule` (or another module that `AppModule` imports). This makes NestJS discover and initialize the gateway.

-----

### **FAANG-level Considerations for Web Sockets:**

1.  **Authentication & Authorization in Gateways**: This is paramount.

      * **On connection**: Validate a token (e.g., JWT) passed during the WebSocket handshake (e.g., in query parameters or custom headers). If invalid, disconnect the client. You can attach the authenticated user's details to the `client.data` object.
      * **On messages (`@SubscribeMessage`)**: Use a custom WebSocket guard that checks the user's roles (from `client.data.user`) against required roles for that specific message handler, similar to how `RolesGuard` works for HTTP requests. The `CanActivate` interface applies here too.
      * **FAANG Example**: A company like Amazon or Google would never allow unauthenticated WebSocket connections to critical services. They'd use mechanisms like signed URLs for temporary access or require a JWT in the connection handshake, often validated by an edge proxy or the WebSocket gateway itself.

2.  **Scaling Web Sockets with Redis Adapter**:

      * In a production environment, you'll likely run multiple instances of your NestJS application (e.g., behind a load balancer). If a client connects to instance A, and another client (or a service) wants to send a message to that client, instance B won't know about the connection on instance A.
      * **Solution**: Use the `Socket.IO Redis Adapter`. This adapter allows all instances of your application to communicate with each other via a Redis Pub/Sub mechanism. When a message is emitted from any instance, Redis broadcasts it to all other instances, ensuring the message reaches the correct client, regardless of which instance they're connected to.
      * **Installation**: `npm install @nestjs/platform-socket.io socket.io-redis redis`
      * **Usage**:
        ```typescript
        // In your main.ts or wherever you create the app
        import { createAdapter } from '@socket.io/redis-adapter';
        import { createClient } from 'redis'; // or 'ioredis'

        async function bootstrap() {
          const app = await NestFactory.create(AppModule);

          // ... other app setup ...

          const pubClient = createClient({ url: 'redis://localhost:6379' });
          const subClient = pubClient.duplicate();

          await Promise.all([pubClient.connect(), subClient.connect()]);

          const redisAdapter = createAdapter(pubClient, subClient);
          app.useWebSocketAdapter(redisAdapter); // Apply the adapter to your NestJS app

          // ... listen ...
        }
        ```
          * **FAANG Insight**: This is a non-negotiable for scalable real-time applications at FAANG. Without it, your Web Sockets won't scale beyond a single instance.

3.  **Graceful Shutdown**: Implement mechanisms to gracefully shut down Web Socket connections when the server restarts or scales down. This involves informing clients to reconnect or handling disconnection logic.

4.  **Error Handling & Logging**: Comprehensive logging within gateways is crucial. Implement `try-catch` blocks for message handlers and emit specific error messages back to clients. Use NestJS's `Logger` for consistency.

5.  **Heartbeats & Ping/Pong**: Socket.IO handles this automatically, but understanding that it sends heartbeats to keep the connection alive and detect disconnections is important.

6.  **Bandwidth & Resource Management**: For very high-throughput systems, be mindful of the number of connected clients and the frequency/size of messages. Consider throttling or batching updates if necessary.

7.  **Client-Side Reconnection Logic**: While Socket.IO clients auto-reconnect, design your frontend to handle temporary disconnections gracefully (e.g., showing a "connecting..." message, re-subscribing to rooms).

8.  **Security Best Practices**:

      * **Input Validation**: Validate all incoming WebSocket messages just like REST payloads. DTOs and `class-validator` can still be used.
      * **Rate Limiting**: Implement rate limiting on Web Socket messages to prevent denial-of-service attacks or abuse. This needs to be custom implemented within your gateway.
      * **Origin Checking**: Strictly define allowed `cors.origin` in production.
      * **Payload Size Limits**: Configure `Socket.IO` to limit message payload size to prevent memory exhaustion attacks.

This covers the critical aspects of implementing Web Sockets for real-time communication in your NestJS e-commerce backend. The key takeaway for FAANG-level systems is not just making it work, but making it **scalable, secure, and resilient**.
