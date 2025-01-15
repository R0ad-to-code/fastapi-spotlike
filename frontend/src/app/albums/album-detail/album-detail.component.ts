import { Component, OnInit } from '@angular/core';
import { Song } from '../../models/song';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-album-detail',
  templateUrl: './album-detail.component.html',
  styleUrl: './album-detail.component.css'
})
export class AlbumDetailComponent implements OnInit {
  songs : Song[] =[]

  constructor (private apiService : ApiService) {}

  ngOnInit(): void {
    this.getSongs();
  }  

  getSongs(): void {
    this.apiService.getSongsOfAlbum().subscribe({
      next: (data: Song[]) => {
        this.songs = data;
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des albums :', err);
      },
    });
  }}
