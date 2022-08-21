import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MenuItem, Message, TreeNode } from 'primeng/api';
import { ContextMenu } from 'primeng/contextmenu';
import { TreeTable } from 'primeng/treetable';
import { CollectionService } from '../service/collection.service';
import * as cloneDeep from 'lodash/cloneDeep';
import { CollectionDisplay, Vocabulary, Mode, VocabularyDisplay } from '../model/collection.model';
import { TreeNodeService } from '../service/treenode.service';
import { MessagesService } from '../service/message.service';
import { deepCopy } from '@firebase/util';
import { CommonService } from '../service/common.service';
import { HelperService } from '../service/helper.service';
@Component({
	selector: 'app-collection-import',
	templateUrl: './collection-import.component.html',
	styleUrls: ['./collection-import.component.scss'],
})
export class CollectionImportComponent implements OnInit {
	@ViewChild('#tt') treeTable: TreeTable;
	@ViewChild('#tt') treeTableRef: ElementRef;
	@ViewChild('#cm') contextMenu: ContextMenu;

	mode = 0;
	vocabularyList: VocabularyDisplay[] = [];
	collectionList: TreeNode[] = [];
	newCollections: TreeNode<any>[];
	updateCollections: TreeNode<any>[];
	deleteCollections: TreeNode<any>[];
	collectionTopicSelection: TreeNode;
	collectionEditing: TreeNode;
	displayCollectionModal = false;
	selectedNode: any = null;
	collectionManagementCols: any[];
	vocabularyCols: any[];
	menuItems: MenuItem[];
	tempMenuItems: MenuItem[];
	msgs: Message[] = [];
	errorMessage = '';
	collectionManagementTempList: TreeNode[];
	collectionSelected: any;
	collectionSelectedName = '';
	displayVocabularyModal = false;
	vocabularySelected = new VocabularyDisplay({});
	vocabulariesSelected: VocabularyDisplay[] = [];
	partOfSpeech: any[] = [];
	partOfSpeechSelected: VocabularyDisplay;
	isFocus = false;
	constructor(
		private common: CommonService,
		private treeNodeService: TreeNodeService,
		private collectionService: CollectionService,
		private messagesService: MessagesService,
		private helper: HelperService
	) {}

	ngOnInit(): void {
		this.collectionManagementCols = [
			{ field: 'name', header: 'Name', width: '250px', align: 'left' },
			{ field: 'note', header: 'Note', width: '250px', align: 'left' },
			{ field: 'size', header: 'Total Words', width: '140px', align: 'center' },
			{ field: 'createdDate', header: 'Created', width: '150px', align: 'left' },
			{ field: 'modifiedDate', header: 'Modified', width: '150px', align: 'left' },
		];
		this.vocabularyCols = [
			{ field: 'word', header: 'Word', width: '200px', align: 'left' },
			{ field: 'phonetic', header: 'Phonetic', width: '100px', align: 'left' },
			{ field: 'pos', header: 'Pos', width: '120px', align: 'left' },
			{ field: 'meaning', header: 'Meaning', width: '250px', align: 'left' },
			{ field: 'stem', header: 'Stem', width: '100px', align: 'left' },
			{ field: 'note', header: 'Note', width: '200px', align: 'left' },
			{ field: 'exampleDisplay', header: 'Examples', width: '250px', align: 'left' },
			{ field: 'antonymDisplay', header: 'Antonyms', width: '150px', align: 'left' },
			{ field: 'synonymDisplay', header: 'Synonyms', width: '100px', align: 'left' },
			{ field: 'createdDate', header: 'Created At', width: '140px', align: 'left' },
			{ field: 'modifiedDate', header: 'Modified At', width: '140px', align: 'left' },
		];

		this.loadPos();
	}

	loadPos() {
		this.partOfSpeech = this.common.loadPartOfSpeech();
	}

	isLastNode(): boolean {
		if (this.selectedNode?.parent === null) {
			return this.collectionList.indexOf(this.selectedNode) === this.collectionList.length - 1;
		} else {
			return this.selectedNode?.parent.children.indexOf(this.selectedNode) === this.selectedNode?.parent.children.length - 1;
		}
	}

	isFirstNode(): boolean {
		if (this.selectedNode?.parent === null) {
			return this.collectionList.indexOf(this.selectedNode) === 0;
		} else {
			return this.selectedNode?.parent.children.indexOf(this.selectedNode) === 0;
		}
	}

	onContextMenu(): void {
		this.tempMenuItems = [
			{
				label: 'Add',
				icon: 'pi pi-plus',
				items: [
					{ label: 'Add Sibling ', command: () => this.addSiblingRow() },
					{ label: 'Add Child', command: () => this.addChildRow() },
				],
			},
			{ label: 'Edit', icon: 'pi pi-pencil', command: () => this.editRow(), disabled: this.selectedNode.data.isEditing },
			{
				label: 'Move',
				icon: 'pi pi-sort-alt',
				items: [
					{ label: 'Move Up', command: () => this.moveUp(), disabled: this.isFirstNode() },
					{ label: 'Move Down', command: () => this.moveDown(), disabled: this.isLastNode() },
				],
				disabled: this.isFirstNode() && this.isLastNode(),
			},
			{ label: 'Delete', icon: 'pi pi-trash', command: () => this.deleteRow() },
		];
	}

	onContextMenuHide() {
		this.collectionList = cloneDeep(this.collectionList);
	}

	getEmptyNode() {
		let id = this.collectionService.nextId();
		let newCollection = new CollectionDisplay({ id: id });
		newCollection.isEditing = true;
		let newNode: TreeNode = {
			data: newCollection,
		};
		return newNode;
	}

	addItemToCollection(item: TreeNode<any>, collections: TreeNode<any>[]) {
		if (collections === undefined) {
			collections = [];
		}
		let index = collections.indexOf(item);
		if (index === -1) {
			collections.push(item);
		}
		return collections;
	}

	initCollection() {
		this.mode = Mode.Edit;
		let newNode = this.getEmptyNode();
		newNode.data.docPath = `Collection/${newNode.data.id}`;
		this.collectionList.push(newNode);
		this.addItemToCollection(newNode, this.newCollections);
		this.collectionList = cloneDeep(this.collectionList);
	}

	addSiblingRow() {
		this.mode = Mode.Edit;
		let newNode = this.getEmptyNode();
		newNode.data.colPath = this.selectedNode.data.colPath;
		newNode.data.docPath = `${this.selectedNode.data.colPath}/${newNode.data.id}`;
		if (this.selectedNode.parent === null) {
			let index = this.collectionList.indexOf(this.selectedNode);
			this.collectionList.splice(index + 1, 0, newNode);
			for (let i = index + 1; i < this.collectionList.length; i++) {
				this.collectionList[i].data.index = i;
			}
		} else {
			let parent = this.selectedNode.parent;
			let index = parent.children.indexOf(this.selectedNode);
			parent.children.splice(index + 1, 0, newNode);
			for (let i = index + 1; i < parent.children.length; i++) {
				parent.children[i].data.index = i;
			}
		}
		this.addItemToCollection(newNode, this.newCollections);
	}

	addChildRow() {
		this.mode = Mode.Edit;
		this.selectedNode.expanded = true;
		let newNode = this.getEmptyNode();
		newNode.data.colPath = `${this.selectedNode.data.docPath}/Collection`;
		newNode.data.docPath = `${this.selectedNode.data.docPath}/Collection/${newNode.data.id}`;
		if (this.selectedNode.children == null) {
			this.selectedNode.children = [];
		}
		newNode.data.index = this.selectedNode.children.length;
		this.selectedNode.children.push(newNode);
		this.addItemToCollection(newNode, this.newCollections);
	}

	moveDown(): void {
		this.mode = Mode.Edit;
		if (this.selectedNode.parent === null) {
			let index = this.collectionList.indexOf(this.selectedNode);
			if (index < this.collectionList.length - 1) {
				let nextNode = this.collectionList[index + 1];
				nextNode.data.index = index;
				this.selectedNode.data.index = index + 1;
				this.collectionList.splice(index, 1);
				this.collectionList.splice(index + 1, 0, this.selectedNode);
			}
		} else {
			let index = this.selectedNode.parent.children.indexOf(this.selectedNode);
			if (index < this.selectedNode.parent.children.length - 1) {
				let nextNode = this.selectedNode.parent.children[index + 1];
				nextNode.data.index = index;
				this.selectedNode.data.index = index + 1;
				this.selectedNode.parent.children.splice(index, 1);
				this.selectedNode.parent.children.splice(index + 1, 0, this.selectedNode);
			}
		}
		if (this.updateCollections === undefined) {
			this.updateCollections = [];
		}
		this.addItemToCollection(this.selectedNode, this.updateCollections);
	}

	moveUp(): void {
		this.mode = Mode.Edit;
		if (this.selectedNode.parent === null) {
			let index = this.collectionList.indexOf(this.selectedNode);
			if (index > 0) {
				let prevNode = this.collectionList[index - 1];
				prevNode.data.index = index;
				this.selectedNode.data.index = index - 1;
				this.collectionList.splice(index, 1);
				this.collectionList.splice(index - 1, 0, this.selectedNode);
			}
		} else {
			let index = this.selectedNode.parent.children.indexOf(this.selectedNode);
			if (index > 0) {
				let prevNode = this.selectedNode.parent.children[index - 1];
				prevNode.data.index = index;
				this.selectedNode.data.index = index - 1;
				this.selectedNode.parent.children.splice(index, 1);
				this.selectedNode.parent.children.splice(index - 1, 0, this.selectedNode);
			}
		}

		this.addItemToCollection(this.selectedNode, this.updateCollections);
	}

	editRow() {
		this.mode = Mode.Edit;
		this.selectedNode.data.isEditing = true;
		if (this.updateCollections === undefined) {
			this.updateCollections = [];
		}
		this.addItemToCollection(this.selectedNode, this.updateCollections);
	}

	deleteRow() {
		this.mode = Mode.Edit;
		if (this.selectedNode.parent === null) {
			let index = this.collectionList.indexOf(this.selectedNode);
			this.collectionList.splice(index, 1);
		} else {
			let parent = this.selectedNode.parent;
			let index = parent.children.indexOf(this.selectedNode);
			parent.children.splice(index, 1);
		}
		this.addItemToCollection(this.selectedNode, this.deleteCollections);
	}

	updateData(collections: TreeNode<any>[], collectionFlat: TreeNode<any>[]) {
		collections.forEach(node => {
			const id = node.data.id;
			const newData = collectionFlat.find(node => node.data.id === id);
			node.data.note = newData?.data.note;
			node.data.name = newData?.data.name;
		});
	}

	isValid(collectionFlat: TreeNode<any>[]): boolean {
		// check unique name
		let uniqueNames = new Set<string>();
		for (let collection of collectionFlat) {
			if (collection.data.name === undefined || collection.data.name === '') {
				this.errorMessage = 'Collection name is required';
				return false;
			}
			if (uniqueNames.has(collection.data.name)) {
				this.errorMessage = 'Collection name must be unique';
				return false;
			}
			uniqueNames.add(collection.data.name);
		}

		if (uniqueNames.size !== collectionFlat.length) {
			return false;
		}

		return true;
	}

	onSaveCollection() {
		let collectionFlat = this.treeNodeService.flattern(this.collectionList);
		if (!this.isValid(collectionFlat)) {
			this.messagesService.showError(this.errorMessage);
			return;
		}
		this.updateData(this.newCollections, collectionFlat);
		this.updateData(this.updateCollections, collectionFlat);
		this.collectionService.saveCollection(this.newCollections, this.updateCollections, this.deleteCollections);
		this.loadCollection();
		this.mode = Mode.Choose;
	}

	onCancel() {
		this.loadCollection();
	}

	showCollectionManagement() {
		this.displayCollectionModal = true;
		this.loadCollection();
	}

	loadCollection() {
		this.mode = Mode.Choose;
		this.newCollections = [];
		this.updateCollections = [];
		this.deleteCollections = [];
		this.collectionService.getAll().subscribe((data: TreeNode<any>[]) => {
			this.collectionList = data;
		});
	}

	getPathName(node: any): string {
		let names: string[] = [];
		if (node.parent !== null) {
			names.push(this.getPathName(node.parent));
		}
		names.push(node.data.name);
		return names.join(' > ');
	}

	chooseCollection() {
		this.displayCollectionModal = false;
		this.collectionSelected = this.selectedNode.data.docPath;
		this.collectionSelectedName = this.getPathName(this.selectedNode);
	}

	showVocabularyNew() {
		this.vocabularySelected = new VocabularyDisplay({ id: this.collectionService.nextId() });
		this.displayVocabularyModal = true;
	}

	isVocabularyValid(): boolean {
		this.errorMessage = '';
		if (this.vocabularySelected.word === undefined || this.vocabularySelected.word === '') {
			this.errorMessage = 'Word is required';
			return false;
		}

		if (this.vocabularySelected.meaning === undefined || this.vocabularySelected.meaning === '') {
			this.errorMessage = 'Meaning is required';
			return false;
		}

		for (let vocabulary of this.vocabularyList) {
			if (vocabulary.word === this.vocabularySelected.word) {
				this.errorMessage = 'Word is already exists';
				return false;
			}
		}

		return true;
	}
	onApply() {
		if (!this.isVocabularyValid()) {
			this.messagesService.showError(this.errorMessage);
			return;
		}
		if (this.vocabularyList === undefined) {
			this.vocabularyList = [];
		}
		this.vocabularyList.push(this.vocabularySelected);
		this.displayVocabularyModal = false;
		console.log(this.vocabularyList);
	}

	autoFill() {
		this.helper.getWordDefinitions(this.vocabularySelected.word).subscribe(data => {
			console.log(data);
		});
	}
}
