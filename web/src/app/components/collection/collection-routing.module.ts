import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { VocabularyListComponent } from './vocabulary/list/list.component';
const routes = [
  {
    path: 'vocabulary',
    component: VocabularyListComponent,
  },
  {
    path: 'vocabulary/add',
    component: VocabularyListComponent,
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class CollectionRoutingModule {}
