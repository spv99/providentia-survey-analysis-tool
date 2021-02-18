import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomepageCardsComponent } from './homepage-cards/homepage-cards.component';
import { HeaderComponent } from './header/header.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { DetailsPageComponent } from './details-page/details-page.component';
import { HttpClientModule } from '@angular/common/http';
import { ProvidentiaComponent } from './providentia/providentia.component';
import { ProvidentiaService } from './providentia/providentia.service';
import { AnalyticsService } from './details-page/details-page.service';

@NgModule({
  entryComponents: [
    HomepageCardsComponent
  ],
  declarations: [
    AppComponent,
    HeaderComponent,
    HomepageCardsComponent,
    DetailsPageComponent,
    ProvidentiaComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [ProvidentiaService, AnalyticsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
