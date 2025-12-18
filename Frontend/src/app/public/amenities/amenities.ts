import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Auth } from '../../core/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-amenities',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './amenities.html',
  styleUrls: ['./amenities.css']
})
export class AmenitiesComponent implements OnInit {
  amenities: any[] = [];
  loading: boolean = true;
  error: string = '';

  constructor(private auth: Auth, private router: Router) {}

  ngOnInit(): void {
    this.loadAmenities();
  }

  loadAmenities(): void {
    this.loading = true;
    this.error = '';
    
    this.auth.getPublicAmenities().subscribe({
      next: (data: any) => {
        this.amenities = data || [];
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Failed to load amenities:', err);
        this.error = 'Failed to load amenities';
        this.loading = false;
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/public/home']);
  }
}
