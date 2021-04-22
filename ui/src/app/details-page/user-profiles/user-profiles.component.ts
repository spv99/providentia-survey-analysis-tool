import { Component, Input, OnInit } from '@angular/core';
import { Profile } from '../../models/profile.model';

@Component({
  selector: 'user-profiles',
  templateUrl: './user-profiles.component.html',
  styleUrls: ['./user-profiles.component.scss']
})

export class UserProfilesComponent implements OnInit {
  @Input() userProfiles: Profile[];
  public profileOne: Profile;
  public profileOneTotal: number;
  public profileTwo: Profile;
  public profileTwoTotal: number;
  public profileThree: Profile;
  public profileThreeTotal: number;
  public profileFour: Profile;
  public profileFourTotal: number;
  public profileFive: Profile;
  public profileFiveTotal: number;
  public showDetails: boolean = false;

  ngOnInit() {
    // if (!!this.profileOne && !!this.profileOne.clusterInfo) {
    //   this.profileOne.clusterInfo.forEach(cluster => {
    //     if (typeof cluster.common_response[0] === "number") {
    //       cluster.common_response.forEach(el => {
    //         el = el.toString();
    //       })
    //     }
    //   });
    // }

    if(!!this.userProfiles[0]) this.profileOne = this.userProfiles[0];
    //@ts-ignore
    if(!!this.profileOne) this.profileOneTotal = this.profileOne[this.profileOne.length - 1].respondents;

    if(!!this.userProfiles[1]) this.profileTwo = this.userProfiles[1];
    //@ts-ignore
    if(!!this.profileTwo) this.profileTwoTotal = this.profileTwo[this.profileTwo.length - 1].respondents;

    if(!!this.userProfiles[2]) this.profileThree = this.userProfiles[2];
    //@ts-ignore
    if(!!this.profileThree) this.profileThreeTotal = this.profileThree[this.profileThree.length - 1].respondents;

    if(!!this.userProfiles[3]) this.profileFour = this.userProfiles[3];
    //@ts-ignore
    if(!!this.profileFour) this.profileFourTotal = this.profileFour[this.profileFour.length - 1].respondents;

    if(!!this.userProfiles[4]) this.profileFive = this.userProfiles[4];
    //@ts-ignore
    if(!!this.profileFive) this.profileFiveTotal = this.profileFive[this.profileFive.length - 1].respondents;
  }
}
