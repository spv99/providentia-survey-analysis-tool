import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent} from './app.component';
import { DetailsPageComponent } from './details-page/details-page.component';


const routes: Routes = [
  { path: '', redirectTo: 'providentia', pathMatch: 'full' },
  { path: 'providentia', component: AppComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
export const routingComponents = [AppComponent, DetailsPageComponent];
