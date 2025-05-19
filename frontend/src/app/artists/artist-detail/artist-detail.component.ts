import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Artist} from '../../models/artist';

@Component({
  selector: 'app-artist-detail',
  templateUrl: './artist-detail.component.html',
  styleUrls: ['./artist-detail.component.css']
})
export class ArtistDetailComponent implements OnInit {
  artist!: Artist;

  constructor(private apiService: ApiService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    const artistId = this.route.snapshot.paramMap.get('id')!;
    this.apiService.getArtistById(artistId).subscribe({
      next: (data: any) => {
        this.artist= data.artist;
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des détails de l’artiste :', err);
      }
    });
  }
}
