import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { environment } from 'src/environments/environment';

const BACKEND_URL = environment.apiUrl + '/user/';

// https://github.com/yash2880/hari/blob/ebe3e9a1a7/src/app/components/pages/signup/signup.component.ts
@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss'],
})
export class SignupComponent implements OnInit {
  isLoggedin: boolean = false;
  passLength: number = 0;
  checkPassword: boolean = true;
  checkEmail: boolean = false;
  emailFailed: boolean = false;
  waitingMsg: boolean = false;
  constructor() {}

  ngOnInit() {}

  signupForm = new FormGroup({
    username: new FormControl(null, [
      Validators.required,
      Validators.minLength(4),
      Validators.maxLength(15),
      Validators.pattern('^[a-zA-Z]{1,}[a-zA-Z0-9_]*$'),
    ]),
    email: new FormControl(null, [
      Validators.required,
      Validators.email,
      Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$'),
    ]),
    password: new FormControl(null, [
      Validators.required,
      Validators.pattern(
        '^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$'
      ),
    ]),
    reenter: new FormControl(null, [
      Validators.required,
      Validators.pattern(
        '^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$'
      ),
    ]),
  });

  async onSubmit() {
    if (this.signupForm.value.password != this.signupForm.value.reenter) {
      // this.alertMsg = false;
      this.checkPassword = false;
      setTimeout(() => {
        this.checkPassword = true;
      }, 3000);
    } else {
      var checkUserExists: any = await this.http
        .get(BACKEND_URL + 'checkSignUp/' + this.signupForm.value.email)
        .toPromise();

      if (checkUserExists.result == 'true') {
        this.checkEmail = true;
        setTimeout(() => {
          this.checkEmail = false;
        }, 5000);
        this.signupForm.reset();
      } else if (checkUserExists.result == 'false') {
        this.checkingUserData();
      }
    }
  }
}
