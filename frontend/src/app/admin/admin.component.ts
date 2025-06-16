import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../Services/auth.service';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
})
export class AdminComponent {
  activeTab = 'artists'; // Onglet actif par défaut

  constructor(private authService: AuthService, private router: Router) {}

  logout() {
    this.authService.logout();
  }

  setActiveTab(tab: string) {
    this.activeTab = tab;
  }
}
