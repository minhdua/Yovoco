import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './yovoco/component/pages/home/home.component';
import { NotFoundComponent } from './yovoco/component/pages/not-found/not-found.component';
import { FeatureModule } from './yovoco/component/feature/feature.module';
import { FormsModule } from '@angular/forms';
import { ToastrModule } from 'ngx-toastr';
@NgModule({
	declarations: [
		AppComponent,
		// AboutComponent,
		HomeComponent,
		NotFoundComponent,
	],
	imports: [
		BrowserModule,
		BrowserAnimationsModule,
		AppRoutingModule,
		FormsModule,
		ToastrModule.forRoot(),
		// provideFirebaseApp(() => initializeApp(environment.firebase)),
		// provideFirestore(() => getFirestore()),
		// provideDatabase(() => getDatabase()),
		FeatureModule,
	],
	providers: [],
	bootstrap: [AppComponent],
})
export class AppModule {}
