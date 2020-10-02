import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { UploadModal } from './modals/uploadModal/uploadModal.component';
import { Project } from './models/project.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  public title = 'Providentia';
  public savedAnalytics: Project;

  constructor(private modalService: NgbModal) {}

  public ngOnInit() {}
  
  public open() {
    const modalRef = this.modalService.open(UploadModal, { centered: true });
  }

}

