import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Router, RouterModule } from '@angular/router';
import { FormBuilder } from '@angular/forms';
import { Routes } from '@angular/router/router';
import { AppComponent } from '../app.component';
import { HeaderComponent } from '../header/header.component';
import { By } from '@angular/platform-browser';
import { ClusterInfo } from '../models/profile.model';
import { DetailsPageComponent } from '../details-page/details-page.component';
import { AnalyticsService } from '../details-page/details-page.service';
import { UserProfilesComponent } from '../details-page/user-profiles/user-profiles.component';
import { ProvidentiaComponent } from '../providentia/providentia.component';
import { ProvidentiaService } from '../providentia/providentia.service';
import { NoGraphViewComponent } from '../details-page/no-graph-view/no-graph-view.component';
import { ModalComponent } from '../reusable-modal/modal.component';

describe('HeaderComponent', () => {
  let component: HeaderComponent;
  let fixture: ComponentFixture<HeaderComponent>;

  const routes: Routes = [
    { path: '', redirectTo: 'providentia', pathMatch: 'full' },
    { path: 'providentia', component: ProvidentiaComponent},
    { path: 'providentia/results', component: HeaderComponent}
  ]
  
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DetailsPageComponent, 
                      ProvidentiaComponent,
                      NoGraphViewComponent,
                      ModalComponent,
                      HeaderComponent, 
                      AppComponent, 
                      UserProfilesComponent ],
      imports: [RouterModule.forRoot(routes)]
    })
    .compileComponents().then(() => {
      fixture = TestBed.createComponent(HeaderComponent);
      component = fixture.componentInstance;
    });;
  }));

  it('should render header', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const img = fixture.debugElement.nativeElement.querySelectorAll('img');

    //act

    // assert
    expect(component).toBeTruthy();
    expect(img[0]['src']).toContain('providentia-large.png');
  });
});