"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    res = []
    for item in paragraphs:
        if select(item):
            res.append(item)
    if k < len(res):
        return res[k]
    else:
        return ''
    # END PROBLEM 1

def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def select(item):
        item = remove_punctuation(item)
        item = lower(item)
        item = split(item)
        for word in topic:
            if word in item:
                return True
        return False
    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if len(typed_words) == 0:
        return 0.0
    cnt = 0
    for typed_word,reference_word in zip(typed_words,reference_words):
        if typed_word == reference_word:
            cnt += 1
    return cnt / len(typed_words) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    if len(typed) == 0:
        return 0.0
    return len(typed) / 5 / elapsed * 60
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    tmp = [0] * len(valid_words) 
    i = 0
    cnt = 0
    for word in valid_words:
        if word == user_word:
            return word
        tmp[i] = diff_function(user_word,word,limit)
        i = i + 1
    for i in range(len(tmp)):
        if tmp[i] == min(tmp):
            cnt = i
            break
    if min(tmp) > limit:
        return user_word
    else:
        return valid_words[cnt]
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    if len(start) == 0 or len(goal) == 0:
        return max(len(start),len(goal)) - min(len(start),len(goal))
    if start[0] != goal[0]:
        if limit == 0:
            return 1
        return 1 + shifty_shifts(start[1:],goal[1:],limit - 1)
    else:
        return shifty_shifts(start[1:],goal[1:],limit)
    # END PROBLEM 6


def meowstake_matches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    if limit < 0: # Fill in the condition
        # BEGIN
        "*** YOUR CODE HERE ***"
        return 0
        # END

    elif len(goal) == 0 or len(start) == 0: # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        return len(goal) + len(start)
        # END
    
    elif start[0] == goal[0]:
        return meowstake_matches(start[1:],goal[1:],limit)
    
    else:
        add_diff = meowstake_matches(start,goal[1:],limit - 1)
        remove_diff = meowstake_matches(start[1:],goal,limit - 1)
        substitute_diff = meowstake_matches(start[1:],goal[1:],limit - 1)
        # BEGIN
        "*** YOUR CODE HERE ***"
        return 1 + min(add_diff,min(remove_diff,substitute_diff))
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    progress = 0
    for w1,w2 in zip(typed,prompt):
        if w1 == w2:
            progress += 1
        else:
            break
    progress /= len(prompt)
    send({'id':id,'progress':progress})
    return progress
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    each_time = []
    for player in times_per_player:
        tmp = []
        for i in range(len(player) - 1):
            tmp.append(player[i+1]-player[i])
        each_time.append(tmp)
    return game(words,each_time)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    '''
    >>> p0 = [2, 2, 3]
    >>> p1 = [6, 1, 2]
    >>> fastest_words(game(['What', 'great', 'luck'], [p0, p1]))
    ? [['What'],['great','luck']]
    -- OK! --
    '''
    players = range(len(all_times(game)))  # An index for each player (0,2)
    words = range(len(all_words(game)))    # An index for each word (0,3)
    time = all_times(game) # [p0,p1]
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    res = [[] for _ in players] # (0,2)
    for i in words: # (0,3)
        tmp = 999
        label = 0
        for j in players: # (0,2)
            if time[j][i] < tmp:
                label = j
                tmp = time[j][i]
        res[label].append(word_at(game,i))
    return res
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you

##########################
# Extra Credit #
##########################

key_distance = get_key_distances()
def key_distance_diff(start, goal, limit):
    """ A diff function that takes into account the distances between keys when
    computing the difference score."""

    start = start.lower() #converts the string to lowercase
    goal = goal.lower() #converts the string to lowercase

    # BEGIN PROBLEM EC1
    "*** YOUR CODE HERE ***"
    if limit < 0:
        return float('inf')
    if len(start) == 0 or len(goal) == 0:
        # BEGIN
        "*** YOUR CODE HERE ***"
        return len(start) + len(goal)
        # END
    elif start[0] == goal[0]:
        return key_distance_diff(start[1:], goal[1:], limit)
    else:
        add_diff = 1 + key_distance_diff(start, goal[1:], limit - 1)
        remove_diff = 1 + key_distance_diff(start[1:], goal, limit - 1) 
        kd = key_distance[(start[0], goal[0])]
        substitute_diff = kd + key_distance_diff(start[1:], goal[1:], limit - 1) 
        # BEGIN
        "*** YOUR CODE HERE ***"
        return min(min(add_diff, remove_diff), substitute_diff)
        # END
    # END PROBLEM EC1

def memo(f):
    """A memoization function as seen in John Denero's lecture on Growth"""

    cache = {}
    def memoized(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return memoized

key_distance_diff = count(key_distance_diff)


def faster_autocorrect(user_word, valid_words, diff_function, limit):
    """A memoized version of the autocorrect function implemented above."""

    # BEGIN PROBLEM EC2
    "*** YOUR CODE HERE ***"
    tmp = [0] * len(valid_words)
    
    memoized = memo(diff_function)
    
    for i, word in enumerate(valid_words):
        if word == user_word:
            return word
        tmp[i] = memoized(user_word, word, limit)
    
    min_distance = min(tmp)
    
    if min_distance > limit:
        return user_word
    
    closest_word_index = tmp.index(min_distance)
    return valid_words[closest_word_index]
    # END PROBLEM EC2


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)