import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Message, MessageService } from 'primeng/api';
import {
  EMAIL_ERROR_MESSAGE,
  EMAIL_MAX_LENGTH,
  EMAIL_MAX_LENGTH_ERROR_MESSAGE,
  EMAIL_MIN_LENGTH,
  EMAIL_MIN_LENGTH_ERROR_MESSAGE,
  EMAIL_REGEX_ERROR_MESSAGE,
  MOBILE_NUMBER_ERROR_MESSAGE,
  MOBILE_NUMBER_MAX_LENGTH,
  MOBILE_NUMBER_MAX_LENGTH_ERROR_MESSAGE,
  MOBILE_NUMBER_MIN_LENGTH,
  MOBILE_NUMBER_MIN_LENGTH_ERROR_MESSAGE,
  MOBILE_NUMBER_REGEX,
  MOBILE_NUMBER_REGEX_ERROR_MESSAGE,
  PASSWORD2_ERROR_MESSAGE,
  PASSWORD2_NOT_MATCH_ERROR_MESSAGE,
  PASSWORD_ERROR_MESSAGE,
  PASSWORD_MAX_LENGTH,
  PASSWORD_MAX_LENGTH_ERROR_MESSAGE,
  PASSWORD_MIN_LENGTH,
  PASSWORD_MIN_LENGTH_ERROR_MESSAGE,
  PASSWORD_REGEX,
  PASSWORD_REGEX_ERROR_MESSAGE,
  USERNAME_ERROR_MESSAGE,
  USERNAME_MAX_LENGTH,
  USERNAME_MAX_LENGTH_ERROR_MESSAGE,
  USERNAME_MIN_LENGTH,
  USERNAME_MIN_LENGTH_ERROR_MESSAGE,
  USERNAME_REGEX,
  USERNAME_REGEX_ERROR_MESSAGE,
} from 'src/app/models/constants';
import { AuthenticationService } from 'src/app/services/authentication.service';
@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss'],
})
export class SignupComponent implements OnInit {
  signupForm: FormGroup;
  errorMessage = '';
  constructor(
    private fb: FormBuilder,
    private authService: AuthenticationService,
    private messageService: MessageService,
    private route: Router
  ) {}

  ngOnInit(): void {
    this.signupForm = this.fb.group({
      username: [
        null,
        [
          Validators.required,
          Validators.minLength(USERNAME_MIN_LENGTH),
          Validators.maxLength(USERNAME_MAX_LENGTH),
          Validators.pattern(USERNAME_REGEX),
        ],
      ],
      email: [
        null,
        [
          Validators.required,
          Validators.email,
          Validators.minLength(EMAIL_MIN_LENGTH),
          Validators.maxLength(EMAIL_MAX_LENGTH),
        ],
      ],
      mobile_number: [
        null,
        [
          Validators.required,
          Validators.minLength(MOBILE_NUMBER_MIN_LENGTH),
          Validators.maxLength(MOBILE_NUMBER_MAX_LENGTH),
          Validators.pattern(MOBILE_NUMBER_REGEX),
        ],
      ],
      password: [
        null,
        [
          Validators.required,
          Validators.minLength(PASSWORD_MIN_LENGTH),
          Validators.maxLength(PASSWORD_MAX_LENGTH),
          Validators.pattern(PASSWORD_REGEX),
        ],
      ],
      password2: [null, [Validators.required]],
    });
  }

  setErrorMessage(field: AbstractControl, error: string, errorMessage: string) {
    this.messageService.clear();
    if (field.hasError(error)) {
      this.errorMessage = errorMessage;
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
    var username = this.signupForm.controls.username;
    return (
      this.setErrorMessage(username, 'required', USERNAME_ERROR_MESSAGE) &&
      this.setErrorMessage(username, 'minlength', USERNAME_MIN_LENGTH_ERROR_MESSAGE) &&
      this.setErrorMessage(username, 'maxlength', USERNAME_MAX_LENGTH_ERROR_MESSAGE) &&
      this.setErrorMessage(username, 'pattern', USERNAME_REGEX_ERROR_MESSAGE)
    );
  }

  validateEmail() {
    var email = this.signupForm.controls.email;
    return (
      this.setErrorMessage(email, 'required', EMAIL_ERROR_MESSAGE) &&
      this.setErrorMessage(email, 'email', EMAIL_REGEX_ERROR_MESSAGE) &&
      this.setErrorMessage(email, 'minlength', EMAIL_MIN_LENGTH_ERROR_MESSAGE) &&
      this.setErrorMessage(email, 'maxlength', EMAIL_MAX_LENGTH_ERROR_MESSAGE) &&
      this.setErrorMessage(email, 'pattern', EMAIL_REGEX_ERROR_MESSAGE)
    );
  }

  validateMobileNumber() {
    var mobile_number = this.signupForm.controls.mobile_number;
    return (
      this.setErrorMessage(mobile_number, 'required', MOBILE_NUMBER_ERROR_MESSAGE) &&
      this.setErrorMessage(mobile_number, 'minlength', MOBILE_NUMBER_MIN_LENGTH_ERROR_MESSAGE) &&
      this.setErrorMessage(mobile_number, 'maxlength', MOBILE_NUMBER_MAX_LENGTH_ERROR_MESSAGE) &&
      this.setErrorMessage(mobile_number, 'pattern', MOBILE_NUMBER_REGEX_ERROR_MESSAGE)
    );
  }

  validatePassword() {
    var password = this.signupForm.controls.password;
    return (
      this.setErrorMessage(password, 'required', PASSWORD_ERROR_MESSAGE) &&
      this.setErrorMessage(password, 'minlength', PASSWORD_MIN_LENGTH_ERROR_MESSAGE) &&
      this.setErrorMessage(password, 'maxlength', PASSWORD_MAX_LENGTH_ERROR_MESSAGE) &&
      this.setErrorMessage(password, 'pattern', PASSWORD_REGEX_ERROR_MESSAGE)
    );
  }

  validateConfirmPassword() {
    var password = this.signupForm.controls.password;
    var password2 = this.signupForm.controls.password2;
    var isNotBlank = this.setErrorMessage(password2, 'required', PASSWORD2_ERROR_MESSAGE);
    if (isNotBlank && password.value !== password2.value) {
      this.errorMessage = PASSWORD2_NOT_MATCH_ERROR_MESSAGE;
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: PASSWORD2_NOT_MATCH_ERROR_MESSAGE,
      });
      return false;
    }
    if (this.errorMessage === PASSWORD2_NOT_MATCH_ERROR_MESSAGE) {
      this.messageService.clear();
    }
    return isNotBlank;
  }

  validateData() {
    return (
      this.validateUsername() &&
      this.validateEmail() &&
      this.validateMobileNumber() &&
      this.validatePassword() &&
      this.validateConfirmPassword()
    );
  }

  onSubmit() {
    if (this.validateData()) {
      this.authService.signup(this.signupForm.value).subscribe({
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
          this.route.navigate(['/login']);
        },
      });
    }
  }
}
