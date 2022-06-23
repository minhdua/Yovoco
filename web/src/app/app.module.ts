import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { HeaderComponent } from './components/header/header.component';
import { NavigationBarComponent } from './components/navigation-bar/navigation-bar.component';
import { MainComponent } from './components/main/main.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LayoutComponent } from './components/layout/layout.component';
import { AuthenticationModule } from './components/authentication/authentication.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { PanelMenuModule } from 'primeng/panelmenu';
import { TableModule } from 'primeng/table';
import { CollectionModule } from './components/collection/collection.module';
@NgModule({
  declarations: [AppComponent, HomeComponent, HeaderComponent, NavigationBarComponent, MainComponent, LayoutComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    AuthenticationModule,
    CollectionModule,
    BrowserAnimationsModule,
    PanelMenuModule,
    TableModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
