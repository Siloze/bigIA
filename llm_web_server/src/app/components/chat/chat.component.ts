import { ChangeDetectorRef, Component, ElementRef, NgZone, OnInit, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api-service/api.service';
import { DomSanitizer } from '@angular/platform-browser';
import { fadeInOut, slideIn, slideHorizontal, zoomInOut, collapseVertical, rotateInOut, flipInOut, delayedFadeIn, slideUp, popIn, bounceIn, fadeLoop, collapseHorizontal, wipeIn, dropTop, dropBottom, shake, flash, pop, rotateInLeft, rotateInRight } from '../../animation/animations'; // adapte le chemin
import { SettingsComponent } from '../settings/settings.component';
import { SettingsServiceService } from '../../services/settings-service/settings-service.service';
import { ChatListComponent } from '../chat-list/chat-list.component';
import { ChatServiceService } from '../../services/chat-service/chat-service.service';

@Component({
  selector: 'app-chat',
  imports: [FormsModule, CommonModule, SettingsComponent, ChatListComponent],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss',
  animations: [rotateInLeft, rotateInRight, fadeInOut, slideIn, slideHorizontal, zoomInOut, collapseVertical, rotateInOut, flipInOut, delayedFadeIn, slideUp, popIn, bounceIn, fadeLoop, collapseHorizontal, wipeIn, dropTop, dropBottom, shake, flash, pop]
})

export class ChatComponent {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  question = '';
  do_websearch = false;
  fichier: File | null = null;
  mouse: any;

  questionSelected: number = -2
  isWaitingAnwser: boolean = false;
  openSetting: boolean = false;
  openHistories: boolean = false;

  constructor(private zone: NgZone, private chatService: ChatServiceService, private settingService: SettingsServiceService, private apiService: ApiService, private cdr: ChangeDetectorRef, private sanitizer: DomSanitizer) {
  }

  getHistory() { return this.chatService.history }

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

  toggleWebSearch() {
    this.do_websearch = !this.do_websearch
  }


  isWaiting() {
    return this.isWaitingAnwser
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
    this.chatService.history.push({question: question, answer: "", id: -1})
    const interval = setInterval(() => {
      if (this.index < toWrite.length) {
        const next_car = toWrite.at(this.index);
        if (next_car) {
          let last_message_question = this.chatService.history[this.chatService.history.length - 1].question
          let last_message_answer = this.chatService.history[this.chatService.history.length - 1].answer
          this.chatService.history.pop()
          if (last_message_answer !== undefined && last_message_question !== undefined) {
            last_message_answer = last_message_answer + next_car
            this.chatService.history.push({question: last_message_question, answer: last_message_answer, id: -1});
          }
        }
        this.index++;
      } else {
        clearInterval(interval);
        this.isWaitingAnwser = false;
        this.do_websearch = false;
        this.chatService.load_history(this.chatService.current_discussion);

      }
    }, 10);
  }

  getTrustHtml(texte: string) {
    return this.sanitizer.bypassSecurityTrustHtml(texte); 
  }

  showWaitingAnimation(question: string) {
    let nb_dot = 0;
    let max_dot = 0;
    this.chatService.history.at(this.chatService.history.length - 1)!.answer = "Reflexion";
    const interval = setInterval(() => {
      let wait_answer = "Reflexion"
      for (let index = 0; index < nb_dot; index++) {
        wait_answer += " . "
      }
      this.chatService.history.at(this.chatService.history.length - 1)!.answer = wait_answer;
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
  answer = ""

  sendQuestion() {
  if (this.isWaitingAnwser || !this.verifyInput(this.question)) return;

  this.question = this.question.trim();
  this.isWaitingAnwser = true;
  const question = this.question;
  this.question = "";

  this.scrollToBottom();
  this.answer = "";

  this.chatService.history.push({ question, answer: "", id: -1 });
  const lastMessage = this.chatService.history[this.chatService.history.length - 1];

  let answerBuffer = "";
  let updateScheduled = false;
  let anim_interval = this.showWaitingAnimation(question)

  this.zone.runOutsideAngular(() => {
    this.apiService.sendQuestion({
      pre_prompt: this.settingService.pre_prompt,
      question,
      chat_id: this.chatService.current_discussion.id,
      file: this.fichier,
      web_search: this.do_websearch,
    }).subscribe({
      next: (token) => {
        if (anim_interval) {
            clearInterval(anim_interval)
            this.chatService.history.at(this.chatService.history.length - 1)!.answer = "";

        }

        if (token === '[DONE]') {
          this.zone.run(() => {
            lastMessage.answer = answerBuffer;
            this.answer = '';
            this.isWaitingAnwser = false;
          });
          return;
        }

        answerBuffer += token;
        
        if (!updateScheduled && answerBuffer.length > 0) {
          updateScheduled = true;
          setTimeout(() => {
            this.zone.run(() => {
              this.answer = answerBuffer;
              updateScheduled = false;
            });
          }, 10); // Réduire la fréquence de mise à jour dans Angular
        }
      },
      error: (err) => {
        this.zone.run(() => {
          console.error("Erreur dans le stream", err);
          this.isWaitingAnwser = false;
        });
      }
    });
  });
}
  // sendQuestion() {
  //   if (this.isWaitingAnwser || !this.verifyInput(this.question))
  //       return ;
  //   this.question = this.question.trim();
  //   this.isWaitingAnwser = true;
  //   const question = this.question;
  //   this.question = "";

  //   this.scrollToBottom()
  //   //let anim_interval = this.showWaitingAnimation(question)
  //   this.answer = ""
  //   this.chatService.history.push({question: question, answer: this.answer, id: -1})

  //   let answerBuffer = ""
  //   this.apiService.sendQuestion({
  //     pre_prompt: this.settingService.pre_prompt, 
  //     question: question,
  //     chat_id: this.chatService.current_discussion.id,
  //     file: this.fichier, 

  //     web_search: this.do_websearch,
  //   }).subscribe({
  //     next: (token) => {
  //       console.log("token: " + token);
  //         if (token === '[DONE]') {
  //           this.chatService.history.at(this.chatService.history.length - 1)!.answer = answerBuffer
  //           this.answer = ""
  //           console.log('Flux terminé');
  //         } else {
  //           answerBuffer += token
  //           if (answerBuffer.length - this.answer.length >= 15)
  //             this.answer = answerBuffer
  //         }
  //       // if (token[0] == " ") {
  //       //   // this.chatService.history.pop()
  //       //   // this.chatService.history.push({question: question, answer: this.answer, id: -1})
  //       // }


  //       // const answer = data.answer
  //       // clearInterval(anim_interval)
  //       // this.chatService.history.pop()
  //       // this.newAnswer(question, answer)
  //     },
  //     error: (err) => {
  //       console.log("error: ")
  //       console.dir(err)
  //       // clearInterval(anim_interval)
  //       // this.chatService.history.pop()
  //       // this.chatService.history.push({question: question, answer: "Error when sending question, please retry.", id: -1})
  //       this.isWaitingAnwser = false;
  //       this.do_websearch = false;
  //     }
  //   })
  // }

  trackByEntry(index: number, entry: { id: number }): number {
  return entry.id;
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


