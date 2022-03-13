import { Directive, EventEmitter, HostBinding, HostListener, Output } from '@angular/core';

@Directive({
  selector: '[appDragAndDrop]'
})
export class DragAndDropDirective {

  @HostBinding('class.fileover') fileOver: boolean;
  @Output() fileDropped = new EventEmitter<any>();
  outside = true;

  constructor() { }

  @HostListener('dragover', ['$event']) onDragOver(event: DragEvent): void {
    if (this.outside) {
      const element = document.getElementById('dropBlock');
      element.classList.add('file-on-drag');
      this.outside = false;
    }
    event.preventDefault();
    event.stopPropagation();
  }

  @HostListener('dragleave', ['$event']) onDragLeave(event: DragEvent): void {
    this.outside = true;
    const element = document.getElementById('dropBlock');
    element.classList.remove('file-on-drag');
    event.preventDefault();
    event.stopPropagation();
  }

  @HostListener('drop', ['$event']) onDrop(event): void  {
    event.preventDefault();
    event.stopPropagation();
    const files = event.dataTransfer.files;

    if (files.length > 0) {
      this.fileDropped.emit(files);
    }
  }
}
