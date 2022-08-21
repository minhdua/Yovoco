import { Observable } from 'rxjs';
import { Collection } from '../model/collection.model';
import {
    AngularFirestore,
    AngularFirestoreCollection,
} from '@angular/fire/compat/firestore';

export class CollectionService {
    collectionRef: any;
    private itemCollection: AngularFirestoreCollection<Collection>;
    item: Observable<Collection>;
    items: Observable<Collection[]>;
    constructor(private afs: AngularFirestore) {
        this.itemCollection = afs.collection<Collection>('Collection');
        this.items = this.itemCollection.valueChanges();
    }

    addItem(item: Collection) {
        this.itemCollection.add(item);
    }

    getItems() {
        return this.items;
    }

    getItem(id: string) {
        this.itemCollection.doc<Collection>(id).valueChanges();
        return this.item;
    }

    // updateItem(item: Collection) {
    //     this.itemCollection.doc<Collection>(item.id).update(item);
    // }

    // deleteItem(item: Collection) {
    //     item.isDeleted = true;
    //     this.itemCollection.doc<Collection>(item.id).update(item);
    // }
}
