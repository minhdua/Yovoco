import { Component, OnInit } from '@angular/core';
import { Firestore } from '@angular/fire/firestore';
import { FormBuilder, FormGroup } from '@angular/forms';
import { addDoc, collection } from 'firebase/firestore';
import { AngularFirestore, AngularFirestoreCollection } from '@angular/fire/compat/firestore';
import { VocabularyService } from 'src/app/services/vocabulary.service';
import { Vocabulary } from 'src/app/models/collection';
import { Observable } from 'rxjs';
//https://github.com/trungdoublelift/PeerJS/blob/e6542ac3e9/src/app/app.component.ts

@Component({
  selector: 'app-add',
  templateUrl: './add.component.html',
  styleUrls: ['./add.component.scss'],
})
export class VocabularyAddComponent implements OnInit {
  addForm: FormGroup;
  private itemsCollection: AngularFirestoreCollection<Vocabulary>;
  items: Observable<Vocabulary[]>;
  constructor(private fb: FormBuilder, private afs: AngularFirestore) {}

  ngOnInit(): void {
    this.addForm = this.fb.group({
      word: [''],
      meaning: [''],
    });
  }

  onSave() {
    const { word, meaning } = this.addForm.value;
    this.itemsCollection = this.afs.collection<Vocabulary>('vocabulary');
    this.items = this.itemsCollection.valueChanges();
    this.items.subscribe({
      next: value => {
        console.log(value);
      },
      error: err => {
        console.log(err);
      },
      complete: () => {
        console.log('complete');
      },
    });
    console.log(this.items);
    //this.itemsCollection.add(new Vocabulary('1', word, meaning, '', '', '', '', '', '', ''));
  }
}
