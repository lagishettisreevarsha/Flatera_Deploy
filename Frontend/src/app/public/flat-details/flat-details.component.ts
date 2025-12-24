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
  encapsulation: ViewEncapsulation.Emulated
})
export class FlatDetailsComponent implements OnInit {
  flat: any = null;
  loading: boolean = true;
  error: string = '';
  success: string = '';
  bookingLoading: boolean = false;
  showErrorModal: boolean = false;
  showSuccessModal: boolean = false;
  modalMessage: string = '';

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
          
          // Ensure features array exists and is properly formatted
          if (!this.flat.features || this.flat.features.length === 0) {
            this.flat.features = ["Parking", "24/7 Security"];
          } else if (typeof this.flat.features === 'string') {
            // Split comma-separated string into array and clean up
            this.flat.features = this.flat.features.split(',').map((feature: string) => feature.trim()).filter((feature: string) => feature.length > 0);
          } else if (!Array.isArray(this.flat.features)) {
            // Convert to array if it's not already
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
          this.modalMessage = 'Booking request submitted successfully! You can check your booking status in My Bookings.';
          this.showSuccessModal = true;
        },
        error: (err: any) => {
          console.error('Booking request error:', err);
          this.bookingLoading = false;
          
          // Handle different error types with specific messages
          if (err.status === 401) {
            this.modalMessage = 'Unauthorized: Please log in again to book this flat.';
            this.showErrorModal = true;
          } else if (err.status === 403) {
            this.modalMessage = 'Access Denied: You do not have permission to book this flat.';
            this.showErrorModal = true;
          } else if (err.status === 404) {
            this.modalMessage = 'Flat Not Found: This flat is no longer available.';
            this.showErrorModal = true;
          } else if (err.status === 400) {
            if (err.error && err.error.message) {
              const errorMessage = err.error.message;
              
              if (errorMessage.includes('already booked')) {
                this.modalMessage = 'Already Booked: This flat is already booked by another tenant.';
              } else if (errorMessage.includes('already booked by you')) {
                this.modalMessage = 'Already Booked: You have already booked this flat.';
              } else if (errorMessage.includes('not available')) {
                this.modalMessage = 'Not Available: This flat is currently not available for booking.';
              } else {
                this.modalMessage = 'Booking Failed: ' + errorMessage;
              }
            } else {
              this.modalMessage = 'Booking Failed: Invalid request. Please try again.';
            }
            this.showErrorModal = true;
          } else if (err.status >= 500) {
            this.modalMessage = 'Server Error: Unable to process booking request. Please try again later.';
            this.showErrorModal = true;
          } else {
            // Handle network errors or other issues
            if (err.error && err.error.message) {
              this.modalMessage = 'Booking Error: ' + err.error.message;
            } else {
              this.modalMessage = 'Booking Error: Unable to complete booking. Please check your connection and try again.';
            }
            this.showErrorModal = true;
          }
        }
      });
    }
  }

  goBack(): void {
    this.router.navigate(['/public/home']);
  }

  onImageError(event: any): void {
    event.target.src = '/assets/images/default-flat.jpg';
  }

  closeErrorModal(): void {
    this.showErrorModal = false;
    this.modalMessage = '';
    console.log('Error modal closed');
  }

  closeSuccessModal(): void {
    this.showSuccessModal = false;
    this.modalMessage = '';
    console.log('Success modal closed');
  }

  goToMyBookings(): void {
    this.showSuccessModal = false;
    this.router.navigate(['/public/bookings']);
  }
}
