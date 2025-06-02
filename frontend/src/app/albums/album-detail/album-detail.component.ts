import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../Services/api.service'; 
import { Song } from '../../models/song';
import { Album } from '../../models/album';
import { Artist } from '../../models/artist';

@Component({
  selector: 'app-album-detail',
  templateUrl: './album-detail.component.html',
  styleUrls: ['./album-detail.component.css']
})
export class AlbumDetailComponent implements OnInit {
  album! : Album;
  artist! : Artist;
  songs : Song[] = []
  

  constructor(private route: ActivatedRoute, private apiService: ApiService) {}

  ngOnInit(): void {
    // Récupération de l'ID depuis les paramètres de l'URL
    const albumId = this.route.snapshot.paramMap.get('id')!;
    this.apiService.getSongsOfAlbum(albumId).subscribe({
      next: (songs) => {
        this.songs = songs.songs;
        console.log(songs);
      },
      error: (err) => console.error('Error fetching songs:', err),
    });
    this.apiService.getAlbumById(albumId).subscribe({
      next: (album: any) => {
        this.album = album.album;
      },
      error: (err) => {
        console.error('Erreur lors de la récupération de l’album :', err);
      }
    });
  }
}
