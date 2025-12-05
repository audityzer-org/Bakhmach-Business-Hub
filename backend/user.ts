import bcrypt from 'bcrypt';

export interface IUser {
  id: string;
  email: string;
  username: string;
  password_hash: string;
  first_name?: string;
  last_name?: string;
  role: string;
  status: string;
  created_at: Date;
  updated_at: Date;
  last_login?: Date;
}

export class User {
  id: string;
  email: string;
  username: string;
  password_hash: string;
  first_name?: string;
  last_name?: string;
  role: string = 'user';
  status: string = 'active';
  created_at: Date;
  updated_at: Date;
  last_login?: Date;

  constructor(data: Partial<IUser>) {
    this.id = data.id || '';
    this.email = data.email || '';
    this.username = data.username || '';
    this.password_hash = data.password_hash || '';
    this.first_name = data.first_name;
    this.last_name = data.last_name;
    this.role = data.role || 'user';
    this.status = data.status || 'active';
    this.created_at = data.created_at || new Date();
    this.updated_at = data.updated_at || new Date();
    this.last_login = data.last_login;
  }

  static async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 10);
  }

  async verifyPassword(password: string): Promise<boolean> {
    return bcrypt.compare(password, this.password_hash);
  }

  getPublicData(): Omit<IUser, 'password_hash'> {
    return {
      id: this.id,
      email: this.email,
      username: this.username,
      first_name: this.first_name,
      last_name: this.last_name,
      role: this.role,
      status: this.status,
      created_at: this.created_at,
      updated_at: this.updated_at,
      last_login: this.last_login
    };
  }

  toJSON(): Omit<IUser, 'password_hash'> {
    return this.getPublicData();
  }
}

export default User;
