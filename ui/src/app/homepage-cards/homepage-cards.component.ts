import { Component, Input } from "@angular/core";

@Component({
    selector: 'homepage-cards',
    templateUrl: './homepage-cards.component.html',
    styleUrls: ['./homepage-cards.component.scss']
})

export class HomepageCardsComponent {
    @Input() title: string;
    @Input() subtitle: string;
    @Input() text: string;
}