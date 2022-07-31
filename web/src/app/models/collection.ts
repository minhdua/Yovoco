import { FormBuilder, FormControl, FormGroup } from '@angular/forms';

export class Customer {
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

export class Collection {
  public collectionForm = new FormGroup({
    id: new FormControl(''),
    collectionName: new FormControl(''),
    topicName: new FormControl(''),
    description: new FormControl(''),
    createdAt: new FormControl(new Date()),
    updatedAt: new FormControl(new Date()),
    createdBy: new FormControl('minhdua'),
    updatedBy: new FormControl('minhdua'),
  });

  public vocabularyForm = new FormGroup({
    id: new FormBuilder().control(''),
    topic: new FormBuilder().control(''),
    word: new FormBuilder().control(''),
    meaning: new FormBuilder().control(''),
    definition: new FormBuilder().control(''),
    example: new FormBuilder().control(''),
    phonetic: new FormBuilder().control(''),
    audio: new FormBuilder().control(''),
    pos: new FormBuilder().control(''),
    synonym: new FormBuilder().control(''),
    antonym: new FormBuilder().control(''),
    createdAt: new FormBuilder().control(new Date()),
    updatedAt: new FormBuilder().control(new Date()),
    createdBy: new FormBuilder().control('minhdua'),
    updatedBy: new FormBuilder().control('minhdua'),
    isDeleted: new FormBuilder().control(false),
    isFavorite: new FormBuilder().control(false),
    isLearned: new FormBuilder().control(false),
    isReviewed: new FormBuilder().control(false),
    lastReviewed: new FormBuilder().control(new Date()),
  });
}
export class Vocabulary {
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
