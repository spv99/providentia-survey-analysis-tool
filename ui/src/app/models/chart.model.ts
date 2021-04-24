import { Profile } from "./profile.model";

export class Chart {
    fileLocation: string;
    renderContent: string;
    categories?: string;
    cluster_profiles?: Profile[];
    titles?: string[];
}

export class Sentiment {
    neg_tokens: string[];
    negative_statements: string[];
    neu_tokens: string[];
    neutral_statements: string[];
    pos_tokens: string[];
    positive_statements: string[];
}