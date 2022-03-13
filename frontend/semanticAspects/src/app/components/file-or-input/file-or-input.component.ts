import { Component, Input, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FileModel } from '../../models/fileModel';

@Component({
  selector: 'app-file-or-input',
  templateUrl: './file-or-input.component.html',
  styleUrls: ['./file-or-input.component.scss']
})
export class FileOrInputComponent implements OnInit {

  @Input()
  files: FileModel[];

  addFileFormGroup: FormGroup;
  updateFileFormGroup: FormArray;

  constructor(private formBuilder: FormBuilder) {}

  public ngOnInit(): void {
    this.addFileFormGroup = this.formBuilder.group({
      recordFormControl: ['', Validators.required],
      recordNameFormControl: ['', Validators.required],
      isHtmlFormControl: [false, []],
    });
  }

  public getGroupFromArray(i: number): FormGroup {
    return this.updateFileFormGroup.controls[i] as FormGroup;
  }

  public addRecordToRecords($event: Event): void {
    if (this.addFileFormGroup.valid) {
      const fileModel = {
        name: this.addFileFormGroup.controls.recordNameFormControl.value,
        textResult: this.addFileFormGroup.controls.recordFormControl.value,
        appliedSegmentation: false,
        segmentationMethod: 'None',
        disallowedMethods: [],
        progress: 100,
        showed: false,
        size: 1,
        type:  this.addFileFormGroup.controls.isHtmlFormControl.value ? 'text/html' : 'text/plain',
        lastModified: Date.now().valueOf(),
        stream: null,
        arrayBuffer: null,
        slice: null,
        text: null,
        somSettings: undefined,
        webkitRelativePath: ''
      };

      this.files.push(fileModel);
      this.addFileFormGroup.reset();
    } else {
      console.log('Error: form for adding file is invalid!');
    }

    this.files.forEach(file => console.log(file.name));

    $event.preventDefault();
    $event.stopPropagation();
  }

  public updateRecord($event: Event, index: number, fileModel: FileModel): void {
    if (fileModel.textResult === undefined) {
      console.log('Please load content of file before saving hiting eye button');
      return;
    }

    const content = $event.target['recordContent' + index.toString()] ?
      $event.target['recordContent' + index.toString()].value : fileModel.textResult;
    this.files[index] = {
      name: $event.target['recordName' + index.toString()].value,
      textResult: content,
      appliedSegmentation: fileModel.appliedSegmentation,
      segmentationMethod: fileModel.segmentationMethod,
      disallowedMethods: [],
      progress: 100,
      showed: false,
      size: 1,
      type:  $event.target['updateIsHtml' + index.toString()].checked ? 'text/html' : 'text/plain',
      lastModified: Date.now().valueOf(),
      stream: null,
      arrayBuffer: null,
      slice: null,
      text: null,
      somSettings: undefined,
      webkitRelativePath: ''
    };

    $event.preventDefault();
    $event.stopPropagation();
  }

  public getFileContent(loadedFile: FileModel): void {
    if (loadedFile.text === null){
      if (loadedFile.textResult === undefined) {
        console.log('Error: content of file is not available!');
      }
    } else {
      loadedFile.text().then(content => loadedFile.textResult = content).catch(error => console.log(error));
    }
  }

  public processShowingFile(loadedFile: FileModel): void {
    console.log(loadedFile.type);
    if (loadedFile.progress === 100 && (loadedFile.type === 'text/plain' || loadedFile.type === 'text/html')){
      this.getFileContent(loadedFile);
      loadedFile.showed = true;
    } else if (loadedFile.progress !== 100) {
      console.log('Error: files are not loaded');
    } else if (loadedFile.type !== 'text/plain') {
      console.log('Error: type of content is not plain text! Type of content is: ' + loadedFile.type);
    }
  }
}
