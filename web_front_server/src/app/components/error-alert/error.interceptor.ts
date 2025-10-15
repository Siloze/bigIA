import { inject } from '@angular/core';
import { HttpHandlerFn, HttpRequest } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { ErrorService } from './error.service';

export function errorInterceptor(req: HttpRequest<any>, next: HttpHandlerFn): Observable<any> {
  const errorService = inject(ErrorService);
  return next(req).pipe(
    catchError((error) => {
      console.dir(error)
      errorService.showError(error.status, error.message);
      return throwError(() => error);
    })
  );
}
