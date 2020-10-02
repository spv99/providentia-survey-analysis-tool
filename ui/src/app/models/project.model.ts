import {User} from './user.model';
import {Note} from './note.model';

export class Project {
    public id: string;
    public name: string;
    public description: string;
    public uploadedDate: Date;
    public uploadedBy: User;
    public modifiedDate: Date;
    public modifiedBy: User;
    public notes: Note[];
}