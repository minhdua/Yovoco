import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { FeatureRoutingModule } from './feature-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { DropdownModule } from 'primeng/dropdown';
import { CollectionImportComponent } from './collection-import/collection-import.component';
import { CollectionManagementComponent } from './collection-management/collection-management.component';
import { StudyComponent } from './study/study.component';
import { TestComponent } from './test/test.component';
import { ReviewComponent } from './review/review.component';
import { TreeSelectModule } from 'primeng/treeselect';
import { TableModule } from 'primeng/table';
import { DialogModule } from 'primeng/dialog';
import { TreeModule } from 'primeng/tree';
import { TreeTableModule } from 'primeng/treetable';
import { TreeNodeService } from './service/treenode.service';
import { HttpClientModule } from '@angular/common/http';
import { APP_BASE_HREF } from '@angular/common';
import { CollectionService } from './service/collection.service';
import { AngularFireModule } from '@angular/fire/compat';
import { AngularFirestoreModule } from '@angular/fire/compat/firestore';
import { environment } from 'src/environments/environment';
import { ContextMenuModule } from 'primeng/contextmenu';
import { FormsModule } from '@angular/forms';
import { ToastModule } from 'primeng/toast';
import { MessagesModule } from 'primeng/messages';
import { MessageModule } from 'primeng/message';
import { MessageService } from 'primeng/api';
import { MessagesService } from './service/message.service';
import { ToolbarModule } from 'primeng/toolbar';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { ChipsModule } from 'primeng/chips';
@NgModule({
	declarations: [DashboardComponent, CollectionImportComponent, CollectionManagementComponent, StudyComponent, TestComponent, ReviewComponent],
	imports: [
		CommonModule,
		FeatureRoutingModule,
		CardModule,
		DropdownModule,
		ButtonModule,
		TreeSelectModule,
		TableModule,
		DialogModule,
		TreeTableModule,
		HttpClientModule,
		ContextMenuModule,
		AngularFireModule.initializeApp(environment.firebase),
		AngularFirestoreModule,
		FormsModule,
		ToastModule,
		MessagesModule,
		MessageModule,
		ToolbarModule,
		InputTextareaModule,
		ChipsModule,
	],
	providers: [{ provide: APP_BASE_HREF, useValue: '/' }, CollectionService, MessagesService, MessageService, TreeNodeService],
})
export class FeatureModule {}
