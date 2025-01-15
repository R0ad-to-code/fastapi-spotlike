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
    this.getAlbumsfromBack();
  }

  getAlbumsfromBack(): void {
    this.apiService.getAlbums().subscribe(data => (this.albums = data));
  }
}
