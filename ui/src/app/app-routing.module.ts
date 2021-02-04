import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DetailsPageComponent } from './details-page/details-page.component';
import { ProvidentiaComponent } from './providentia/providentia.component';


const routes: Routes = [
  { path: '', redirectTo: 'providentia', pathMatch: 'full' },
  { path: 'providentia', component: ProvidentiaComponent},
  { path: 'providentia/results', component: DetailsPageComponent}
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
