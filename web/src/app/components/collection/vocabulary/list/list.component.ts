import { Component, OnInit } from '@angular/core';
import { VocabularyService } from 'src/app/services/vocabulary.service';
import { Vocabulary } from 'src/app/models/collection';
@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.scss'],
})
export class VocabularyListComponent implements OnInit {
  isLoading = false;
  vocabularies: Vocabulary[] = [];

  first = 0;

  rows = 10;

  constructor(private vocabularyService: VocabularyService) {}

  ngOnInit() {}

  next() {
    this.first = this.first + this.rows;
  }

  prev() {
    this.first = this.first - this.rows;
  }

  reset() {
    this.first = 0;
  }

  isLastPage(): boolean {
    return this.vocabularies ? this.first === this.vocabularies.length - this.rows : true;
  }

  isFirstPage(): boolean {
    return this.vocabularies ? this.first === 0 : true;
  }

  onSearch() {
    this.vocabularyService.search().subscribe({
      next: data => {
        this.vocabularies = data['results'];
        this.isLoading = false;
      },
      error: error => {
        this.isLoading = false;
      },
    });
  }
}
