import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Auth } from '../../core/auth';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class HomeComponent implements OnInit {
  flats: any[] = [];

  constructor(private router: Router, private auth: Auth) {}

  ngOnInit(): void {
    this.loadFlats();
  }

  loadFlats(): void {
    this.auth.getFlats().subscribe({
      next: (data: any) => {
        this.flats = data;
      },
      error: (err: any) => {
        console.error('Failed to load flats:', err);
        // Fallback to mock data if API fails
        this.flats = [
          {
            id: '1',
            flat_no: 'A-101',
            bedrooms: 2,
            sqft: 1200,
            rent: 25000,
            is_available: true
          },
          {
            id: '2',
            flat_no: 'B-205',
            bedrooms: 3,
            sqft: 1800,
            rent: 35000,
            is_available: false
          },
          {
            id: '3',
            flat_no: 'C-309',
            bedrooms: 1,
            sqft: 800,
            rent: 18000,
            is_available: true
          },
          {
            id: '4',
            flat_no: 'D-412',
            bedrooms: 2,
            sqft: 1100,
            rent: 22000,
            is_available: true
          },
          {
            id: '5',
            flat_no: 'E-501',
            bedrooms: 4,
            sqft: 2200,
            rent: 45000,
            is_available: false
          },
          {
            id: '6',
            flat_no: 'F-618',
            bedrooms: 3,
            sqft: 1600,
            rent: 32000,
            is_available: true
          }
        ];
      }
    });
  }

  viewFlatDetails(flatId: string): void {
    this.router.navigate(['/public/flat-details', flatId]);
  }

  book(flatId: string): void {
    // Navigate to flat details instead of showing alert
    this.viewFlatDetails(flatId);
  }

  onLogout(): void {
    // Handle logout logic
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
