import { Timestamp } from '@angular/fire/firestore';
import * as moment from 'moment';

// export class CollectionImport {
// 	id: number;
// 	collection: string;
// 	topic: string;
// 	word: string;
// 	phonetic: string;
// 	pos: string;
// 	meaning: string;
// 	example: string;
// 	synonyms: string;
// 	antonyms: string;
// 	stem: string;
// 	note: string;
// }

export class Phonetic {
	text: string;
	audio: string;
}

export class Definition {
	definition: string;
	example: string;
	synonyms: string[];
	antonyms: string[];
}
export class Meaning {
	partOfSpeech: string;
	definitions: Definition[];
}

export class WordDefinition {
	word: string;
	phonetic: string;
	phonetics: Phonetic[];
	origin: string;
	meanings: Meaning[];
}

export class Word {
	word: string;
	totalTimes: number;
	rightTimes: number;
	createdAt: Timestamp;
	modifiedAt: Timestamp;
	isDeleted: boolean;
}

export class Vocabulary {
	wordRef: string;
	index: number;
	phonetic: string;
	pos: string;
	definitions: string[];
	meaning: string;
	examples: string[];
	synonyms: string[];
	antonyms: string[];
	stem: string;
	note: string;
	createdAt: Timestamp;
	updatedAt: Timestamp;

	constructor(data: any) {
		this.wordRef = data.wordRef;
		this.index = data.index || 0;
		this.phonetic = data.phonetic || '';
		this.pos = data.pos || '';
		this.definitions = data.definitions || '';
		this.meaning = data.meaning || '';
		this.examples = data.examples || [];
		this.synonyms = data.synonyms || '';
		this.antonyms = data.antonyms || '';
		this.stem = data.stem || data.word || '';
		this.note = data.note || '';
		this.createdAt = data.createdAt || Timestamp.now();
		this.updatedAt = data.updatedAt || Timestamp.now();
	}

	displayVocabulary(Vocabulary: Vocabulary): VocabularyDisplay {
		return new VocabularyDisplay(Vocabulary);
	}
}

export class VocabularyDisplay extends Vocabulary {
	id: string;
	createdDate: string;
	modifiedDate: string;
	exampleDisplay: string;
	synonymsDisplay: string;
	antonymsDisplay: string;
	definitionDisplay: string;
	word: string;

	constructor(data) {
		super(data);
		this.id = data.id;
		this.word = data.word || '';
		this.createdDate = data && data.createdAt ? moment(data.createdAt.toDate()).format('DD/MM/YYYY') : '';
		this.modifiedDate = data && data.updatedAt ? moment(data.updatedAt.toDate()).format('DD/MM/YYYY') : '';
		this.exampleDisplay = data.examples ? data.examples.join('; ') : '';
		this.synonymsDisplay = data.synonyms ? data.synonyms.join('; ') : '';
		this.antonymsDisplay = data.antonym ? data.antonyms.join('; ') : '';
	}
}

export class Collection {
	name: string;
	index: number = 0;
	note: string;
	createdAt: Timestamp;
	modifiedAt: Timestamp;
	words: Vocabulary[];
	isDeleted: boolean = false;

	constructor(data: any) {
		this.name = data.name || '';
		this.index = data.index || 0;
		this.note = data.note || '';
		this.createdAt = data.createdAt;
		this.modifiedAt = data.modifiedAt;
		this.words = data.words || [];
		this.isDeleted = data.isDeleted || false;
	}

	newCollection(id: number): Collection {
		return new CollectionDisplay({ id: id });
	}

	displayCollection(): any {
		return new CollectionDisplay(this);
	}
}

export class CollectionDisplay extends Collection {
	id: string;
	nameOriginal: string;
	noteOriginal: string;
	size: number | string;
	createdDate: string;
	modifiedDate: string;
	isEditing: boolean;
	docPath: string;
	colPath: string;
	isChanged: boolean;
	isNew: boolean;

	constructor(data: any) {
		super(data);
		this.id = data.id;
		this.nameOriginal = data.name;
		this.noteOriginal = data.note;
		this.size = data.words ? this.words.length : '';
		this.createdDate = this.createdAt ? moment(this.createdAt.toDate()).format('DD/MM/YYYY') : '';
		this.modifiedDate = this.modifiedAt ? moment(this.modifiedAt.toDate()).format('DD/MM/YYYY') : '';
		this.isEditing = data.isEditing || false;
		this.docPath = data.path || '';
		this.colPath = data.colPath || '';
		this.isChanged = data.isChanged || false;
		this.isNew = data.isNew || false;
	}
}

export enum Mode {
	Choose,
	Edit,
}
