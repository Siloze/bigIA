import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../llama_api/api.service';
@Component({
  selector: 'app-chat',
  imports: [FormsModule, CommonModule],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss'
})

export class ChatComponent {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  question = '';
  pre_prompt = '';
  rag_prompt = '';
  fichier: File | null = null;
  history : {question: string, answer: string}[] = []

  isWaitingAnwser: boolean = false;

  constructor(private apiService: ApiService) {
    this.refresh_history();
    this.apiService.get_config_param("prompting", "pre_prompt").subscribe({ next: (data) => {this.pre_prompt = data.value}})
    this.apiService.get_config_param("prompting", "rag_prompt").subscribe({ next: (data) => this.rag_prompt = data.value })

  }

  isWaiting() {
    return this.isWaitingAnwser
  }

  refresh_history(){
    this.apiService.get_all_history().subscribe({ next: (data) => this.history = data })
  }
  onFileSelected(event: any) {
    this.fichier = event.target.files[0];
  }

  sendQuestion() {
    this.isWaitingAnwser = true;
    this.history.push({question: this.question, answer: "Reflexion..."})
    this.apiService.sendQuestion(this.question, this.pre_prompt, this.rag_prompt, this.fichier!).subscribe({
      next: (data) => {this.refresh_history(); this.isWaitingAnwser = false;     this.scrollToBottom()   }
    })
    this.question = ""
  }

  scrollToBottom(): void {
    const element = this.scrollContainer.nativeElement;
    element.scrollTop = element.scrollHeight;
  }
}


