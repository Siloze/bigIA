import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ErrorService {
  constructor() {}

  private errorSubject = new BehaviorSubject<string | null>(null);
  error$ = this.errorSubject.asObservable();

  showError(status: number, message: string) {
      this.errorSubject.next(message);
  }

  clearError() {
    this.errorSubject.next(null);
  }

}