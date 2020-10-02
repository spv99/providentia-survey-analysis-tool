import { Component } from "@angular/core";
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormGroup, FormBuilder, FormControl, Validators } from '@angular/forms';

@Component({
  selector: "upload-modal",
  templateUrl: "./uploadModal.component.html"
})
export class UploadModal {
  public  myForm: FormGroup;
  
  constructor(public activeModal: NgbActiveModal, private formBuilder: FormBuilder) {
      this.createForm();
  }

  private createForm() {
    this.myForm = this.formBuilder.group({
      username: '',
      password: ''
    });
  }
  private submitForm() {
    this.activeModal.close(this.myForm.value);
  }

}
