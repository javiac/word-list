import {Component, OnInit, OnDestroy} from '@angular/core';
import { Subscription } from 'rxjs';
import {CdkDragDrop, moveItemInArray} from '@angular/cdk/drag-drop';
import { Word } from './word.model';
import { WordsApiService } from './word-api.service';

interface ISortingChange{
  previousIndex: number;
  currentIndex: number;
}

@Component({
  selector: 'app-word-list',
  templateUrl: './word-list.component.html',
  styleUrls: ['./word-list.component.scss']
})
export class WordListComponent implements OnInit, OnDestroy {
  private wordListSubscribtion: Subscription|null = null;
  public words: Word[] = [];
  private sortingChanges: ISortingChange[] = [];
  private sortTimeout: number | null = null;
  private searchTimeout: number | null = null;
  public anagrams: string[] = [];

  constructor(private wordsApi: WordsApiService) {
  }

  ngOnInit() {
    this.wordListSubscribtion = this.wordsApi
      .getWords()
      .subscribe(res => {
          this.words = res;
        },
        console.error
      );
  }

  ngOnDestroy() {
    if (this.wordListSubscribtion){
      this.wordListSubscribtion.unsubscribe();
    }
  }

  public drop(event: CdkDragDrop<string[]>) {
    if (event.previousIndex === event.currentIndex){
      return;
    }

    moveItemInArray(this.words, event.previousIndex, event.currentIndex);

    this.sortingChanges.push({previousIndex: event.previousIndex, currentIndex: event.currentIndex});

    if (this.sortTimeout){
      window.clearTimeout(this.sortTimeout);
    }

    this.sortTimeout = window.setTimeout(() => {
      this.wordsApi.saveSortingChanges([...this.sortingChanges]).subscribe(() => {
        return;
      });
      this.sortingChanges = [];
    }, 500);
  }

  public onSearch(event: Event){
    if (event.target){
      if (this.searchTimeout){
        window.clearTimeout(this.searchTimeout);
      }

      this.searchTimeout = window.setTimeout(() => {
        this.anagrams = [];
        this.wordsApi.getAnagrams((event.target  as HTMLInputElement).value).subscribe((result: any) => {
          this.anagrams = result;
        });
      }, 500);
    }
  }
}
