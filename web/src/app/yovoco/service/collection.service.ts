import { Observable } from 'rxjs';
import { Collection } from '../model/collection.model';
import {
    AngularFirestore,
    AngularFirestoreCollection,
} from '@angular/fire/compat/firestore';
import { Injectable } from '@angular/core';
import { Firestore } from '@angular/fire/firestore';
import { addDoc, collection, doc, updateDoc } from 'firebase/firestore';
import { docData } from 'rxfire/firestore';

@Injectable({ providedIn: 'root' })
export class CollectionService {
    collectionRef: any;
    constructor(private fs: Firestore) {
        this.collectionRef = collection(this.fs, 'Collection');
    }

    insert(item: Collection) {
        addDoc(this.collectionRef, item);
    }

    getAll() {
        const collectionDocRef = doc(this.collectionRef);
        return docData(collectionDocRef);
    }

    getById(id: string) {
        const collectionDocRef = doc(this.collectionRef, `Collection/${id}`);
        return docData(collectionDocRef, { idField: 'id' });
    }

    update(item: Collection, id: string) {
        item.modifiedAt = new Date();
        return updateDoc(this.collectionRef, id, item);
    }

    delete(item: Collection) {
        item.isDeleted = true;
        item.modifiedAt = new Date();
        updateDoc(this.collectionRef, item.id, item);
    }
}
