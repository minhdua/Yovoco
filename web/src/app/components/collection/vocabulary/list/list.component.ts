import { Component, OnInit } from '@angular/core';
import { VocabularyService } from 'src/app/services/vocabulary.service';

class Customer {
  name: string;
  country: string;
  company: string;
  representative: string;

  constructor(name: string, country: string, company: string, representative: string) {
    this.name = name;
    this.country = country;
    this.company = company;
    this.representative = representative;
  }
}

class Vocabulary {
  id: string;
  word: string;
  meaning: string;
  example: string;
  phonetic: string;
  audio: string;
  pos: string;
  language: string;
  collection: string;
  pos_extend: string;

  constructor(
    id: string,
    word: string,
    meaning: string,
    example: string,
    phonetic: string,
    audio: string,
    pos: string,
    language: string,
    collection: string,
    pos_extend: string
  ) {
    this.id = id;
    this.word = word;
    this.meaning = meaning;
    this.example = example;
    this.phonetic = phonetic;
    this.audio = audio;
    this.pos = pos;
    this.language = language;
    this.collection = collection;
    this.pos_extend = pos_extend;
  }
}
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
