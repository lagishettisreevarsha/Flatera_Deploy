import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-landing',
  imports: [CommonModule,FormsModule,RouterModule],
  templateUrl: './landing.html',
  styleUrl: './landing.css',
})
export class Landing {

  features = [
    {
      image: 'https://www.decorilla.com/online-decorating/wp-content/uploads/2023/07/Combined-living-and-dining-room-design-by-Decorilla.jpg',
      title: 'Spacious Living Areas',
      description: 'Open-concept designs that seamlessly blend living and dining spaces'
    },
    {
      image: 'https://i.pinimg.com/736x/7a/71/ad/7a71ad1c7acfb658f4ee7dbb3654504a.jpg',
      title: 'Gourmet Kitchens',
      description: 'State-of-the-art appliances and premium finishes for culinary excellence'
    },
    {
      image: 'https://img.freepik.com/premium-photo/master-bedroom-interior-luxury-apartment-net-clean-lines-decor_848676-5126.jpg',
      title: 'Master Suites',
      description: 'Retreat to your private sanctuary with luxurious bedroom designs'
    },
    {
      image: 'https://i.pinimg.com/736x/7b/00/fb/7b00fbf194f606fcd4775341266990d6.jpg',
      title: 'Fitness Center',
      description: 'State-of-the-art equipment and wellness facilities for active lifestyle'
    },
    {
      image: 'https://i.pinimg.com/736x/a4/da/8c/a4da8c0ec78263c5c6d4991f841df184.jpg',
      title: 'Pool',
      description: 'Premium materials and exquisite craftsmanship throughout'
    },
    {
      image: 'https://i.pinimg.com/736x/8a/07/63/8a07638d4724674699b73d0e30716355.jpg',
      title: 'Spa Bathrooms',
      description: 'Premium materials and exquisite craftsmanship throughout'
    }
  ];

  amenities = [
    {
      title: '24/7 Concierge',
      description: 'Premium service and assistance around the clock'
    },
    {
      title: 'Fitness Center',
      description: 'State-of-the-art equipment and wellness facilities'
    },
    {
      title: 'Rooftop Terrace',
      description: 'Stunning views and entertainment spaces'
    },
    {
      title: 'Business Center',
      description: 'Professional workspace and meeting facilities'
    }
  ];

  constructor(private router: Router) {}

  goToLogin() {
    this.router.navigate(['/login']);
  }

  goToRegister() {
    this.router.navigate(['/register']);
  }

  exploreProperties() {
    this.router.navigate(['/login']);
  }

  scheduleTour() {
    this.router.navigate(['/register']);
  }

  getStarted() {
    this.router.navigate(['/register']);
  }

  learnMore() {
    // Scroll to features section or navigate to a details page
    document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' });
  }
}
