import { Component } from '@angular/core';
import { SettingsServiceService } from '../../services/settings-service/settings-service.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { fadeInOut, slideIn, slideHorizontal, zoomInOut, collapseVertical, rotateInOut, flipInOut, delayedFadeIn, slideUp, popIn, bounceIn, fadeLoop, collapseHorizontal, wipeIn, dropTop, dropBottom, shake, flash, pop } from '../../animation/animations'; // adapte le chemin
import { ApiService } from '../../services/api-service/api.service';

@Component({
  selector: 'app-settings',
  imports: [FormsModule, CommonModule],
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.scss',
  animations: [fadeInOut, slideIn, slideHorizontal, zoomInOut, collapseVertical, rotateInOut, flipInOut, delayedFadeIn, slideUp, popIn, bounceIn, fadeLoop, collapseHorizontal, wipeIn, dropTop, dropBottom, shake, flash, pop]
  
})
export class SettingsComponent {

  openExtraSettings: boolean = false;
  doError: boolean = false;
  constructor(public settingService: SettingsServiceService, private apiService: ApiService) { this.refreshSettings() }

  dirtySections = {
    rag: false,
    directMemory: false,
    semanticMemory: false
  };
  markDirty(section: 'rag' | 'directMemory' | 'semanticMemory') {
    this.dirtySections[section] = true;
  }

  saveSetting(section: 'rag' | 'directMemory' | 'semanticMemory') {
    console.log(`Saving settings for: ${section}`, this.settingService);

    if (section == 'rag') {
      this.apiService.set_config_param("prompting", "rag_prompt", this.settingService.rag_prompt).subscribe({
        next: (data) => { this.apiService.set_config_param("rag", "rag_count", String(this.settingService.rag_count)).subscribe({
          next: (data) => {  this.apiService.set_config_param("rag", "data_path", this.settingService.rag_data_path).subscribe({
            next: (data) => {this.settingService.updateRagSettings()},
            error: (err) => {this.settingService.updateRagSettings()},
          }) }, error: (err) => { this.settingService.updateRagSettings() }
        })
        }, error: (err) => { this.settingService.updateRagSettings()}
      })
    }

    if (section == 'directMemory') {
      this.apiService.set_config_param("prompting", "direct_memory_prompt", this.settingService.direct_memory_prompt).subscribe({
        next: (data) => { this.apiService.set_config_param("memory", "direct_memory_count", String(this.settingService.direct_memory_count)).subscribe({
          next: (data) => { this.settingService.updateDirectMemorySettings() }, error: (err) => {this.settingService.updateDirectMemorySettings()}
        })
        }, error: (err) => { this.settingService.updateDirectMemorySettings()}
      })
    }

    if (section == 'semanticMemory') {
      this.apiService.set_config_param("prompting", "semantic_memory_prompt", this.settingService.semantic_memory_prompt).subscribe({
        next: (data) => { this.apiService.set_config_param("memory", "semantic_memory_count", String(this.settingService.semantic_memory_count)).subscribe({
          next: (data) => { this.settingService.updateSemanticMemorySettings() }, error: (err) => {this.settingService.updateSemanticMemorySettings()}
        })
        }, error: (err) => { this.settingService.updateSemanticMemorySettings()}
      })
    }

    // Ex: this.settingsApi.save(this.settingService).subscribe(() => { ... });

    this.dirtySections[section] = false; // Reset l'état après sauvegarde
  }

  refreshSettings() {
    this.settingService.updateRagSettings().subscribe({error: (err) => this.doError = true})
    this.settingService.updateSemanticMemorySettings().subscribe({error: (err) => this.doError = true})
    this.settingService.updateDirectMemorySettings().subscribe({error: (err) => this.doError = true})
  }

  semanticMemoryEnabled() { return this.settingService.do_semantic_memory }
  directMemoryEnabled() { return this.settingService.do_direct_memory }
  isRagPromptActivate() { return this.settingService.do_rag }
  getPrePrompt() { return this.settingService.pre_prompt }
  getRagPrompt() { return this.settingService.rag_prompt }

  toggleExtraSettings() { this.openExtraSettings = !this.openExtraSettings }
  toggleRag() { this.settingService.do_rag = !this.settingService.do_rag }
  toggleDirectMemory() { this.settingService.do_direct_memory = !this.settingService.do_direct_memory }
  toggleSemanticMemory() { this.settingService.do_semantic_memory = !this.settingService.do_semantic_memory }
  
  reload_rag() { this.apiService.reload_rag().subscribe({next: (data) => {}}) }
}
