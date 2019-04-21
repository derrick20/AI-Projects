import os, re
import random
import time
import sys

BLOCKCHAR = "#"
OPENCHAR = "-"
PROTECTEDCHAR = "~"
width = -1  # arbitrary, but we use this to derive height, so global makes sense
crossword = ""  # only necessary for the purposes of the recursive connectivity checker
word_domains = {} # (length, pos, char) -> [apple, apply...]
# letter_domains = {} # pos -> [a, c, d...]
# words = {} #
freq_table = {
    'E': 0.12702,
    'T': 0.09056,
    'A': 0.08167,
    'O': 0.07507,
    'I': 0.06966,
    'N': 0.06749,
    'S': 0.06327,
    'H': 0.06094,
    'R': 0.05987,
    'D': 0.04253,
    'L': 0.04025,
    'C': 0.02782,
    'U': 0.02758,
    'M': 0.02406,
    'W': 0.0236,
    'F': 0.02228,
    'G': 0.02015,
    'Y': 0.01974,
    'P': 0.01929,
    'B': 0.01492,
    'V': 0.00978,
    'K': 0.00772,
    'J': 0.00153,
    'X': 0.0015,
    'Q': 0.00095,
    'Z': 0.00074
}
'''with open("ghostDictionary.txt") as file:
        entries = [line.upper().strip().split("\t") for line in file]
        freq_table = {
            entry[0]: float(entry[1]) for entry in entries
        }'''


#['crossword_Liang_D.py', '13x13', '27', 'xwords.txt', 'H6x4no#on', 'v5x5rot', 'v0x0instep', 'h0x4Trot', 'H0x9arch', 'V0x12heel']
# python3 crossword_Liang_D.py 9x15 24 xwords.txt "V0x7fan" "V6x7tic"


def setup_board():  # TODO not sure what the inputs are
    global width
    inTest = [r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V)(\d+)x(\d+)(.+)$"]  # TODO what's the point of the 3 regices
    fixed_words = []  # store the words that are given

    # Now, build the xw using the fixedWords
    #line = sys.argv
    #line = ['crossword_Liang_D.py', '13x13', '27', 'xwords.txt', 'H6x4no#on', 'v5x5rot', 'v0x1instep', 'h0x4Trot', 'H0x9arch', 'V0x12heel']
    line = ['crossword_Liang_D.py', '4x4', '0', 'xwords.txt']
    height, width = [int(i) for i in line[1].split('x')]
    blocks = int(line[2])
    xw = BLOCKCHAR * (width + 2) + (BLOCKCHAR + OPENCHAR * width + BLOCKCHAR) * height + BLOCKCHAR * (
            width + 2)  # pad the edges

    for i in range(4, len(line)):
        pattern = r"^(H|V)(\d+)x(\d+)(.+)$"
        match = re.search(pattern, line[i], re.I)
        orientation, vpos, hpos, word = match.group(1).upper(), int(match.group(2)), int(match.group(3)), match.group(
            4).upper()
        fixed_words.append([orientation, vpos, hpos, word])  # since match will have a H or V in the beginning

    xw = fill_words(xw, fixed_words)

    for i in range(len(xw)):  # go through and substitute all the letters into protected chars
        if xw[i].isalpha():
            xw = replace(xw, i, PROTECTEDCHAR)

    current_blocks = 0
    if blocks % 2 == 1:
        if width % 2 == 1 and height % 2 == 1:
            xw = replace(xw, len(xw) // 2, BLOCKCHAR)  # center must be blocked if odd # blocks
            current_blocks += 1
        else:
            print("Impossible board")
    else:
        if width % 2 == 1 and height % 2 == 1:
            xw = replace(xw, len(xw) // 2, PROTECTEDCHAR)  # center must be protected if even # blocks
        # we can't deduce anything if board has no center and even # blocks needed

    pos_list = [i for i in range(len(xw)) if xw[i] == OPENCHAR]
    pos_list_copy = pos_list[:]

    true_width = width + 2
    height = len(xw) // true_width - 2
    edge_blocks = 2 * (width + height) + 4
    copy = xw[:]

    while current_blocks < blocks:
        pos = random.choice(pos_list_copy)
        pos_list_copy.remove(pos)
        copy = replace(copy, pos, BLOCKCHAR)

        copy = deduce_squares(copy)

        current_blocks = copy.count(BLOCKCHAR) - edge_blocks
        if current_blocks == blocks and check_connectivity_iterative(copy):
            break
        if copy == None or current_blocks > blocks or (
                current_blocks == blocks and not check_connectivity_iterative(copy)):
            copy = xw[:]  # reset and try again
            current_blocks = copy.count(BLOCKCHAR) - edge_blocks
            pos_list_copy = pos_list[:]


    copy = copy.replace(PROTECTEDCHAR, OPENCHAR)
    copy = fill_words(copy, fixed_words)

    display_clean(copy, False)
    return copy, fixed_words


# Flood fill in a random position, and compare the count of spaces to the total number of spaces
# This is a quick litmus test to see if we have a fully connected crossword, and that's all the info we need
def check_connectivity_iterative(xw):  # way faster,,,
    global width
    true_width = width + 2
    if OPENCHAR in xw:
        pos = xw.index(OPENCHAR)  # just the first char we see, and floodfill from there. Minimize the work we have to
    # ... do. All we want to know is if it's connected, so just see if one area filled = total open/protected spaces
    elif PROTECTEDCHAR in xw:
        pos = xw.index(PROTECTEDCHAR)
    elif xw.count(BLOCKCHAR) == len(xw):  # If by some chance there's not a single open char lol
        return True
    dx = [-1, 0, 1, 0]
    dy = [0, -true_width, 0, true_width]

    queue = [pos]
    count = 0
    while len(queue) > 0:
        curr = queue.pop()
        if xw[curr] in BLOCKCHAR + '?':
            continue
        else:
            xw = replace(xw, curr, '?')
            count += 1
            for i in range(4):
                queue.append(curr + dx[i] + dy[i])
    total_spaces = len(xw) - xw.count(BLOCKCHAR)
    return count == total_spaces

'''def check_connectivity(xw):
    global crossword
    pos = xw.index(OPENCHAR) # just the first char we see, and floodfill from there. Minimize the work we have to
    # ... do. All we want to know is if it's connected, so just see if one area filled = total open/protected spaces
    if pos == -1:
        pos = xw.index(PROTECTEDCHAR) # If by some chance there's not a single open char lol
    crossword = xw[:]
    filled_spaces = check_connectivity_helper(pos) # need to preserve the original, so copy it
    total_spaces = xw.count(PROTECTEDCHAR) + xw.count(OPENCHAR)

    return filled_spaces == total_spaces

def check_connectivity_helper(pos):
    global width
    global crossword
    true_width = width + 2
    dx = [-1, 0, 1, 0]
    dy = [0, -true_width, 0, true_width]
    if crossword[pos] in BLOCKCHAR + '?': # this means it is either the border (nice since we are filling area) or visited
        return 0
    else:
        crossword = replace(crossword, pos, '?')
        count = 1 # since we place a marker at pos, in addition to whatever we explore elsewhere
        for i in range(4):
            count += check_connectivity_helper(pos + dx[i] + dy[i])
        return count'''

'''def recur(xw, current_blocks, blocks, pos_list):
    if current_blocks == blocks and check_connectivity_iterative(xw):  # we assume that it has been deduced correctly. It wouldn't get passed in if it isn't correct
        return xw
    # place a random block
    while len(pos_list) > 0:
        pos = random.choice(pos_list)
        pos_list.remove(pos)
        xw = replace(xw, pos, BLOCKCHAR)

        xw = deduce_squares(xw)
        if xw != None:
            display_crossword(xw, False)
        if xw != None:
            recur(xw, current_blocks + 1, blocks, pos_list[:])'''


# Return a string with the crossword with deduced blocked squares,
# or None if it is impossible. Updates the protected squares by
# determining all positions that connect with any word characters
# to form a word to reach length 3 at the minimum.
def deduce_squares(xw):
    global width
    true_width = width + 2
    illegalRE = "{0}(.?{1}|{1}.?){0}".format(BLOCKCHAR,
                                             PROTECTEDCHAR)  # if we see a protected wedged between a gap that's < 3, then we have a contradiction
    subRE1 = "{0}{1}{0}".format(BLOCKCHAR, OPENCHAR)
    subRE2 = "{0}{1}{1}{0}".format(BLOCKCHAR,
                                   OPENCHAR)  # we need a separate one since we need to know exactly how many to replace it with

    transposed = transpose(xw)
    revert_width(xw)
    # notice that after placing blocks, this might lead to more deductions,
    while re.search(subRE1, xw) or re.search(subRE2, xw) or re.search(subRE1, transposed) or re.search(subRE2, transposed):
        # Fill out the blocked squares
        xw = re.sub(subRE1, BLOCKCHAR * 3, xw)
        xw = re.sub(subRE2, BLOCKCHAR * 4, xw)
        transposed = transpose(xw)

        # do it for vertical as well
        transposed = re.sub(subRE1, BLOCKCHAR * 3, transposed)
        transposed = re.sub(subRE2, BLOCKCHAR * 4, transposed)

        # revert to original orientation
        xw = transpose(transposed)
        xw = make_symmetric(xw, BLOCKCHAR)  # once we've determined blocks, let's make it symmetrical before protecting chars
        # Illegal case

        transposed = transpose(xw)
        revert_width(xw)
        if re.search(illegalRE, xw) or re.search(illegalRE, transposed):
            return BLOCKCHAR * len(xw)
    # TODO THERE's a case where it wasn't any deduction but we placed a block
    xw = make_symmetric(xw, BLOCKCHAR)

    # *--Note we had to separate the blocking and protecting phases!!--*
    # fill protected squares, substituting in one of these cases
    xw = fill_protected_squares(xw)
    # repeat when transposed
    transposed = transpose(xw)
    transposed = fill_protected_squares(transposed)
    xw = transpose(transposed)

    xw = make_symmetric(xw, PROTECTEDCHAR)  # Now, symmetrize the protected squares
    # need to check one last time if it's illegal after protecting squares
    transposed = transpose(xw)
    revert_width(xw)
    if re.search(illegalRE, xw) or re.search(illegalRE, transposed):
        return BLOCKCHAR * len(xw)
    return xw


def fill_protected_squares(xw):
    b = BLOCKCHAR
    p = PROTECTEDCHAR
    o = OPENCHAR
    cases = {  # these are the only ways we can deduce a square is protected
        b + p + o + o: b + 3 * p,
        b + p + p + o: b + 3 * p,
        b + p + o + p: b + 3 * p, # UGH you can't assume that bp is followed by o's and p's, there may be blocks after
    }
    for pos in range(len(xw)):
        for case in cases:
            length = len(case)
            if xw[pos: pos + length] == case:  # note, we know for sure that we can always replace the ones ...
                xw = xw[:pos] + cases[case] + xw[pos + 4:]
                # ... beyond the block with protected, since they can't be blocks ...
                # ... (otherwise we would've filled in this area already). Also, all substitutions are length 4, good!
    xw = xw[::-1]  # do this again, but we must mirror things, since replacement in strings works from left to right.
    for pos in range(len(xw)):
        for case in cases:
            length = len(case)
            if xw[pos: pos + length] == case:
                xw = xw[:pos] + cases[case] + xw[pos + 4:]
    xw = xw[::-1]
    return xw


def make_symmetric(str, char): # TODO UGH THE LOGIC!
    length = len(str)
    for pos in range(
            length):  # may be redundant for some parts, but others might be only in the second half, so we can't just stop halfway
        if str[pos] == char:
            if str[length - pos - 1] == OPENCHAR: # we can't ever substitute a Protected or BLock
                str = replace(str, length - pos - 1, char)
            elif str[length - pos - 1] != char:
                return BLOCKCHAR * len(str)  # it can't substitute someone else
    return str


def replace(str, pos, char):
    return str[:pos] + char + str[pos + 1:]


# Only place all the words down, don't make any assumptions yet.
def fill_words(xw, fixed_words):  # not that many words, so let's give ourselves an easy time and take it slow
    global width
    true_width = width + 2
    true_height = len(xw) // true_width
    for e in fixed_words:
        # orientation, vpos, hpos, word. Thus, the row is how far vertically, col is horizontally along
        row, col = e[1] + 1, e[2] + 1  # we need to convert to one-index, since we padded with block chars
        orientation, word = e[0], e[3]
        if orientation == 'H':
            pos = col + true_width * row
            xw = xw[:pos] + e[3] + xw[pos + len(
                word):]  # up until pos, so pos was unfilled. Start back up len spots further, and still unfilled, so we can write from there (no +1)

        elif orientation == 'V':
            pos = row + true_height * col  # It is exactly the inverse of before. The height is how long a row is, the row is the column, the column is row
            transposed = transpose(xw)
            transposed = transposed[:pos] + e[3] + transposed[
                                                   pos + len(word):]  # TODO swap with protectedchar * len(word)
            xw = transpose(transposed)

    return xw


def display_crossword(xw, transposed):
    global width
    true_width = width + 2
    true_height = len(xw) // true_width
    if transposed:
        true_width, true_height = true_height, true_width  # clever
    print('\n'.join([' '.join(xw[(true_width) * (p): (true_width) * (p + 1)]) for p in range(true_height)]) +
          '\n')


def display_clean(xw, transposed):
    global width
    true_width = width + 2
    true_height = len(xw) // true_width
    if transposed:
        true_width, true_height = true_height, true_width  # clever
    print('\n'.join([' '.join(xw[(true_width) * (p) + 1: (true_width) * (p + 1) - 1]) for p in range(1, true_height - 1)]) +
          '\n')


def revert_width(xw):
    # confusing AF
    global width
    true_width = width + 2
    width = len(xw) // true_width - 2  # we need to realize that width has changed after this transposition


def transpose(xw):  # just so the extra blocks aren't weird, we pad the blocks in the beginning before everything
    global width
    true_width = width + 2  # AKA the hidden width
    ret = "".join([xw[col::true_width] for col in range(true_width)])
    revert_width(xw)
    return ret
    # we go from col 0 to col(width) and for each one, progress downward jumping in incr of width. This downward movement corresponds to a row


def calc_freq(word):
    global freq_table
    letters = [char for char in word if char.isalpha()]
    return sum([freq_table[char] for char in letters]) / len(letters)


def setup_structures(xw, fixed_words):
    global width, word_domains
    true_width = width + 2
    true_height = len(xw) // true_width
    dictionary = []
    with open("twentyk.txt") as file:
        for line in file:
            word = line.rstrip().upper()
            # if re.match("[A-Z]+", word):  # regex is find if just once
            dictionary.append(word)

    for element in fixed_words:
        word = element[3].upper()  # other components are useless
        if word in dictionary:
            dictionary.remove(word)

            # bucket all words by length
    # also include bucketing of a single letter as that helps reduce the
    for word in dictionary:
        length = len(word)
        if length < 3:
            continue
        ''' # create buckets for words based on length NOT NECESSARY!
        if length not in word_domains:
            word_domains[length] = [word]
        else:
            word_domains[length].append(word)'''

        # create buckets for words based on length and the position of a single character (since ~6 average word length
        # isn't too much of a size increase
        for pos, char in enumerate(list(word)):
            if (length, pos, char) not in word_domains:
                word_domains[(length, pos, char)] = [word]
            else:
                word_domains[(length, pos, char)].append(word)

    # Sort words within buckets by letter freq, giving words that have probable intersections with other words
    for tup, domain in word_domains.items():  # enumerate for dicts gives the keys indexed, whereas items is key, value
        domain.sort(key=calc_freq, reverse=True) # we want to sort so BIG values are picked earlier

    # words: (pos, orient)->(length, index, char)
    word_RE = r"(\w|-)+"  # will munch as many of these word or - chars until it reaches a block

    # for every possible position and orientation, indicate the word it is part of (the start index, length, current
    # word placed there (may contain '-'), and the domain of possibilities.
    # At the same time, give a start on the letter domains

    words = {}
    transposed = transpose(xw)
    revert_width(xw)
    boards = [xw, transposed]
    orientations = ['H', 'V']
    increments = [1, true_width]
    for i in range(2):
        board = boards[i]
        orientation = orientations[i]
        increment = increments[i]

        matches = [x for x in re.finditer(word_RE, board)]
        for match in matches:
            word = match.group()
            length = len(word)
            pos = match.start()
            if orientation == 'V':
                row, col = pos // true_height, pos % true_height  # height acts as width. How many widths to reach pos?
                row, col = col, row # essentially transpose that row, col
                pos = true_width * row + col # convert to a regular position

            for j in range(length):
                curr_domain = find_word_domain(word)
                words[(pos + j * increment, orientation)] = [length, pos, word, curr_domain]

    # Set up letter_domains. During this time, look through all '-' positions, and give them a current domain
    # of possible letters. TODO

    # We can only modify the values of letters at non-letter, non-block spots!
    # Populate it with sets, we will be adding values, so don't repeat!
    letter_domains = {
        pos: set() for pos in range(len(xw)) if xw[pos] == OPENCHAR
    }

    # We only need to modify the domains of letters that can be modified. Filled squares do not affect us
    for element in words:
        pos, orient = element
        update_letter_domains(xw, pos, orient, words, letter_domains)
    for pos in letter_domains:
        if len(letter_domains[pos]) == 0:
            letter_domains[pos] = {'E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'L', 'D', 'C', 'U', 'M', 'F', 'P', 'G', 'W', 'Y', 'B', 'V', 'K', 'X', 'J', 'Q', 'Z'}

    return words, letter_domains


# At a specific position, we look at the whole word it is part of (Vertical and Horizontal)
# Looking at every possibility of words within the domain, we update the number of letters possible at each
# position within that word.
def update_letter_domains(xw, pos, orient, words, letter_domains):
    global width
    true_width = width + 2
    increment = 1 if orient == 'H' else true_width
    length, index, current, current_domain = words[(pos, orient)]

    for j in range(length):
        pos = index + j * increment  # Absolute position within the xw
        if xw[pos] == OPENCHAR:  # If it is filled, we shouldn't care since it's fixed
            letter_domains[pos] = set()  # Reset it
            for word in current_domain:  # In all possible words at that spot, input letters into letter_domain
                letter_domains[pos].add(word[j])  # The letter at that relative position within the word


# This returns the updated list of possible words, say for "A-PL-" is apple, apply, etc.
# Tries to preserve the order while merging word_domains, so that better words are placed early
# Additionally, intersections are done wisely to minimize work (constrain letters earlier)
# Lastly, be careful not to alter the original word_domains global variable, otherwise it will impact later work
def find_word_domain(word):
    global word_domains
    priority = "ZQJXKVBYWGPFMUCDLHRSNIOATE"
    curr_domain = []
    length = len(word)
    word = word.upper()  # just in case
    been_filled = False  # this tracks the first case, thereafter, if we become empty, it's our fault
    for char in priority:  # essentially parse all the possible number of letters it contains, and use that to update D
        if char not in word:
            continue
        positions = [i for i, letter in enumerate(list(word)) if letter == char]
        for pos in positions:
            if len(curr_domain) == 0:  # nothing has been added, so set this as the first domain
                if not been_filled:
                    curr_domain = word_domains[(length, pos, char)]
                    been_filled = True
                else:  # This means we ran out of words
                    break
            else:  # then just intersect with what's available
                other = set(word_domains[(length, pos, char)])
                curr_domain = [x for x in curr_domain if x in other]  # ordered intersection O(n),
                # n is size of curr_domain,
                # which is smaller most likely, since we  are only restricting as we progress to more letters
    return curr_domain


# After selecting some position to place a letter (least-constraining var) and the letter to be placed (min-remaining
# value), place that letter and see the implications on: word_domains and letter_domains,
# keeping in mind that IF no more words and thus letters are allowed, we must backtrack
# return updated version
def place_letter(xw, pos, char, words, letter_domains, visited):
    global word_domains, width
    true_width = width + 2
    xw = replace(xw, pos, char)
    for o in ['H', 'V']:
        index = words[(pos, o)][1]
        words[(pos, o)][2] = replace(words[(pos, o)][2], pos - index, char)
    del letter_domains[pos]  # can no longer update that letter in this branch. If we fail, we will go up in the tree
    # to a point where the letter_domains still had that position open for change

    # Constrain the current_domains of each position upon realizing that a letter is placed there
    completed_word = (False, '')
    orientations = ['H', 'V']
    increments = [1, true_width]
    for i in range(2):
        orientation = orientations[i]
        increment = increments[i]
        length, index, current, current_domain = words[(pos, orientation)]
        if len(current_domain) == 0:  # if it is clean, need to give it something to start with
            words[(pos, orientation)][3] = word_domains[(length, (pos - index)/increment, char)]  # use the RELATIVE position
        else:  # intersect it with the other
            other = set(word_domains[(length, (pos - index)/increment, char)])
            current_domain = [x for x in current_domain if x in other]
        # This means we completed a word. We would have removed any already filled words
        if OPENCHAR not in current and current not in visited:  # The word we have reached is something NEW
            completed_word = (True, current)  # from the words list, otherwise we'd be pruning for no reason
            del words[(pos, orientation)]  # Now, we don't have to consider this position
            visited.add(current)  # We track the fact that this word has been used

    # Update the current_domains of each individual word that might contain this finished word
    if completed_word[0]:  # Now we need to update the domains of all other words
        word = completed_word[1]
        for key, value in words.items():  # now smaller by one!
            current_domain = value[3]
            if word in current_domain:
                current_domain.remove(word)
                if len(current_domain) == 0:
                    return None, 0, 0, 0  # this means we precluded a location!!! Backtrack time!
                # In some cases, this deduction allows us to immediately deduce a new word, but it's probably not worth
                # it to do this deduction. The more pressing time constraint is actually finding good letters
    for orientation in['H', 'V']:
        update_letter_domains(xw, pos, orientation, words, letter_domains)
    return xw, words, letter_domains, visited  # updated version


# TODO Maybe implement tie-breakers
# Pick variable with fewest remaining values
def pick_MRV_var(letter_domains):
    dict = {
        pos: len(domain) for pos, domain in letter_domains.items()
    }
    min_value = dict[min(dict, key=dict.get)]  # sort from fewest remaining to the most
    mins = [pos for pos, value in dict.items() if value == min_value]
    # tie-breaking
    if len(mins) == 1:
        return mins[0]
    else:
        #  Sort the positions by the length sum of the two words horizontal and vertical. TODO
        return mins[0] #  for now


def LCV_values(letter_domain):
    global freq_table
    priority = "ETAOINSRHLDCUMFPGWYBVKXJQZ"
    # sort the letter_domain by their position in the priority string
    dict = {
        char: priority.index(char.upper()) for char in letter_domain
    }
    return sorted(dict, key=dict.get)


def copy_words(words):
    dict = {}
    for key, value in words.items():
        length, index, current, current_domain = value
        dict[key] = [length, index, current, current_domain[:]]
    return dict

def copy_letter_domains(letter_domains):
    return {
        key: set(list(value)[:]) for key, value in letter_domains.items()
    }

def solve_puzzle(xw, words, letter_domains, visited):
    global width, word_domains
    #  Failed case
    if xw == None:
        return None, 0, 0, 0
    #  Finished board
    elif OPENCHAR not in xw:
        return xw, words, letter_domains, visited
    else: # Use delta_var_domains and or have some copy method
        pos = pick_MRV_var(letter_domains)
        letters = LCV_values(list(letter_domains[pos]))
        display_clean(xw, False)
        for e in words.items():
            print(e)
        for letter in letters:
            xw, words, letter_domains, visited = place_letter(xw, pos, letter, copy_words(words), copy_letter_domains(letter_domains), set(list(visited)[:]))
            [print(item) for item in letter_domains.items()]
            if xw == None:
                return None, 0, 0, 0
            return solve_puzzle(xw, words, letter_domains, visited)
    return None, 0, 0, 0


    # TODO NEED EXIT CASES

# Take a word (having some number of word characters, then repeatedly union with word_domains of those containing single
# character. Order by letters which shrink the amount of work first (z, y, j, etc.)


def main():
    global word_domains
    xw, fixed_words = setup_board()
    words, letter_domains = setup_structures(xw, fixed_words)

    visited = set()  # Notably, the inputted words are already filtered out from our range of possibility. We also
    # track visited by directly adding them to a set, since that's easier than removing from the giant word_domains dict
    xw, words, letter_domains, visited = solve_puzzle(xw, words, letter_domains, visited)
    display_clean(xw, False)


if __name__ == '__main__':
    main()