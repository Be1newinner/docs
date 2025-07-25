import { Injectable, OnApplicationBootstrap } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Injectable()
export class SeedService implements OnApplicationBootstrap {
  constructor(private readonly Prisma: PrismaService) {}

  async onApplicationBootstrap() {
    await this.seedRoles();
  }

  private async seedRoles() {
    const roles = ['USER', 'ADMIN'];
    return await Promise.all(
      roles.map((role) =>
        this.Prisma.role.upsert({
          where: { name: role },
          update: {},
          create: {
            name: role,
            description: `${role} role`,
          },
        }),
      ),
    );
  }
}
