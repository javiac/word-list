import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { API_URL } from '../env';
import { IWord } from './word.model';
import { Observable } from 'rxjs';

@Injectable()
export class WordsApiService {

  constructor(private http: HttpClient) {
  }

  public getWords(searchAnagram?: string): Observable<IWord[]> {
    const queryParams = searchAnagram !== undefined ? `?searchAnagram=${searchAnagram}` : '';
    return this.http.get<IWord[]>(`${API_URL}/words${queryParams}`);
  }

  public saveSortingChanges(data: any) {
    return this.http.post(`${API_URL}/words/sort`, data);
  }

  public delete(word: IWord) {
    return this.http.delete<IWord[]>(`${API_URL}/words`, { params: { id: word._id?.$oid ?? '' } });
  }

  public save(word: IWord) {
    let url = `${API_URL}/words`;

    if (word._id) {
      url += `/${word._id ? word._id?.$oid : ''}`;
    }
    return this.http.post<IWord[]>(url, word);
  }
}
