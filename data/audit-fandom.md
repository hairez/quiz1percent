# Fandom wiki audit

Compared **980** records in `public/questions.json` against **744** records parsed from `data/raw/fandom/` (only-connect-questions.fandom.com).

Headline: **130 conflicts on UK S4** (86 clean), **520 new questions available** (UK S1-S3 + specials), **210 parse warnings**.

---

## 1. UK S4 conflicts

Each entry lists the categories that fired, then prints the two records side-by-side so you can decide if the wiki version should override (via `MANUAL_OVERRIDES` in `scraper/build.py`).

Conflicts by category:

- **wiki_missing_answer**: 44
- **different_question_text**: 39
- **richer_explanation_on_wiki**: 26
- **richer_question_on_wiki**: 25
- **wiki_missing_options**: 25
- **different_correct_answer**: 22
- **answer_substring_mismatch**: 17
- **missing_options**: 9
- **we_have_placeholder_wiki_has_real_options**: 6
- **different_options**: 5

Records present in ours but not on wiki (3):

- `uk-s4-e16-1`
- `uk-s4-e16-60`
- `uk-s4-e16-70`

Records present on wiki but not in ours (8):

- `uk-s4-e10-1`
- `uk-s4-e10-80`
- `uk-s4-e10-90`
- `uk-s4-e13-45`
- `uk-s4-e15-10`
- `uk-s4-e15-70`
- `uk-s4-e6-1`
- `uk-s4-e6-80`

### `uk-s4-e1-10`

Category: **answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: If you change the letter at the beginning of the first word, the letter in the middle of the second word and the letter at the end of the third word, they all now have something in common. What is it?  CAT    BOATS   SCARE
  opts: (none)
  ans: Clothes
  expl: You can change CAT to HAT, BOATS to BOOTS, and SCARE to SCARF. [This is a tricky one since there are a lot of possibilities for word changes. The main thing to focus on are what SCARE could change into, which would be SCARF, SCARS, and S...
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_1#10pct)
```
  Q: If you change the letter at the beginning of the first word, the letter in the middle of the second word and the letter at the end of the third word, they all now have something in common. What is it? CAT BOATS SCARE
  opts: (none)
  ans: H
  expl: HAT BOOTS SCARF Clothes
  img: (none)
```

### `uk-s4-e1-15`

Category: **different_question_text, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: In the puzzle below, what four words replace the question mark?  Shatter the frozen water = Break the ice You can’t access a novel by its dust jacket = You can’t judge a book by its cover Illustrious intellects imagine identically = ?
  opts: (none)
  ans: Great minds think alike
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_1#15pct)
```
  Q: In the puzzle below, what four words replace the question mark? Shatter the frozen water = Break the ice You can’t assess a novel by its dust jacket = You can’t judge a book by its cover
  opts: (none)
  ans: Great minds think alike
  expl: Illustrious intellects imagine identically = Great minds think alike
  img: (none)
```

### `uk-s4-e1-20`

Category: **richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What number replaces the question mark in the sequence below?  7 8 5 5 3 4 4 ? 9 7 8 8
  opts: (none)
  ans: 6
  expl: The sequence is the number of letters in the names of the months in a calendar year. The question mark represents August and there are six letters in August.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_1#20pct)
```
  Q: What number replaces the question mark in the sequence below?
  opts: (none)
  ans: 6
  expl: 7 8 5 5 3 4 4 6 9 7 8 8 J F M A M J J A S O N D The sequence is the number of letters in the names of the months in a calendar year. The question mark represents August and there are six letters in August.
  img: (none)
```

### `uk-s4-e1-30`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Below is the recipe for a Big Mack burger. If I have nine whole buns, nine cheese slices, eight tomato slices, and ten patties, what is the maximum number of Big Mack burgers I can make?
  opts: (none)
  ans: 5
  expl: Each burger has two patties so ten patties limit the number of burgers to five. [It is assumed that the buns are cut in half.]
  img: questions/uk-s4-e1-30.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_1#30pct)
```
  Q: Below is the recipe for a Big Mack burger. If I have nine whole buns, nine cheese slices, eight tomato slices and ten patties, what is the maximum number of Big Mack burgers I can make?
  opts: (none)
  ans: five
  expl: Each burger has two patties so ten patties limit the number of burgers to five.
  img: Big Mack.png
```

### `uk-s4-e1-35`

Category: **missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of the following words is still a recognised word if you substitute the first letter for the next letter in the alphabet and the last letter for the previous letter in the alphabet?
  opts: ['BRINK', 'CROWN', 'CREST']
  ans: CREST
  expl: [The instructions would turn this word into DRESS.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_1#35pct)
```
  Q: Which of the following words is still a recognised word if you substitute the first letter for the next letter in the alphabet and the last letter for the previous letter in the alphabet?
  opts: ['BRINK', 'CROWN', 'CREST', 'CRINJ', 'DROWM', 'DRESS']
  ans: CREST
  expl: (none)
  img: (none)
  parse_notes: multiple bolded cells (2)
```

### `uk-s4-e1-60`

Category: **answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Although some have been rotated, which two of these flags are exactly the same?
  opts: (none)
  ans: Flags A and C
  expl: (none)
  img: questions/uk-s4-e1-60.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_1#60pct)
```
  Q: Although some have been rotated, which two of these flags are exactly the same?
  opts: (none)
  ans: A and C
  expl: (none)
  img: Flag.png
```

### `uk-s4-e1-70`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these is incorrect?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (C)
  expl: Change the images to words to make new words. DUCKLONGING is not a word.
  img: questions/uk-s4-e1-70.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_1#70pct)
```
  Q: Which of these is incorrect? Change the images to words to make new words. DUCKLONGING is not a word.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Ducklonging.png
  parse_notes: no bolded answer
```

### `uk-s4-e1-90`

Category: **different_question_text, different_options, answer_substring_mismatch, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Sara has almost finished this crossword and just has 7 down left to fill in. The clue is: Investigate. Which of these is the correct answer?
  opts: ['EXPLORE', 'EXAMINE', 'EXPOSE']
  ans: EXPLORE
  expl: Only A fits in the grid.
  img: questions/uk-s4-e1-90.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_1#90pct)
```
  Q: (none)
  opts: ['S', 'P', 'R', 'E', 'A', 'D', 'T', 'R', 'X', 'E', 'W', 'H', 'I', 'P', 'P', 'E', 'T', 'I', 'O', 'L', 'E', 'N', 'E', 'R', 'V', 'O', 'U', 'S', 'R', 'T', 'A', 'H', 'E', 'E', 'D', 'S']
  ans: E
  expl: {| class="fandom-table" ! colspan="3" |Sara has almost finished this crossword and just has 7 down left to fill in. The clue is: Investigate. Which of these is the correct answer? |- |EXPLORE |EXAMINE |EXPOSE |} Only A fits in the grid.
  img: (none)
  parse_notes: multiple bolded cells (7)
```

### `uk-s4-e10-10`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What number replaces the question mark in the picture below?
  opts: (none)
  ans: 12
  expl: The number in the roof is revealed by adding the numbers in the two windows together and taking away the number on the door. 5 + 12 = 17 and 17 – 5 = 12.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_10#10pct)
```
  Q: What number replaces the question mark in the picture below? The number in the roof is revealed by adding the numbers in the two windows together and taking away the number on the door. 5 + 12 = 17 and 17 – 5 = 12
  opts: (none)
  ans: (none)
  expl: (none)
  img: Four houses.png
  parse_notes: no bolded answer
```

### `uk-s4-e10-20`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What will be the next year where the four digits will add up to the same total as the digits in 2025?
  opts: (none)
  ans: 2034
  expl: 2 + 0 + 2 + 5 = 9. 2 + 0 + 3 + 4 = 9.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_10#20pct)
```
  Q: What will be the next year where the four digits will add up to the same total as the digits in 2025? 2 + 0 + 2 + 5 = 9 2 + 0 + 3 + 4 = 9
  opts: (none)
  ans: (none)
  expl: (none)
  img: (none)
  parse_notes: no bolded answer
```

### `uk-s4-e10-40`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Here are some very clever chemical elements. What letter replaces the question mark?
  opts: (none)
  ans: S
  expl: The chemical symbols spell out the word ‘GENIUS’.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_10#40pct)
```
  Q: Here are some very clever chemical elements. What letter replaces the question mark? The chemical symbols spell out the word ‘GENIUS’.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Genius.png
  parse_notes: no bolded answer
```

### `uk-s4-e10-5`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What is the hidden pattern in these four phrases that makes them have something in common?
  opts: (none)
  ans: COMPASS DIRECTIONS
  expl: A compass point appears in each pair of words. [NOR and TH in the first pair make NORTH, EA and ST in the second pair make EAST, S and OUTH in the third pair make SOUTH, and WE and ST in the fourth pair make WEST.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_10#5pct)
```
  Q: What is the hidden pattern in these four phrases that makes them have something in common?
  opts: (none)
  ans: OR TH
  expl: MINOR THERAPY TEA STRAINER GLASS OUTHOUSE FELIXSTOWE STATION A compass point appears in each pair of words.
  img: (none)
```

### `uk-s4-e10-70`

Category: **richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What four-letter word logically fills the gap?  Characters in books who start off EVIL and VILE usually draw a VEIL over their behaviour and decide they want to ____ a purposeful life.
  opts: (none)
  ans: LIVE
  expl: All the words in uppercase are anagrams of each other. LIVE is the only other word that uses the same letters and fits the gap.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_10#70pct)
```
  Q: What four-letter word logically fills the gap?
  opts: (none)
  ans: LIVE
  expl: Characters in books who start off EVIL and VILE usually draw a VEIL over their behaviour and decide they want to LIVE a purposeful life. All the words in upper case are anagrams of each other. LIVE is the only word that uses the same let...
  img: (none)
```

### `uk-s4-e11-1`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: I keep forgetting my four-digit PIN number. I know each digit is higher than the previous digit but I need this diagram to remember it. What is my four-digit PIN number?
  opts: (none)
  ans: 1489
  expl: [You can find ONE, FOUR, EIGHT, and NINE in the word search.]
  img: questions/uk-s4-e11-1.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_11#1pct)
```
  Q: I keep forgetting the four-digit PIN number. I know each digit is higher than the previous digit but I need this diagram to remember it. What is my four-digit PIN number?
  opts: (none)
  ans: 1489
  expl: Category:1% Club Season 4
  img: 1489.png
```

### `uk-s4-e11-10`

Category: **answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: The solution to this puzzle is nearly impossible to find. What is it?  HAANYESETDALCEK
  opts: (none)
  ans: A NEEDLE IN A HAYSTACK
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_11#10pct)
```
  Q: The solution to this puzzle is nearly impossible to find. What is it?
  opts: (none)
  ans: A
  expl: HAANYESETDALCEK A NEEDLE IN A HAYSTACK
  img: (none)
```

### `uk-s4-e11-25`

Category: **wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these statements is true?
  opts: ['In this statement, the word “the” occurs twice and so does the word “in”', 'In this statement, the word “and” occurs twice and so does the word “word”', 'In this statement, the word “in” occurs twice and so does the word “so”']
  ans: In this statement, the word “in” occurs twice and so does the word “so”
  expl: [The words in quotations still count.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_11#25pct)
```
  Q: Which of these statements is true?
  opts: ['In this statement, the word “the” occurs twice and so does the word “in”.', 'In this statement, the word “and” occurs twice and so does the word “word”.', 'In this statement, the word “in” occurs twice and so does the word “so”.']
  ans: (none)
  expl: (none)
  img: (none)
  parse_notes: no bolded correct cell
```

### `uk-s4-e11-35`

Category: **wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these is the missing piece for this image?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (C)
  expl: The piece is upside down but it fits. The other two pieces are already in the puzzle.
  img: questions/uk-s4-e11-35.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_11#35pct)
```
  Q: Which of these is the missing piece for this image?
  opts: (none)
  ans: C
  expl: The piece is upside down but it fits. The other two pieces are already in the puzzle.
  img: UK puzzle.png
```

### `uk-s4-e11-40`

Category: **different_correct_answer, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Answer this question: How many Ps are there in total in the following tongue twister?  PAUL AND PEARL POPPER PACKED POTS OF PEAS. IN EACH POT THERE WERE 100 PEAS. PAUL PACKED 16 POTS AND PEARL PACKED 19 POTS. WHEN PAUL AND PEARL PACKED A...
  opts: (none)
  ans: 21
  expl: The question is asking you to count the number of times the letter P appears, not the food item.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_11#40pct)
```
  Q: Answer this question: How many Ps are there in total in the following tongue twister?
  opts: (none)
  ans: P
  expl: PAUL AND PEARL POPPER PACKED POTS OF PEAS. IN EACH POT THERE WERE 100 PEAS. PAUL PACKED 16 POTS AND PEARL PACKED 19 POTS. WHEN PAUL AND PEARL PACKED ALL THEIR POTS, THERE WERE SO MANY PEAS! 21: The question is asking you to count the num...
  img: (none)
```

### `uk-s4-e11-45`

Category: **different_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: In this puzzle you need to stay IN the game. Which of these words is the odd one out?
  opts: ['JURY', 'CREASE', 'DEED', 'CRY']
  ans: CRY
  expl: If you put IN before the other words, it makes new words [INJURY, INCREASE, INDEED]. INCRY is not a word although OUTCRY is.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_11#45pct)
```
  Q: In this puzzle you need to stay IN the game. Which of these words is the odd one out?
  opts: ['INJURY', 'INCREASE', 'INDEED', 'CRY']
  ans: CRY
  expl: If you put IN before the other words, it makes new words. INCRY is not a word although OUTCRY is.
  img: (none)
```

### `uk-s4-e11-5`

Category: **different_question_text, answer_substring_mismatch, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What 2 words in this question each make a common new word if you move the last letter from the end to the beginning?
  opts: (none)
  ans: WORDS and END
  expl: “Words” becomes SWORD and END becomes DEN.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_11#5pct)
```
  Q: (none)
  opts: (none)
  ans: words
  expl: What 2 words in this question each make a common new word if you move the last letter from the end to the beginning? words become sword and end becomes den.
  img: (none)
  parse_notes: empty question text
```

### `uk-s4-e11-70`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these grids contains an even number of singular squares within it?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (B)
  expl: A has 15 squares, C has 49 squares, but B has 32 squares.
  img: questions/uk-s4-e11-70.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_11#70pct)
```
  Q: Which of these grids contains an even number of singular squares within it? A = 15, C = 49 but B = 32
  opts: (none)
  ans: (none)
  expl: (none)
  img: Even squares.png
  parse_notes: no bolded answer
```

### `uk-s4-e11-80`

Category: **missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Rebecca and Thomas are going to the zoo. They want to see lions, tigers and bears but they are in three separate areas. Bears are not found in the Red Zone. The Green and Yellow Zones have no lions. Tigers occupy the Green Zone. Where do...
  opts: ['Red Zone', 'Green Zone', 'Yellow Zone']
  ans: Red Zone
  expl: [The question says the Green and Yellow Zones have no lions so they can only be in the Red Zone.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_11#80pct)
```
  Q: Rebecca and Thomas are going to the zoo. They want to see lions, tigers and bears but they are in three separate areas. Bears are not found in the Red Zone. The Green and Yellow Zones have no lions. Tigers occupy the Green Zone. Where do...
  opts: ['Red Zone', 'Yellow Zone', 'Green Zone', 'Lions', 'Tigers', 'Bears']
  ans: Red Zone
  expl: The question says the Green and Yellow Zones have no lions so they can only be in the Red Zone.
  img: (none)
  parse_notes: multiple bolded cells (2)
```

### `uk-s4-e12-10`

Category: **richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What number comes next in this sequence?  ONE  THREE  FIVE  NINE  TWELVE  TWENTY-ONE  ?
  opts: (none)
  ans: TWENTY-THREE
  expl: This is the next number to end with an E.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_12#10pct)
```
  Q: What number comes next in this sequence?
  opts: (none)
  ans: TWENTY-THREE
  expl: ONE THREE FIVE NINE TWELVE TWENTY-ONE TWENTY-THREE TWENTY-THREE is the next number to end with an E.
  img: (none)
```

### `uk-s4-e12-15`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which two options need to be swapped to make this list correct?  A – CORN B – LEAF C – MAIL D – RAIL E – SAW
  opts: (none)
  ans: C & E
  expl: Each word sounds like a new word if you include the letter in front of it.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_12#15pct)
```
  Q: Which two options need to be swapped to make this list correct? A – CORN ACORN B – LEAF BELIEF C – MAIL EMAIL D – RAIL DERAIL E – SAW SEESAW
  opts: (none)
  ans: C & E
  expl: Each word sounds like a new word if you include the letter in front of it.
  img: (none)
```

### `uk-s4-e12-20`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Changing the first letter of each of these words will create new words with a theme in common. What is the common theme?  DOG, PAIN, FIST, MAIL
  opts: (none)
  ans: Weather
  expl: [DOG can become FOG, PAIN to RAIN, FIST to MIST, and MAIL to HAIL.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_12#20pct)
```
  Q: Changing the first letter of each of these words will create new words with a theme in common. What is the common theme?
  opts: (none)
  ans: F
  expl: DOG PAIN FIST MAIL FOG RAIN MIST HAIL Weather
  img: (none)
```

### `uk-s4-e12-25`

Category: **different_correct_answer, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Answer this question: How many times does NOT appear in the sentence below?  YOU MIGHT NOTICE THAT THIS IS A SNOTTY KNOTTY PROBLEM IF YOU COME FROM NOTTINGHAM, KNOW WHATNOT AND SUPPORT NOTTS COUNTY, BUT IT’S ANOTHER ONE THAT I CANNOT HEL...
  opts: (none)
  ans: 8
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_12#25pct)
```
  Q: Answer this question: How many times does NOT appear in the sentence below?
  opts: (none)
  ans: NOT
  expl: YOU MIGHT NOTICE THAT THIS IS A SNOTTY KNOTTY PROBLEM IF YOU COME FROM NOTTINGHAM, KNOW WHATNOT AND SUPPORT NOTTS COUNTY, BUT IT’S ANOTHER ONE THAT I CANNOT HELP YOU WITH.
  img: (none)
```

### `uk-s4-e12-30`

Category: **different_correct_answer, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Without reordering any letters, which six-letter food appears in this sentence?  DAISY THE COW PRODUCED EXCELLENT PRODUCTS BUT TERRIFIED VISITORS TO THE FARM
  opts: (none)
  ans: BUTTER
  expl: [From BUT and TERRIFIED.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_12#30pct)
```
  Q: Without reordering any letters, which six-letter food appears in this sentence?
  opts: (none)
  ans: BUT TER
  expl: DAISY THE COW PRODUCED EXCELLENT PRODUCTS BUT TERRIFIED VISITORS TO THE FARM.
  img: (none)
```

### `uk-s4-e12-35`

Category: **different_question_text, wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Jessica wants to paint her family’s nails but only wants to paint every THIRD nail. She starts counting from the little finger on Charlie’s left hand. Who is the only person who will NOT have either of their thumbs painted?
  opts: ['Charlie', 'Joanne', 'Marcus', 'Chris']
  ans: Marcus
  expl: Jessica will paint the right thumbs of Charlie and Chris and the left thumb of Joanne. [Also, Marcus’s thumbs would be in position 25 and 26, two numbers not divisible by 3.]
  img: questions/uk-s4-e12-35.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_12#35pct)
```
  Q: Jessica wants to paint every family’s nails but only wants to paint every THIRD nail. She starts counting from the little finger on Charlie’s left hand. Who is the only person who will NOT have either of their thumbs painted?
  opts: (none)
  ans: Marcus
  expl: Jessica will paint the right thumbs of Charlie and Chris and the left thumb of Joanne.
  img: Hands5.png
```

### `uk-s4-e12-40`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Lisa wants her bathroom floor to have more suns than moons, more moons than hearts and more hearts than diamonds. Which tile can she use to complete her design?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (A)
  expl: Option B gives you more diamonds than hearts. Option C gives you the same number of suns and moons.
  img: questions/uk-s4-e12-40.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_12#40pct)
```
  Q: Lisa wants her bathroom floor to have more suns than moons, more moons than hearts and more hearts than diamonds. Which tile can she use to complete her design? B gives you more diamonds than hearts. C gives you the same number of suns a...
  opts: (none)
  ans: (none)
  expl: (none)
  img: Tiles.png
  parse_notes: no bolded answer
```

### `uk-s4-e12-45`

Category: **answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Clare opens up an envelope posted through her letterbox and inside she sees this code written in the card. What do the Hs stand for?
  opts: (none)
  ans: Happy
  expl: [The letters represent the first letter in the traditional “Happy Birthday To You” song.]
  img: questions/uk-s4-e12-45.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_12#45pct)
```
  Q: Clare opens up an envelope posted through her letterbox and inside she sees this code written in the card. What do the Hs stand for?
  opts: (none)
  ans: H
  expl: HAPPY BIRTHDAY TO YOU HAPPY BIRTHDAY TO YOU HAPPY BIRTHDAY DEAR CLARE HAPPY BIRTHDAY TO YOU
  img: (none)
```

### `uk-s4-e12-5`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: The eight of diamonds, six of spades and six of hearts are shown here. What number logically represents the clubs?
  opts: (none)
  ans: FIVE
  expl: The number of each card represents the number of letters in the name of its suit..
  img: questions/uk-s4-e12-5.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_12#5pct)
```
  Q: The eight of diamonds, six of spades and six of hearts are shown here. What number logically represents the clubs? The number on each card represents the number of letters in the name of its suit.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Cards4.png
  parse_notes: no bolded answer
```

### `uk-s4-e12-70`

Category: **different_question_text, wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of the options below is the umbrella seen from above?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (C)
  expl: [The sequence of the blue-and-white polka dot, black-and-yellow stripe, black-and-purple polka dot, and orange-and-white checker is in C.]
  img: questions/uk-s4-e12-70.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_12#70pct)
```
  Q: Which of the options below is this umbrella seen from above?
  opts: (none)
  ans: C
  expl: (none)
  img: Umbrella.png
```

### `uk-s4-e13-1`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: My SON TED ate raw FOOD and got SICK, then went to BED with me by his SIDE  My SON TED ate raw FOOD and got SICK, then went to BED with me by his SIDE.
  opts: (none)
  ans: SEA
  expl: The word SEA can be put in front of each of the capitalised words to make new words – SEASON, SEATED, SEAFOOD, SEASICK, SEABED, and SEASIDE.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_13#1pct)
```
  Q: What new word links the capitalised words below? My SON TED ate raw FOOD and got SICK, then went to BED with me by his SIDE.
  opts: (none)
  ans: SEA
  expl: The word SEA can be put in front of each of the capitalised words to make new words – SEASON, SEATED, SEAFOOD, SEASICK, SEABED and SEASIDE. Category:1% Club Season 4
  img: (none)
```

### `uk-s4-e13-10`

Category: **answer_substring_mismatch, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: In the sentence below, what word can you make if you take the first letter of each word that contains two of the same letters together  JUST BEFORE THE SCHOOL DAY COMMENCED, IZZY QUIETLY SAID SORRY TO THE MEMBERS OF STAFF IN THE ADMIN OF...
  opts: (none)
  ans: SCISSORS
  expl: [From the first letters of SCHOOL, COMMENCED, IZZY, SORRY, STAFF, OFFICE, REALLY, and SUPPLIES.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_13#10pct)
```
  Q: In the sentence below, what word can you make if you take the first letter of each word that contains two of the same letters together?
  opts: (none)
  ans: S
  expl: JUST BEFORE THE SCHOOL DAY COMMENCED, IZZY QUIETLY SAID SORRY TO THE MEMBERS OF STAFF IN THE ADMIN OFFICE AS THEY WERE GOING TO BE REALLY BUSY SORTING OUT THE STATIONERY SUPPLIES. SCISSORS
  img: (none)
```

### `uk-s4-e13-20`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: You are a zookeeper and it’s weigh-in day at the zoo. How many lions weigh the same as six rhinos?
  opts: (none)
  ans: 8 lions
  expl: If 3 rhinos = 2 hippos and 4 lions = 2 hippos, then 6 rhinos = 8 lions.
  img: questions/uk-s4-e13-20.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_13#20pct)
```
  Q: You are a zookeeper and it’s weigh-in day at the zoo. How many lions weigh the same as six rhinos? If 3 rhinos = 2 hippos and 4 lions = 2 hippos, then 6 rhinos = 8 lions.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Rhino.png
  parse_notes: no bolded answer
```

### `uk-s4-e13-25`

Category: **different_question_text, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: I’m putting a line through some words. DICE CHICK OXIDE . On reflection, which on of these words should I also put a line through?
  opts: ['FIX', 'HIKER', 'BOXED', 'MILK', 'LEDGE']
  ans: BOXED
  expl: BOXED is the only other word in which everything below the line is a reflection of everything above.
  img: questions/uk-s4-e13-25.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_13#25pct)
```
  Q: I’m putting a line through some words. DICE CHICK OXIDE  On reflection, which one of these words should I also put a line through?
  opts: ['FIX', 'HIKER', 'BOXED', 'MILK', 'LEDGE']
  ans: (none)
  expl: BOXED is the only other word in which everything below the line is a reflection of everything above.
  img: (none)
  parse_notes: no bolded correct cell
```

### `uk-s4-e13-40`

Category: **wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: It’s well known in the comedy world that Alan Carr adores Charleston but that John Bishop jives badly and Bill Bailey ballrooms brilliantly. The next headline to hit is that Lee Mack loves… which of these?
  opts: ['Hokey Cokey', 'Cha Cha Slide', 'Moonwalking']
  ans: Moonwalking
  expl: The initials of the comedians dictate their tastes. [The words Alan Carr start with an ‘a’ and ‘c’, which is why the next two words that follow that is “adores” and “Charleston.” The other names follow the same pattern.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_13#40pct)
```
  Q: It’s well known in the comedy world that Alan Carr adores Charleston but that John Bishop jives badly and Bill Bailey ballrooms brilliantly. The next headline to hit is that Lee Mack loves… which of these?
  opts: ['Hokey Cokey', 'Cha Cha Slide', 'Moonwalking']
  ans: (none)
  expl: The initials of the comedians dictate their tastes.
  img: (none)
  parse_notes: no bolded correct cell
```

### `uk-s4-e13-5`

Category: **different_question_text, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: On this clock, the hour hand is past the five and the minute hand is pointing at six. On a normal clock, those hands pointing at those numbers would mean it’s half past five. Assuming the hands move round this clockface normally, what ti...
  opts: (none)
  ans: 10 o’clock
  expl: If the hour hand is on 10 and the minute hands in on 12, then the time is 10 o’clock.
  img: questions/uk-s4-e13-5.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_13#5pct)
```
  Q: On this clock, the hour hand is past the five and the minute hand is pointing at the six. On a normal clock, those hands pointing at those numbers would mean it’s half past five. Assuming the hands move round this clockface normally, wha...
  opts: (none)
  ans: (none)
  expl: (none)
  img: Clock4.png
  parse_notes: no bolded answer
```

### `uk-s4-e13-90`

Category: **missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of the following words still makes a valid word if you change the first letter to the next letter in the alphabet?
  opts: ['PAGE', 'RAGE', 'WAGE']
  ans: RAGE
  expl: [RAGE becomes SAGE, which is still a valid word.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_13#90pct)
```
  Q: Which of the following words still makes a valid word if you change the first letter to the next letter in the alphabet?
  opts: ['PAGE', 'RAGE', 'WAGE', 'QAGE', 'SAGE', 'XAGE']
  ans: RAGE
  expl: (none)
  img: (none)
  parse_notes: multiple bolded cells (2)
```

### `uk-s4-e14-1`

Category: **richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What number sequence replaces the question mark?
  opts: (none)
  ans: 12345
  expl: The numbers indicate the order the letters come alphabetically. The letters in FORTY are in alphabetical order so the answer is 12345.
  img: questions/uk-s4-e14-1.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_14#1pct)
```
  Q: What number sequence replaces the question mark?
  opts: (none)
  ans: 12345
  expl: ONE = 321 TWO = 231 FOUR = 1243 EIGHT = 14235 FORTY = 12345 The numbers indicate the order the letters come alphabetically. The letters in FORTY are in alphabetical order so the answer is 12345. Category:1% Club Season 4
  img: (none)
```

### `uk-s4-e14-20`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: This is something wrong with this list of instructions. What is it?
  opts: (none)
  ans: Number 5 is missing
  expl: The instructions jump from 4 to 6.
  img: questions/uk-s4-e14-20.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_14#20pct)
```
  Q: There is something wrong with this list of instructions. What is it? 1) PUT TEABAG INTO MUG 2) FILL KETTLE WITH WATER AND BRING TO BOIL 3) POUR BOILING WATER INTO MUG 4) ALLOW TO REST TO REACH REQUIRED STRENGTH 6) REMOVE TEABAG FROM MUG ...
  opts: (none)
  ans: Number 5 is missing
  expl: The instructions jump from 4 to 6.
  img: (none)
```

### `uk-s4-e14-5`

Category: **we_have_placeholder_wiki_has_real_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: The words below go before the names of different body parts to make well-known terms. Put the words in order from highest to lowest according to where on this body the relevant parts are.
  opts: (none)
  ans: C, A, D, B
  expl: [It goes EAGLE EYE, TREASURE CHEST, BUTTERFINGERS, and ACHILLES HEEL.]
  img: questions/uk-s4-e14-5.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_14#5pct)
```
  Q: The words below go before the names of different body parts to make well-known terms. Put the words in order from highest to lowest according to where on this body the relevant parts are.  D
  opts: ['TREASURE', 'ACHILLES', 'EAGLE', 'BUTTER', 'CHEST', 'HEEL', 'EYE', 'FINGERS']
  ans: (none)
  expl: CADB
  img: Human.png
  parse_notes: no bolded correct cell
```

### `uk-s4-e14-50`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What replaces the question mark in this sequence?
  opts: (none)
  ans: CUB
  expl: Each word has an E added to it to describe the picture. FIR / FIRE, KIT / KITE and then CUB / CUBE.
  img: questions/uk-s4-e14-50.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_14#50pct)
```
  Q: What replaces the question mark in this sequence?
  opts: (none)
  ans: E
  expl: Each word has an E added to it to describe the picture. FIR / FIRE, KIT / KITE and then CUB / CUBE
  img: CUB.png
```

### `uk-s4-e14-60`

Category: **wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Who does not belong in this group?
  opts: ['CARL NOONAN', 'DAN THOMAS', 'MEG NIGHTINGALE', 'BECKY MORNINGSIDE']
  ans: DAN THOMAS
  expl: All the others have a time of day in their name. [NOON in NOONAN, NIGHT in NIGHTINGALE, MORNING in MORNINGSIDE.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_14#60pct)
```
  Q: Who does not belong in this group?
  opts: ['CARL NOONAN', 'DAN THOMAS', 'MEG NIGHTINGALE', 'BECKY MORNINGSIDE']
  ans: (none)
  expl: (none)
  img: (none)
  parse_notes: no bolded correct cell
```

### `uk-s4-e14-70`

Category: **we_have_placeholder_wiki_has_real_options, answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What new word can be formed by joining together one word from each of the three boxes below?
  opts: (none)
  ans: CONTESTANT
  expl: (none)
  img: questions/uk-s4-e14-70.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_14#70pct)
```
  Q: What new word can be formed by joining together one word from each of the three boxes below?
  opts: ['CON', 'EXAM', 'MOTH']
  ans: CON
  expl: (none)
  img: (none)
```

### `uk-s4-e15-1`

Category: **richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which commonly used word can go in front of these words to make three new words?  SING BAG RING
  opts: (none)
  ans: TEA
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#1pct)
```
  Q: Which commonly used word can go in front of these words to make three new words?
  opts: (none)
  ans: TEA
  expl: TEASING TEABAG TEARING Category:1% Club Season 4
  img: (none)
```

### `uk-s4-e15-15`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What three consecutive numbers add up to 3000?
  opts: (none)
  ans: 999, 1000, 1001
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#15pct)
```
  Q: What three consecutive numbers add up to 3000?
  opts: (none)
  ans: 999, 1000 and 1001
  expl: (none)
  img: (none)
```

### `uk-s4-e15-20`

Category: **richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What number replaces the question mark below?  E – 1 = F W – 2 = V Q – 1 = 0 H – 2 = I E – ? = L
  opts: (none)
  ans: 2
  expl: The number refers to the number of lines that get removed from the first letter to make the second letter.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#20pct)
```
  Q: What number replaces the question mark below?
  opts: (none)
  ans: 2
  expl: E – 1 = F W – 2 = V Q – 1 = O H – 2 = I E - 2 = L The number refers to the number of lines that get removed from the first letter to make the second letter.
  img: (none)
```

### `uk-s4-e15-25`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What letter replaces the question mark in this sequence?
  opts: (none)
  ans: R
  expl: The letters represent the first letter of their positions within the boxes – UP, DOWN, LEFT and then R for RIGHT.
  img: questions/uk-s4-e15-25.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#25pct)
```
  Q: What letter replaces the question mark in this sequence?
  opts: (none)
  ans: U
  expl: The letters represent the first letter of their positions within the boxes – UP, DOWN, LEFT and then R for RIGHT.
  img: UDLR.png
```

### `uk-s4-e15-35`

Category: **different_question_text, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What number replaces the question mark when you read clockwise from the start?
  opts: (none)
  ans: 27
  expl: Alternate segments reveal consecutive multiples of three. 27 is the next number in the three times table.
  img: questions/uk-s4-e15-35.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#35pct)
```
  Q: What number replaces the question mark when you read clockwise from the star? Alternate segments reveal consecutive multiples of three. 27 is the next number in the three times table.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Wheel number.png
  parse_notes: no bolded answer
```

### `uk-s4-e15-45`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these is the odd one out?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (B)
  expl: Cows does not rhyme with the others – fox, box and socks.
  img: questions/uk-s4-e15-45.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#45pct)
```
  Q: Which of these is the odd one out? Cows does not rhyme with the others – fox, box and socks.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Animals.png
  parse_notes: no bolded answer
```

### `uk-s4-e15-5`

Category: **different_question_text, answer_substring_mismatch, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: There are six different letters when you write out the number one to ten. What common word can you spell using all of these six letters?  ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN
  opts: (none)
  ans: SOFTEN
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#5pct)
```
  Q: There are six different first letters when you write out the numbers from one to ten. What common word can you spell using all of these six letters?
  opts: (none)
  ans: O
  expl: ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN SOFTEN
  img: (none)
```

### `uk-s4-e15-50`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which colour ring news to be cut to free all the others?
  opts: ['RED', 'GREEN', 'YELLOW', 'BLUE']
  ans: BLUE
  expl: (none)
  img: questions/uk-s4-e15-50.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#50pct)
```
  Q: Which colour ring needs to be cut to free all the others?
  opts: ['RED', 'GREEN', 'YELLOW', 'BLUE']
  ans: BLUE
  expl: (none)
  img: Rings.png
```

### `uk-s4-e15-60`

Category: **different_options, different_correct_answer, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of the words below is not displayed either horizontally, vertically or diagonally in this word search box?
  opts: ['BAT', 'DUCK', 'LIZARD', 'PORCUPINE']
  ans: PORCUPINE
  expl: PORCUPINE has 9 letters so can’t fit in a 6 x 6 grid.
  img: questions/uk-s4-e15-60.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#60pct)
```
  Q: Which of the words below is not displayed either horizontally, vertically or diagonally in this word search box?
  opts: ['P', 'K', 'R', 'U', 'S', 'R', 'L', 'O', 'T', 'C', 'P', 'E', 'D', 'R', 'A', 'Z', 'I', 'L', 'H', 'U', 'B', 'P', 'D', 'A', 'N', 'B', 'C', 'F', 'E', 'H', 'E', 'P', 'A', 'K', 'R', 'W']
  ans: S
  expl: {| class="fandom-table" |BAT |DUCK |LIZARD |- |PORCUPINE |SPIDER |WHALE |} PORCUPINE has 9 letters so can’t fit in a 6 x 6 grid.
  img: (none)
  parse_notes: multiple bolded cells (20)
```

### `uk-s4-e15-80`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of the options does NOT correctly fill in any of the gaps in the sentences below?  At the ATM, Rakesh couldn’t remember his _ number. Bilbo the dog was great at herding sheep into the ___. The greasy frying ___ was the worst thing ...
  opts: ['PAN', 'PUN', 'PIN', 'PEN']
  ans: PUN
  expl: [PIN goes into the first sentence. PEN goes into the second. And PAN goes into third.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#80pct)
```
  Q: At the ATM, Rakesh couldn’t remember his PIN number. Bilbo the dog was great at herding sheep into the PEN. The greasy frying PAN was the worst thing to wash up.  Which of the options does NOT correctly fill in any of the gaps in the sen...
  opts: ['PAN', 'PUN', 'PIN', 'PEN']
  ans: PUN
  expl: (none)
  img: (none)
```

### `uk-s4-e15-90`

Category: **wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which item of cutlery is there the most of in this image?
  opts: ['Knives', 'Forks', 'Spoons']
  ans: Spoons
  expl: There are nine spoons, seven forks and six knives.
  img: questions/uk-s4-e15-90.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_15#90pct)
```
  Q: Which item of cutlery is there the most of in this image?
  opts: ['Knives', 'Forks', 'Spoons']
  ans: (none)
  expl: There are nine spoons, seven forks and six knives.
  img: Cutlery.png
  parse_notes: no bolded correct cell
```

### `uk-s4-e2-1`

Category: **different_question_text, different_correct_answer, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: The words below share a specific pattern. Why could VOTING also be part of the group?  BANDLEADER   NICKELODEON   SILVERBACK
  opts: (none)
  ans: They all contain the names of metals
  expl: [BANDLEADER has LEAD, NICKELODEON has NICKEL, and SILVERBACK has SILVER.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_2#1pct)
```
  Q: (none)
  opts: (none)
  ans: TIN
  expl: The words below share a specific pattern. Why could VOTING also be part of the group? BANDLEADER NICKELODEON SILVERBACK They all contain the names of metals. Category:1% Club Season 4
  img: (none)
  parse_notes: empty question text
```

### `uk-s4-e2-40`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What sport replaces the question mark?
  opts: (none)
  ans: GOLF
  expl: [GOAL – AL + LF = GOLF]
  img: questions/uk-s4-e2-40.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_2#40pct)
```
  Q: Which sport replaces the question mark?
  opts: (none)
  ans: GOLF
  expl: GOAL – AL + LF = GOLF
  img: Golf.png
```

### `uk-s4-e2-5`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Without reordering any letters, how many animals appear in the sequence below?  P H E A S A N T O R T O I S E A L I O N
  opts: (none)
  ans: 6
  expl: PHEASANT, SEALION, ANT, SEAL, TORTOISE and LION. [Yes, ants are animals.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_2#5pct)
```
  Q: Without reordering any letters, how many animals appear in the sequence below? PHEASANTORTOISEALION
  opts: (none)
  ans: 6
  expl: PHEASANT, SEALION, ANT, SEAL, TORTOISE and LION.
  img: (none)
```

### `uk-s4-e2-80`

Category: **wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Lee always paints a circle. Lee never paints squares. Lee always paints four triangles. Which of these is one of Lee’s paintings?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (A)
  expl: B has squares and C has only three triangles so it must be A.
  img: questions/uk-s4-e2-80.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_2#80pct)
```
  Q: Lee always paints a circle. Lee never paints squares. Lee always paints four triangles. Which of these is one of Lee’s paintings?
  opts: (none)
  ans: A
  expl: B has squares and C has only three triangles so it must be A.
  img: Shapes 3.png
```

### `uk-s4-e2-90`

Category: **wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Four people are in a maze trying to reach the centre. Which of them is going the wrong way?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (B)
  expl: [Person B is heading toward dead ends.]
  img: questions/uk-s4-e2-90.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_2#90pct)
```
  Q: Four people are in a maze trying to reach the centre. Which of them is going the wrong way?
  opts: (none)
  ans: B
  expl: (none)
  img: Maze.png
```

### `uk-s4-e3-1`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: If you remove all the underlined letters from the sentence below, what word can be spelt if you rearrange all of the remaining letters?  A N IMAL T O S H UN IN ST A M PE D E
  opts: (none)
  ans: ELEPHANT
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_3#1pct)
```
  Q: If you remove all the underlined letters from the sentence below, what word can be spelt if you rearrange all of the remaining letters? ANIMAL TO SHUN IN STAMPEDE
  opts: (none)
  ans: ELEPHANT
  expl: Category:1% Club Season 4
  img: (none)
```

### `uk-s4-e3-10`

Category: **different_question_text, different_correct_answer, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Is saw this newspaper headline on a ski trip. Which word is the odd one out?  Skiing officials allegedly announce accidents will soon require immediate attention
  opts: (none)
  ans: “require”
  expl: It’s the only word that doesn’t contain double letters.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_3#10pct)
```
  Q: I saw this newspaper headline on a ski trip. Which word is the odd one out?
  opts: (none)
  ans: ii
  expl: Skiing officials allegedly announce accidents will soon require immediate attention It’s the only word that doesn’t contain double letters.
  img: (none)
```

### `uk-s4-e3-30`

Category: **we_have_placeholder_wiki_has_real_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: If you begin at one of the corners of this square and move clockwise around the outer edge to finish in the centre, what nine-letter word can you spell?
  opts: (none)
  ans: SEARCHING
  expl: [Start with the letter S and go clockwise around the board.]
  img: questions/uk-s4-e3-30.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_3#30pct)
```
  Q: If you begin at one of the corners of this square and move clockwise around the outer edge to finish in the centre, what nine-letter word can you spell?
  opts: ['C', 'H', 'I', 'R', 'G', 'N', 'A', 'E', 'S']
  ans: (none)
  expl: SEARCHING
  img: (none)
  parse_notes: no bolded correct cell
```

### `uk-s4-e3-35`

Category: **wiki_missing_options, different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of the options links the following?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (D)
  expl: The word CAR goes in front of each of the words to make new words. [This creates the words CARPET, CARGO, and CARNATION.
  img: questions/uk-s4-e3-35.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_3#35pct)
```
  Q: Which of the options links the following?
  opts: (none)
  ans: CAR
  expl: CARPET CARGO CARNATION The word CAR goes in front of each of the words to make new words.
  img: (none)
```

### `uk-s4-e3-45`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Without reordering any letters, what fruit appears in the sentence below?  I’D MAKE MY OWN JUICE WHILE MONEY ROLLS IN
  opts: (none)
  ans: LEMON
  expl: [It’s found between WHILE and MONEY.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_3#45pct)
```
  Q: Without reordering any letters, what fruit appears in the sentence below?
  opts: (none)
  ans: LE MON
  expl: I’D MAKE MY OWN JUICE WHILE MONEY ROLLS IN
  img: (none)
```

### `uk-s4-e3-60`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Amlan is very particular about how he lays out the apps on his home screen. Which of these completes Amlan’s layout?
  opts: ['PLUM', 'BAKE', 'MILK']
  ans: MILK
  expl: [The logos on the apps spell out DON’T CRY OVER SPILT… and so MILK completes the sequence.]
  img: questions/uk-s4-e3-60.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_3#60pct)
```
  Q: Amlan is very particular about how he lays out the apps on his home screen. Which of these completes Amlan’s layout? The logos on the apps spell out DON’T CRY OVER SPILT… and so MILK completes the sequence.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Apps.png
  parse_notes: no bolded answer
```

### `uk-s4-e3-70`

Category: **missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Serena is about to cast a vote for her local council. She picks the candidate with a name that is an anagram of ‘electoral system’. Who does she vote for?
  opts: ['Caroline Genteel', 'Scarlett Moseley', 'Nicola Gollete', 'Phil Gobolton', 'Lexi Plot']
  ans: Scarlett Moseley
  expl: It’s the only name that has any Ss.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_3#70pct)
```
  Q: Serena is about to cast a vote for her local council. She picks the candidate with a name that is an anagram of ‘electoral system’. Who does she vote for?
  opts: ['Caroline Genteel', 'Scarlett Moseley', 'Nicola Collete', 'Phil Gobolton', 'Lexi Plot', 'general election', 'electoral system', 'local election', 'polling booth', 'exit poll']
  ans: Scarlett Moseley
  expl: It’s the only name that has any Ss
  img: (none)
  parse_notes: multiple bolded cells (2)
```

### `uk-s4-e3-80`

Category: **different_question_text, wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Shanti is bored and removes her sunglasses, keys, pen, train ticket and lipstick from her handbag, puts them in alphabetical order and takes a photo from above. Which of these is the correct photo?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (B)
  expl: [In alphabetical order, it goes Keys, Lipstick, Pen, Sunglasses, and Train Ticket.]
  img: questions/uk-s4-e3-80.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_3#80pct)
```
  Q: Shanti is bored and removes her sunglasses, keys, pen, train ticket and lipstick from her handbag, pugs them in alphabetical order and takes a photo from above. Which of these is the correct photo?
  opts: (none)
  ans: B
  expl: (none)
  img: Train.png
```

### `uk-s4-e3-90`

Category: **missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these does not make a word when the letters are placed in reverse order?
  opts: ['STUN', 'DUST', 'SNUB']
  ans: DUST
  expl: [DUST reversed is TSUD, which isn’t a word.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_3#90pct)
```
  Q: Which of these does not make a word when the letters are placed in reverse order?
  opts: ['STUN', 'DUST', 'SNUB', 'NUTS', 'TSUD', 'BUNS']
  ans: DUST
  expl: (none)
  img: (none)
  parse_notes: multiple bolded cells (2)
```

### `uk-s4-e4-1`

Category: **richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What common four-word phrase is represented here?  SPRAINED ANKLE + “YOU ARE STUPID!”
  opts: (none)
  ans: ADDING INSULT TO INJURY
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_4#1pct)
```
  Q: What common four-word phrase is represented here? SPRAINED ANKLE + “YOU ARE STUPID!”
  opts: (none)
  ans: ADDING INSULT TO INJURY
  expl: ADDING INSULT TO INJURY is the answer. Category:1% Club Season 4
  img: (none)
```

### `uk-s4-e4-10`

Category: **different_question_text, answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Each of the gaps below can be filled by a different three-letter sequences that goes after the first word and before the second word to make two new words. What nine-letter word is made when you put the three sequences together, in order...
  opts: (none)
  ans: BARTENDER
  expl: [BAR completes HANDLEBAR and BARBELL. TEN completes FORGOTTEN and TENANT. DER completes SHREDDER and DERBY.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_4#10pct)
```
  Q: Each of the gaps below can be filled by a different three-letter sequence that goes after the first word and before the second word to make two new words. What nine-letter word is made when you put the three sequences together, in order?
  opts: (none)
  ans: BAR
  expl: HANDLE BAR BELL FORGOT TEN ANT SHRED DER BY BARTENDER is the answer.
  img: (none)
```

### `uk-s4-e4-15`

Category: **different_question_text, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: You roll three standard dice to find a three-digit number, e.g. 235. What is the highest number you can roll where all digits add up to 10?
  opts: (none)
  ans: 631
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_4#15pct)
```
  Q: (none)
  opts: (none)
  ans: 631
  expl: You roll three standard dice to find a three-digit number, e.g. 235. What is the highest number you can roll where all three digits add up to 10? 631 is the answer.
  img: (none)
  parse_notes: empty question text
```

### `uk-s4-e4-20`

Category: **different_options, wiki_missing_answer, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: The words in each square have something in common that puts them in that square. Which of these words can go into all three squares?
  opts: ['STOP', 'BRING', 'LEVEL', 'PEEP']
  ans: PEEP
  expl: The word needs to read the same backwards and forwards (first square), end with a P (second square) and have four letters (third square).
  img: questions/uk-s4-e4-20.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_4#20pct)
```
  Q: The words in each square have something in common that puts them in that square. Which of these words can go into all three squares?
  opts: ['REFER NOON EYE', 'TAP RIP SHIP', 'BEAN RANT CHIP']
  ans: (none)
  expl: {| class="fandom-table" |STOP |BRING |LEVEL |PEEP |} The answer is that the word needs to read the same backwards and forwards (first square), end with a P (second square) and have four letters (third square).
  img: (none)
  parse_notes: no bolded correct cell
```

### `uk-s4-e4-30`

Category: **missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: In a new word game, you score one point for every letter in the word. Then you take off two points if the word contains the letter E. Finally, double the points if the word contains a double letter. Which of these words would score the h...
  opts: ['QUIZ', 'FITTING', 'CORRECT', 'QUICKSAND']
  ans: FITTING
  expl: [FITTING will score 14 points. Meanwhile, QUIZ will score 4 points, CORRECT 10 points, and QUICKSAND 9 points.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_4#30pct)
```
  Q: In a new word game, you score one point for every letter in the word. then you take off two points if the word contains the letter E. Finally, double the points if the word contains a double letter. Which of these words would score the h...
  opts: ['QUIZ', 'FITTING', 'CORRECT', 'QUICKSAND', '4 points', '14 points', '10 points', '9 points']
  ans: FITTING
  expl: FITTING is the answer.
  img: (none)
```

### `uk-s4-e4-40`

Category: **missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of the following words cannot have a letter removed to leave a real word that sounds exactly the same as before?
  opts: ['Chord', 'Boarder', 'Source', 'Mourning']
  ans: Source
  expl: [Chord can be turned into Cord, Boarder into Border, and Mourning into Morning.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_4#40pct)
```
  Q: Which of the following words cannot have a letter removed to leave a real word that sounds exactly the same as before?
  opts: ['Chord', 'Boarder', 'Source', 'Mourning', 'Cord', 'Border', 'Morning']
  ans: Source
  expl: The answer is that Sorce is not a real word.
  img: (none)
```

### `uk-s4-e4-5`

Category: **different_question_text, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: If you remove all the words in this sentence that contain recurring letters within them, which becomes the ninth word in this sentence?
  opts: (none)
  ans: word
  expl: [‘Recurring letters’ here means letters that occur more than once in a word.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_4#5pct)
```
  Q: (none)
  opts: (none)
  ans: word
  expl: If you remove all the words in this sentence that contain recurring letters within them, which becomes the ninth word in this sentence? The word in bold is the answer.
  img: (none)
  parse_notes: empty question text
```

### `uk-s4-e4-60`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Sisters Holly, Alisha, Steph and Eliza all booked an appointment at their favourite hairdresser on the same day. Steph went after Alisha and Holly were first. If Eliza went after Steph, what order did the girls go in?
  opts: ['Holly, Steph, Alisha, Eliza', 'Holly, Eliza, Alisha, Steph', 'Holly, Alisha, Steph, Eliza']
  ans: Holly, Alisha, Steph, Eliza
  expl: [In A Steph doesn’t go after Alisha. And in B Eliza doesn’t go after Steph.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_4#60pct)
```
  Q: Sisters Holly, Alisha, Steph and Eliza all booked an appointment at their favourite hairdresser on the same day. Steph went after Alisha and Holly went first. If Eliza went after Steph, what order did the girls go in?
  opts: ['Holly, Steph, Alisha, Eliza', 'Holly, Eliza, Alisha, Steph', 'Holly, Alisha, Steph, Eliza']
  ans: Holly, Alisha, Steph, Eliza
  expl: The third one is the answer.
  img: (none)
```

### `uk-s4-e4-70`

Category: **different_question_text, wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these dominos has more spots than the number of wheels on two tricycles but fewer than the legs on two zebras?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (B)
  expl: There are six wheels on two tricycles and eight legs on two zebras so it has to be B. [It has seven dots.]
  img: questions/uk-s4-e4-70.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_4#70pct)
```
  Q: Which of these dominoes has more spots than the number of wheels on two tricycles but fewer than the legs on two zebras?
  opts: (none)
  ans: B
  expl: The answer is that there are six wheels on two tricycles and eight legs on two zebras so it has to be B.
  img: Dominoes.png
```

### `uk-s4-e5-1`

Category: **different_question_text, answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Peter has recently found his old diary that he’d written in secret code but he can’t remember how to decipher what he wrote. Can you check the code to find out what the underlined word is?  WH89 I GR1W UP I WA92 21 B8 A 5L1RI72
  opts: (none)
  ans: FLORIST
  expl: Where he could, he replaced a letter with a digit that starts with that letter. [An alternate method is figuring out that the 1 is an O from GR1W (GROW) and the 2 is a T from WA92 (WANT). That makes the last word _LORI_T, and from there ...
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_5#1pct)
```
  Q: Peter has recently found his old diary that he’d written in secret code but he can’t remember how to decipher what he wrote. Can you crack the code to find out what the underlined word is?
  opts: (none)
  ans: WHEN I GROW UP I WANT TO BE A FLORIST
  expl: WH89 I GR1W UP I WA92 21 B8 A 5L1RI72 WHEN I GROW UP I WANT TO BE A FLORIST Where he could, he replaced a letter with a digit that starts with that letter. Category:1% Club Season 4
  img: (none)
```

### `uk-s4-e5-10`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: There are four letters written on the circle. The other letters are all outside the circle. You need to turn the circle clockwise until a colour is spelt out. How many 90 degree turns do you need to make?
  opts: (none)
  ans: 2
  expl: After two turns, the p turns to d so the word red appears.
  img: questions/uk-s4-e5-10.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_5#10pct)
```
  Q: There are four letters written on the circle. The other letters are all outside the circle. You need to turn the circle clockwise until a colour is spelt out. How many 90 degree turns do you need to make?
  opts: (none)
  ans: two
  expl: After two turns, the p turns to d so the word red appears.
  img: Colour 2.png
```

### `uk-s4-e5-15`

Category: **different_question_text, different_correct_answer, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: If my old brown woolly jumper contains two holes for every o in this sentence, how many holes are there?
  opts: (none)
  ans: 22
  expl: The letter o appears 11 times. 11 x 2 = 22.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_5#15pct)
```
  Q: (none)
  opts: (none)
  ans: o
  expl: If my old brown woolly jumper contains two holes for every o in this sentence, how many holes are there? The letter o appears 11 times. 11 x 2 = 22
  img: (none)
  parse_notes: empty question text
```

### `uk-s4-e5-20`

Category: **answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: There is only one number missing from this pattern?
  opts: (none)
  ans: 4
  expl: There’s one 1, two 2s, three 3s and five 5s but only three 4s.
  img: questions/uk-s4-e5-20.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_5#20pct)
```
  Q: There is only one number missing from this pattern. What is it?
  opts: (none)
  ans: 4s
  expl: There’s one 1, two 2s, three 3s and five 5s but only three 4s.
  img: Number pattern.png
```

### `uk-s4-e5-25`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which three different whole numbers – all lower than 10 – give you the same total whether you add them together or multiply them together?
  opts: (none)
  ans: 1, 2, and 3
  expl: 1 + 2 + 3 = 6 and 1 x 2 x 3 = 6.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_5#25pct)
```
  Q: Which three different whole numbers – all lower than 10 – give you the same total whether you add them together or multiply them together? 1 + 2 + 3 = 6 and 1 x 2 x 3 = 6
  opts: (none)
  ans: (none)
  expl: (none)
  img: (none)
  parse_notes: no bolded answer
```

### `uk-s4-e5-35`

Category: **answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What single word goes in the gaps below to make new words?  QUICK_____ THOU_____ _____STONE
  opts: (none)
  ans: SAND
  expl: [This makes QUICKSAND, THOUSAND, and SANDSTONE.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_5#35pct)
```
  Q: What single word goes in the gaps below to make new words?
  opts: (none)
  ans: <u>SAND</u>
  expl: QUICKSAND THOUSAND SANDSTONE
  img: (none)
```

### `uk-s4-e5-45`

Category: **answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: If you remove a playing card from the first word, a pet from the second word, an insect from the third word and a drink from the fourth word, what number appears?  FACE COAT AUNT TEAR
  opts: (none)
  ans: FOUR
  expl: [Remove ACE from FACE, CAT from COAT, ANT from AUNT, and TEA from TEAR.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_5#45pct)
```
  Q: If you remove a playing card from the first word, a pet from the second word, an insect from the third word and a drink from the fourth word, what number appears?
  opts: (none)
  ans: F
  expl: FACE COAT AUNT TEAR FOUR
  img: (none)
```

### `uk-s4-e5-5`

Category: **answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Today, the three witches in Macbeth are discussing when the three should meet again. Witch 1 is available every fourth day, Witch 2 is available every fifth day, and Witch 3 is available every sixth day. How many days from today will the...
  opts: (none)
  ans: 60 days
  expl: 60 is the first number that is divisible by four, five and six.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_5#5pct)
```
  Q: Today, the three witches in Macbeth are discussing when the three should meet again. Witch 1 is available every fourth day, Witch 2 is available every fifth day and Witch 3 is available every sixth day. How many days from today will they...
  opts: (none)
  ans: 60
  expl: 60 is the first number that is divisible by four, five and six.
  img: (none)
```

### `uk-s4-e5-60`

Category: **different_correct_answer, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What four-letter word replaces the question mark?  SOFTENING –> SONG RADIOACTIVE –> RAVE WHITECOAT –> WHAT FAVOURITE –> ?
  opts: (none)
  ans: FATE
  expl: Each new word is created by using the first two and the last two letters of the original.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_5#60pct)
```
  Q: What four-letter word replaces the question mark?
  opts: (none)
  ans: SO
  expl: SOFTENING <math>\rightarrow</math> SONG RADIOACTIVE <math>\rightarrow</math> RAVE WHITECOAT <math>\rightarrow</math> WHAT FAVOURITE <math>\rightarrow</math> FATE Each new word is created by using the first two and the last two letters of...
  img: (none)
```

### `uk-s4-e5-70`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these structures is made up of a different set of blocks to the other two?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (C)
  expl: C has a difference orange block and is missing the green bridge.
  img: questions/uk-s4-e5-70.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_5#70pct)
```
  Q: Which of these structures is made up of a different set of blocks to the other two? C has a different orange block and is missing the green bridge.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Blocks.png
  parse_notes: no bolded answer
```

### `uk-s4-e6-10`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Answer this question: What word do you get if you take the third letter of the alphabet and and and the twenty-fifth letter of the twenty-fifth letter of the alphabet?
  opts: (none)
  ans: CANDY
  expl: C and AND and Y.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_6#10pct)
```
  Q: Answer this question: What word do you get if you take the third letter of the alphabet and and and the twenty-fifth letter of the alphabet?
  opts: (none)
  ans: candy
  expl: c and and and y.
  img: (none)
```

### `uk-s4-e6-20`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which prominent UK person is this rhyming code for?
  opts: (none)
  ans: Keir Starmer
  expl: Kier Starmer rhymes with Deer Llama.
  img: questions/uk-s4-e6-20.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_6#20pct)
```
  Q: Which prominent UK person is this rhyming code for?
  opts: (none)
  ans: Kier Starme
  expl: Kier Starmer rhymes with Deer Llama.
  img: Kier Starmer.png
```

### `uk-s4-e6-25`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Maddie’s step counter watch starts at zero at the bottom of a staircase. She climbs 35 stairs but drops her watch to the very bottom and runs down to pick it up. When she gets to the top of the stairs, her watch says she has climbed 100 ...
  opts: (none)
  ans: 65 steps
  expl: 100 steps minus the 35 she originally climbed means the staircase is 65 steps high. The steps on the way back down weren’t counted because she has dropped the watch.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_6#25pct)
```
  Q: Maddie’s step counter watch starts at zero at the bottom of a staircase. She climbs 35 stairs but drops her watch to the very bottom and runs down to pick it up. When she gets to the top of the stairs, her watch says she has climbed 100 ...
  opts: (none)
  ans: (none)
  expl: (none)
  img: (none)
  parse_notes: no bolded answer
```

### `uk-s4-e6-30`

Category: **different_question_text, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: If image A is Downtime, what is image B?
  opts: (none)
  ans: Bigwig
  expl: TOWN is written down = Downtown, WIG is big = Bigwig.
  img: questions/uk-s4-e6-30.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_6#30pct)
```
  Q: If image A is Downtown, what is image B? TOWN is written down – Downtown, WIG is big = Bigwig.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Downtown.png
  parse_notes: no bolded answer
```

### `uk-s4-e6-35`

Category: **wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these words would logically come next in this sequence?  ABUZZ BREEZY COMPLEX
  opts: ['DETOX', 'DIARY', 'DRAW']
  ans: DRAW
  expl: The start of every word goes forward one letter alphabetically and the end of every word goes back one letter.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_6#35pct)
```
  Q: Which of these words would logically come next in this sequence?  ABUZZ BREEZY COMPLEX
  opts: ['DETOX', 'DIARY', 'DRAW']
  ans: (none)
  expl: The start of every word goes forward one letter alphabetically and the end of every word goes back one letter.
  img: (none)
  parse_notes: no bolded correct cell
```

### `uk-s4-e6-45`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Three people are singing ‘Head, Shoulders, Knees and Toes’. Tom does the four actions to match the lyrics. Dick always does the four actions in the reverse order to how they appear in the title. Harry does the four actions in alphabetica...
  opts: (none)
  ans: 2
  expl: Tom goes Head, Shoulders, Knees, Toes. Dick goes Toes, Knees, Shoulders, Head. Harry goes Head, Knees, Shoulders, Toes.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_6#45pct)
```
  Q: Three people are singing ‘Head, Shoulders, Knees and Toes’. Tom does the four actions to match the lyrics. Dick always does the four actions in the reverse order to how they appear in the title. Harry does the four actions in alphabetica...
  opts: (none)
  ans: Dick
  expl: Tom – Head, Shoulders, Knees, Toes. Dick – Toes, Knees, Shoulders, Head. Harry – Head, Knees, Shoulders, Toes.
  img: (none)
```

### `uk-s4-e6-50`

Category: **wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: This arrow is pointing up. Logically, which of these words could also go into the arrow.
  opts: ['KITTEN', 'PUPPY', 'CALF']
  ans: PUPPY
  expl: All the words in the arrow have the word UP in them.
  img: questions/uk-s4-e6-50.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_6#50pct)
```
  Q: This arrow is pointing up. Logically, which of these words could also go into the arrow?
  opts: ['KITTEN', 'PUPPY', 'CALF']
  ans: (none)
  expl: All the words in the arrow have the word UP in them.
  img: Up arrow.png
  parse_notes: no bolded correct cell
```

### `uk-s4-e6-70`

Category: **different_options, different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Nicole is trying to think of a new password for her email account. She is going to use her middle name, an animal and a colour in a random order. Which of the following passwords must be hers?
  opts: ['Sarah SharkStick', 'Olivia OrangeOlga', 'Purple ParrotPaula']
  ans: Purple ParrotPaula
  expl: A doesn’t have a colour and B has no animal.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_6#70pct)
```
  Q: Nicole is trying to think of a new password for her email account. She is going to use her middle name, an animal and a colour in a random order. Which of the following passwords must be hers?
  opts: ['SarahSharkStick', 'OliviaOrangeOlga', 'PurpleParrotPaula']
  ans: PurpleParrotPaula
  expl: A doesn’t have a colour and B has no animal.
  img: (none)
```

### `uk-s4-e7-1`

Category: **richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What is the lowest number to have the same value as ten times the number of letters in its name?
  opts: (none)
  ans: FIFTY
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_7#1pct)
```
  Q: What is the lowest number to have the same value as ten times the number of letters in its name?
  opts: (none)
  ans: FIFTY
  expl: FIFTY has five letters. 5 x 10 = 50 Category:1% Club Season 4
  img: (none)
```

### `uk-s4-e7-10`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: In this puzzle, which one of these words doesn’t belong?
  opts: (none)
  ans: HUNG
  expl: All the other wards can be paired to make the names of countries (GERMANY, DENMARK, NORWAY, ICELAND, and SPAIN). You would need ARY to make HUNG+ARY.
  img: questions/uk-s4-e7-10.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_7#10pct)
```
  Q: In this puzzle, which one of these words doesn’t belong? All the other words can be paired to make the names of countries. You would need ARY to make HUNG+ARY.
  opts: (none)
  ans: (none)
  expl: (none)
  img: HUNGARY.png
  parse_notes: no bolded answer
```

### `uk-s4-e7-25`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: This figure (picture of a man) starts in square number 1. It makes each time in the direction in which it points. What number square does it end up in?
  opts: (none)
  ans: 19
  expl: (none)
  img: questions/uk-s4-e7-25.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_7#25pct)
```
  Q: This figure starts in square 1. It makes ten moves as shown below. It moves each time in the direction in which it points. What number square does it end up in?
  opts: (none)
  ans: 19
  expl: (none)
  img: Man square.png
```

### `uk-s4-e7-40`

Category: **different_question_text, wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Barbra is about to perform in the opening night of a West End show and is looking out for her partner, James. She knows he is sitting in row B, seat 8. Where does he appear from her view on stage?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (B)
  expl: [It would be the second row but going from seats 9 to 1 from left to right.]
  img: questions/uk-s4-e7-40.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_7#40pct)
```
  Q: Barbra is about to perform in the opening night of a West End show and is looking out for her partner, James. She knows he is sitting in row B, seat 8. Where does he appear from her view on the stage?
  opts: (none)
  ans: B
  expl: (none)
  img: Stage.png
```

### `uk-s4-e7-45`

Category: **different_question_text, missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these words can have two of its letters swapped over and still result in a valid word?
  opts: ['CONVERSATION', 'DIALOGUE', 'CHAT']
  ans: CONVERSATION
  expl: [The V and S in CONVERSATION can be swapped to form the word CONSERVATION.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_7#45pct)
```
  Q: Which of these can have two of its letters swapped over and still result in a valid word?
  opts: ['CONVERSATION', 'DIALOGUE', 'CHAT', 'CONSERVATION']
  ans: (none)
  expl: (none)
  img: (none)
  parse_notes: no bolded correct cell
```

### `uk-s4-e7-5`

Category: **different_correct_answer, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: How many different words are there in the tongue twister below?  SHE SELLS SEA SHELLS BY THE SEASHORE. THE SHELLS SHE SELLS ARE SURELY SEA SHELLS. SO IF SHE SELLS SHELLS ON THE SEASHORE, I AM SURE SHE SELLS SEASHORE SHELLS.
  opts: (none)
  ans: 15
  expl: [The words are SHE, SELLS, SEA, SHELLS, BY, THE, SEASHORE, ARE, SURELY, SO, IF, ON, I, AM, and SURE.]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_7#5pct)
```
  Q: How many different words are there in the tongue twister below?
  opts: (none)
  ans: SHE SELLS SEA SHELLS BY THE SEASHORE
  expl: SHE SELLS SEA SHELLS BY THE SEASHORE. THE SHELLS SHE SELLS ARE SURELY SEA SHELLS. SO IF SHE SELLS SHELLS ON THE SEASHORE, I AM SURE SHE SELLS SEASHORE SHELLS. 15
  img: (none)
```

### `uk-s4-e7-60`

Category: **wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these butterflies is exactly the same on both sides?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (B)
  expl: [A is missing a left antennae while C has different dot placements between the lower left and lower right wings.]
  img: questions/uk-s4-e7-60.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_7#60pct)
```
  Q: Which of these butterflies is exactly the same on both sides?
  opts: (none)
  ans: B
  expl: (none)
  img: Butterflies.png
```

### `uk-s4-e7-70`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: The rules of this puzzle are that the triangle can fit inside both the circle and the square. However, the circle can only fit inside the square. Which of these is the only one which follows the rules?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (C)
  expl: C is the only option in which the circle fits inside the square.
  img: questions/uk-s4-e7-70.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_7#70pct)
```
  Q: The rules of this puzzle are that the triangle can fit inside both the circle and the square. However, the circle can only fit inside the square. Which of these is the only one which follows the rules? C is the only option in which the c...
  opts: (none)
  ans: (none)
  expl: (none)
  img: SQUARE CIRCLE.png
  parse_notes: no bolded answer
```

### `uk-s4-e7-80`

Category: **different_correct_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What word is represented here?  LEM ADE
  opts: (none)
  ans: LEMONADE
  expl: LEM is on ADE.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_7#80pct)
```
  Q: What word is represented here?
  opts: (none)
  ans: <BR>
  expl: LEM ADE LEMONADE: LEM is on ADE.
  img: (none)
```

### `uk-s4-e7-90`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of the following emojis replaces the question mark in this sequence?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (C)
  expl: The bottom row of emojis are upset and C is the only option that follows that pattern.
  img: questions/uk-s4-e7-90.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_7#90pct)
```
  Q: Which of the following emojis replaces the question mark in this sequence? The bottom row of emojis are upset and C is the only option that follows that pattern.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Emojis.png
  parse_notes: no bolded answer
```

### `uk-s4-e8-1`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Yolande takes one tablet on every day of the week that has three vowels in it. She starts this pack on 2nd March. What date will she need to start a new pack?
  opts: (none)
  ans: 26th March
  expl: There are 10 tablets and she has to take one every Saturday, Tuesday, and Wednesday.
  img: questions/uk-s4-e8-1.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#1pct)
```
  Q: Yolande takes one tablet on every day of the week that has three vowels in total in it. She starts this pack on 2nd March. What date will she need to start a new pack?
  opts: (none)
  ans: 26th March
  expl: There are 10 tablets and she has to take one every Saturday, Tuesday and Wednesday. Category:1% Club Season 4
  img: Pill.png
```

### `uk-s4-e8-10`

Category: **answer_substring_mismatch, richer_explanation_on_wiki**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What job do you get by following these dates?  1st FEBRUARY 2nd MARCH 3rd APRIL 1st MAY 4th JUNE 9th SEPTEMBER
  opts: (none)
  ans: FARMER
  expl: The date corresponds to the position of the letter in the name of the month so 1st FEBRUARY is F, 2nd MARCH is A and so on.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#10pct)
```
  Q: What job do you get by following these dates?
  opts: (none)
  ans: F
  expl: 1st FEBRUARY 2nd MARCH 3rd APRIL 1st MAY 4th JUNE 9th SEPTEMBER The date corresponds to the position of the letter in the name of the month so 1st FEBRUARY is F, 2nd MARCH is A and so on.
  img: (none)
```

### `uk-s4-e8-20`

Category: **we_have_placeholder_wiki_has_real_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Give this question a whirl. What is the answer?
  opts: (none)
  ans: TWELVE
  expl: Start at the W in the top left and wind around the box to reveal the question “WHAT IS THE TEN PLUS TWO?”
  img: questions/uk-s4-e8-20.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#20pct)
```
  Q: Give this question a whirl. What is the answer?
  opts: ['W', 'U', 'L', 'P', 'H', 'S', 'O', 'N', 'A', 'T', 'W', 'E', 'T', 'I', 'S', 'T']
  ans: (none)
  expl: TWELVE: Start at the W in the top left and wind around the box to reveal the question “WHAT IS TEN PLUS TWO?”
  img: (none)
  parse_notes: no bolded correct cell
```

### `uk-s4-e8-25`

Category: **wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these images below completes the sequence?(A), (B), (C), and (D)
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (C)
  expl: The dice rotates to the left each time.
  img: questions/uk-s4-e8-25.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#25pct)
```
  Q: Which of these images below completes the sequence?
  opts: (none)
  ans: C
  expl: The dice rotates to the left each time.
  img: Dice2.png
```

### `uk-s4-e8-30`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which word is the odd one out when everything is paired up?
  opts: (none)
  ans: KALE
  expl: BEEF, LAMG and PORK are meats. KALE is a vegetable.
  img: questions/uk-s4-e8-30.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#30pct)
```
  Q: Which word is the odd one out when everything is paired up? BEEF, LAMB and PORK are meats. KALE is a vegetable
  opts: (none)
  ans: (none)
  expl: (none)
  img: Kale.png
  parse_notes: no bolded answer
```

### `uk-s4-e8-35`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Andy, Brian and Chris go to a tapas restaurant where every dish on the menu is the same price. They agree to split the bill equally. Andy orders twice as many dishes as Brian and Brian orders twice as many dishes as Chris. The total bill...
  opts: (none)
  ans: £20
  expl: The question states they agree to split the bill equally so they will pay £20 each.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#35pct)
```
  Q: Andy, Brian and Chris go to a tapas restaurant where every dish on the menu is the same price. They agree to split the bill equally. Andy orders twice as many dishes as Brian and Brian orders twice as many dishes as Chris. The total bill...
  opts: (none)
  ans: (none)
  expl: (none)
  img: (none)
  parse_notes: no bolded answer
```

### `uk-s4-e8-40`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these images can never produce a correct compass image, no matter how many times you rotate it or flip it?
  opts: (none)
  ans: In B, when the Nand the S come into the right positions, the E and the W are back to front and in the wrong positions
  expl: (none)
  img: questions/uk-s4-e8-40.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#40pct)
```
  Q: Which of these images can never produce a correct compass image, no matter how many times you rotate it or flip it? In B, when the N and the S come into the right positions, the E and the W are back to front and in the wrong positions.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Compass2.png
  parse_notes: no bolded answer
```

### `uk-s4-e8-45`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What word can go after each of these images to make three well-known things?
  opts: (none)
  ans: ROLL
  expl: Sausage ROLL, drum ROLL, and spring ROLL.
  img: questions/uk-s4-e8-45.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#45pct)
```
  Q: What word can go after each of these images to make three well-known things? sausage ROLL, drum ROLL and spring ROLL.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Roll.png
  parse_notes: no bolded answer
```

### `uk-s4-e8-50`

Category: **we_have_placeholder_wiki_has_real_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these words is the only one without an identical match?
  opts: (none)
  ans: DING
  expl: (none)
  img: questions/uk-s4-e8-50.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#50pct)
```
  Q: Which of these words is the only one without an identical match?
  opts: ['RING', 'KNOCK', 'BEEP', 'CHOP', 'BAM', 'BANG', 'BEEP', 'RING', 'BOOM', 'BAM', 'BANG', 'KNOCK', 'BOOM', 'DING', 'CHOP']
  ans: DING
  expl: (none)
  img: (none)
```

### `uk-s4-e8-60`

Category: **wiki_missing_options, answer_substring_mismatch**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: In this puzzle, which of these replaces the question mark to make the name of a fish?(A), (B), (C), and (D)
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (A)
  expl: A represents ADD. [HADDOCK is a type of fish.]
  img: questions/uk-s4-e8-60.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#60pct)
```
  Q: In this puzzle, which of these replaces the question mark to make the name of a fish?
  opts: (none)
  ans: ADD
  expl: HADDOCK A represents ADD.
  img: (none)
```

### `uk-s4-e8-70`

Category: **different_question_text**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: This is Lee’s shopping list. By placing the paper with holes over the list, his fifth items will be revealed. What is his secret item?
  opts: (none)
  ans: CAKE
  expl: (none)
  img: questions/uk-s4-e8-70.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#70pct)
```
  Q: This is Lee’s shopping list. By placing the paper with holes over the list, his fifth item will be revealed. What is his secret item?
  opts: (none)
  ans: CAKE
  expl: (none)
  img: Cake2.png
```

### `uk-s4-e8-80`

Category: **missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these is the word ABRACADABRA backwards?
  opts: ['ARBRACADRBA', 'ARBACADABRA', 'ARBADACARBA']
  ans: ARBADACARBA
  expl: (none)
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#80pct)
```
  Q: Which of these is the word ABRACADABRA backwards?
  opts: ['ARBRACADRBA', 'ARBACADABRA', 'ARBADACARBA', 'ABRDACARBRA', 'ARBADACABRA', 'ABRACADABRA']
  ans: ARBADACARBA
  expl: (none)
  img: (none)
  parse_notes: multiple bolded cells (2)
```

### `uk-s4-e8-90`

Category: **different_question_text, wiki_missing_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Kemi’s favourite hat doesn’t have feathers and isn’t next a hat with features. Which is Kemi’s favourite hat?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (A)
  expl: It is the only one that isn’t next to a hat with feathers.
  img: questions/uk-s4-e8-90.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_8#90pct)
```
  Q: Kemi’s favourite hat doesn’t have feathers and isn’t next to a hat with feathers. Which is Kemi’s favourite hat?
  opts: (none)
  ans: A
  expl: It is the only one that isn’t next to a hat with feathers.
  img: Hat.png
```

### `uk-s4-e9-10`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: A family of five are doing the Hokey Cokey. Grandma always gets it wrong and puts an arm in when everyone else puts a leg in and a leg in when everyone else puts an arm in. When the song says “you put your left leg in”, how many legs in ...
  opts: (none)
  ans: 6
  expl: Four people are doing it correctly so have one leg in and one leg out but grandma has her arm in and both legs out. 4 + 2 = 6.
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_9#10pct)
```
  Q: A family of five are doing the Hokey Cokey. Grandma always gets it wrong and puts an arm in when everyone else puts a leg in and a leg in when everyone else puts an arm in. when the song says “you put your left leg in”, how many legs in ...
  opts: (none)
  ans: (none)
  expl: (none)
  img: (none)
  parse_notes: no bolded answer
```

### `uk-s4-e9-15`

Category: **different_question_text, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What word can go after each of these images to make three new things?
  opts: (none)
  ans: FLY
  expl: [This forms the words butterFLY, dragonFLY, and fruit FLY.]
  img: questions/uk-s4-e9-15.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_9#15pct)
```
  Q: What word can go after each of these things to make three new things? butterFLY, dragonFLY and fruit FLY
  opts: (none)
  ans: (none)
  expl: (none)
  img: FLY.png
  parse_notes: no bolded answer
```

### `uk-s4-e9-20`

Category: **richer_question_on_wiki, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What word replaces the question mark in this Venn diagram?
  opts: (none)
  ans: SEAT
  expl: The left circle contains synonyms for chair. The right circle contains words that are anagrams of each other. The only word that fits both is SEAT.
  img: questions/uk-s4-e9-20.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_9#20pct)
```
  Q: What word replaces the question mark in this VENN diagram? The left circle contains synonyms for chair. The right circle contains words that are anagrams of each other. The only word that fits both is SEAT.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Seat.png
  parse_notes: no bolded answer
```

### `uk-s4-e9-35`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which symbol replaces the question mark to complete this sequence?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (D)
  expl: The center of each image represents the letters of the alphabet, specifically, V, W, X, Y, and, Z, with lines added at their points to create symbols.
  img: questions/uk-s4-e9-35.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_9#35pct)
```
  Q: Which symbol replaces the question mark to complete this sequence? They are the letters V, W, X, Y & Z with lines added at their points to create symbols.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Origami.png
  parse_notes: no bolded answer
```

### `uk-s4-e9-40`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of the options replaces the question mark to complete the sequence?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (C)
  expl: The images represent the four card suits – SPADES, DIAMONDS, HEARTS, and the CLUBS.
  img: questions/uk-s4-e9-40.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_9#40pct)
```
  Q: Which of the options replaces the question mark to complete the sequence? The images represent the four card suits – SPADES, DIAMONDS, HEARTS and then CLUBS.
  opts: (none)
  ans: (none)
  expl: (none)
  img: SUITS.png
  parse_notes: no bolded answer
```

### `uk-s4-e9-45`

Category: **different_question_text, we_have_placeholder_wiki_has_real_options**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What single letter of the alphabet can fit into the three spaces to complete these four words?
  opts: (none)
  ans: Y
  expl: [This forms the words COSY, CRYPT, YEAR, and TINY.]
  img: questions/uk-s4-e9-45.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_9#45pct)
```
  Q: What single letter of the alphabet can fit into the three empty spaces to complete these four words?
  opts: ['C', 'O', 'S', 'Y', 'R', 'Y', 'E', 'A', 'R', 'P', 'T', 'I', 'N', 'Y']
  ans: Y
  expl: (none)
  img: (none)
  parse_notes: multiple bolded cells (3)
```

### `uk-s4-e9-60`

Category: **different_question_text, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Nick has mixed up his pie charts by mistake. He remembers that PURPLE is larger than GREEN, but not GRAY. GREEN is the smallest of all. GREY is smaller than RED. Which pie chart does he need?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (C)
  expl: [In A, GRAY is bigger than RED so that’s not it. And in B, GREEN is not the smallest slice.]
  img: questions/uk-s4-e9-60.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_9#60pct)
```
  Q: Nick has mixed up his pie charts by mistake. He remembers that PURPLE is larger than GREEN, but not GREY. GREEN is the smallest of all. GREY is smaller than RED. Which pie chart does he need? C
  opts: (none)
  ans: (none)
  expl: (none)
  img: Pie chart.png
  parse_notes: no bolded answer
```

### `uk-s4-e9-70`

Category: **richer_question_on_wiki, wiki_missing_options, wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which of these options replaces the question mark in this set of diagrams?
  opts: ['(A)', '(B)', '(C)', '(D)']
  ans: (C)
  expl: There are three different shapes in each row, overlaid by three different line symbols. The missing shape is a heart and the missing line symbol is an arrow.
  img: questions/uk-s4-e9-70.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_9#70pct)
```
  Q: Which of these options replaces the question mark in this set of diagrams? There are three different shapes in each row, overlaid by three different line symbols. The missing shape is a heart and the missing line symbol is an arrow.
  opts: (none)
  ans: (none)
  expl: (none)
  img: Cupid.png
  parse_notes: no bolded answer
```

### `uk-s4-e9-80`

Category: **wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: Which statement below is correct?
  opts: ['Two words in this sentence have two letters', 'Three words in this sentence have three letters', 'Four words in this sentence have four letters']
  ans: Four words in this sentence have four letters
  expl: [The four words with four letters in them are “Four,” “this,” “have,” and “four.”]
  img: (none)
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_9#80pct)
```
  Q: Which statement below is correct?
  opts: ['Two words in this sentence have two letters.', 'Three words in this sentence have three letters.', 'Four words in this sentence have four letters.']
  ans: (none)
  expl: (none)
  img: (none)
  parse_notes: no bolded correct cell
```

### `uk-s4-e9-90`

Category: **wiki_missing_answer**

**Ours** (https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025)
```
  Q: What movie is represented below?
  opts: (none)
  ans: Batman
  expl: (none)
  img: questions/uk-s4-e9-90.jpg
```

**Wiki** (https://only-connect-questions.fandom.com/wiki/1%25_Club_Season_4_Episode_9#90pct)
```
  Q: What movie is represented below? Batman
  opts: (none)
  ans: (none)
  expl: (none)
  img: Batman.png
  parse_notes: no bolded answer
```

---

## 2. New questions available

The wiki covers UK Seasons 1-3 and three specials, which the current build does not include. **520 questions** total. To import, add a follow-up pass to `scraper/build.py` that ingests `data/questions-fandom.json` and matches the public schema (the wiki records use `image_filename` and have no downloaded images).

| Page | Questions | High-confidence | Low-confidence |
|------|-----------|-----------------|----------------|
| UK S1 E1 | 15 | 15 | 0 |
| UK S1 E2 | 15 | 13 | 2 |
| UK S1 E3 | 15 | 15 | 0 |
| UK S1 E4 | 15 | 14 | 1 |
| UK S1 E5 | 14 | 14 | 0 |
| UK S1 E6 | 15 | 10 | 5 |
| UK S1 E7 | 14 | 6 | 8 |
| UK S1 E8 | 15 | 9 | 6 |
| UK S2 E1 | 15 | 9 | 6 |
| UK S2 E2 | 15 | 9 | 6 |
| UK S2 E3 | 15 | 11 | 4 |
| UK S2 E4 | 15 | 11 | 4 |
| UK S2 E5 | 15 | 12 | 3 |
| UK S2 E6 | 15 | 9 | 6 |
| UK S2 E7 | 15 | 10 | 5 |
| UK S2 E8 | 15 | 11 | 4 |
| UK S3 E1 | 14 | 9 | 5 |
| UK S3 E2 | 15 | 5 | 10 |
| UK S3 E3 | 14 | 7 | 7 |
| UK S3 E4 | 15 | 12 | 3 |
| UK S3 E5 | 15 | 4 | 11 |
| UK S3 E6 | 15 | 13 | 2 |
| UK S3 E7 | 15 | 8 | 7 |
| UK S3 E8 | 15 | 10 | 5 |
| UK S3 E9 | 15 | 14 | 1 |
| UK S3 E10 | 15 | 13 | 2 |
| UK S3 E11 | 14 | 10 | 4 |
| UK S3 E12 | 15 | 9 | 6 |
| UK S3 E13 | 15 | 8 | 7 |
| UK S3 E14 | 15 | 11 | 4 |
| UK S3 E15 | 15 | 13 | 2 |
| UK S3 E16 | 15 | 12 | 3 |
| Special: christmas-2023 | 15 | 10 | 5 |
| Special: christmas-2024 | 15 | 12 | 3 |
| Special: soccer-aid-2025 | 15 | 14 | 1 |

---

## 3. Parse warnings

Wiki records the parser flagged as low-confidence. Most are wiki-side issues (no bolded answer, picture-only answers, multi-row letter grids) rather than parser bugs.

### no bolded answer (141)

`uk-special-christmas-2023-80`, `uk-special-christmas-2023-50`, `uk-special-christmas-2023-25`, `uk-special-christmas-2023-5`, `uk-special-christmas-2024-25`, `uk-s1-e2-1`, `uk-s1-e6-90`, `uk-s1-e6-70`, `uk-s1-e6-30`, `uk-s1-e6-35`, `uk-s1-e6-25`, `uk-s1-e7-90`, `uk-s1-e7-60`, `uk-s1-e7-50`, `uk-s1-e7-30`, `uk-s1-e7-25`, `uk-s1-e8-90`, `uk-s1-e8-35`, `uk-s1-e8-20`, `uk-s1-e8-10`, `uk-s1-e8-5`, `uk-s2-e1-70`, `uk-s2-e1-50`, `uk-s2-e1-45`, `uk-s2-e1-35`, `uk-s2-e2-90`, `uk-s2-e2-60`, `uk-s2-e2-45`, `uk-s2-e2-40`, `uk-s2-e2-1`, `uk-s2-e3-70`, `uk-s2-e3-45`, `uk-s2-e3-40`, `uk-s2-e3-5`, `uk-s2-e4-50`, `uk-s2-e4-5`, `uk-s2-e5-90`, `uk-s2-e6-80`, `uk-s2-e6-45`, `uk-s2-e6-30`, `uk-s2-e6-25`, `uk-s2-e6-20`, `uk-s2-e6-15`, `uk-s2-e7-80`, `uk-s2-e7-10`, `uk-s2-e7-5`, `uk-s2-e8-80`, `uk-s2-e8-50`, `uk-s2-e8-20`, `uk-s3-e1-70`, `uk-s3-e1-35`, `uk-s3-e1-30`, `uk-s3-e1-20`, `uk-s3-e1-15`, `uk-s3-e10-10`, `uk-s3-e11-80`, `uk-s3-e11-50`, `uk-s3-e12-90`, `uk-s3-e12-25`, `uk-s3-e12-20`

... and 81 more

### no bolded correct cell (35)

`uk-special-christmas-2024-60`, `uk-special-christmas-2024-15`, `uk-s1-e4-90`, `uk-s1-e7-45`, `uk-s2-e1-90`, `uk-s2-e4-80`, `uk-s2-e5-40`, `uk-s2-e7-35`, `uk-s2-e8-60`, `uk-s3-e11-70`, `uk-s3-e11-25`, `uk-s3-e12-30`, `uk-s3-e13-70`, `uk-s3-e13-50`, `uk-s3-e13-15`, `uk-s3-e14-40`, `uk-s3-e15-80`, `uk-s3-e16-30`, `uk-s3-e3-40`, `uk-s3-e7-25`, `uk-s3-e7-10`, `uk-s3-e8-30`, `uk-s4-e11-25`, `uk-s4-e13-40`, `uk-s4-e13-25`, `uk-s4-e14-60`, `uk-s4-e14-5`, `uk-s4-e15-90`, `uk-s4-e3-30`, `uk-s4-e4-20`, `uk-s4-e6-50`, `uk-s4-e6-35`, `uk-s4-e7-45`, `uk-s4-e8-20`, `uk-s4-e9-80`

### empty question text (19)

`uk-s1-e2-15`, `uk-s1-e7-40`, `uk-s1-e7-20`, `uk-s1-e8-60`, `uk-s2-e1-40`, `uk-s2-e2-35`, `uk-s2-e5-20`, `uk-s2-e7-50`, `uk-s3-e13-1`, `uk-s3-e2-60`, `uk-s3-e2-25`, `uk-s3-e8-35`, `uk-s3-e9-25`, `uk-s4-e11-5`, `uk-s4-e13-45`, `uk-s4-e2-1`, `uk-s4-e4-15`, `uk-s4-e4-5`, `uk-s4-e5-15`

### multiple bolded cells (2) (7)

`uk-s4-e1-35`, `uk-s4-e11-80`, `uk-s4-e13-90`, `uk-s4-e3-90`, `uk-s4-e3-70`, `uk-s4-e8-80`, `uk-special-soccer-aid-2025-70`

### multiple bolded cells (3) (3)

`uk-special-christmas-2023-1`, `uk-s3-e10-5`, `uk-s4-e9-45`

### multiple bolded cells (5) (1)

`uk-s2-e4-40`

### multiple bolded cells (35) (1)

`uk-s3-e16-60`

### multiple bolded cells (4) (1)

`uk-s3-e5-5`

### multiple bolded cells (7) (1)

`uk-s4-e1-90`

### multiple bolded cells (20) (1)

`uk-s4-e15-60`
