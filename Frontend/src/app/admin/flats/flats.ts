import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Auth } from '../../core/auth';

@Component({
  selector: 'app-flats',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './flats.html',
  styleUrls: ['./flats.css']
})
export class FlatsComponent implements OnInit {
  flats: any[] = [];
  towers: any[] = [];
  newFlat: any = { 
    tower_id: null, 
    flat_no: '', 
    bedrooms: '', 
    sqft: '', 
    rent: '', 
    is_available: true,
    floor: '',
    description: '',
    features: ''
  };
  editingFlat: any = null;
  error: string | null = null;
  success: string | null = null;
  selectedImage: File | null = null;
  imagePreview: string | null = null;

  constructor(private auth: Auth) {}

  ngOnInit(): void {
    this.loadTowers();
  }


  loadFlats(): void {
    this.auth.getFlats().subscribe({
      next: (data: any) => {
        this.flats = data;
        this.error = null;
      },
      error: (err: any) => {
        this.error = 'Failed to load flats: ' + (err.error?.message || err.message);
        this.success = null;
      }
    });
  }

 loadTowers(): void {
  this.auth.getTowers().subscribe({
    next: (data: any) => {
      this.towers = data;
      this.loadFlats(); // load flats AFTER towers
    },
    error: (err: any) => {
      this.error = 'Failed to load towers';
    }
  });
}


  addFlat(): void {
    if (!this.newFlat.tower_id || !this.newFlat.flat_no.trim()) {
      this.error = 'Tower and flat number are required';
      return;
    }
    
    // Create FormData for file upload
    const formData = new FormData();
    formData.append('tower_id', this.newFlat.tower_id);
    formData.append('flat_no', this.newFlat.flat_no.trim());
    formData.append('bedrooms', this.newFlat.bedrooms || '1');
    formData.append('sqft', this.newFlat.sqft || '0');
    formData.append('rent', this.newFlat.rent || '0');
    formData.append('is_available', this.newFlat.is_available ? 'true' : 'false');
    formData.append('floor', this.newFlat.floor || '');
    formData.append('description', this.newFlat.description || '');
    formData.append('features', this.newFlat.features || '');
    
    // Add image if selected
    if (this.selectedImage) {
      formData.append('image', this.selectedImage);
    }
    
    console.log('Sending flat data with image:', formData);
    
    this.auth.addFlat(formData).subscribe({
      next: (response) => {
        console.log('Flat added response:', response);
        this.success = 'Flat added successfully';
        this.error = null;
        this.newFlat = { 
          tower_id: null, 
          flat_no: '', 
          bedrooms: '', 
          sqft: '', 
          rent: '', 
          is_available: true,
          floor: '',
          description: '',
          features: ''
        };
        this.selectedImage = null;
        this.imagePreview = null;
        this.loadFlats();
      },
      error: (err: any) => {
        console.error('Add flat error:', err);
        console.error('Error status:', err.status);
        console.error('Error details:', err.error);
        this.error = 'Failed to add flat: ' + (err.error?.message || err.message || 'Validation error');
        this.success = null;
      }
    });
  }

  onImageSelect(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedImage = file;
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.imagePreview = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  editFlat(flat: any): void {
    this.editingFlat = { ...flat };
  }

  updateFlat(): void {
    if (!this.editingFlat || !this.editingFlat.tower_id || !this.editingFlat.flat_no.trim()) {
      this.error = 'Tower and flat number are required';
      return;
    }
    
    const flatData = {
      tower_id: parseInt(this.editingFlat.tower_id),
      flat_no: this.editingFlat.flat_no.trim(),
      bedrooms: parseInt(this.editingFlat.bedrooms) || 1,
      sqft: parseInt(this.editingFlat.sqft) || 0,
      rent: parseInt(this.editingFlat.rent) || 0,
      is_available: Boolean(this.editingFlat.is_available)
    };
    
    console.log('Updating flat data:', flatData);
    
    this.auth.updateFlat(this.editingFlat.id, flatData).subscribe({
      next: (response) => {
        console.log('Flat updated response:', response);
        this.success = 'Flat updated successfully';
        this.error = null;
        this.editingFlat = null;
        this.loadFlats();
      },
      error: (err: any) => {
        console.error('Update flat error:', err);
        console.error('Error status:', err.status);
        console.error('Error details:', err.error);
        this.error = 'Failed to update flat: ' + (err.error?.message || err.message || 'Validation error');
        this.success = null;
      }
    });
  }

  cancelEdit(): void {
    this.editingFlat = null;
  }

  deleteFlat(id: number): void {
    console.log('Deleting flat with ID:', id);
    this.auth.deleteFlat(id).subscribe({
      next: () => {
        this.success = 'Flat deleted successfully';
        this.error = null;
        this.loadFlats();
      },
      error: (err: any) => {
        console.error('Delete error:', err);
        this.error = 'Failed to delete flat: ' + (err.error?.message || err.message);
        this.success = null;
      }
    });
  }

  getTowerName(towerId: number): string {
    const tower = this.towers.find(t => t.id === towerId);
    return tower ? tower.name : 'Unknown';
  }
}