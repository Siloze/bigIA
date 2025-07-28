import { Component } from '@angular/core';
import { ChatServiceService } from '../../services/chat-service/chat-service.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-chat-list',
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-list.component.html',
  styleUrl: './chat-list.component.scss'
})
export class ChatListComponent {
  constructor(private chatService: ChatServiceService) {
    this.chatService.refresh_all_discussion();
  }

  create_discussion() { this.chatService.create_discussion() }
  delete_discussion(id: number) { this.chatService.delete_discussion(id) }
  load_discussion(id: number) { this.chatService.load_discussion(id) }

  getCurrentDiscussion() { return this.chatService.current_discussion }
  getDiscussions() { return this.chatService.discussions }

}
