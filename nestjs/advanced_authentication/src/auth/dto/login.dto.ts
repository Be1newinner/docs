import { ApiProperty } from '@nestjs/swagger';
import {
  IsEmail,
  IsString,
  Matches,
  MaxLength,
  MinLength,
} from 'class-validator';

export class LoginDTO {
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
}
