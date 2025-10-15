import { Injectable } from '@angular/core';
import { ApiService } from '../api-service/api.service';
import { forkJoin, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SettingsServiceService {

  pre_prompt: string = ""

  rag_data_path : string = ""

  rag_prompt: string = ""
  semantic_memory_prompt: string = ""
  direct_memory_prompt: string = ""

  rag_count: number = 0
  semantic_memory_count: number = 0
  direct_memory_count: number = 0


  do_rag: boolean = false;
  do_semantic_memory: boolean = false;
  do_direct_memory: boolean = false;

  ragprompt_activate_label: string = ""

  constructor(private apiService: ApiService) { 
    this.apiService.get_config_param("prompting", "pre_prompt").subscribe({ next: (data) => {this.pre_prompt = data.value}})
  }

  setRagPrompt(value: string) {
    this.rag_prompt = value
  }
  setRagCount(value: number) {
    this.rag_count = value
  }

  setSemanticPrompt(value: string) {
    this.semantic_memory_prompt = value
  }
  setSemanticCount(value: number) {
    this.semantic_memory_count = value
  }

  setDirectPrompt(value: string) {
    this.direct_memory_prompt = value
  }
  setDirectCount(value: number) {
    this.direct_memory_count = value
  }
  
  updateRagSettings() {
    const Prompt$ = this.apiService.get_config_param("prompting", "rag_prompt");
    const Count$ = this.apiService.get_config_param("rag", "rag_count");
    const Path$ = this.apiService.get_config_param("rag", "data_path");

    return forkJoin([Prompt$, Count$, Path$]).pipe(
      map(([PromptData, CountData, PathData]) => {
        this.setRagPrompt(PromptData.value)
        this.setRagCount(CountData.value)
        this.rag_data_path = PathData.value;
        return { prompt: this.rag_prompt, count: this.rag_count, data_path: this.rag_data_path};
      })
    );
  }

  updateSemanticMemorySettings() {
    const Prompt$ = this.apiService.get_config_param("prompting", "semantic_memory_prompt");
    const Count$ = this.apiService.get_config_param("memory", "semantic_memory_count");
  
    return forkJoin([Prompt$, Count$]).pipe(
      map(([PromptData, CountData]) => {
        this.setSemanticPrompt(PromptData.value)
        this.setSemanticCount(CountData.value)
        return { prompt: this.semantic_memory_prompt, count: this.semantic_memory_count };
      })
    );
  }

  updateDirectMemorySettings() {
    const Prompt$ = this.apiService.get_config_param("prompting", "direct_memory_prompt");
    const Count$ = this.apiService.get_config_param("memory", "direct_memory_count");
  
    return forkJoin([Prompt$, Count$]).pipe(
      map(([PromptData, CountData]) => {
        this.setDirectPrompt(PromptData.value)
        this.setDirectCount(CountData.value)
        return { prompt: this.direct_memory_prompt, count: this.direct_memory_count };
      })
    );

  }

  isRagPromptActivate() {
    return this.do_rag
  }

  toggle_do_rag() {
    this.do_rag = !this.do_rag
  }
}
