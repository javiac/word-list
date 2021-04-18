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
  private timeout: number | null = null;

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

  drop(event: CdkDragDrop<string[]>) {
    if (event.previousIndex === event.currentIndex){
      return;
    }

    moveItemInArray(this.words, event.previousIndex, event.currentIndex);

    this.sortingChanges.push({previousIndex: event.previousIndex, currentIndex: event.currentIndex});

    if (this.timeout){
      window.clearTimeout(this.timeout);
    }

    this.timeout = window.setTimeout(() => {
      this.wordsApi.saveSortingChanges([...this.sortingChanges]).subscribe(() => {
        return;
      });
      this.sortingChanges = [];
    }, 1000);
  }
}
