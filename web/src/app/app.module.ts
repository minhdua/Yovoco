import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { HeaderComponent } from './components/header/header.component';
import { NavigationBarComponent } from './components/navigation-bar/navigation-bar.component';
import { MainComponent } from './components/main/main.component';
import { IonicModule } from '@ionic/angular';
import { AddVocabularyComponent } from './components/vocabulary/add/add.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LayoutComponent } from './components/layout/layout.component';
import { ComponentsModule } from './components/components.module';
import { HttpClientModule } from '@angular/common/http';
@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    HeaderComponent,
    NavigationBarComponent,
    MainComponent,
    AddVocabularyComponent,
    LayoutComponent,
  ],
  // https://github.com/Smruthi01/Node_Angular/tree/a9c77355ee/FrontEnd/angular/src/app/shared/modules
  imports: [
    BrowserModule,
    AppRoutingModule,
    IonicModule.forRoot(),
    FormsModule,
    ReactiveFormsModule,
    ComponentsModule,

  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
