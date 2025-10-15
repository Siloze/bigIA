import { Injectable } from '@angular/core';
import { ApiService } from '../api-service/api.service';

@Injectable({
  providedIn: 'root'
})
export class ChatServiceService {

  history : {question: string, answer: string, id: number}[] = [];
  discussions: {name: string, path: string, id: number}[] = [];
  current_discussion: {name: string, path: string, id: number} = {name: "", path: "", id: 0};

  constructor(private apiService: ApiService) {
    this.load_all_discussion();
  }

  load_history(discussion: {name: string, path: string, id: number}){
    return this.apiService.get_all_history(discussion.id).subscribe({ 
      next: (data: Array<{question: string, answer: string, id: number}>) => { 
        this.history = data;
        this.current_discussion = discussion;
      }
    })
  }

  load_discussion(id: number) {
    return this.apiService.get_discussion(id).subscribe({
      next: (data) => {
        this.load_history(data);
      }
    })
  } 


  load_all_discussion(){
    return this.apiService.get_all_discussions().subscribe({ next: (data: Array<{name: string, path: string, id: number}>) => {
          this.load_history( data[data.length - 1])
        this.discussions = data.reverse();
      }
    })
  }

  refresh_all_discussion() {
    return this.apiService.get_all_discussions().subscribe({ next: (data: Array<{name: string, path: string, id: number}>) => { 
        this.discussions = data.reverse();
      }
    })   
  }

  create_discussion() {
    return this.apiService.create_new_discussions().subscribe({
      next: (data) => {
        this.refresh_all_discussion();
        this.load_history(data);
      }
    })
  }

  delete_discussion(id: number) {
    return this.apiService.delete_discussion(id).subscribe({
      next: (data) => {
        this.refresh_all_discussion()
        this.current_discussion = this.discussions[this.discussions.length - 1]

      }
    })
  }
}
