import { SomSettings } from './somSettings';

export interface FileModel extends File{
    progress: number;
    showed: boolean;
    textResult: string;
    appliedSegmentation: boolean;
    segmentationMethod: string;
    disallowedMethods: string[];
    somSettings: undefined | SomSettings;
}
