import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Song } from '../../models/song';
import { Subscription } from 'rxjs';
import { Album } from '../../models/album';

@Component({
  selector: 'app-album-detail',
  templateUrl: './album-detail.component.html',
  styleUrls: ['./album-detail.component.css']
})
export class AlbumDetailComponent implements OnInit {
  albumId!: string;
  songs : Song[] = []
  private subscription!: Subscription;
  @Input album : Album;

  constructor(private route: ActivatedRoute, private apiService: ApiService) {}

  ngOnInit(): void {
    // Récupération de l'ID depuis les paramètres de l'URL
    this.albumId = this.route.snapshot.paramMap.get('id')!;
    this.subscription = this.apiService.albumSongsSubject.subscribe({
      next: (songs) => {
        this.songs = songs;
      },
      error: (err) => console.error('Error fetching songs:', err),
    });
    
    this.apiService.getSongsOfAlbum(this.albumId); 
  }
}
