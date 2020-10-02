import { User } from './user.model';

export class Note {
    public componentName: string;
    public componentNotes: string;
    public modifiedBy: User;
    public modifiedDate: Date;
}