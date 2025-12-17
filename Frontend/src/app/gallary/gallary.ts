import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-gallary',
  imports: [CommonModule],
  templateUrl: './gallary.html',
  styleUrl: './gallary.css',
})
export class Gallary {
  
  images = [
   
    {
      url: 'https://i.pinimg.com/1200x/4b/9c/49/4b9c49bd73e47982937bd01585c9cd74.jpg',
      title: 'Master Bedroom',
      description: 'Elegant master suite with panoramic city views'
    },
  
    {
      url: 'https://i.pinimg.com/736x/aa/d5/0d/aad50dbfe766bb32ad7f7c31ddb5f3a8.jpg',
      title: 'Modern Kitchen',
      description: 'Contemporary kitchen with island and premium appliances'
    },
    {
      url: 'https://i.pinimg.com/736x/ad/5e/98/ad5e98535b8834b60cd5e44d41c1d090.jpg',
      title: 'Elegant Bedroom',
      description: 'Sophisticated bedroom with luxurious textiles and decor'
    },
    {
      url: 'https://i.pinimg.com/1200x/da/93/a7/da93a72e64c94e440f539193488fb80b.jpg',
      title: 'Luxury Suite',
      description: 'Spacious suite with panoramic windows and modern furnishings'
    },
    {
      url: 'https://i.pinimg.com/736x/90/3a/61/903a61a4fee0150f8581cb78807a9f85.jpg',
      title: 'Designer Living Room',
      description: 'High-end living space with designer furniture and art'
    },
    {
      url: 'https://i.pinimg.com/736x/73/48/6f/73486f2a202cbb124ff98f5733331d62.jpg',
      title: 'Penthouse View',
      description: 'Exclusive penthouse with breathtaking city skyline views'
    },
    {
      url: 'https://i.pinimg.com/736x/32/75/1e/32751e511b073258f0a8798f01fd4044.jpg',
      title: 'Marble Bathroom',
      description: 'Luxurious bathroom with marble finishes and modern fixtures'
    },
    {
      url: 'https://i.pinimg.com/736x/d3/d7/4d/d3d74ddcd1277ab7faedbc83bb27e729.jpg',
      title: 'Gourmet Dining',
      description: 'Elegant dining area with premium materials and lighting'
    },
    {
      url: 'https://i.pinimg.com/736x/69/36/74/6936746e50cfb894ae4a3e7c85b27ba8.jpg',
      title: 'City View Terrace',
      description: 'Private terrace with stunning urban landscape views'
    },
    {
      url: 'https://i.pinimg.com/1200x/74/e4/a5/74e4a573ea294d400c7bea174ad350dd.jpg',
      title: 'Executive Suite',
      description: 'Premium suite with executive amenities and sophisticated design'
    },
    {
      url: 'https://i.pinimg.com/1200x/8a/5b/f9/8a5bf99443de968716aa32c0b10b1feb.jpg',
      title: 'Sky Lounge',
      description: 'Exclusive lounge area with panoramic city and sky views'
    }
  ];

}
