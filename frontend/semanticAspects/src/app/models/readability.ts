export interface ReadabilityIndexes {
    fleschReadingEase: FleschReadingEaseScore;
    fleschKincaidGrade: FleschKincaidGradeScore;
    colemanLiauIndex: ColemanLiauIndexScore;
    automatedReadabilityIndex: AutomatedReadabilityIndexScore;
    daleChallReadabilityScore: DaleChallReadabilityScore;
    linsearWriteFormula: LinsearWriteFormulaScore;
    gunningFog: GunningFogScore;
    textStandard: string;
    difficultWords: number;
}

// https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch_reading_ease
export enum FleschReadingEaseCategory {
    VeryEasy = 'Very easy - 5th grade',
    Easy = 'Easy - 6th grade',
    FairlyEasy = 'Fairly easy - 7th grade',
    PlainEnglish = 'Plain english - 8th - 9th grade',
    FairlyDifficult = 'Fairly difficult - 10th - 12th grade',
    College = 'College - difficult to read',
    CollegeGraduate = 'College graduate - very difficult to read',
    Professional = 'Professional - extremely difficult to read'
}

export interface FleschReadingEaseScore {
    score: number;
    fleschReadingCategory: FleschReadingEaseCategory;
}

// https://en.wikipedia.org/wiki/Gunning_fog_index
export enum GunningFogCategory {
    SixthGrade = 'Grade 6',
    SeventhGrade = 'Grade 7',
    EighthGrade = 'Grade 8',
    HighSchoolFreshman = 'Grade 9',
    HighSchoolSophomore = 'Grade 10',
    HighSchoolJunior = 'Grade 11',
    HighSchoolSenior = 'Grade 12',
    CollegeFreshman = 'Grade 13',
    CollegeSophomore = 'Grade 14',
    CollegeJunior = 'Grade 15',
    CollegeSenior = 'Grade 16',
    CollegeGraduate = 'Grade 17'
}

export interface GunningFogScore {
    score: number;
    gunningFogCategory: GunningFogCategory;
}

// https://en.wikipedia.org/wiki/Automated_readability_index
export enum AutomatedReadabilityIndexCategory {
    Kindergarten = 'Score 1, age 5-6',
    FirstGrade = 'Score 2, age 6-7',
    SecondGrade = 'Score 3, age 7-8',
    ThirdGrade = 'Score 4, age 7-9',
    FourthGrade = 'Score 5, age 9-10',
    FifthGrade = 'Score 6, age 10-11',
    SixthGrade = 'Score 7, age 11-12',
    SeventhGrade = 'Score 8, age 12-13',
    EighthGrade = 'Score 9, age 13-14',
    NinthGrade = 'Score 10, age 14-15',
    TenthGrade = 'Score 11, age 15-16',
    EleventhGrade = 'Score 12, age 16-17',
    TwelfthGrade = 'Score 13, age 17-18',
    CollegeStudent = 'Score 14, age 18-22',
}


export interface AutomatedReadabilityIndexScore {
    score: number;
    automatedReadabilityIndexCategory: AutomatedReadabilityIndexCategory;
}

// https://clickhelp.com/software-documentation-tool/user-manual/coleman-liau-index.html
export enum ColemanLiauIndexCategory {
    BasicLevel = 'Basic level, Pre-kindergarten - 1st grade, age: 3 - 7',
    VeryEasy = 'Very easy, 1st grade - 5th grade, age: 7 - 11',
    AverageReader= 'For average reader, 5th grade - 8th grade, age: 11 - 14',
    FairlyDifficult = '"Fairly difficult, 8th grade - 11th grade, age: 14 - 17',
    TooHard = 'Too hard to read, 11th grade - college, age: 17+',
}

export interface ColemanLiauIndexScore {
    score: number;
    colemanLiauIndexCategory: ColemanLiauIndexCategory;
}

// https://clickhelp.com/software-documentation-tool/user-manual/flesch-kincaid-grade-level.html
export enum FleschKincaidGradeCategory {
    BasicLevel = 'Basic level, Pre-kindergarten - 1st grade, age: 3 - 7',
    VeryEasy = 'Very easy, 1st grade - 5th grade, age: 7 - 11',
    AverageReader = 'For average reader, 5th grade - 11th grade, age: 11 - 17',
    TooHard = 'Too hard to read, 11th grade - college, age: 17+',
}

export interface FleschKincaidGradeScore {
    score: number;
    fleschKincaidGradeCategory: FleschKincaidGradeCategory;
}

// https://www.npmjs.com/package/text-readability
export enum DaleChallReadabilityCategory {
    FourthGrade = 'Score 4.9 or lower, average 4th-grade student or lower',
    FifthSixthGrade = 'Score 5.0–5.9, average 5th or 6th-grade student',
    SeventhEightGrade = 'Score 6.0–6.9,	average 7th or 8th-grade student',
    NinthTenthGrade = 'Score 7.0–7.9, average 9th or 10th-grade student',
    EleventhTwelfthGrade = 'Score 8.0–8.9, average 11th or 12th-grade student',
    ThirteenthFifteenthGrade = 'Score 9.0–9.9, average 13th to 15th-grade (college) student'
}

export interface DaleChallReadabilityScore {
    score: number;
    daleChallReadabilityCategory: DaleChallReadabilityCategory;
}

// https://clickhelp.com/software-documentation-tool/user-manual/linsear-write.html
export enum LinsearWriteFormulaCategory {
    BasicLevel = 'Basic level, Pre-kindergarten - 1st grade, age: 3 - 7',
    VeryEasy = 'Very easy, 1st grade - 5th grade, age: 7 - 11',
    AverageReader= 'For average reader, 5th grade - 8th grade, age: 11 - 14',
    FairlyDifficult = 'Fairly difficult, 8th grade - 11th grade, age: 14 - 17',
    TooHard = 'Too hard to read, 11th grade - college, age: 17+',
}

export interface LinsearWriteFormulaScore {
    score: number;
    linsearWriteFormulaCategory: LinsearWriteFormulaCategory;
}

