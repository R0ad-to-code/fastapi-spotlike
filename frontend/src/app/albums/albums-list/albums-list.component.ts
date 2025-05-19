import { Component, OnInit, OnDestroy } from '@angular/core';
import { Album } from '../../models/album';
import { ApiService } from '../../services/api.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-albums-list',
  templateUrl: './albums-list.component.html',
  styleUrl: './albums-list.component.css'
})
export class AlbumsListComponent implements OnInit, OnDestroy {
  albums: Album[] = [];
  private subscription!: Subscription;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    // Abonnement direct au BehaviorSubject
    this.subscription = this.apiService.albumsSubject.subscribe({
      next: (albums) => {
        this.albums = albums;
      },
      error: (err) => console.error('Error fetching albums:', err),
    });
    
    this.apiService.fetchAlbums();
  }

  ngOnDestroy(): void {
    // Désabonnement pour éviter les fuites de mémoire
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}