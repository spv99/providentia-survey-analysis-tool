import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Router, RouterModule } from '@angular/router';
import { FormBuilder } from '@angular/forms';
import { Routes } from '@angular/router/router';
import { AppComponent } from '../app.component';
import { ProvidentiaComponent } from '../providentia/providentia.component';
import { ProvidentiaService } from '../providentia/providentia.service';
import { DetailsPageComponent } from './details-page.component';
import { AnalyticsService } from './details-page.service';
import { NoGraphViewComponent } from './no-graph-view/no-graph-view.component';
import { ModalComponent } from '../reusable-modal/modal.component';
import { UserProfilesComponent } from './user-profiles/user-profiles.component';
import { HeaderComponent } from '../header/header.component';
import { By } from '@angular/platform-browser';
import { ClusterInfo } from '../models/profile.model';

describe('DetailsPageComponent', () => {
  let component: DetailsPageComponent;
  let fixture: ComponentFixture<DetailsPageComponent>;

  const routes: Routes = [
    { path: '', redirectTo: 'providentia', pathMatch: 'full' },
    { path: 'providentia', component: ProvidentiaComponent},
    { path: 'providentia/results', component: DetailsPageComponent}
  ]
  
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DetailsPageComponent, 
                      ProvidentiaComponent,
                      HeaderComponent, 
                      AppComponent, 
                      NoGraphViewComponent,
                      ModalComponent, 
                      UserProfilesComponent ],
      imports: [RouterModule.forRoot(routes)],
      providers: [
        { provide: AnalyticsService},
        { provide: FormBuilder},
        { provide: Router},
        { provide: ProvidentiaService}]
    })
    .compileComponents().then(() => {
      fixture = TestBed.createComponent(DetailsPageComponent);
      component = fixture.componentInstance;
    });;
  }));

  it('should render results page side navigation', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;

    //act

    // assert
    expect(component).toBeTruthy();
    expect(render.textContent).toContain('Insights Overview');
    expect(render.textContent).toContain('Univariate Analysis');
    expect(render.textContent).toContain('Bar Graphs');
    expect(render.textContent).toContain('Pie Charts');
    expect(render.textContent).toContain('Box Plots');
    expect(render.textContent).toContain('Free Text Analysis');
    expect(render.textContent).toContain('Sentiment Analysis');
    expect(render.textContent).toContain('Thematic Analysis');
    expect(render.textContent).toContain('Bivariate Analysis');
    expect(render.textContent).toContain('Bivariate Relationships');
    expect(render.textContent).toContain('Clustered Bar Graphs');
    expect(render.textContent).toContain('Stacked Bar Graphs');
    expect(render.textContent).toContain('Scatter Plots');
    expect(render.textContent).toContain('Multivariate Analysis');
    expect(render.textContent).toContain('Sunburst Chart');
    expect(render.textContent).toContain('Treemap Chart');
    expect(render.textContent).toContain('User Profiles');
  });

  it('should render default Insight Overview page on page load', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const table = fixture.nativeElement.querySelectorAll('table')
    const tableRows = fixture.nativeElement.querySelectorAll('tr');
    const openModalText = fixture.debugElement.query(By.css('.emphasis')).nativeElement;

    // act
    openModalText.click();

    // assert
    expect(render.querySelector('h3').textContent).toEqual('Insights Overview');
    expect(table).toBeTruthy();
    expect(tableRows.length).toBe(13);
    expect(component.modalConfig.modalTitle).toContain('Univariate, Bivariate and Multivariate Analysis');
  });

  it('should render bargraph iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const bargraph = fixture.debugElement.queryAll(By.css('.hover'))[1].nativeElement;
    const bargraphRender = fixture.debugElement.queryAll(By.css('.hide'))[0].nativeElement;

    // act
    bargraph.click();

    // assert
    expect(bargraph.textContent).toContain("Bar Graphs");
    expect(bargraphRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render piechart iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const piechart = fixture.debugElement.queryAll(By.css('.hover'))[2].nativeElement;
    const piechartRender = fixture.debugElement.queryAll(By.css('.hide'))[1].nativeElement;

    // act
    piechart.click();

    // assert
    expect(piechart.textContent).toContain("Pie Charts");
    expect(piechartRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render box plots iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const boxPlots = fixture.debugElement.queryAll(By.css('.hover'))[3].nativeElement;
    const boxPlotsRender = fixture.debugElement.queryAll(By.css('.hide'))[2].nativeElement;

    // act
    boxPlots.click();

    // assert
    expect(boxPlots.textContent).toContain("Box Plots");
    expect(boxPlotsRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render sentiment analysis charts iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const sentiments = fixture.debugElement.queryAll(By.css('.hover'))[4].nativeElement;
    const sentimentsRender = fixture.debugElement.queryAll(By.css('.hide'))[3].nativeElement;

    // act
    sentiments.click();

    // assert
    expect(sentiments.textContent).toContain("Sentiment Analysis");
    expect(sentimentsRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render thematic analysis charts iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const themes = fixture.debugElement.queryAll(By.css('.hover'))[5].nativeElement;
    const themesRender = fixture.debugElement.queryAll(By.css('.hide'))[4].nativeElement;

    // act
    themes.click();

    // assert
    expect(themes.textContent).toContain("Thematic Analysis");
    expect(themesRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render bivariate relationships chart iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const bivariateRelationship = fixture.debugElement.queryAll(By.css('.hover'))[6].nativeElement;
    const bivariateRelationshipRender = fixture.debugElement.queryAll(By.css('.hide'))[5].nativeElement;

    // act
    bivariateRelationship.click();

    // assert
    expect(bivariateRelationship.textContent).toContain("Bivariate Relationships");
    expect(bivariateRelationshipRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render clustered bar graphs iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const clustered = fixture.debugElement.queryAll(By.css('.hover'))[7].nativeElement;
    const clusteredRender = fixture.debugElement.queryAll(By.css('.hide'))[6].nativeElement;

    // act
    clustered.click();

    // assert
    expect(clustered.textContent).toContain("Clustered Bar Graphs");
    expect(clusteredRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render stacked bar graphs iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const stacked = fixture.debugElement.queryAll(By.css('.hover'))[8].nativeElement;
    const stackedRender = fixture.debugElement.queryAll(By.css('.hide'))[7].nativeElement;

    // act
    stacked.click();

    // assert
    expect(stacked.textContent).toContain("Stacked Bar Graph");
    expect(stackedRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render scatter plots iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const scatter = fixture.debugElement.queryAll(By.css('.hover'))[9].nativeElement;
    const scatterRender = fixture.debugElement.queryAll(By.css('.hide'))[8].nativeElement;

    // act
    scatter.click();

    // assert
    expect(scatter.textContent).toContain("Scatter Plots");
    expect(scatterRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render sunburst chart iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const sunburstPlots = fixture.debugElement.queryAll(By.css('.hover'))[10].nativeElement;
    const sunburstPlotsRender = fixture.debugElement.queryAll(By.css('.hide'))[9].nativeElement;

    // act
    sunburstPlots.click();

    // assert
    expect(sunburstPlots.textContent).toContain("Sunburst Chart");
    expect(sunburstPlotsRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render treemap chart iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const treemap = fixture.debugElement.queryAll(By.css('.hover'))[11].nativeElement;
    const treemapRender = fixture.debugElement.queryAll(By.css('.hide'))[10].nativeElement;

    // act
    treemap.click();

    // assert
    expect(treemap.textContent).toContain("Treemap Chart");
    expect(treemapRender.querySelector('iframe')).toBeTruthy();
  });

  it('should render user profiles iFrame on selection', () => {
    // arrange
    const render = fixture.debugElement.nativeElement;
    const userProfiles = fixture.debugElement.queryAll(By.css('.hover'))[11].nativeElement;
    const userProfilesRender = fixture.debugElement.queryAll(By.css('.hide'))[10].nativeElement;
    const mockProfiles: ClusterInfo[] = [{"question": "test1",
                                          "common_response": ["1", "2", "3"],
                                          "common_response_count": [31, 42, 23]},
                                           {"question": "test2",
                                           "common_response": ["a", "b", "c"],
                                           "common_response_count": [11, 12, 13]}];

    // act
    userProfiles.click()
    component.userProfiles = mockProfiles;

    // assert
    expect(userProfiles.textContent).toContain("Treemap Chart");
    expect(userProfilesRender.querySelector('iframe')).toBeTruthy();
  });

});
