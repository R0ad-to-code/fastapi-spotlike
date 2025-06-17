import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../Services/auth.service';
import { ApiService } from '../Services/api.service';
import { Artist } from '../models/artist';
import { Album } from '../models/album';
import { Song } from '../models/song';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  activeTab = 'artists'; // Onglet actif par défaut
  
  // Listes de données
  artists: Artist[] = [];
  albums: Album[] = [];
  songs: Song[] = [];
  
  // Formulaires
  artistForm: FormGroup;
  albumForm: FormGroup;
  songForm: FormGroup;
  
  // États des formulaires
  showArtistForm = false;
  showAlbumForm = false;
  showSongForm = false;
  
  // Gestion des notifications
  notification = {
    show: false,
    message: '',
    type: ''
  };
  
  // État d'édition
  editingArtistId: string | null = null;
  editingAlbumId: string | null = null;
  editingSongId: string | null = null;
  
  // Prévisualisations d'images
  artistImagePreview: string | null = null;
  albumImagePreview: string | null = null;

  constructor(
    private authService: AuthService, 
    private router: Router,
    private apiService: ApiService,
    private fb: FormBuilder
  ) {
    // Initialisation des formulaires
    this.artistForm = this.fb.group({
      name: ['', Validators.required],
      biography: ['', Validators.required],
      avatar: ['', Validators.required]
    });
    
    this.albumForm = this.fb.group({
      title: ['', Validators.required],
      cover_image: ['', Validators.required],
      release_date: ['', Validators.required],
      artist_id: ['', Validators.required]
    });
    
    this.songForm = this.fb.group({
      title: ['', Validators.required],
      duration: [0, [Validators.required, Validators.min(1)]],
      artist_id: ['', Validators.required],
      album_id: ['', Validators.required],
      genres: [''] // Ce sera transformé en tableau avant envoi
    });
  }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    // Chargement des artistes
    this.apiService.getArtists().subscribe({
      next: (response: any) => {
        // Vérifier la structure de la réponse API
        this.artists = Array.isArray(response) 
          ? response 
          : (response && Array.isArray(response.artists)) 
            ? response.artists 
            : [];
      },
      error: (err) => this.showNotification('Erreur lors du chargement des artistes', 'error')
    });

    // Chargement des albums
    this.apiService.getAlbums().subscribe({
      next: (response: any) => {
        // Vérifier la structure de la réponse API
        this.albums = Array.isArray(response) 
          ? response 
          : (response && Array.isArray(response.albums)) 
            ? response.albums 
            : [];
      },
      error: (err) => this.showNotification('Erreur lors du chargement des albums', 'error')
    });

    // Chargement des chansons
    this.apiService.getAllSongs().subscribe({
      next: (response: any) => {
        // Vérifier la structure de la réponse API
        this.songs = Array.isArray(response) 
          ? response 
          : (response && Array.isArray(response.songs)) 
            ? response.songs 
            : [];
      },
      error: (err) => this.showNotification('Erreur lors du chargement des chansons', 'error')
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  setActiveTab(tab: string) {
    this.activeTab = tab;
  }
  
  // --- GESTION DES ARTISTES ---
  toggleArtistForm(): void {
    this.showArtistForm = !this.showArtistForm;
    if (!this.showArtistForm) {
      this.resetArtistForm();
    }
  }
  
  resetArtistForm(): void {
    this.artistForm.reset();
    this.editingArtistId = null;
    this.artistImagePreview = null;
  }
  
  onArtistImageChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length) {
      const file = input.files[0];
      // Pour une application réelle, vous implémenteriez un upload de fichier
      // Ici, nous simulons juste avec une URL d'image pour la prévisualisation
      this.artistForm.patchValue({
        avatar: file.name // Dans une application réelle, ce serait l'URL retournée par le serveur
      });
      
      // Prévisualisation de l'image
      const reader = new FileReader();
      reader.onload = () => {
        this.artistImagePreview = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  }
  
  saveArtist(): void {
    if (this.artistForm.invalid) {
      this.artistForm.markAllAsTouched();
      return;
    }
    
    const artistData = this.artistForm.value;
    
    if (this.editingArtistId) {
      // Mode édition
      this.apiService.updateArtist(this.editingArtistId, artistData).subscribe({
        next: () => {
          this.showNotification('Artiste mis à jour avec succès', 'success');
          this.loadData();
          this.toggleArtistForm();
        },
        error: (err) => this.showNotification('Erreur lors de la mise à jour de l\'artiste', 'error')
      });
    } else {
      // Mode création
      this.apiService.createArtist(artistData).subscribe({
        next: () => {
          this.showNotification('Artiste créé avec succès', 'success');
          this.loadData();
          this.toggleArtistForm();
        },
        error: (err) => this.showNotification('Erreur lors de la création de l\'artiste', 'error')
      });
    }
  }
  
  editArtist(artist: Artist): void {
    this.editingArtistId = artist.id;
    this.artistForm.patchValue({
      name: artist.name,
      biography: artist.biography,
      avatar: artist.avatar
    });
    this.artistImagePreview = artist.avatar;
    this.showArtistForm = true;
  }
  
  deleteArtist(id: string): void {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet artiste ?')) {
      this.apiService.deleteArtist(id).subscribe({
        next: () => {
          this.showNotification('Artiste supprimé avec succès', 'success');
          this.loadData();
        },
        error: (err) => this.showNotification('Erreur lors de la suppression de l\'artiste', 'error')
      });
    }
  }
  
  // --- GESTION DES ALBUMS ---
  toggleAlbumForm(): void {
    this.showAlbumForm = !this.showAlbumForm;
    if (!this.showAlbumForm) {
      this.resetAlbumForm();
    }
  }
  
  resetAlbumForm(): void {
    this.albumForm.reset();
    this.editingAlbumId = null;
    this.albumImagePreview = null;
  }
  
  onAlbumImageChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length) {
      const file = input.files[0];
      // Pour une application réelle, vous implémenteriez un upload de fichier
      this.albumForm.patchValue({
        cover_image: file.name // Dans une application réelle, ce serait l'URL retournée par le serveur
      });
      
      // Prévisualisation de l'image
      const reader = new FileReader();
      reader.onload = () => {
        this.albumImagePreview = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  }
  
  saveAlbum(): void {
    if (this.albumForm.invalid) {
      this.albumForm.markAllAsTouched();
      return;
    }
    
    const albumData = this.albumForm.value;
    
    if (this.editingAlbumId) {
      // Mode édition
      this.apiService.updateAlbum(this.editingAlbumId, albumData).subscribe({
        next: () => {
          this.showNotification('Album mis à jour avec succès', 'success');
          this.loadData();
          this.toggleAlbumForm();
        },
        error: (err) => this.showNotification('Erreur lors de la mise à jour de l\'album', 'error')
      });
    } else {
      // Mode création
      this.apiService.createAlbum(albumData).subscribe({
        next: () => {
          this.showNotification('Album créé avec succès', 'success');
          this.loadData();
          this.toggleAlbumForm();
        },
        error: (err) => this.showNotification('Erreur lors de la création de l\'album', 'error')
      });
    }
  }
  
  editAlbum(album: Album): void {
    this.editingAlbumId = album.id.toString();
    this.albumForm.patchValue({
      title: album.title,
      cover_image: album.cover_image,
      release_date: album.release_date,
      artist_id: album.artist_id
    });
    this.albumImagePreview = album.cover_image;
    this.showAlbumForm = true;
  }
  
  deleteAlbum(id: number): void {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet album ?')) {
      this.apiService.deleteAlbum(id.toString()).subscribe({
        next: () => {
          this.showNotification('Album supprimé avec succès', 'success');
          this.loadData();
        },
        error: (err) => this.showNotification('Erreur lors de la suppression de l\'album', 'error')
      });
    }
  }
  
  // --- GESTION DES CHANSONS ---
  toggleSongForm(): void {
    this.showSongForm = !this.showSongForm;
    if (!this.showSongForm) {
      this.resetSongForm();
    }
  }
  
  resetSongForm(): void {
    this.songForm.reset();
    this.editingSongId = null;
  }
  
  saveSong(): void {
    if (this.songForm.invalid) {
      this.songForm.markAllAsTouched();
      return;
    }
    
    const songData = { ...this.songForm.value };
    
    // Conversion des genres de chaîne en tableau
    if (typeof songData.genres === 'string') {
      songData.genres = songData.genres.split(',').map((genre: string) => genre.trim());
    }
    
    if (this.editingSongId) {
      // Mode édition
      this.apiService.updateSong(this.editingSongId, songData).subscribe({
        next: () => {
          this.showNotification('Chanson mise à jour avec succès', 'success');
          this.loadData();
          this.toggleSongForm();
        },
        error: (err) => this.showNotification('Erreur lors de la mise à jour de la chanson', 'error')
      });
    } else {
      // Mode création
      this.apiService.createSong(songData).subscribe({
        next: () => {
          this.showNotification('Chanson créée avec succès', 'success');
          this.loadData();
          this.toggleSongForm();
        },
        error: (err) => this.showNotification('Erreur lors de la création de la chanson', 'error')
      });
    }
  }
  
  editSong(song: Song): void {
    // Nous supposons que la chanson a un ID string qui n'est pas visible dans l'interface Song
    // Dans une application réelle, vous devriez avoir accès à l'ID dans votre modèle
    // Pour cet exemple, nous allons utiliser le titre comme identifiant temporaire
    this.editingSongId = song.title; // En réalité, ce serait song.id
    
    // Conversion des genres du tableau en chaîne pour l'édition
    const genresString = song.genres ? song.genres.join(', ') : '';
    
    this.songForm.patchValue({
      title: song.title,
      duration: song.duration,
      artist_id: song.artist_id,
      album_id: song.album_id,
      genres: genresString
    });
    
    this.showSongForm = true;
  }
  
  deleteSong(song: Song): void {
    // Comme pour l'édition, dans un cas réel vous auriez un ID unique
    const songId = song.title; // En réalité, ce serait song.id
    
    if (confirm('Êtes-vous sûr de vouloir supprimer cette chanson ?')) {
      this.apiService.deleteSong(songId).subscribe({
        next: () => {
          this.showNotification('Chanson supprimée avec succès', 'success');
          this.loadData();
        },
        error: (err) => this.showNotification('Erreur lors de la suppression de la chanson', 'error')
      });
    }
  }
  
  // --- GESTION DES NOTIFICATIONS ---
  showNotification(message: string, type: 'success' | 'error'): void {
    this.notification = {
      show: true,
      message,
      type
    };
    
    // Masquer la notification après 3 secondes
    setTimeout(() => {
      this.notification.show = false;
    }, 3000);
  }
  
  // --- UTILITAIRES ---
  findArtistName(artistId: string): string {
    const artist = this.artists.find(a => a.id === artistId);
    return artist ? artist.name : 'Inconnu';
  }
  
  findAlbumTitle(albumId: string): string {
    const album = this.albums.find(a => a.id.toString() === albumId);
    return album ? album.title : 'Inconnu';
  }
  
  formatDuration(seconds: number): string {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  }
}
