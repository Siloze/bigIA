import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  apiURL = 'http://127.0.0.1:5000'
  constructor(private http: HttpClient) {}

  sendQuestion(question: string, pre_prompt: string, rag_prompt: string, file: File | null = null, do_websearch: boolean, doUseRag: boolean) {
    const formData = new FormData();
    formData.append('question', question);
    formData.append('pre_prompt', pre_prompt);
    formData.append('rag_prompt', rag_prompt);
    formData.append('web_search', String(do_websearch));
    formData.append('use_rag', String(doUseRag));

    if (file) {
      formData.append('fichier', file, file.name);
    }

    console.log("request: ")
    console.log("question " + question + "\npre_prompt: " + pre_prompt + "\nrag_prompt: " + rag_prompt + "\web_search:" + String(do_websearch), "\nUse_rag: " + String(doUseRag))
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
