import { Component } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { ChatComponent } from './chat/chat.component';
@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ChatComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'llm_web_server';
  constructor(private router: Router){
    this.router.navigate(['/chat'])
  }
}
