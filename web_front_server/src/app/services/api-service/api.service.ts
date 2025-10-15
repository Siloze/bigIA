import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  apiURL = 'http://127.0.0.1:5000'
  constructor(private http: HttpClient) {}

  // sendQuestion(body: {
  //   question: string, 

  //   file: File | null, 
  //   web_search: boolean, 
  //   chat_id: number,
  
  //   pre_prompt: string,

  // }) {
  //   const formData = new FormData();
  //   formData.append('question', body.question);

  //   formData.append('web_search', String(body.web_search));
  //   formData.append('id', String(body.chat_id));
  //   if (body.file) { formData.append('fichier', body.file, body.file.name); }

  //   formData.append('pre_prompt', body.pre_prompt);

  //   return this.http.post<any>(`${this.apiURL}/response`, formData);
  // }

  sendQuestion(body: {
  question: string,
  file: File | null,
  web_search: boolean,
  chat_id: number,
  pre_prompt: string,
}): Observable<string> {
  // On construit les query params (SSE ne supporte pas FormData directement)
  const params = new URLSearchParams();
  params.set('question', body.question);
  params.set('web_search', String(body.web_search));
  params.set('id', String(body.chat_id));
  params.set('pre_prompt', body.pre_prompt);

  const url = `${this.apiURL}/response?${params.toString()}`;

  return new Observable<string>((observer) => {
    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      observer.next(event.data);  // Chaque token reçu du backend
    };

    eventSource.onerror = (error) => {
      observer.error(error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  });
}

  get_all_history(id: number) {
    const params = {id}
    return this.http.get<any>(`${this.apiURL}/history`, { params });
  }

  get_discussion(id: number) {
    const params = {id}
    return this.http.get<any>(`${this.apiURL}/discussion`, {params});
  }

  get_all_discussions() {
    return this.http.get<any>(`${this.apiURL}/all_discussions`);
  }

  create_new_discussions() {
    return this.http.post<any>(`${this.apiURL}/all_discussions`, {})
  }

  delete_discussion(id: number) {
    return this.http.delete(`${this.apiURL}/discussion/${id}`);
  }

  renameDiscussion(id: number, newName: string) {
    return this.http.put(`${this.apiURL}/discussion/${id}`, { name: newName });
  }

  get_config_param(section: string, key: string) {
    const params = {section, key}
    return this.http.get<any>(`${this.apiURL}/config`, { params })
  }

  set_config_param(section: string, key: string, value: string) {
    const body = {section, key, value}
    return this.http.post<any>(`${this.apiURL}/config`, body)
  }

  reload_rag() {
    const body = {}
    return this.http.post<any>(`${this.apiURL}/rag/reload`, body)
  }
}
