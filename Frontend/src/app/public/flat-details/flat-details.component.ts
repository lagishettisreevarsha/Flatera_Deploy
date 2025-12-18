import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Auth } from '../../core/auth';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-flat-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './flat-details.component.html',
  styleUrls: ['./flat-details.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FlatDetailsComponent implements OnInit {
  flat: any = null;
  loading: boolean = true;
  error: string = '';
  success: string = '';
  bookingLoading: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private auth: Auth,
    public sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    const flatId = this.route.snapshot.paramMap.get('id');
    if (flatId) {
      this.loadFlatDetails(flatId);
    } else {
      this.error = 'Flat ID not provided';
      this.loading = false;
    }
  }

  loadFlatDetails(flatId: string): void {
    this.loading = true;
    this.error = '';
    
    // Use specific flat details endpoint
    this.auth.getFlatDetails(flatId).subscribe({
      next: (flat: any) => {
        this.flat = flat;
        
        // Process flat data from backend
        if (this.flat) {
          
          // Ensure features array exists
          if (!this.flat.features || this.flat.features.length === 0) {
            this.flat.features = ["Parking", "24/7 Security"];
          }
          
          // Use description from backend as-is
          if (!this.flat.description || this.flat.description.trim() === '') {
            this.flat.description = 'No description available for this flat.';
          }
          
          // Use location from backend or construct basic one
          if (!this.flat.location || this.flat.location.trim() === '') {
            this.flat.location = this.flat.tower_name ? `Tower ${this.flat.tower_name}` : 'Location not specified';
          }
        }
        
        this.loading = false;
        
        if (!this.flat) {
          this.error = 'Flat not found';
        }
      },
      error: (err: any) => {
        console.error('Failed to load flat details:', err);
        this.error = 'Failed to load flat details';
        this.loading = false;
      }
    });
  }


  bookFlat(): void {
    if (this.flat && this.flat.is_available) {
      this.bookingLoading = true;
      this.error = '';
      this.success = '';
      
      this.auth.requestBooking(parseInt(this.flat.id)).subscribe({
        next: (response: any) => {
          console.log('Booking request response:', response);
          this.bookingLoading = false;
          this.success = 'Booking request submitted successfully! Redirecting to your bookings...';
          
          // Clear success message after 3 seconds and navigate
          setTimeout(() => {
            this.router.navigate(['/public/bookings']);
          }, 3000);
        },
        error: (err: any) => {
          console.error('Booking request error:', err);
          this.bookingLoading = false;
          
          // Handle specific error messages
          const errorMessage = err.error?.message || err.message || '';
          
          if (errorMessage.includes('already has a booking') || errorMessage.includes('already have a booking')) {
            this.error = 'You have already booked this flat. Check your bookings for the status.';
          } else if (errorMessage.includes('Flat not available') || errorMessage.includes('not available')) {
            this.error = 'This flat is no longer available for booking.';
          } else if (errorMessage.includes('Flat not found')) {
            this.error = 'This flat is no longer available.';
          } else {
            this.error = 'Unable to book this flat at the moment. Please try again later.';
          }
        }
      });
    }
  }

  goBack(): void {
    this.router.navigate(['/public/home']);
  }
}
