import {Component, OnInit, OnDestroy} from '@angular/core';
import { Word } from './words/word.model';
import { WordsApiService } from './words/word-api.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  public title = 'app';
  private wordListSubscribtion: Subscription|null = null;
  public words: Word[] = [];

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
}
