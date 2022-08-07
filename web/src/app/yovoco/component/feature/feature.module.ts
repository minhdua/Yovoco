import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { FeatureRoutingModule } from './feature-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { CollectionImportComponent } from './collection-import/collection-import.component';
import { CollectionManagementComponent } from './collection-management/collection-management.component';
import { StudyComponent } from './study/study.component';
import { TestComponent } from './test/test.component';
import { ReviewComponent } from './review/review.component';
import { CollectionService } from '../../service/collection.service';


@NgModule({
  declarations: [
    DashboardComponent,
    CollectionImportComponent,
    CollectionManagementComponent,
    StudyComponent,
    TestComponent,
    ReviewComponent
  ],
  imports: [
    CommonModule,
    FeatureRoutingModule,
    CardModule,
    ButtonModule,
  ],providers: [CollectionService],
})
export class FeatureModule { }
