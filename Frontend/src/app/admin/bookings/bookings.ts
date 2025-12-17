import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Auth } from '../../core/auth';

@Component({
  standalone: true,
  imports: [CommonModule],
  templateUrl: './bookings.html',
  styleUrls: ['./bookings.css'],
})
export class Bookings implements OnInit {
  bookings: any[] = [];
  loading: boolean = true;
  error: string = '';
  
  constructor(private api: Auth) {}
  
  ngOnInit() { 
    this.load(); 
  }
  
  load() {
    this.loading = true;
    this.error = '';
    
    this.api.getPendingBookings().subscribe({
      next: (data: any) => {
        this.bookings = data || [];
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Failed to load bookings:', err);
        this.error = 'Failed to load bookings';
        this.loading = false;
      }
    });
  }
  
  approve(b: any) {
    if (!b.id) return;
    
    this.api.approveBooking(b.id).subscribe({
      next: (response: any) => {
        console.log('Booking approved:', response);
        this.load(); // Reload the list
      },
      error: (err: any) => {
        console.error('Failed to approve booking:', err);
        alert('Failed to approve booking: ' + (err.error?.message || err.message));
      }
    });
  }
  
  decline(b: any) {
    if (!b.id) return;
    
    this.api.declineBooking(b.id).subscribe({
      next: (response: any) => {
        console.log('Booking declined:', response);
        this.load(); // Reload the list
      },
      error: (err: any) => {
        console.error('Failed to decline booking:', err);
        alert('Failed to decline booking: ' + (err.error?.message || err.message));
      }
    });
  }
  
  getUserName(booking: any): string {
    return booking.user_name || booking.tenant_name || `User ${booking.user_id}`;
  }
  
  getFlatInfo(booking: any): string {
    return booking.flat_no || `Flat ${booking.flat_id}`;
  }
  
  getStatusClass(status: string): string {
    switch(status?.toLowerCase()) {
      case 'pending': return 'pending';
      case 'approved': return 'approved';
      case 'declined': return 'declined';
      default: return '';
    }
  }
}
