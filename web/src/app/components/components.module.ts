import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ComponentsRoutingModule } from './components-routing.module';
import { SignupComponent } from './signup/signup.component';
import { LoginComponent } from './login/login.component';
import { HttpClientModule } from '@angular/common/http';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { MessageService } from 'primeng/api';
import { MessageModule } from 'primeng/message';
import { MessagesModule } from 'primeng/messages';
import { ToastModule } from 'primeng/toast';
@NgModule({
  declarations: [SignupComponent, LoginComponent],
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    ComponentsRoutingModule,
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
export class ComponentsModule {}
