import { Component, Input } from '@angular/core';
import { Artist } from '../../models/artist';

@Component({
  selector: 'app-artists-list',
  templateUrl: './artists-list.component.html',
  styleUrls: ['./artists-list.component.css']
})
export class ArtistsListComponent {
  @Input() artists: Artist[] = [];
}
