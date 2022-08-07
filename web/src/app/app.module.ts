import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
import { getFirestore, provideFirestore } from '@angular/fire/firestore';
import { provideDatabase, getDatabase } from '@angular/fire/database';
import { environment } from 'src/environments/environment';
import { AboutComponent } from './yovoco/component/pages/about/about.component';
import { HomeComponent } from './yovoco/component/pages/home/home.component';
import { NotFoundComponent } from './yovoco/component/pages/not-found/not-found.component';
import { FeatureModule } from './yovoco/component/feature/feature.module';
@NgModule({
    declarations: [
        AppComponent,
        // AboutComponent,
        // HomeComponent,
        // NotFoundComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        provideFirebaseApp(() => initializeApp(environment.firebase)),
        provideFirestore(() => getFirestore()),
        provideDatabase(() => getDatabase()),
        FeatureModule,
    ],
    providers: [],
    bootstrap: [AppComponent],
})
export class AppModule {}
