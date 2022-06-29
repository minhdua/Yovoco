import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { TokenService } from './token.service';

const BACKEND_URL = environment.apiUrl + '/vocabularies/';

@Injectable({
  providedIn: 'root',
})
export class VocabularyService {
  constructor(private http: HttpClient, private tokenService: TokenService) {}

  search() {
    return this.http.get(BACKEND_URL, {
      headers: {
        Authorization: 'Bearer ' + this.tokenService.getAccessToken(),
      },
    });
  }
}
