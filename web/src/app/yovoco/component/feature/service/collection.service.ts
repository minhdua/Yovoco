import { Injectable } from '@angular/core';
import { AngularFirestore, AngularFirestoreCollection, AngularFirestoreDocument } from '@angular/fire/compat/firestore';
import { map } from 'rxjs';
import { TreeNode } from 'primeng/api';
import { Collection } from '../model/collection.model';
import { Timestamp } from '@angular/fire/firestore';

@Injectable({ providedIn: 'root' })
export class CollectionService {
	mChildren: any[] = [];
	get(vocabularyRef: any) {
		return this.db.doc(vocabularyRef).valueChanges();
	}
	documents: AngularFirestoreDocument<any>;
	collections: AngularFirestoreCollection<any>;

	constructor(private db: AngularFirestore) {
		this.collections = db.collection(`Collection`);
	}

	nextId() {
		return this.db.createId();
	}

	loadDeepCollection(nodes: TreeNode<any>[]) {
		nodes.forEach(element => {
			let path = element.data?.docPath ?? '';
			if (path !== '') {
				this.getSubCollection(path).subscribe((child: TreeNode[]) => {
					element.children = child;
					this.loadDeepCollection(child);
				});
			}
		});
	}

	getAll() {
		return this.getSubCollection('');
	}

	getSubCollection(path: string) {
		let colPath = `${path}/Collection`;
		return this.db
			.collection(colPath, ref => ref.where('isDeleted', '==', false).orderBy('index'))
			.snapshotChanges()
			.pipe(
				map(actions =>
					actions.map(a => {
						const data = new Collection(a.payload.doc.data()).displayCollection();
						data.id = a.payload.doc.id;
						data.docPath = a.payload.doc.ref.path;
						data.colPath = colPath;
						const newNode: TreeNode<any> = {
							data: data,
						};
						return newNode;
					})
				)
			)
			.pipe(
				map(nodes => {
					this.loadDeepCollection(nodes);
					return nodes;
				})
			);
	}

	newCollection(collections: TreeNode<any>[]) {
		collections.forEach(collection => {
			let data = new Collection(collection.data);
			data.createdAt = Timestamp.now();
			data.modifiedAt = Timestamp.now();
			data.isDeleted = false;
			let path = collection.data.docPath || this.nextId();
			this.db
				.doc(path)
				.set(Object.assign({}, data))
				.then(_ => console.log('success'))
				.catch(err => console.log(err, 'You dont have access!'));
		});
	}

	updateCollections(collections: TreeNode<any>[]) {
		collections.forEach(collection => {
			if (collection.data.name !== collection.data.nameOriginal || collection.data.note !== collection.data.noteOriginal) {
				let data = new Collection(collection.data);
				data.modifiedAt = Timestamp.now();
				let path = collection.data.docPath || this.nextId();
				this.db
					.doc(path)
					.set(Object.assign({}, data))
					.then(_ => console.log('success'))
					.catch(err => console.log(err, 'You dont have access!'));
			}
		});
	}

	deleteCollections(collections: TreeNode<any>[]) {
		collections.forEach(collection => {
			let data = new Collection(collection.data);
			data.modifiedAt = Timestamp.now();
			data.isDeleted = true;
			let path = collection.data.docPath || this.nextId();
			this.db
				.doc(path)
				.set(Object.assign({}, data))
				.then(_ => console.log('success'))
				.catch(err => console.log(err, 'You dont have access!'));
		});
	}

	saveCollection(newCollections: TreeNode<any>[], updateCollections: TreeNode<any>[], deleteCollections: TreeNode<any>[]) {
		this.newCollection(newCollections);
		this.updateCollections(updateCollections);
		this.deleteCollections(deleteCollections);
	}
}
