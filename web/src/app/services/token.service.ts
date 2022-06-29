import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { RefreshToken, Token } from '../models/authentication';
import { AuthenticationService } from './authentication.service';

@Injectable({
  providedIn: 'root',
})
export class TokenService {
  accessToken: string;
  constructor(private authService: AuthenticationService, private router: Router) {}

  getToken(): Token {
    return JSON.parse(localStorage.getItem('token')!);
  }

  getAccessToken(): string {
    var token = this.getToken();
    if (token === null) {
      this.router.navigate(['/login']);
    }

    // var refresh = token.refresh;
    // this.authService.refreshToken(new RefreshToken(refresh)).subscribe({
    //   next: data => {
    //     var newToken = data['results'];
    //     this.accessToken = newToken['access'];
    //     localStorage.setItem('token', JSON.stringify(newToken));
    //   },
    //   error: error => {
    //     this.router.navigate(['/login']);
    //     return '';
    //   },
    // });
    return token.access;
  }
}
