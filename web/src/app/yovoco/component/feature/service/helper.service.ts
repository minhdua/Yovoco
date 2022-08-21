import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map } from 'rxjs';
import { WordDefinition } from '../model/collection.model';

@Injectable({
	providedIn: 'root',
})
export class HelperService {
	constructor(private httpClient: HttpClient) {}

	getWordDefinitions(word: string) {
		return this.httpClient.get(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`).pipe(map((res: any) => <WordDefinition[]>res));
	}
}
