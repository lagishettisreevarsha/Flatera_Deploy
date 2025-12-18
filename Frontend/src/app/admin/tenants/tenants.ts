import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Auth } from '../../core/auth';

@Component({
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tenants.html',
  styleUrls: ['./tenants.css']
})
export class Tenants implements OnInit {
  tenants: any[] = [];
  loading: boolean = true;
  error: string = '';
  
  constructor(private api: Auth) {}
  
  ngOnInit() { 
    this.load(); 
  }
  
  load() {
    this.loading = true;
    this.error = '';
    
    this.api.getTenants().subscribe({
      next: (data: any) => {
        console.log('Tenants data received:', data); // Debug log
        this.tenants = data || [];
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Failed to load tenants:', err);
        this.error = 'Failed to load tenants';
        this.loading = false;
      }
    });
  }
  
  getTenantName(tenant: any): string {
    console.log('Tenant object:', tenant); // Debug log
    // Try multiple possible name fields
    if (tenant.user_name && tenant.user_name !== 'public') {
      return tenant.user_name;
    }
    if (tenant.name && tenant.name !== 'public') {
      return tenant.name;
    }
    if (tenant.email) {
      return tenant.email.split('@')[0]; // Use email username as fallback
    }
    return `Tenant ${tenant.user_id}`;
  }
  
  getFlatInfo(tenant: any): string {
    return tenant.flat_no || `Flat ${tenant.flat_id}`;
  }
  
  getTowerInfo(tenant: any): string {
    return tenant.tower_name || `Tower ${tenant.tower_id}` || 'Unknown Tower';
  }
}
