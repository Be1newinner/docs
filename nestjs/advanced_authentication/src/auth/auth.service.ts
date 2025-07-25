// import { Prisma } from 'generated/prisma';
import { UsersService } from './../users/users.service';
import { Injectable } from '@nestjs/common';
import { hash, compare } from 'bcrypt';
import { RegisterDTO } from './dto/register.dto';
import { LoginDTO } from './dto/login.dto';

@Injectable()
export class AuthService {
  constructor(private UsersService: UsersService) {}

  async register(registerDTO: RegisterDTO) {
    const { email, password, name, gender, phone } = registerDTO;
    // console.log(registerDTO);
    const existingUser = await this.UsersService.findUserByEmail(email);
    if (existingUser) throw new Error('User already exists');

    const hashedPassword = await hash(password, 10);
    const newUser = await this.UsersService.createUser({
      email,
      password: hashedPassword,
      name,
      gender,
      phone,
    });
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { password: _, ...newUserWithoutPassword } = newUser;
    return newUserWithoutPassword;
  }

  async login(loginDTO: LoginDTO) {
    const { email, password } = loginDTO;
    const user = await this.UsersService.findUserByEmail(email);
    if (!user) return null;
    const isValid = await compare(password, user?.password);

    if (isValid)
      return {
        status: 'success',
        message: 'user retrieved success!',
        code: 200,
        applicationCode: 2000,
        data: user,
      };
    else
      return {
        status: 'fail',
        message: 'unauthorized user!',
        code: 401,
        applicationCode: 4011,
        data: null,
      };
  }
}
