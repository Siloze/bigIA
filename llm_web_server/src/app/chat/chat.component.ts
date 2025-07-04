import { ChangeDetectorRef, Component, ElementRef, ViewChild } from '@angular/core';
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
  ragprompt_activate_label = '';
  do_rag = false;
  do_websearch = false;
  fichier: File | null = null;
  history : {question: string, answer: string}[] = []

  isWaitingAnwser: boolean = false;

  constructor(private apiService: ApiService, private cdr: ChangeDetectorRef) {
    this.refresh_history();
    this.apiService.get_config_param("prompting", "pre_prompt").subscribe({ next: (data) => {this.pre_prompt = data.value}})
    this.apiService.get_config_param("prompting", "rag_prompt").subscribe({ next: (data) => { 
      this.rag_prompt = data.value 
      if (this.rag_prompt.length) {
        this.do_rag = true;
        this.updateRagPromptActivateLabel();
      }
    }})

  }

  updateRagPromptActivateLabel() {
    if (this.do_rag)
        this.ragprompt_activate_label = "Désactiver le RAG"
    else
      this.ragprompt_activate_label = "Activer le RAG"
  }

  isRagPromptActivate() {
    return this.do_rag
  }

  toggleRagPromptActivate() {
    this.do_rag = !this.do_rag
    this.updateRagPromptActivateLabel()
  }

  toggleWebSearch() {
    this.do_websearch = !this.do_websearch
  }


  isWaiting() {
    return this.isWaitingAnwser
  }

  refresh_history(){
    this.apiService.get_all_history().subscribe({ next: (data) => { 
        this.history = data
        this.scrollToBottom()
      }
    })
  }
  onFileSelected(event: any) {
    this.fichier = event.target.files[0];
  }

  getFileName() {
    if (this.fichier) {
      return this.fichier.name
    } else {
      return ""
    }
  }

  sendQuestion() {
    this.isWaitingAnwser = true;
    this.history.push({question: this.question, answer: "Reflexion..."})
    this.scrollToBottom()
    this.apiService.sendQuestion(this.question, this.pre_prompt, this.rag_prompt, this.fichier, this.do_websearch, this.do_rag).subscribe({
      next: (data) => {
        this.refresh_history();
        this.isWaitingAnwser = false;
        this.do_websearch = false;
      }
    })
    this.question = ""
  }

  scrollToBottom(): void {
    // Force Angular à détecter les changements
    this.cdr.detectChanges();

    // Ensuite on attend la fin du DOM update
    setTimeout(() => {
      const element = this.scrollContainer.nativeElement;
      element.scrollTop = element.scrollHeight;
    }, 0);
  }
}


