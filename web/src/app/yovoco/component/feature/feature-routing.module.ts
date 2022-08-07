import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CollectionImportComponent } from './collection-import/collection-import.component';
import { CollectionManagementComponent } from './collection-management/collection-management.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ReviewComponent } from './review/review.component';
import { StudyComponent } from './study/study.component';
import { TestComponent } from './test/test.component';

const routes: Routes = [
    { path: '', component: DashboardComponent },
    { path: 'collection-management', component: CollectionManagementComponent },
    { path: 'collection-import', component: CollectionImportComponent },
    { path: 'study', component: StudyComponent },
    { path: 'test', component: TestComponent },
    { path: 'review', component: ReviewComponent },
    { path: '**', component: DashboardComponent },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class FeatureRoutingModule {}
