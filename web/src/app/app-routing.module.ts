import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { LayoutComponent } from './components/layout/layout.component';

const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('./components/authentication/authentication.module').then(m => m.AuthenticationModule),
  },
  {
    path: 'collection',
    loadChildren: () => import('./components/collection/collection.module').then(m => m.CollectionModule),
  },
  {
    path: 'home',
    component: HomeComponent,
  },
  {
    path: 'layout',
    component: LayoutComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
