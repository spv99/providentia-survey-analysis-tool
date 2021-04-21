import { Profile } from "./profile.model";

export class Chart {
    fileLocation: string;
    renderContent: string;
    categories?: string;
    cluster_profiles?: Profile[];
}