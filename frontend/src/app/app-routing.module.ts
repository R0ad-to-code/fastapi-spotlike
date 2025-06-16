import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { AlbumsComponent } from './albums/albums.component';
import { ArtistsComponent } from './artists/artists.component';
import { AlbumDetailComponent } from './albums/album-detail/album-detail.component';
import { ArtistDetailComponent } from './artists/artist-detail/artist-detail.component';
import { ArtistsListComponent } from './artists/artists-list/artists-list.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { AuthGuard } from './guards/auth.guard';
import { AdminComponent } from './admin/admin.component';

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'home', component: HomeComponent},
  {path: 'albums', component: AlbumsComponent},
  {path: 'albums/:id', component: AlbumDetailComponent},
  { path: 'artists', component: ArtistsComponent },
  { path: 'artists/:id', component: ArtistDetailComponent},
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'admin', component: AdminComponent, canActivate: [AuthGuard] }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }