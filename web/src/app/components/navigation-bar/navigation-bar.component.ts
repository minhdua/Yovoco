import { Component, OnInit } from '@angular/core';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-navigation-bar',
  templateUrl: './navigation-bar.component.html',
  styleUrls: ['./navigation-bar.component.scss'],
})
export class NavigationBarComponent implements OnInit {
  items: MenuItem[];

  ngOnInit() {
    this.items = [
      {
        label: 'Vocabulary',
        icon: 'pi pi-pw pi-th-large',
        items: [{ label: 'Vocabularies', icon: 'pi pi-fw pi-box' }],
      },
    ];
  }
}
