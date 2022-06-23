import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { LayoutComponent } from './components/layout/layout.component';
import { VocabularyComponent } from './components/collection/vocabulary.component';

const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('./components/authentication/authentication.module').then(m => m.AuthenticationModule),
  },
  {
    path: 'home',
    component: HomeComponent,
  },
  {
    path: 'layout',
    component: LayoutComponent,
  },
  {
    path: 'vocabulary',
    component: VocabularyComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
