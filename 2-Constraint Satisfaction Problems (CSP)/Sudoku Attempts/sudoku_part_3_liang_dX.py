import time
import math

conn = []  # for each index, stores the indexes of cells in the same row/column/box
groups = []  # for each index, stores a list for each row/column/box that the index is in
store_conn = {}  # stores the "conn" variable for each n, so we don't have to recalculate it
store_groups = {}  # stores the "groups" variable for each n, so we don't have to recalculate it
int_to_string = []  # converts the integer values into their appropriate string values for printing
path_len = 0  # stores len(path), so we don't have to call that method
'''
sets up "conn", "groups", "int_to_string", "path_len"
updates store_conn and store_groups
'''


def setup_tables(n):
    global conn, groups, store_conn, store_groups, int_to_string, path_len  # accesses global variables
    path_len = n * n  # sets path_len
    h = int(math.sqrt(n))  # determines the height of each box
    w = int(n / h)  # determines width of each box
    int_to_string = []  # resets "int_to_string"
    for i in range(n + 1):  # iterates over the possible integers
        if i < 10:  # if the integer is less than 10...
            int_to_string += [str(i)]  # ... it's the same string
        else:  # otherwise ...
            int_to_string += [chr(i + ord("A") - 10)]  # ... add the corresponding letter
    if n in store_conn:  # check if we have created the "conn" variable for "n" before
        conn = store_conn[n]  # use the old "conn"
        groups = store_groups[n]  # use the old "groups"
        return  # returns early if we can just use previously calculated "conn" and "groups"
    partition = []  # stores all the row/column/boxes
    for i in range(n):  # iterates through each row
        partition += [[]]  # creates new list for this row
        for j in range(n):  # for each index in this row
            partition[i] += [i * n + j]  # adds the index to the list
    for i in range(n):  # iterates through each column
        partition += [[]]  # creates new list for this column
        for j in range(n):  # for each index in this column
            partition[-1] += [i + j * n]  # adds the index to the list
    for i in range(w):  # for each horizontal segment
        for j in range(h):  # for each vertical segment
            partition += [[]]  # adds new list for this box
            for a in range(h):  # for each column in this box
                for b in range(w):  # for each row in this box
                    partition[-1] += [n * (h * i + a) + (w * j + b)]  # adds the index to the list
    conn = [[] for i in range(n * n)]  # creates empty list for each index
    for i in range(n * n):  # for each index
        for p in partition:  # for each row/column/box
            if i in p:  # if the index is in the row/column/box
                for c in p:  # for each index in the row/column/box
                    if i != c and c not in conn[
                        i]:  # if the row/column/box's index is not the same as the original index and is not already in "conn"
                        conn[i] += [c]  # add the row/column/box's index to this list
    groups = [[] for i in range(n * n)]  # creates empty list for each index
    for p in partition:  # adds row/column/box from "partition" into "groups"
        for pi in p:  # for each index in the row/column/box
            groups[pi] += [p]  # add this row/column/box to the "groups" of this index
    store_conn[n] = conn  # stores "conn" for future use
    store_groups[n] = groups  # stores "groups" for future use


def output(path, n):  # prints out puzzles in list of lists format
    h = int(math.sqrt(n))
    w = int(n / h)
    for i in range(n):
        for j in range(n):
            if path[n * i + j] < 10:
                print(path[n * i + j], end=" ")
            else:
                print(chr(path[n * i + j] - 10 + ord("A")), end=" ")
            if (j + 1) % w == 0:
                print(end=" ")
        if (i + 1) % h == 0:
            print()
        print()


def output2(path, n):  # prints out puzzles in string format
    h = int(math.sqrt(n))
    w = int(n / h)
    for i in range(n):
        for j in range(n):
            print(path[n * i + j], end=" ")
            if (j + 1) % w == 0:
                print(end=" ")
        if (i + 1) % h == 0:
            print()
        print()


def copy(path):  # deep copy of list of lists
    new_path = []
    for p in path:
        new_path += [[]]
        for c in p:
            new_path[-1] += [c]
    return new_path


def check_sum(puzzle):  # used to check if puzzles are correct
    if puzzle is None:
        return None
    total = -48 * path_len
    for c in puzzle:
        total += ord(c)
    # n = int(math.sqrt(path_len))
    # assert(total == n*n*(n+1)/2)
    return total


def status(path):  # checks if "path" is finished
    for p in path:  # for each index
        if len(p) != 1:  # if there is more than one possibility ...
            return 0  # ... we aren't done
    return 1  # if all the indexes only have one possibility, then we're done


'''
returns True is successful
returns None if the current "path" is unsolvable
removes a value from a given index of "path" and updates the rest of the "path"
if that was the last possible value at the index, then failed
if removing that value leaves only one possible value at the index, then remove the remaining value from all cells in the same row/column/box
for the row/column/box that the current index is in, check if there is only one possible index that the current "val" can go
   if so, update it
   if there are no remaining places, then also failed
'''


def remove(path, index, val):
    if val not in path[index]:  # if this "val" has already been removed
        return True  # return early since it has already been processed
    cur_len = len(path[index])  # calculate the number of possibilites at this "index"
    if cur_len == 1:  # if this is the last possibility ...
        return None  # ... this "path" cannot be correct, return failure
    path[index].remove(val)  # remove the "val" from the possibilities at this "index"
    # don't actually assign things, just remove possibilities until 1 left

    # now attempt to clean out all of its neighbors
    if cur_len == 2:  # if removing this "val" will leave only one more possibility ...
        for c in conn[index]:  # ... remove the last possibility from each of this "index"'s neighbors
            if remove(path, c, path[index][0]) is None:  # if a "remove()" failed ...
                return None  # ... this "path" cannot be correct, return failure

    # within each group,
    for g in groups[index]:  # for each row/column/box that this "index" is in
        new_i = -1  # set the new index to -1 to show that no possible index has been found
        for i in g:  # for each index inside this row/column/box
            if val in path[i]:  # if the "val" is possible in this index inside this row/column/box
                if new_i != -1:  # if this is not the first index that can be "val" ...
                    new_i = -2  # ... signal that there is more than one index that "val" can be in
                    break  # break early since this optimization failed
                new_i = i  # if this is the first index that can be "val", then set "new_i" to this index inside this row/column/box

        # -2 means that we encountered > 2 positions that could have that value, including that first position
        # -1 means we never saw someone who had this value in domain
        # Basically, we want to see if this removal left only one member of the group with this in their domain,
        # then go and update board/remove the value from IT'S domain

        if new_i == -2:  # if there is more than one index that can be "val" ...
            continue  # ... continue early since this optimization failed
        if new_i == -1:  # if there are no indexes that can be "val" ...
            return None  # ... this "path" cannot be correct, return failure

        # Try placing that deduced value at the new_i position. Remember, we realized that there was one other
        # member of the group that had this value, Thus, that one is forced to take this value, and we will now
        # perform arc consistency to see if shrinking this guy's domain will lead another person to have only
        # one remaining value in their domain/path. This is good.
        if len(path[new_i]) != 1:  # if "new_i" has not already been processed since more than one value remains
            if update(path, new_i, val) is None:  # if the "update()" failed ...
                return None  # ... this "path" cannot be correct, return failure
    return True  # return True if successfully completed all steps


'''
places a value at a certain index by removing all other possible values at that index
returns None if any of the "remove()" calls weren't possible
'''
# Are these methods changing the original path??

def update(path, index, val):
    if val not in path[index]:  # if this "val" cannot exist at the "index"
        return None  # ... this "path" cannot be correct, return failure
    del_vals = [p for p in path[index] if p != val]  # stores all the possible values at "index" except for "val"

    # in order to check that placing this value is legal, we consider the opposite: what can we deduce IF we reduce
    # all other possibilities from this positions domain? Most of the time, it will yield nothing, but occasionally,
    # we can prove other positions must be certain values and cascade forward!!

    for dv in del_vals:  # for each of the possible values at "index" except for "val"
        if remove(path, index, dv) is None:  # if "remove()" failed ...
            return None  # ... this "path" cannot be correct, return failure
    return path  # return updated "path" if completed all steps successfully


'''
if the current "path" is finished, return the list of strings version of it
otherwise, find the index with the least number of possible values
for each possible value of that index, make a copy, update that copy, and recur on it
'''


def dfs(path):
    if status(path) == 1:  # if this "path" is complete
        return [int_to_string[p[0]] for p in path]  # return the list of ints version of "path"
    lowest = 1000  # set "lowest" to arbitrarily large number
    index = None  # initialize "index"

    # Finding the minimum remaining values var

    for i in range(path_len):  # for each index
        if 1 < len(path[i]) < lowest:  # if the path length is lower than the current minimum and greater than 1
            lowest = len(path[i])  # update "lowest"
            index = i  # update the lowest "index"
    if index is None:  # if no indexes were found
        return None  # ... this "path" cannot be correct, return failure

    # Try each value, potentially could add least constraining values!

    for val in path[index]:  # for each possible value at the current index
        new_path = update(copy(path), index, val)  # "update()" a "copy()" of the "path" at the "index" with "val"
        if new_path is None:  # if the "update()" failed
            continue  # continue early since this "new_path" cannot be correct
        result = dfs(new_path)  # recur on this "new_path"
        if result:  # if a "path" was found
            return result  # return the solution
    return None  # no correct "path" was found, return failure


def solve(word):  # takes in a puzzle in string format and returns the solution in string format
    n = int(math.sqrt(len(word)))  # finds the side length of the puzzle
    zero_indexed = False  # stores whether the current puzzle is 0-indexed
    last_char = str(n)  # stores the last character of a puzzle with size "n" that is 1-indexed
    if n >= 10:  # if "n" is greater than or equal to 10
        last_char = chr(ord("A") + n - 10)  # "last_char" is a letter
    if "0" in word:  # if "0" is in the puzzle ...
        zero_indexed = True  # ... the puzzle is 0-indexed
    elif last_char in word:  # otherwise if the "last_char" is in the puzzle ...
        zero_indexed = False  # ... the puzzle is 1-indexed
    if zero_indexed:  # if puzzle is 0-indexed
        new_word = ""  # initialize a new puzzle
        for w in word:  # for each character in the old puzzle
            if w == ".":  # if the character is unknown ...
                new_word += "."  # ... add an unknown character to the new puzzle
            elif w == "9":  # otherwise if the character is a "9" ...
                new_word += "A"  # ... add an "A" to the new puzzle
            else:  # otherwise
                new_word += chr(ord(w) + 1)  # add a character with an incremented ASCII value
        word = new_word  # set the old puzzle to the new puzzle
    setup_tables(n)  # sets up the required information for a puzzle of size "n"
    path = []  # stores the possible values at each index
    for i in range(len(word)):  # for each index
        path += [[i for i in range(1, n + 1)]]  # initializes a list with all values
    for i in range(len(word)):  # for each index
        if word[i] == ".":  # if the character at the index is unknown ...
            continue  # ... do nothing
        if word[i].isdigit():  # if the character at the index is a number ...
            path = update(path, i, int(word[i]))  # ... update the "path" at "index" with the number
        else:  # otherwise the character must be a letter
            path = update(path, i, ord(word[i]) - ord(
                "A") + 10)  # update the "path" at "index" with the integer value of the letter
    solution = "".join(dfs(path))  # find the solution
    if zero_indexed:  # if puzzle is 0-indexed
        new_solution = ""  # initialize a new solution
        for s in solution:  # for each character in the old solution
            if s == "A":  # if the character is an "A" ...
                new_solution += "9"  # ... append a "9" to the new solution
            else:  # otherwise
                new_solution += chr(ord(s) - 1)  # add a character with an decremented ASCII value
        solution = new_solution  # set the old solution to the new solution
    return solution  # returns the solution of the puzzle


def main():  # formatting + timing
    decision = input("Solve a file? (y/n) ")  # asks whether we are solving a file of puzzles or a single puzzle
    if decision == "y":  # if we are solving a file of puzzles
        file_name = input("File Name: ")  # read in the file name
        # for trials in range(100):
        total_time = time.time()  # start overall timing
        with open(file_name) as f:  # open the file
            initial_states = f.readlines()  # read all of the lines
            initial_states = [w.strip() for w in initial_states]  # format the lines into a list of puzzles
        count = 0  # stores the number of the puzzle we are on
        for word in initial_states:  # for each puzzle
            cur_time = time.time()  # start timing
            count += 1  # increment the number of the puzzle we are on
            result = solve(word)  # solve the puzzle
            # print(str(count)+":", word) # print the number of the puzzle and the puzzle
            print("solution:", result, "checksum:", check_sum(result), "time:",
                  str(time.time() - cur_time)[:6])  # print the solution, checksum, and time for this puzzle
    print("total:", str(time.time() - total_time)[:6])  # print the total amount of time
    return  # end of solving a file of puzzles


    word = input("Word? ")  # read in the single puzzle we are solving
    cur_time = time.time()  # start timing
    result = solve(word)  # solve the puzzle
    output2(word, int(math.sqrt(path_len)))  # print the sudoku formatted puzzle
    print("-" * (2 * n + 1), end="\n\n")  # formatting
    if result is None:  # if there was no solution ...
        print("No Solution")  # ... print "No Solution"
    else:  # otherwise
        output(result, int(math.sqrt(path_len)))  # print the sudoku formatted solution
    print("Duration: ", time.time() - cur_time)  # print the time it took to solve this single puzzle

if __name__ == '__main__':
    main()
