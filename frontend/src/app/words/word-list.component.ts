import {Component, OnInit, OnDestroy} from '@angular/core';
import { Subscription } from 'rxjs';
import {CdkDragDrop, moveItemInArray} from '@angular/cdk/drag-drop';
import { IWord, Word } from './word.model';
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
  public words: IWord[] = [];
  private sortingChanges: ISortingChange[] = [];
  private sortTimeout: number | null = null;
  private searchTimeout: number | null = null;
  public anagrams: string[] = [];
  public wordEditing: IWord | null = null;
  public newWord: string | null = null;

  constructor(private wordsApi: WordsApiService) {
  }

  ngOnInit() {
    this.wordListSubscribtion = this.wordsApi
      .getWords()
      .subscribe(result => {
          this.words = result;
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
        this.wordsApi.getWords((event.target  as HTMLInputElement).value).subscribe((result: IWord[]) => {
          this.anagrams = result.map(word => word.value);
        });
      }, 500);
    }
  }

  public onDelete(word: IWord){
    this.wordsApi.delete(word).subscribe(result => {
      this.words = result;
    });
  }

  public onEdit(word: IWord){
    this.wordEditing = word;
  }

  public onUpdate(word: IWord){
    this.wordsApi.save(word).subscribe(result => {
      this.words = result;
      this.wordEditing = null;
    });
  }

  public onSave(){
    if (!this.newWord){
      return;
    }

    const newWord: IWord = {
      value: this.newWord,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    this.wordsApi.save(newWord).subscribe(result => {
      this.words = result;
      this.newWord = null;
    });
  }
}
