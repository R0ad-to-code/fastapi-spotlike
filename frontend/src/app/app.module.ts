import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AlbumsComponent } from './albums/albums.component';
import { HomeComponent } from './home/home.component';
import { ArtistsComponent } from './artists/artists.component';
import { AlbumsListComponent } from './albums/albums-list/albums-list.component';
import { AlbumDetailComponent } from './albums/album-detail/album-detail.component';

@NgModule({
  declarations: [
    AppComponent,
    AlbumsComponent,
    HomeComponent,
    ArtistsComponent,
    AlbumsListComponent,
    AlbumDetailComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [
    provideClientHydration()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
