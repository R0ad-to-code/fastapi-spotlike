import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'; // Ajout du module HttpClient
import { RouterModule } from '@angular/router';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AlbumsComponent } from './albums/albums.component';
import { HomeComponent } from './home/home.component';
import { ArtistsComponent } from './artists/artists.component';
import { AlbumsListComponent } from './albums/albums-list/albums-list.component';
import { AlbumDetailComponent } from './albums/album-detail/album-detail.component';
import { ArtistsListComponent } from './artists/artists-list/artists-list.component';
import { ArtistDetailComponent } from './artists/artist-detail/artist-detail.component';

import { ApiService } from './Services/api.service'; 
@NgModule({
  declarations: [
    AppComponent,
    AlbumsComponent,
    HomeComponent,
    ArtistsComponent,
    AlbumsListComponent,
    AlbumDetailComponent,
    ArtistsListComponent,
    ArtistDetailComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule
  ],
  providers: [
    ApiService, 
    provideClientHydration()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
