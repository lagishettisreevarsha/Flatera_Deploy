import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Auth } from '../../core/auth';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './towers.html',
  styleUrls: ['./towers.css']
})
export class Towers implements OnInit {
  towers: any[] = [];
  newTowerName = '';
  error: string | null = null;
  success: string | null = null;

  constructor(private api: Auth, private router: Router) {}

  ngOnInit() {
    this.load();
  }

  load() {
    this.error = null; this.success = null;
    this.api.getTowers().subscribe({
      next: (d: any) => this.towers = d,
      error: (err) => this.error = err?.error?.message || 'Failed to load towers.'
    });
  }

  create() {
    this.error = null; this.success = null;
    if (!this.newTowerName.trim()) { this.error = 'Name is required'; return; }
    this.api.createTower({ name: this.newTowerName.trim() }).subscribe({
      next: () => { this.success = 'Tower created'; this.newTowerName = ''; this.load(); },
      error: (err) => this.error = err?.error?.message || 'Failed to create tower.'
    });
  }

  update(t: any) {
    const name = prompt('New tower name', t.name);
    if (name === null) return;
    this.error = null; this.success = null;
    this.api.updateTower(t.id, { name }).subscribe({
      next: () => { this.success = 'Tower updated'; this.load(); },
      error: (err) => this.error = err?.error?.message || 'Failed to update tower.'
    });
  }

  delete(t: any) {
    if (!confirm('Delete this tower?')) return;
    this.error = null; this.success = null;
    this.api.deleteTower(t.id).subscribe({
      next: () => { this.success = 'Tower deleted'; this.load(); },
      error: (err) => this.error = err?.error?.message || 'Failed to delete tower.'
    });
  }
  
  goBack(): void {
    this.router.navigate(['/admin/dashboard']);
  }
}
