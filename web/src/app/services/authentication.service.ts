import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

const BACKEND_URL = environment.apiUrl + '/user/';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  constructor(private http: HttpClient) {}

  register(signupForm: any) {
    return this.http.post(BACKEND_URL + 'registration/', signupForm);
  }

  login(signinForm: any) {
    return this.http.post(BACKEND_URL + 'login/', signinForm);
  }

  refreshToken(refreshToken: any) {
    return this.http.post(BACKEND_URL + 'refresh/', refreshToken);
  }

  logout() {
    localStorage.removeItem('token');
  }
}
