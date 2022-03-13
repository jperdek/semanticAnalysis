import { Injectable } from '@angular/core';
import { ReadabilityIndexes, FleschReadingEaseCategory,
  FleschKincaidGradeCategory, ColemanLiauIndexCategory,
  AutomatedReadabilityIndexCategory,
  DaleChallReadabilityCategory,
  LinsearWriteFormulaCategory,
  GunningFogCategory} from 'src/app/models/readability';
import * as rs from 'text-readability';
// https://www.npmjs.com/package/text-readability

@Injectable({
  providedIn: 'root'
})
export class ReadabilityAnalysisService {

  public test(): void {
    const testData = `
      Playing games has always been thought to be important to
      the development of well-balanced and creative children;
      however, what part, if any, they should play in the lives
      of adults has never been researched that deeply. I believe
      that playing games is every bit as important for adults
      as for children. Not only is taking time out to play games
      with our children and other adults valuable to building
      interpersonal relationships but is also a wonderful way
      to release built up tension. `;

    console.log(rs.fleschReadingEase(testData));
    console.log(rs.fleschKincaidGrade(testData));
    console.log(rs.colemanLiauIndex(testData));
    console.log(rs.automatedReadabilityIndex(testData));
    console.log(rs.daleChallReadabilityScore(testData));
    console.log(rs.difficultWords(testData));
    console.log(rs.linsearWriteFormula(testData));
    console.log(rs.gunningFog(testData));
    console.log(rs.textStandard(testData));
  }

  private getCategoryForFleschReadingEase(score: number, debug= false): FleschReadingEaseCategory {
    if (0.0 <= score && score < 10.0) {
      return FleschReadingEaseCategory.Professional;
    } else if (10.0 <= score && score < 30.0) {
      return FleschReadingEaseCategory.CollegeGraduate;
    } else if (30.0 <= score && score < 50.0) {
      return FleschReadingEaseCategory.College;
    } else if (50.0 <= score && score < 60.0) {
      return FleschReadingEaseCategory.FairlyDifficult;
    } else if (60.0 <= score && score < 70.0) {
      return FleschReadingEaseCategory.PlainEnglish;
    } else if (70.0 <= score && score < 80.0) {
      return FleschReadingEaseCategory.FairlyEasy;
    } else if (80.0 <= score && score < 90.0) {
      return FleschReadingEaseCategory.Easy;
    } else if (90.0 <= score) {
      return FleschReadingEaseCategory.VeryEasy;
    } else {
      if (debug) {
        console.log('Unknow Flesch reading ease score!' + score.toString());
      }
      return null;
    }
  }

  private getCategoryForFleschKincaidGrade(score: number, debug= false): FleschKincaidGradeCategory {
    if (0.0 <= score && score < 1.0) {
      return FleschKincaidGradeCategory.BasicLevel;
    } else if (1.0 <= score && score < 5.0) {
      return FleschKincaidGradeCategory.VeryEasy;
    } else if (5.0 <= score && score < 11.0) {
      return FleschKincaidGradeCategory.AverageReader;
    } else if (11.0 <= score) {
      return FleschKincaidGradeCategory.TooHard;
    } else {
      if (debug) {
        console.log('Unknow Flesch Kincaid Grade Score!' + score.toString());
      }
      return null;
    }
  }

  private getCategoryForColemanLiauIndex(score: number, debug= false): ColemanLiauIndexCategory {
    if (0.0 <= score && score < 1.0) {
      return ColemanLiauIndexCategory.BasicLevel;
    } else if (1.0 <= score && score < 5.0) {
      return ColemanLiauIndexCategory.VeryEasy;
    } else if (5.0 <= score && score < 8.0) {
      return ColemanLiauIndexCategory.AverageReader;
    } else if (8.0 <= score && score < 11.0) {
      return ColemanLiauIndexCategory.FairlyDifficult;
    } else if (11.0 <= score) {
      return ColemanLiauIndexCategory.TooHard;
    } else {
      if (debug) {
        console.log('Unknow Coleman Liau index score!' + score.toString());
      }
      return null;
    }
  }

  private getAutomatedReadabilityIndexScore(score: number, debug= true): AutomatedReadabilityIndexCategory {
    if (1.0 <= score && score < 2.0) {
      return AutomatedReadabilityIndexCategory.Kindergarten;
    } else if (2.0 <= score && score < 3.0) {
      return AutomatedReadabilityIndexCategory.FirstGrade;
    } else if (3.0 <= score && score < 4.0) {
      return AutomatedReadabilityIndexCategory.SecondGrade;
    } else if (4.0 <= score && score < 5.0) {
      return AutomatedReadabilityIndexCategory.ThirdGrade;
    } else if (5.0 <= score && score < 6.0) {
      return AutomatedReadabilityIndexCategory.FourthGrade;
    } else if (6.0 <= score && score < 7.0) {
      return AutomatedReadabilityIndexCategory.FifthGrade;
    } else if (7.0 <= score && score < 8.0) {
      return AutomatedReadabilityIndexCategory.SixthGrade;
    } else if (8.0 <= score && score < 9.0) {
      return  AutomatedReadabilityIndexCategory.SeventhGrade;
    } else if (9.0 <= score && score < 10.0) {
      return AutomatedReadabilityIndexCategory.EighthGrade;
    } else if (10.0 <= score && score < 11.0) {
      return AutomatedReadabilityIndexCategory.NinthGrade;
    } else if (11.0 <= score && score < 12.0) {
      return AutomatedReadabilityIndexCategory.TenthGrade;
    } else if (12.0 <= score && score < 13.0) {
      return AutomatedReadabilityIndexCategory.EleventhGrade;
    } else if (13.0 <= score && score < 14.0) {
      return AutomatedReadabilityIndexCategory.TwelfthGrade;
    } else if (14.0 <= score) {
      return AutomatedReadabilityIndexCategory.CollegeStudent;
    } else {
      if (debug) {
        console.log('Unknown Automated readability index score!' + score.toString());
      }
      return null;
    }
  }

  private getDaleChallReadabilityScore(score: number, debug= false): DaleChallReadabilityCategory {
    if (score <= 4.9) {
      return DaleChallReadabilityCategory.FourthGrade;
    } else if (4.9 < score && score <= 5.9) {
      return DaleChallReadabilityCategory.FifthSixthGrade;
    } else if (5.9 < score && score <= 6.9) {
      return DaleChallReadabilityCategory.SeventhEightGrade;
    } else if (6.9 < score && score <= 7.9) {
      return DaleChallReadabilityCategory.NinthTenthGrade;
    } else if (7.9 < score && score <= 8.9) {
      return DaleChallReadabilityCategory.EleventhTwelfthGrade;
    } else if (8.9 < score) {
      return DaleChallReadabilityCategory.ThirteenthFifteenthGrade;
    } else {
      if (debug) {
        console.log('Unknow Dale Chall readability score!' + score.toString());
      }
      return null;
    }
  }

  private getLinsearWriteFromulaScore(score: number, debug= false): LinsearWriteFormulaCategory {
    if (0.0 <= score && score < 1.0) {
      return LinsearWriteFormulaCategory.BasicLevel;
    } else if (1.0 <= score && score < 5.0) {
      return LinsearWriteFormulaCategory.VeryEasy;
    } else if (5.0 <= score && score < 8.0) {
      return LinsearWriteFormulaCategory.AverageReader;
    } else if (8.0 <= score && score < 11.0) {
      return LinsearWriteFormulaCategory.FairlyDifficult;
    } else if (11.0 <= score) {
      return LinsearWriteFormulaCategory.TooHard;
    } else {
      if (debug) {
        console.log('Unknow Linsear Write readability formula score!' + score.toString());
      }
      return null;
    }
  }

  private getGunningFogScore(score: number, debug = false): GunningFogCategory {
    if (6 <= score && score < 7.0) {
      return GunningFogCategory.SixthGrade;
    } else if (7.0 <= score && score < 8.0) {
      return GunningFogCategory.SeventhGrade;
    } else if (8.0 <= score && score < 9.0) {
      return GunningFogCategory.EighthGrade;
    } else if (9.0 <= score && score < 10.0) {
      return GunningFogCategory.HighSchoolFreshman;
    } else if (10.0 <= score && score < 11.0) {
      return GunningFogCategory.HighSchoolSophomore;
    } else if (11.0 <= score && score < 12.0) {
      return GunningFogCategory.HighSchoolJunior;
    } else if (12.0 <= score && score < 13.0) {
      return GunningFogCategory.HighSchoolSenior;
    } else if (13.0 <= score && score < 14.0) {
      return  GunningFogCategory.CollegeFreshman;
    } else if (14.0 <= score && score < 15.0) {
      return GunningFogCategory.CollegeSophomore;
    } else if (15.0 <= score && score < 16.0) {
      return GunningFogCategory.CollegeJunior;
    } else if (16.0 <= score && score < 17.0) {
      return GunningFogCategory.CollegeSenior;
    } else if (17.0 <= score) {
      return GunningFogCategory.CollegeGraduate;
    } else {
      if (debug) {
        console.log('Unknow Gunning Fog readability score!' + score.toString());
      }
      return null;
    }
  }

  public analyzeText(text: string, usedMethods: string[]): any {
    let all = false;
    if (usedMethods.length === 0){
      all = true;
    }

    const readabilityIndexes: ReadabilityIndexes = {
      fleschReadingEase: undefined,
      fleschKincaidGrade: undefined,
      colemanLiauIndex: undefined,
      automatedReadabilityIndex: undefined,
      daleChallReadabilityScore: undefined,
      linsearWriteFormula: undefined,
      gunningFog: undefined,
      textStandard: undefined,
      difficultWords: -1
    };

    if (all || 'fleschEase' in usedMethods) {
      try{
        const fleschEaseScore = rs.fleschReadingEase(text);
        if (fleschEaseScore !== null) {
          readabilityIndexes.fleschReadingEase = {
            score: fleschEaseScore,
            fleschReadingCategory: this.getCategoryForFleschReadingEase(fleschEaseScore)
          };
        }
      } catch (error) {
        console.log(error);
      }
    }

    if (all || 'fleschKincaid' in usedMethods) {
      try{
        const fleschKincaidScore = rs.fleschKincaidGrade(text);
        if (fleschKincaidScore !== null) {
          readabilityIndexes.fleschKincaidGrade = {
            score: fleschKincaidScore,
            fleschKincaidGradeCategory: this.getCategoryForFleschKincaidGrade(fleschKincaidScore)
          };
        }
      } catch (error) {
        console.log(error);
      }
    }

    if (all || 'colemanLiau' in usedMethods) {
      try{
        const colemanLiauScore = rs.colemanLiauIndex(text);
        if (colemanLiauScore !== null) {
          readabilityIndexes.colemanLiauIndex = {
            score: colemanLiauScore,
            colemanLiauIndexCategory: this.getCategoryForColemanLiauIndex(colemanLiauScore)
          };
        }
      } catch (error) {
        console.log(error);
      }
    }

    if (all || 'automatedReadability' in usedMethods) {
      try{
        const automatedReadabilityScore = rs.automatedReadabilityIndex(text);
        if (automatedReadabilityScore !== null) {
          readabilityIndexes.automatedReadabilityIndex = {
            score: automatedReadabilityScore,
            automatedReadabilityIndexCategory: this.getAutomatedReadabilityIndexScore(automatedReadabilityScore)
          };
        }
      } catch (error) {
        console.log(error);
      }
    }

    if (all || 'daleChall' in usedMethods) {
      try{
        const daleChallScore = rs.daleChallReadabilityScore(text);
        if (daleChallScore !== null) {
          readabilityIndexes.daleChallReadabilityScore = {
            score: daleChallScore,
            daleChallReadabilityCategory: this.getDaleChallReadabilityScore(daleChallScore)
          };
        }
      } catch (error) {
        console.log(error);
      }
    }

    if (all || 'difficultWords' in usedMethods) {
      try{
        readabilityIndexes.difficultWords = rs.difficultWords(text);
      } catch (error) {
        console.log(error);
      }
    }

    if (all || 'linsearWrite' in usedMethods) {
      try{
        const linsearWriteFormulaScore = rs.linsearWriteFormula(text);
        if (linsearWriteFormulaScore !== null) {
          readabilityIndexes.linsearWriteFormula = {
            score: linsearWriteFormulaScore,
            linsearWriteFormulaCategory: this.getLinsearWriteFromulaScore(linsearWriteFormulaScore)
          };
        }
      } catch (error) {
        console.log(error);
      }
    }

    if (all || 'gunningFog' in usedMethods) {
      try{
        const gunningFogScore = rs.gunningFog(text);
        if (gunningFogScore !== null) {
          readabilityIndexes.gunningFog = {
            score: gunningFogScore,
            gunningFogCategory: this.getGunningFogScore(gunningFogScore)
          };
        }
      } catch (error) {
        console.log(error);
      }
    }

    if (all || 'textStandard' in usedMethods) {
      try{
        readabilityIndexes.textStandard = rs.textStandard(text);
        console.log(readabilityIndexes.textStandard);
      } catch (error) {
        console.log(error);
      }
    }

    return readabilityIndexes;
  }
}
