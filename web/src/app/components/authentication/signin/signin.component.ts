import { Token } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { PASSWORD_ERROR_MESSAGE, USERNAME_ERROR_MESSAGE } from 'src/app/models/constants';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { LocalStorageService } from 'src/app/services/localstorage.service';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.scss'],
})
export class SigninComponent implements OnInit {
  signinForm: FormGroup;
  token: Token;

  constructor(
    private fb: FormBuilder,
    private authService: AuthenticationService,
    private localStorage: LocalStorageService,
    private messageService: MessageService,
    private route: Router
  ) {}

  ngOnInit(): void {
    this.signinForm = this.fb.group({
      username: [null, [Validators.required]],
      password: [null, [Validators.required]],
    });
  }

  setErrorMessage(field: AbstractControl, error: string, errorMessage: string) {
    this.messageService.clear();
    if (field.hasError(error)) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: errorMessage,
      });
      return false;
    }
    return true;
  }

  validateUsername() {
    var username = this.signinForm.controls.username;
    return this.setErrorMessage(username, 'required', USERNAME_ERROR_MESSAGE);
  }

  validatePassword() {
    var password = this.signinForm.controls.password;
    return this.setErrorMessage(password, 'required', PASSWORD_ERROR_MESSAGE);
  }

  validateData() {
    return this.validateUsername() && this.validatePassword();
  }

  onSubmit(): void {
    if (this.validateData()) {
      this.authService.login(this.signinForm.value).subscribe({
        next: data => {
          this.token = data['results'];
          this.localStorage.setItem('token', this.token);
        },
        error: err => {
          for (const k in err.error) {
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: err.error[k],
            });
          }
        },
        complete: () => {
          this.route.navigate(['collection/vocabulary']);
        },
      });
    }
  }
}
