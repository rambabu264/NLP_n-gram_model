import { FormControl } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { map, startWith } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { WordsModel } from 'src/models/words';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  constructor(private http: HttpClient) {
    this.ngramwords = new WordsModel();
  }
  title = 'ngram';
  myControl = new FormControl('');
  wordsControl = new FormControl('');
  ngramwords: WordsModel;
  inputString = '';
  selectedWord: string = '';
  filteredWords?: string[];
  //options: string[] = ['One', 'Two', 'Three'];
  filteredOptions?: Observable<string[]>;
  ngramUrl: string = '/assets/words.json';

  ngOnInit() {
    // this.filteredOptions = this.myControl.valueChanges.pipe(
    //   startWith(''),
    //   map((value) => this._filter(value || ''))
    // );
    // this.filteredWords = this.wordsControl.valueChanges.pipe(
    //   startWith(''),
    //   map((value) => this._filterWords(value || ''))
    // );
    this.spellCheck();
  }
  onWordSelect(word: string) {
    console.log(word);
    console.log(this.inputString);
    this.inputString = this.inputString + ' ' + word;
  }
  // private _filter(value: string): string[] {
  //   const filterValue = value.toLowerCase();

  //   return this.options.filter((option) =>
  //     option.toLowerCase().includes(filterValue)
  //   );
  // }
  private _filterWords(value: string): string[] {
    const filterValue = value.toLowerCase();

    if (this.ngramwords.words != undefined) {
      return this.ngramwords.words.filter((word) =>
        word.toLowerCase().includes(filterValue)
      );
    } else {
      return [];
    }
  }

  public spellCheck(str: string = '') {
    let resp = this.getWords(str).subscribe({
      next: (result) => {
        this.ngramwords = result;
        this.filteredWords = this.ngramwords.words;
        console.log(result);
      },
    });
  }
  public getWords(str: string): Observable<WordsModel> {
    return this.http.get<WordsModel>(`${this.ngramUrl}?sent=${str}`, {
      responseType: 'json',
    });
    //return data;
  }
}
