import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { SignupComponent } from './signup/signup.component';
import { HttpClientModule } from '@angular/common/http';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { MessageService } from 'primeng/api';
import { MessageModule } from 'primeng/message';
import { MessagesModule } from 'primeng/messages';
import { ToastModule } from 'primeng/toast';
import { SigninComponent } from './signin/signin.component';
import { AuthenticationRoutingModule } from './authentication-routing.module';
@NgModule({
  declarations: [SignupComponent, SigninComponent],
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    AuthenticationRoutingModule,
    FormsModule,
    HttpClientModule,
    CardModule,
    ButtonModule,
    InputTextModule,
    MessageModule,
    MessagesModule,
    ToastModule,
  ],
  exports: [],
  providers: [MessageService],
})
export class AuthenticationModule {}
