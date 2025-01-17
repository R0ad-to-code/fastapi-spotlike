import { Component, OnInit, OnDestroy } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Artist } from '../../models/artist';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-artists-list',
  templateUrl: './artists-list.component.html',
  styleUrls: ['./artists-list.component.css']
})
export class ArtistsListComponent implements OnInit, OnDestroy {
  artists: Artist[] = [];
  private subscription!: Subscription;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    // Abonnement direct au BehaviorSubject
    this.subscription = this.apiService.artistsSubject.subscribe({
      next: (artists) => {
        this.artists = artists;
      },
      error: (err) => console.error('Error fetching artists:', err),
    });
    
    this.apiService.fetchArtists();
  }
  
  ngOnDestroy(): void {
    // Désabonnement pour éviter les fuites de mémoire
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}
