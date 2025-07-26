import { Injectable } from '@nestjs/common';
import { Gender } from 'src/auth/dto/register.dto';
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
    gender?: Gender;
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
            name: 'user',
          },
        },
      },
    });
  }
}
