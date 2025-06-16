import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

interface LoginResponse {
  access_token: string;
  user_id: number;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://spotlike-alb-576527027.eu-west-3.elb.amazonaws.com/api';
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();
  private isBrowser: boolean;

  constructor(
    private http: HttpClient, 
    private router: Router, 
    @Inject(PLATFORM_ID) platformId: Object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
    
    // Initialiser l'état d'authentification seulement côté client
    if (this.isBrowser) {
      this.isAuthenticatedSubject.next(this.hasToken());
      
      // En développement local, on utilisera /api (path relatif)
      // En production, on utilisera l'URL complète
      const isLocalhost = window.location.hostname === 'localhost';
      if (isLocalhost) {
        this.apiUrl = '/api';
      }
    }
  }

  login(username: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/users/login`, { username, password })
      .pipe(
        tap(response => {
          if (this.isBrowser) {
            localStorage.setItem('token', response.access_token);
            localStorage.setItem('user_id', response.user_id.toString());
            this.isAuthenticatedSubject.next(true);
          }
        })
      );
  }

  register(user: { username: string, email: string, password: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/users/register`, user);
  }

  logout(): void {
    if (this.isBrowser) {
      localStorage.removeItem('token');
      localStorage.removeItem('user_id');
    }
    this.isAuthenticatedSubject.next(false);
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    if (this.isBrowser) {
      return localStorage.getItem('token');
    }
    return null;
  }

  private hasToken(): boolean {
    if (this.isBrowser) {
      return !!localStorage.getItem('token');
    }
    return false;
  }

  isAuthenticated(): boolean {
    return this.hasToken();
  }
}