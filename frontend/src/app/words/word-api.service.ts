import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {API_URL} from '../env';
import { Word } from './word.model';
import { Observable } from 'rxjs';

@Injectable()
export class WordsApiService {

  constructor(private http: HttpClient) {
  }

  private static handleError(err: HttpErrorResponse | any): void {
    throw new Error(err.message || 'Error: Unable to complete request.');
  }

  public getWords(): Observable<Word[]> {
    return this.http.get<Word[]>(`${API_URL}/words`);
  }

  public saveSortingChanges(data: any){
    return this.http.post(`${API_URL}/words/sort`, data);
  }

  public getAnagrams(value: string){
    return this.http.get(`${API_URL}/words/anagrams?value=${value}`);
  }
}
