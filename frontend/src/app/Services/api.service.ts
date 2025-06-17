import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { Observable, BehaviorSubject, tap } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Album } from '../models/album';
import { Artist } from '../models/artist';
import { Song } from '../models/song';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api';  // URL mise à jour

  public albumsSubject = new BehaviorSubject<Album[]>([]);
  public albumSongsSubject = new BehaviorSubject<Song[]>([]);
  public artistsSubject = new BehaviorSubject<Artist[]>([]);
  private isBrowser: boolean;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
  this.isBrowser = isPlatformBrowser(platformId);
    if (this.isBrowser) {
      const isLocalhost = window.location.hostname === 'localhost';
      if (!isLocalhost) {
        this.apiUrl = 'http://spotlike-alb-576527027.eu-west-3.elb.amazonaws.com/api';
      }
    }
  }

  fetchAlbums(): void {
      this.http.get<any[]>(`${this.apiUrl}/albums`).subscribe({
        next: (albums) => this.albumsSubject.next(Object.values(albums)[0]),
        error: (err) => console.error('Failed to fetch albums', err),
      });
  }

  // Récupérer les artistes et mettre à jour le BehaviorSubject
  fetchArtists(): void {
    this.http.get<any[]>(`${this.apiUrl}/artists`).subscribe({
      next: (artists) => this.artistsSubject.next(Object.values(artists)[0]),
      error: (err) => console.error('Failed to fetch albums', err),
    });
  }

  // Méthodes pour récupérer les données spécifiques
  getAlbums(): Observable<Album[]> {
    return this.http.get<Album[]>(`${this.apiUrl}/albums`);
  }

  getSongsOfAlbum(albumId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/albums/${albumId}/songs`);
  }

  getArtists(): Observable<Artist[]> {
    return this.http.get<Artist[]>(`${this.apiUrl}/artists`);
  }

  getAlbumById(id: string): Observable<Album> {
    return this.http.get<Album>(`${this.apiUrl}/albums/${id}`);
  }

  getArtistById(id: string): Observable<Artist> {
    return this.http.get<Artist>(`${this.apiUrl}/artists/${id}`);
  }
  
  // CRUD pour les artistes
  createArtist(artist: Partial<Artist>): Observable<Artist> {
    return this.http.post<Artist>(`${this.apiUrl}/artists`, artist).pipe(
      tap(() => this.fetchArtists())
    );
  }
  
  updateArtist(id: string, artist: Partial<Artist>): Observable<Artist> {
    return this.http.put<Artist>(`${this.apiUrl}/artists/${id}`, artist).pipe(
      tap(() => this.fetchArtists())
    );
  }
  
  deleteArtist(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/artists/${id}`).pipe(
      tap(() => this.fetchArtists())
    );
  }
  
  // CRUD pour les albums
  createAlbum(album: Partial<Album>): Observable<Album> {
    return this.http.post<Album>(`${this.apiUrl}/albums`, album).pipe(
      tap(() => this.fetchAlbums())
    );
  }
  
  updateAlbum(id: string, album: Partial<Album>): Observable<Album> {
    return this.http.put<Album>(`${this.apiUrl}/albums/${id}`, album).pipe(
      tap(() => this.fetchAlbums())
    );
  }
  
  deleteAlbum(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/albums/${id}`).pipe(
      tap(() => this.fetchAlbums())
    );
  }
  
  // CRUD pour les chansons
  createSong(song: Partial<Song>): Observable<Song> {
    return this.http.post<Song>(`${this.apiUrl}/songs`, song);
  }
  
  updateSong(id: string, song: Partial<Song>): Observable<Song> {
    return this.http.put<Song>(`${this.apiUrl}/songs/${id}`, song);
  }
  
  deleteSong(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/songs/${id}`);
  }
  
  getAllSongs(): Observable<Song[]> {
    return this.http.get<Song[]>(`${this.apiUrl}/songs`);
  }
}
