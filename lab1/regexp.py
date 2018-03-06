import re


def extract_money(judgment_text):
    regex = '''
        (?:
            [1-9]\d*                    # digits, first being non-zero
            (?:[\. ]\d+)*               # . or space to group by thousands e.g. 123 742  or 659.041.328
        )+
        (?:,\d+)?\                      # fractional part followed by space   e.g. 2,5   391.678,99 
        (?:
            tys\.? |mln\.? |mld\.? |
            \(\w+[ \w+]*\)\             # e.g.  360 (trzysta sześćdziesiąt)
        )?
        (?=zł)
    '''
    return map(normalize, re.findall(regex, judgment_text, re.VERBOSE))


def normalize(money_text: str):
    money_text = money_text.strip()  # space at the end
    d = {'tys': 3, 'mln': 6, 'mld': 9}

    if re.match('(?:[1-9]\d*(?:[\. ]\d+)*)+\s*\([\w+\s]+\)',
                money_text):  # e.g. '360 (trzysta sześćdziesiąt)'  => extract 360
        money_text = money_text[:money_text.find('(')]

    money_text = money_text.replace('.', ' ').strip()  # '3.319.726' -> '3 319 726'

    if not any(money_text.endswith(key) for key in d):  # does not contain tys. or mln or mln
        try:  # '90 853,33'  => ignore fractional part ,33
            money_text = money_text[:money_text.index(',')]
        except ValueError:  # does not contain fractional part
            pass
        return int(money_text.replace(' ', ''))

    *numbers, word = money_text.split(' ')
    if len(numbers) == 1:  # e.g.  52 mln  -> 52000000
        return float(numbers[0].replace(',', '.')) * 10 ** d[word]
    else:  # e.g. 802 054 tys. -> 802054
        return int(''.join(numbers))


def references_article_of_regulation(reference, regulation, article):
    regex = 'art\.\s+' + str(article)
    return reference['journalTitle'].lower() == regulation.lower() and bool(re.search(regex, reference['text']))


def contains_any_word_case(judgment_text, cases):
    regex = '|'.join(rf'\b{case}\b' for case in cases)
    return bool(re.search(regex, judgment_text))
