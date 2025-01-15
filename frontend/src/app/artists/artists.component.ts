import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Artist } from '../models/artist';

@Component({
  selector: 'app-artists',
  templateUrl: './artists.component.html',
  styleUrls: ['./artists.component.css']
})
export class ArtistsComponent implements OnInit {
  artists: Artist[] = [];

  constructor(private apiService: ApiService) {
    console.log('ApiService injecté :', this.apiService);
  }

  ngOnInit(): void {
    this.loadArtists();
  }

  loadArtists(): void {
    this.apiService.getArtists().subscribe({
      next: (data: Artist[]) => {
        this.artists = data;
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des artistes :', err);
      }
    });
  }
}
