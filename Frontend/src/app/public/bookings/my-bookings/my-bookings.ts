import { Component, OnInit, inject, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Auth } from '../../../core/auth';

@Component({
  selector: 'app-my-bookings',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './my-bookings.html',
  styleUrls: ['./my-bookings.css']
})
export class MyBookingsComponent implements OnInit {
  bookings: any[] = [];
  loading: boolean = true;
  error: string = '';

  private auth = inject(Auth);
  private router = inject(Router);

  ngOnInit(): void {
    this.loadMyBookings();
  }

  loadMyBookings(): void {
    this.loading = true;
    this.error = '';
    
    this.auth.getMyBookings().subscribe({
      next: (data: any) => {
        this.bookings = data || [];
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load bookings:', err);
        this.error = 'Failed to load your bookings';
        this.loading = false;
      }
    });
  }

  getStatusClass(status: string): string {
    switch(status?.toLowerCase()) {
      case 'pending': return 'pending';
      case 'approved': return 'approved';
      case 'declined': return 'declined';
      default: return '';
    }
  }

  goBack(): void {
    this.router.navigate(['/public/home']);
  }
}
