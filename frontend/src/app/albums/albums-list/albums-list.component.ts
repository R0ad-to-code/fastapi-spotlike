import { Component, OnInit, OnDestroy } from '@angular/core';
import { Album } from '../../models/album';
import { Artist } from '../../models/artist';
import { ApiService } from '../../Services/api.service'; 
import { Subscription, forkJoin } from 'rxjs';

// Interface pour étendre l'Album avec l'artiste complet
interface AlbumWithArtist extends Album {
  artist?: Artist;
}

@Component({
  selector: 'app-albums-list',
  templateUrl: './albums-list.component.html',
  styleUrl: './albums-list.component.css'
})
export class AlbumsListComponent implements OnInit, OnDestroy {
  albums: AlbumWithArtist[] = [];
  private subscriptions: Subscription[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    // Abonnement direct au BehaviorSubject
    const albumSub = this.apiService.albumsSubject.subscribe({
      next: (albums) => {
        this.albums = albums;
        this.loadArtistsForAlbums();
      },
      error: (err) => console.error('Error fetching albums:', err),
    });
    
    this.subscriptions.push(albumSub);
    this.apiService.fetchAlbums();
  }
  
  loadArtistsForAlbums(): void {
    this.albums.forEach(album => {
      if (album.artist_id) {
        const artistSub = this.apiService.getArtistById(album.artist_id).subscribe({
          next: (artist) => {
            album.artist = artist;
          },
          error: (err) => console.error(`Error fetching artist for album ${album.title}:`, err)
        });
        
        this.subscriptions.push(artistSub);
      }
    });
  }

  ngOnDestroy(): void {
    // Désabonnement pour éviter les fuites de mémoire
    this.subscriptions.forEach(sub => {
      if (sub) {
        sub.unsubscribe();
      }
    });
  }
}