import { CategoryRating } from './category';

export interface Aggregation {
    meaning: string;
    priority: number;
    matched: any[];
}

export interface AggregationStructure {
    name: string;
    data: Aggregation[];
}

export interface AggregationRepresentants {
    meaning: string;
    representants: CategoryRating[];
}
