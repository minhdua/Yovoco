export class Token {
  access: string;
  refresh: string;
}

export class RefreshToken {
  refresh: string;
  constructor(refresh: string) {
    this.refresh = refresh;
  }
}
