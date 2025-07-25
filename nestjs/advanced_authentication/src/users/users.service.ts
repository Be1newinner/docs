import { Injectable } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  async findUserByEmail(email: string) {
    return this.prisma.user.findUnique({
      where: {
        email,
      },
    });
  }

  async createUser(data: { email: string; password: string }) {
    return this.prisma.user.create({
      data: {
        email: data.email,
        password: data.password,
        roles: {
          connect: {
            name: 'user',
          },
        },
      },
    });
  }
}
