import { Role } from './role';

export class UserRole {
  role: Role;

  constructor(){
      this.role = Role.Guest;
  }
}

export interface User {
  id: string | undefined;
  name: string;
  email: string;
  password: string;
  role: Role;
}
