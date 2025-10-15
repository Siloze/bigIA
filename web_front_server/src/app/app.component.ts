import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ChatComponent } from './components/chat/chat.component';
import { ErrorAlertComponent } from './components/error-alert/error-alert.component';
@Component({
  selector: 'app-root',
  imports: [ChatComponent, ErrorAlertComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'llm_web_server';
  constructor(private router: Router){
    this.router.navigate(['/chat'])
  }
}
