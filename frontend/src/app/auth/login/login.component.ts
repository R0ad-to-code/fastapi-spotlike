import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../Services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  loginForm: FormGroup;
  loading = false;
  error = '';
  returnUrl: string = '/admin';
  showPassword = false;
  isFocused: string | null = null;

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthService
  ) {
    // Redirection si déjà connecté
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/admin']);
    }

    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });

    // Récupération de l'URL de retour depuis les paramètres de route ou '/admin' par défaut
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/admin';
  }

  // Getter pour un accès facile aux champs du formulaire
  get f() { return this.loginForm.controls; }

  onSubmit() {
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;
    this.error = '';
    
    this.authService.login(this.f['username'].value, this.f['password'].value)
      .subscribe({
        next: () => {
          this.router.navigate([this.returnUrl]);
        },
        error: error => {
          this.error = error.error?.detail || 'Une erreur est survenue lors de la connexion';
          this.loading = false;
        }
      });
  }

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  onFocus(field: string) {
    this.isFocused = field;
  }

  onBlur() {
    this.isFocused = null;
  }
}
