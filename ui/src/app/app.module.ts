import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { UploadModal } from './modals/uploadModal/uploadModal.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  entryComponents: [
    UploadModal,
  ],
  declarations: [
    AppComponent,
    HeaderComponent,
    UploadModal
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    BrowserModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
