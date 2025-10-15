import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ErrorService } from './error.service';
@Component({
  selector: 'app-error-alert',
  imports: [CommonModule],
  templateUrl: 'error-alert.component.html',
  styleUrl: 'error-alert.component.scss'
})
export class ErrorAlertComponent {
  constructor(private errorService: ErrorService) {
    this.errorService.error$.subscribe((message) => {
      this.message = message;
      console.log("errorSub: " + message )

    });

  }
  message: string | null = null;

  close() {
    this.errorService.clearError();
  }
}