import { HttpClient } from '@angular/common/http';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthenticationService } from 'src/app/services/authentication.service';


// https://github.com/yash2880/hari/blob/ebe3e9a1a7/src/app/components/pages/signup/signup.component.ts
@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss'],
})
export class SignupComponent implements OnInit {

  hasError: boolean = false;
  errors: any = {};
  isLoggedIn: boolean = false;
  passLength: number = 0;
  checkPassword: boolean = true;
  checkEmail: boolean = false;
  emailFailed:boolean = false;
  waitingMsg:boolean = false;
  // alertMsg: boolean = false;
  constructor(private http: HttpClient,private authService: AuthenticationService, private route: Router) {

  }

  ngOnInit(): void {
  }

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
    'mobile_number': new FormControl(null, [ 
      Validators.required, 
      Validators.pattern('^[0-9]{10}$'), 
      Validators.minLength(10), Validators.maxLength(10)
    ]),
    password: new FormControl(null, [Validators.required,Validators.pattern('^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$')]),
    password2: new FormControl(null, [Validators.required,Validators.pattern('^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$')]),
  });

  keyPress(event: any) {
    const pattern = /[0-9]/;
    let inputChar = String.fromCharCode(event.charCode);
    if (event.keyCode != 8 && !pattern.test(inputChar)) {
      event.preventDefault();
    }
  }

  async onSubmit() {
    this.authService.signup(this.signupForm.value).subscribe({
      next: (data) => {
        console.log(data);
        this.waitingMsg = true;
        setTimeout(() => {
          this.waitingMsg = false;
          this.route.navigate(['/login']);
        }
        , 3000);
      },
      error: (err) => {
        this.hasError = true;
        this.errors = err.error;
        if (err.status == 400) {
          console.log(typeof(this.errors),this.errors);
        }
      }
    });
  }
}
