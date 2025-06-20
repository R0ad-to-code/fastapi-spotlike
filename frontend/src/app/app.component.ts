import { Component } from '@angular/core';
import { AuthService } from './Services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'SpotiLike';

  constructor(public authService: AuthService) {}

  logout(): void {
    this.authService.logout();
  }
}
