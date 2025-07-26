import { Injectable, OnApplicationBootstrap } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import { RoleType } from 'generated/prisma';

@Injectable()
export class SeedService implements OnApplicationBootstrap {
  constructor(private readonly Prisma: PrismaService) {}

  async onApplicationBootstrap() {
    await this.seedRoles();
  }

  private async seedRoles() {
    return await Promise.all(
      Object.keys(RoleType).map((role: RoleType) => {
        return this.Prisma.role.upsert({
          where: { name: role },
          update: {},
          create: {
            name: role,
          },
        });
      }),
    );
  }
}
