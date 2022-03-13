
export interface SenseResult {
    analyzed_text: string;
    results: SenseRating[];
}

export interface SenseRating {
    category: string;
    value: number;
}
