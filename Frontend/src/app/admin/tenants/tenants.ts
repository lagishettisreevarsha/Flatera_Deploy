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
    return tenant.user_name || tenant.tenant_name || `Tenant ${tenant.user_id}`;
  }
  
  getFlatInfo(tenant: any): string {
    return tenant.flat_no || `Flat ${tenant.flat_id}`;
  }
  
  getTowerInfo(tenant: any): string {
    return tenant.tower_name || `Tower ${tenant.tower_id}` || 'Unknown Tower';
  }
}
