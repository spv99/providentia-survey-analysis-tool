import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { Profile } from '../../models/profile.model';
import * as $ from 'jquery';

@Component({
  selector: 'user-profiles',
  templateUrl: './user-profiles.component.html',
  styleUrls: ['./user-profiles.component.scss']
})

export class UserProfilesComponent implements OnInit  {
    @Input() userProfiles: Profile[];
    
    ngOnInit() {
        const t = $(".material-icons")
        console.log(t)
    }
}
