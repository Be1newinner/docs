import {
  IsEmail,
  IsPhoneNumber,
  IsString,
  MinLength,
  MaxLength,
  IsEnum,
  IsOptional,
  Matches,
} from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { IsNotEmpty } from 'class-validator';

export enum Gender {
  MALE = 'MALE',
  FEMALE = 'FEMALE',
  OTHER = 'OTHER',
  PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY',
}

export class RegisterDTO {
  @ApiProperty({
    description: 'User email address',
    example: 'user@example.com',
    type: String,
  })
  @IsEmail({}, { message: 'Invalid email address format.' })
  @MaxLength(255, { message: 'Email address cannot exceed 255 characters.' })
  email: string;

  @ApiProperty({
    description: 'User password (min 8, max 32 characters, with special chars)',
    example: 'StrongP@ssw0rd!',
    type: String,
  })
  @IsString({ message: 'Password must be a string.' })
  @MinLength(8, { message: 'Password must be at least 8 characters long.' })
  @MaxLength(32, { message: 'Password must be at most 32 characters long.' })
  @Matches(
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}[\]|;:'",.<>/?`~-]).{8,32}$/,
    {
      message:
        'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.',
    },
  )
  password: string;

  @ApiProperty({
    description: 'User full name',
    example: 'John Doe',
    type: String,
  })
  @IsString({ message: 'Name must be a string.' })
  @MinLength(2, { message: 'Name must be at least 2 characters long.' })
  @MaxLength(100, { message: 'Name must be at most 100 characters long.' })
  @IsNotEmpty({ message: 'Name cannot be empty.' })
  name: string;

  @ApiProperty({
    description: 'User gender',
    enum: Gender,
    example: Gender.MALE,
    enumName: 'Gender',
    required: false,
  })
  @IsEnum(Gender, {
    message:
      'Invalid gender value. Must be one of: ' +
      Object.values(Gender).join(', ') +
      '.',
  })
  @IsOptional()
  gender?: Gender;

  @ApiProperty({
    description: 'User phone number (with country code, e.g., +15551234567)',
    example: '+12345678900',
    type: String,
  })
  @IsPhoneNumber('IN', {
    message:
      'Invalid phone number format. Must include international calling code if region is not specified.',
  })
  @IsOptional()
  phone?: string;
}
