import { ChangeDetectorRef, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../llama_api/api.service';
import { DomSanitizer } from '@angular/platform-browser';
import { fadeInOut, slideIn, slideHorizontal, zoomInOut, collapseVertical, rotateInOut, flipInOut, delayedFadeIn, slideUp, popIn, bounceIn, fadeLoop, collapseHorizontal, wipeIn, dropTop, dropBottom, shake, flash } from '../animation/animations'; // adapte le chemin

@Component({
  selector: 'app-chat',
  imports: [FormsModule, CommonModule],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss',
  animations: [fadeInOut, slideIn, slideHorizontal, zoomInOut, collapseVertical, rotateInOut, flipInOut, delayedFadeIn, slideUp, popIn, bounceIn, fadeLoop, collapseHorizontal, wipeIn, dropTop, dropBottom, shake, flash]
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
  mouse: any;

  history : {question: string, answer: string, id: number}[] = [];
  discussions: {name: string, path: string, id: number}[] = [];
  current_discussion: {name: string, path: string, id: number} = {name: "", path: "", id: 0};

  questionSelected: number = -2
  isWaitingAnwser: boolean = false;
  openSetting: boolean = false;
  openHistories: boolean = false;

  constructor(private apiService: ApiService, private cdr: ChangeDetectorRef, private sanitizer: DomSanitizer) {
    this.load_all_discussion();
    this.apiService.get_config_param("prompting", "pre_prompt").subscribe({ next: (data) => {this.pre_prompt = data.value}})
    this.apiService.get_config_param("prompting", "rag_prompt").subscribe({ next: (data) => { 
      this.rag_prompt = data.value 
      if (this.rag_prompt.length) {
        this.do_rag = true;
        this.updateRagPromptActivateLabel();
      }
    }})
  }

  toggle_setting() {
    this.openSetting = !this.openSetting;
  }

  toggle_histories() {
    this.openHistories = !this.openHistories;
  }
  isSettingOpen() {
    return this.openSetting;
  }

  isHistoriesOpen() {
    return this.openHistories;
  }

  isQuestionSelected(id: number) {
    return id === this.questionSelected && id >= 0
  }

  getEditText(id: number) {
    if (this.isQuestionSelected(id)) {
      return "Edit"
    }
    return " "
  }
  mouseOverMessage(event: any, id: number) {
    this.questionSelected = id;
  }

  mouseLeaveMessage(event: any, id: number) {
    this.questionSelected = -2;
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

  load_history(discussion: {name: string, path: string, id: number}){
    return this.apiService.get_all_history(discussion.id).subscribe({ 
      next: (data: Array<{question: string, answer: string, id: number}>) => { 
        this.history = data;
        this.current_discussion = discussion;
        this.scrollToBottom();
      }
    })
  }

  load_discussion(id: number) {
    if (this.isWaitingAnwser)
      return ;
    return this.apiService.get_discussion(id).subscribe({
      next: (data) => {
        this.load_history(data);
      }
    })
  } 

  load_all_discussion(){
    if (this.isWaitingAnwser)
      return ;
    return this.apiService.get_all_discussions().subscribe({ next: (data: Array<{name: string, path: string, id: number}>) => { 
        this.discussions = data;
        this.load_history( this.discussions[this.discussions.length - 1])
      }
    })
  }

  refresh_all_discussion() {
    return this.apiService.get_all_discussions().subscribe({ next: (data: Array<{name: string, path: string, id: number}>) => { 
        this.discussions = data;
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

  verifyInput(input: string) {
    if (!input.length || !input.trim().length) {
      return false;
    }
    return true;
  }

  index = 0;
  newAnswer(question: string, toWrite: string) {
    this.index = 0;
    this.history.push({question: question, answer: "", id: -1})
    const interval = setInterval(() => {
      if (this.index < toWrite.length) {
        const next_car = toWrite.at(this.index);
        if (next_car) {
          let last_message_question = this.history[this.history.length - 1].question
          let last_message_answer = this.history[this.history.length - 1].answer
          this.history.pop()
          if (last_message_answer !== undefined && last_message_question !== undefined) {
            last_message_answer = last_message_answer + next_car
            this.history.push({question: last_message_question, answer: last_message_answer, id: -1});
          }
        }
        this.index++;
      } else {
        clearInterval(interval);
        this.isWaitingAnwser = false;
        this.do_websearch = false;
        this.load_history(this.current_discussion);

      }
    }, 10);
  }

  getTrustHtml(texte: string) {
    return this.sanitizer.bypassSecurityTrustHtml(texte); 
  }

  showWaitingAnimation(question: string) {
    let nb_dot = 0;
    let max_dot = 0;
    this.history.push({question: question, answer: "Reflexion", id: -1})
    const interval = setInterval(() => {
      this.history.pop();
      let wait_answer = "Reflexion"
      for (let index = 0; index < nb_dot; index++) {
        wait_answer += " . "
      }
      this.history.push({question: question, answer: wait_answer, id: -1})
      nb_dot++;

      if (nb_dot > max_dot) {
        max_dot = nb_dot;
        nb_dot = 0;
      }
      if (max_dot > 20) {
        max_dot = 0;
      }

    }, 200);
    return interval
  }

  sendQuestion() {
    if (this.isWaitingAnwser || !this.verifyInput(this.question))
        return ;
    this.question = this.question.trim();
    this.isWaitingAnwser = true;
    const question = this.question;
    this.question = "";

    this.scrollToBottom()
    
    let anim_interval = this.showWaitingAnimation(question)

    this.apiService.sendQuestion(question, this.pre_prompt, this.rag_prompt, this.fichier, this.do_websearch, this.do_rag, this.current_discussion.id).subscribe({
      next: (data) => {
        const answer = data.answer
        clearInterval(anim_interval)
        this.history.pop()
        this.newAnswer(question, answer)
      }
    })
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


