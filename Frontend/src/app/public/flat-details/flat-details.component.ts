import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Auth } from '../../core/auth';

@Component({
  selector: 'app-flat-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './flat-details.component.html',
  styleUrls: ['./flat-details.component.css']
})
export class FlatDetailsComponent implements OnInit {
  flat: any = null;
  loading: boolean = true;
  error: string = '';
  imageLoading: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private auth: Auth
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
    this.imageLoading = true;
    
    // Use specific flat details endpoint
    this.auth.getFlatDetails(flatId).subscribe({
      next: (flat: any) => {
        this.flat = flat;
        
        // Process flat data from backend
        if (this.flat) {
          // Handle image from backend
          if (this.flat.image) {
            if (!this.flat.image.startsWith('http')) {
              // If it's a relative path, construct full URL
              this.flat.image = `${this.auth.apiUrl}/images/flats/${this.flat.image}`;
            }
          } else {
            // No image provided by backend - use a placeholder
            this.flat.image = 'https://via.placeholder.com/800x600/6F4E37/FFFFFF?text=No+Image+Available';
          }
          
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

  onImageLoad(event: any): void {
    this.imageLoading = false;
  }

  onImageError(event: any): void {
    console.log('Backend image failed to load, using placeholder');
    // Use a placeholder image if the backend image fails
    event.target.src = 'https://via.placeholder.com/800x600/6F4E37/FFFFFF?text=Image+Not+Available';
    this.imageLoading = false;
  }

  bookFlat(): void {
    if (this.flat && this.flat.is_available) {
      this.auth.requestBooking(parseInt(this.flat.id)).subscribe({
        next: (response: any) => {
          alert(`Booking request submitted for flat ${this.flat.flat_no}`);
          console.log('Booking request response:', response);
        },
        error: (err: any) => {
          console.error('Booking request error:', err);
          alert('Failed to submit booking request: ' + (err.error?.message || err.message));
        }
      });
    }
  }

  goBack(): void {
    this.router.navigate(['/public/home']);
  }
}
