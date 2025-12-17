import { Routes } from '@angular/router';


import { authGuard, guestGuard } from './core/auth-guard';
import { Login } from './auth/login/login';
import { Register } from './auth/register/register';
import { HomeComponent } from './public/home/home';
import { FlatDetailsComponent } from './public/flat-details/flat-details.component';
import { MyBookings } from './public/bookings/my-bookings/my-bookings';
import { Dashboard }                                                                       from './admin/dashboard/dashboard';
import { Bookings } from './admin/bookings/bookings';
import { Towers } from './admin/towers/towers';
import { FlatsComponent } from './admin/flats/flats';
import { AmenitiesComponent } from './admin/amenities/amenities';
import { Tenants } from './admin/tenants/tenants';
// import { LandingComponent } from './landing/landing';
// import { LandingComponent } from './landing/landing';
import { Gallary } from './gallary/gallary';
import { Landing } from './landing/landing';

export const routes: Routes = [
  { path: '', redirectTo: 'landing', pathMatch: 'full' },
  { path: 'landing', component: Landing },
  { path: 'gallery', component: Gallary },
  { path: 'login', component: Login, canActivate: [guestGuard] },
  { path: 'register', component: Register, canActivate: [guestGuard]},

  {
    path: 'public',
    canActivate: [authGuard],
    children: [
      { path: 'home', component: HomeComponent },
      { path: 'flat-details/:id', component: FlatDetailsComponent },
      { path: 'bookings', component: MyBookings }
    ]
  },

  {
    path: 'admin',
    canActivate: [authGuard],
    children: [
      { path: 'dashboard', component: Dashboard },
      { path: 'bookings', component: Bookings },
      { path: 'towers', component: Towers },
      { path: 'flats', component: FlatsComponent },
      { path: 'amenities', component: AmenitiesComponent },
      { path: 'tenants', component: Tenants }
    ]
  },

];
