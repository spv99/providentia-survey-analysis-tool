import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { DetailsPageComponent } from './details-page/details-page.component';
import { HttpClientModule } from '@angular/common/http';
import { ProvidentiaComponent } from './providentia/providentia.component';
import { ProvidentiaService } from './providentia/providentia.service';
import { AnalyticsService } from './details-page/details-page.service';
import { TagCloudModule } from 'angular-tag-cloud-module';
import { UserProfilesComponent } from './details-page/user-profiles/user-profiles.component';
import { NoGraphViewComponent } from './details-page/no-graph-view/no-graph-view.component';
import { ModalComponent } from './reusable-modal/modal.component';

@NgModule({
  entryComponents: [
  ],
  declarations: [
    AppComponent,
    HeaderComponent,
    DetailsPageComponent,
    ProvidentiaComponent,
    UserProfilesComponent,
    NoGraphViewComponent,
    ModalComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    TagCloudModule
  ],
  providers: [ProvidentiaService, AnalyticsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
