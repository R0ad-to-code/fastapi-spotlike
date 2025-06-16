import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../Services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerForm: FormGroup;
  loading = false;
  submitted = false;
  error = '';
  success = '';

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {
    // Rediriger si déjà connecté
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/admin']);
    }

    this.registerForm = this.formBuilder.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required]
    }, {
      validator: this.passwordMatchValidator
    });
  }

  // Facilite l'accès aux champs du formulaire
  get f() { return this.registerForm.controls; }

  // Validateur personnalisé pour vérifier que les mots de passe correspondent
  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;

    return password === confirmPassword ? null : { passwordMismatch: true };
  }

  onSubmit() {
    this.submitted = true;

    if (this.registerForm.invalid) {
      return;
    }

    this.loading = true;
    this.error = '';
    
    this.authService.register({
      username: this.f['username'].value,
      email: this.f['email'].value,
      password: this.f['password'].value
    }).subscribe({
      next: () => {
        this.success = 'Inscription réussie !';
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 1500);
      },
      error: error => {
        this.error = error.error?.detail || 'Une erreur est survenue lors de l\'inscription';
        this.loading = false;
      }
    });
  }
}
