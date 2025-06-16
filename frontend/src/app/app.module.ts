import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AlbumsComponent } from './albums/albums.component';
import { HomeComponent } from './home/home.component';
import { ArtistsComponent } from './artists/artists.component';
import { AlbumsListComponent } from './albums/albums-list/albums-list.component';
import { AlbumDetailComponent } from './albums/album-detail/album-detail.component';
import { ArtistsListComponent } from './artists/artists-list/artists-list.component';
import { ArtistDetailComponent } from './artists/artist-detail/artist-detail.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';

import { ApiService } from './Services/api.service';
import { AuthService } from './Services/auth.service';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { AdminComponent } from './admin/admin.component';
@NgModule({
  declarations: [
    AppComponent,
    AlbumsComponent,
    HomeComponent,
    ArtistsComponent,
    AlbumsListComponent,
    AlbumDetailComponent,
    ArtistsListComponent,
    ArtistDetailComponent,
    LoginComponent,
    RegisterComponent,
    AdminComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    ApiService,
    AuthService,
    provideClientHydration(),
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
