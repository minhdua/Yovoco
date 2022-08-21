import { Injectable } from '@angular/core';

@Injectable({
	providedIn: 'root',
})
export class CommonService {
	constructor() {}

	loadPartOfSpeech() {
		return [
			{ label: 'Unknown', value: 'unknown' },
			{ label: 'Noun', value: 'noun' },
			{ label: 'Verb', value: 'verb' },
			{ label: 'Adjective', value: 'adjective' },
			{ label: 'Adverb', value: 'adverb' },
			{ label: 'Conjunction', value: 'conjunction' },
			{ label: 'Preposition', value: 'preposition' },
			{ label: 'Interjection', value: 'interjection' },
			{ label: 'Pronoun', value: 'pronoun' },
			{ label: 'Determiner', value: 'determiner' },
			{ label: 'Particle', value: 'particle' },
			{ label: 'Numeral', value: 'numeral' },
			{ label: 'Exclamation', value: 'exclamation' },
			{ label: 'Question', value: 'question' },
			{ label: 'Symbol', value: 'symbol' },
		];
	}
}
