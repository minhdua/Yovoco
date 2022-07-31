import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { VocabularyAddComponent } from './vocabulary/add/add.component';
import { VocabularyListComponent } from './vocabulary/list/list.component';
const routes = [
  {
    path: 'vocabulary',
    component: VocabularyListComponent,
  },
  {
    path: 'vocabulary/add',
    component: VocabularyAddComponent,
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class CollectionRoutingModule {}
