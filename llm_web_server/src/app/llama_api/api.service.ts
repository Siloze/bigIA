import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  apiURL = 'http://127.0.0.1:5000'
  constructor(private http: HttpClient) {}

  sendQuestion(question: string, pre_prompt: string, rag_prompt: string, file: File) {
    const formData = new FormData();
    formData.append('question', question);
    formData.append('pre_prompt', pre_prompt);
    formData.append('rag_prompt', rag_prompt);

    if (file) {
      formData.append('fichier', file, file.name);
    }

    return this.http.post<any>(`${this.apiURL}/response`, formData);
  }

  get_all_history() {
    return this.http.get<any>(`${this.apiURL}/history`);
  }

  get_config_param(section: string, key: string) {
    const params = {section, key}
    return this.http.get<any>(`${this.apiURL}/config`, { params })
  }

  set_config_param(section: string, key: string, value: string) {
    const body = {section, key, value}
    return this.http.post<any>(`${this.apiURL}/config`, body)
  }
}
