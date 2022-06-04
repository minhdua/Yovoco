import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { SignupComponent } from './components/signup/signup.component';
import { AddVocabularyComponent } from './components/vocabulary/add/add.component';

const routes: Routes = [
  {
    path: '',
    loadChildren: () =>
      import('./components/components.module').then(m => m.ComponentsModule),
  },
  {
    path: 'home',
    component: HomeComponent,
  },
  {
    path: 'vocabulary/add',
    component: AddVocabularyComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
