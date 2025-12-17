import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class Auth{
  private API = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {}

  get apiUrl(): string {
    return this.API;
  }

  register(data: any) {
    return this.http.post(`${this.API}/auth/register`, data);
  }

  login(data: any) {
    return this.http.post(`${this.API}/auth/login`, data);
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
  }

  getFlats() {
    return this.http.get(`${this.API}/public/flats`);
  }

  getFlatDetails(flatId: string) {
    return this.http.get(`${this.API}/public/flats/${flatId}`);
  }

  requestBooking(flatId: number) {
    return this.http.post(`${this.API}/public/book/${flatId}`, {});
  }

  getMyBookings() {
    return this.http.get(`${this.API}/public/bookings`);
  }

  getPendingBookings() {
    return this.http.get(`${this.API}/admin/bookings`);
  }
  approveBooking(bookingId: number) {
    return this.http.post(`${this.API}/admin/booking/${bookingId}/approve`, {});
  }
  declineBooking(bookingId: number) {
    return this.http.post(`${this.API}/admin/booking/${bookingId}/decline`, {});
  }

  getTowers() {
    return this.http.get(`${this.API}/admin/towers`);
  }
  createTower(data: { name: string }) {
    return this.http.post(`${this.API}/admin/towers`, data);
  }
  updateTower(towerId: number, data: { name: string }) {
    return this.http.put(`${this.API}/admin/towers/${towerId}`, data);
  }
  deleteTower(towerId: number) {
    return this.http.delete(`${this.API}/admin/towers`, { body: { tower_id: towerId } });
  }

  getAdminFlats() {
    return this.http.get(`${this.API}/admin/flats`);
  }
  

  addFlat(data: any) {
    return this.http.post(`${this.API}/admin/flats`, data);
  }
  updateFlat(flatId: number, data: any) {
    return this.http.put(`${this.API}/admin/flats/${flatId}`, data);
  }
  deleteFlat(flatId: number) {
    return this.http.delete(`${this.API}/admin/flats/${flatId}`);
  }

  getAmenities() {
    return this.http.get(`${this.API}/admin/amenities`);
  }
  addAmenity(data: any) {
    return this.http.post(`${this.API}/admin/amenities`, data);
  }
  updateAmenity(amenityId: number, data: { name: string }) {
    return this.http.put(`${this.API}/admin/amenities/${amenityId}`, data);
  }
  deleteAmenity(amenityId: number) {
    return this.http.delete(`${this.API}/admin/amenities/${amenityId}`);
  }

  getTenants() {
    return this.http.get(`${this.API}/admin/tenants`);
  }
}
