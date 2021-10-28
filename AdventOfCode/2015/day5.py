"""
Santa needs help figuring out which strings in his text file are naughty or nice.

A nice string is one with all of the following properties:

It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
For example:

ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...), a double letter (...dd...), and none of the disallowed substrings.
aaa is nice because it has at least three vowels and a double letter, even though the letters used by different rules overlap.
jchzalrnumimnmhp is naughty because it has no double letter.
haegwjzuvuyypxyu is naughty because it contains the string xy.
dvszwmarrgswjxmb is naughty because it contains only one vowel.
How many strings are nice?

PART 2:

Now, a nice string is one with all of the following properties:

It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.

"""

# RULE SET 1 ---
def rule_1 (in_string, min_vowels=3):
    """ See problem descriptions. Return True if "nice"
        Default is >=3 vowels
    """
    vowel_cnt = 0
    rule_pass = False
    for vowel in list("aeiou"):
        mod_string = in_string.replace(vowel, "")  # replace space
        vowel_cnt += (len(in_string) - len(mod_string))

    if vowel_cnt >= min_vowels:
        rule_pass = True

    return rule_pass


def rule_2 (in_string):
    """ See problem descriptions. Return True if "nice"
        Rule = check double letters
    """
    rule_pass = False

    for i in range(1, len(in_string)):
        if in_string[i - 1] == in_string[i]:
            rule_pass = True
            break

    return rule_pass

def rule_3 (in_string):
    """ See problem descriptions. Return True if "nice"
    naughty if: ab, cd, pq, or xy
    """
    naughty = ["ab", "cd", "pq", "xy"]
    rule_pass = True

    for pat in naughty:
        if pat in in_string:
            rule_pass = False
            break

    return rule_pass

# PART 2 ---

def rule_21 (in_string):
    """ See problem descriptions. Return True if "nice"
    pair of any two letters that appears at least twice
    """
    rule_pass = False

    for i in range(0, len(in_string)-2):
        pat = in_string[i: (i + 2)]
        tmp = in_string.replace(pat, "")  # replace will ignore "overlaps"
        if len(tmp) <= (len(in_string) - 4):
            rule_pass = True
            break

    return rule_pass

def rule_22 (in_string):
    """ See problem descriptions. Return True if "nice"
    contains at least one letter which repeats with exactly one letter between them
    """
    rule_pass = False

    for i in range(0, len(in_string) - 2):
        if in_string[i] == in_string[(i+2)]:
            rule_pass = True
            break

    return rule_pass


# MAIN ---

def main (strings):
    nice_cnt_1 = 0  # hold count of nice strings
    nice_cnt_2 = 0  # hold count of nice strings

    # PART 1
    for string in strings:
        if rule_1(string) & rule_2(string) & rule_3(string):
            nice_cnt_1 += 1
    print(f"NICE COUNT RULE SET 1: {nice_cnt_1}")

    # PART 2
    for string in strings:
        if rule_21(string) & rule_22(string):
            nice_cnt_2 += 1
    print(f"NICE COUNT RULE SET 2: {nice_cnt_2}")


if __name__ == '__main__':
    """ Very simple entry point for problem solution"""
    TEST1 = False
    TEST2 = False

    if not TEST1 and not TEST2:
        with open('./inputs/day5_input.txt', 'r') as f:
            strings = f.readlines()
        for i, string in enumerate(strings):
            strings[i] = string.strip('\n')  # strip newlines
        main(strings)
    elif TEST1:
        test_dict = {
            "ugknbfddgicrmopn": True,
            "jchzalrnumimnmhp": False,
            "haegwjzuvuyypxyu": False,
            "dvszwmarrgswjxmb": False,
        }

        for test_str in test_dict.keys():
            output = rule_1(test_str) & rule_2(test_str) & rule_3(test_str)
            if output != test_dict[test_str]:
                print(f"FAILED: {test_str}")
            else:
                print(f"PASSED: {test_str}")
    else:
        test_dict = {
            "qjhvhtzxzqqjkmpb": True,
            "xxyxx": True,
            "uurcxstgmygtbstg": False,
            "ieodomkazucvgmuy": False,
        }

        for test_str in test_dict.keys():

            output = rule_21(test_str) & rule_22(test_str)
            if output != test_dict[test_str]:
                print(f"FAILED: {test_str}. RULE 21: {rule_21(test_str)} RULE 22: {rule_22(test_str)}")
            else:
                print(f"PASSED: {test_str}")
