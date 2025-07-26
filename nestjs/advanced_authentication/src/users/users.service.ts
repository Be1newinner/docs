import { Injectable } from '@nestjs/common';
import { GenderType, RoleType } from 'generated/prisma';
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

  async createUser(data: {
    email: string;
    password: string;
    name?: string;
    gender?: GenderType;
    phone?: string;
  }) {
    return this.prisma.user.create({
      data: {
        email: data.email,
        password: data.password,
        name: data?.name,
        gender: data?.gender,
        phone: data?.phone,
        role: {
          connect: {
            name: RoleType.USER,
          },
        },
      },
    });
  }
}
