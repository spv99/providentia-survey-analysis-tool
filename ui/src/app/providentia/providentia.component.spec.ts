import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Router, RouterModule } from '@angular/router';
import { Routes } from '@angular/router/router';
import { AppComponent } from '../app.component';
import { HeaderComponent } from '../header/header.component';
import { UserProfilesComponent } from '../details-page/user-profiles/user-profiles.component';
import { ProvidentiaService } from '../providentia/providentia.service';
import { NoGraphViewComponent } from '../details-page/no-graph-view/no-graph-view.component';
import { ModalComponent } from '../reusable-modal/modal.component';
import { DetailsPageComponent } from '../details-page/details-page.component';
import { ProvidentiaComponent } from './providentia.component';

describe('ProvidentiaComponent', () => {
  let component: ProvidentiaComponent;
  let fixture: ComponentFixture<ProvidentiaComponent>;

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
      imports: [RouterModule.forRoot(routes)],
      providers: [{provide: ProvidentiaService},
                  {provide: Router}]
    })
    .compileComponents().then(() => {
      fixture = TestBed.createComponent(ProvidentiaComponent);
      component = fixture.componentInstance;
    });;
  }));

  it('should render landing page', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const img = fixture.debugElement.nativeElement.querySelectorAll('img');
    const header = fixture.debugElement.nativeElement.querySelectorAll('providentia-header');

    //act

    // assert
    expect(component).toBeTruthy();
    expect(header).toBeTruthy();
    expect(img.length).toBe(9);
    expect(render.textContent).toContain('Get insights into your data in seconds');
    expect(render.textContent).toContain('Upload');
  });
});