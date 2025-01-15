// albums.component.ts
import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Album } from '../models/album';

@Component({
  selector: 'app-albums',
  templateUrl: './albums.component.html',
  styleUrls: ['./albums.component.css'],
})
export class AlbumsComponent implements OnInit {
  albums: Album[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.getAlbums();
  }

  getAlbums(): void {
    this.apiService.getAlbumsFromAPi().subscribe({
      next: (data: Album[]) => {
        this.albums = data;
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des albums :', err);
      },
    });
  }
}
