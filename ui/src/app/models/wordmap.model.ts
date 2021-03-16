export class Wordmap {
    categories: Category[];
}

export class Category {
    question: string;
    wordmap: WordData[]
}

export class WordData {
    word: string;
    count: number;
}