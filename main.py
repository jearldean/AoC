# Beginning Advent of Code 2021. This looks fun.
from pprint import pprint
from random import choice


class ElfSub:
    """Help the elves deliver Santa's gifts via submarine."""

    ox = "0b"  # I only vote for winners in my pack
    co = "0b"  # I only vote for losers in my pack

    neighbor_coordinates_in_basin = []

    lefties = ["(", "{", "[", "<"]
    righties = [")", "}", "]", ">"]
    partners = {"(": ")", ")": "(",
                "{": "}", "}": "{",
                "[": "]", "]": "[",
                "<": ">", ">": "<"}

    im_going_critical = []
    i_have_been_served = []

    cave_map = {}
    cave_paths = []

    current_roll_value = 0
    roll_counter = 0

    def __init__(self):
        """ Might init instance variables in the future: self.things = things """
        self.first_illegal_char = None

    # -=-=-=-=-=- Day 1 -=-=-=-=-=-

    def smooth_the_data(self, data_path):
        """Open a file containing one data point on each line, convert each to int, return a list.

        >>> elf_help = ElfSub()
        >>> elf_help.smooth_the_data('data/day1.data')[:3]
        [189, 190, 199]

        :param data_path: str. A file path.
        :return: A list of integers.
        """
        smoothed_data = []
        f = open(data_path)
        for line in f:
            smoothed_data.append(int(line))
        return smoothed_data

    def increasing_sonar_readings(self, depth_guage_readings, sliding_window_measure=1):
        """ Measure the data in the sliding_window, count the steps where data increases in value.

        :param depth_guage_readings: List[int]. Gathered from day1.data.
        :param sliding_window_measure: int. Indicates the size of data "steps".
        :return: increasing_values_count, int. The count of data "steps" where value increased.
        ("Upward steps.")
        """
        increasing_values_count = 0

        for index_ in range(len(depth_guage_readings) - sliding_window_measure):
            a = 0
            b = 0
            for ii in range(sliding_window_measure):
                a += depth_guage_readings[index_ + ii]
                b += depth_guage_readings[index_ + ii + 1]
            if b > a:
                increasing_values_count += 1

        return increasing_values_count

    def sonar_report(self, data_path, sliding_window_measure=1):
        """Smooth data in data_path and perform the increasing_sonar_readings calculation.

        >>> elf_help = ElfSub()
        >>> elf_help.sonar_report('data/day1.data')
        1390
        >>> elf_help.sonar_report('data/day1.data', sliding_window_measure=3)
        1457
        >>> elf_help.sonar_report('data/day1.data', sliding_window_measure=5)
        1567

        :param data_path: str. A file path.
        :param sliding_window_measure: int. Indicates the size of data "steps".
        :return: increasing_values_count, int. The count of data "steps" where value increased.
        ("Upward steps.")
        """
        smooth_data = self.smooth_the_data(data_path)
        increasing_values_count = self.increasing_sonar_readings(
            depth_guage_readings=smooth_data,
            sliding_window_measure=sliding_window_measure)
        return increasing_values_count

    # -=-=-=-=-=- Day 2 -=-=-=-=-=-

    def import_trajectory_data(self, data_path):
        """ https://adventofcode.com/2021/day/2

        >>> elf_help = ElfSub()
        >>> elf_help.import_trajectory_data('data/day2.data')
        (1996, 1022, 2039912, 972980, 1942068080)
        """
        horizontal = 0
        depth1 = 0
        depth2 = 0
        aim = 0

        f = open(data_path)
        for line in f:
            x = int(line.split(" ")[1])
            if 'forward' in line:
                horizontal += x
                depth2 += (aim * x)
            elif 'down' in line:
                depth1 += x
                aim += x
            elif 'up' in line:
                depth1 -= x
                aim -= x
            else:
                print("Something unexpected in the data.")
        return horizontal, depth1, horizontal * depth1, depth2, horizontal * depth2

    # -=-=-=-=-=- Day 3 -=-=-=-=-=-

    def get_data_for_day3(self):
        data_pack = []
        f = open('data/day3.data')
        for line in f:
            data_pack.append(line.strip())
        return data_pack

    def binary_diagnostic(self):
        """ https://adventofcode.com/2021/day/3

        >>> elf_help = ElfSub()
        >>> elf_help.binary_diagnostic()
        ('0b100110110100', 2484, '0b011001001011', 1611, 4001724)
        """
        gamma = "0b"
        epsilon = "0b"
        data_pack = self.get_data_for_day3()

        for bit_position in range(12):
            (winning_value, losing_value) = self.what_is_the_winning_value(data_pack, bit_position)
            gamma += winning_value
            epsilon += losing_value

        gamma_rate = int(gamma, 2)
        epsilon_rate = int(epsilon, 2)

        power_consumption = gamma_rate * epsilon_rate
        return (gamma, gamma_rate, epsilon, epsilon_rate, power_consumption)

    def binary_diagnostic2(self):
        """ https://adventofcode.com/2021/day/3
        To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being considered.
        To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the position being considered.

        >>> elf_help = ElfSub()
        >>> elf_help.binary_diagnostic2()
        ('0b100111110001', 2545, '0b000011100111', 231, 587895)
        """
        original_data_pack = self.get_data_for_day3()

        self.oh_no_recursion(original_data_pack, bit_position=0, update_ox_or_co='ox')
        self.oh_no_recursion(original_data_pack, bit_position=0, update_ox_or_co='co')

        oxygen_generator_rating = int(self.ox, 2)
        CO2_scrubber_rating = int(self.co, 2)

        life_support_rating = oxygen_generator_rating * CO2_scrubber_rating
        return (self.ox, oxygen_generator_rating, self.co, CO2_scrubber_rating, life_support_rating)

    def oh_no_recursion(self, data_pack, bit_position, update_ox_or_co):
        if len(data_pack) == 1:  # Hacky, but IDC. It's 12:30 AM.
            if update_ox_or_co == 'ox':
                self.ox = f"0b{data_pack[0]}"
            else:
                self.co = f"0b{data_pack[0]}"
            return  # If there's just one value left, that's your answer!
        winning_value, winners, losers = self.wrapping_function(data_pack, bit_position)
        if update_ox_or_co == 'ox':
            self.ox += winning_value
            data_pack = winners
        else:
            data_pack = losers
            if winning_value == "1":
                self.co += "0"
            else:
                self.co += "1"
        bit_position += 1
        if bit_position == 12:  # 12 = len of one line of data
            return  # This prevents runaway recursion.
        self.oh_no_recursion(data_pack, bit_position, update_ox_or_co)

    def wrapping_function(self, data_pack, bit_position):
        (winning_value, losing_value) = self.what_is_the_winning_value(data_pack, bit_position)
        winners, losers = self.who_are_the_winners(data_pack, winning_value, bit_position)
        return winning_value, winners, losers

    def what_is_the_winning_value(self, data_pack, bit_position):
        column_eval = 0
        for ii in range(len(data_pack)):
            column_eval += int(data_pack[ii][bit_position])
        if column_eval >= (len(data_pack) / 2):
            winning_value = "1"
            losing_value = "0"
        elif column_eval < (len(data_pack) / 2):
            winning_value = "0"
            losing_value = "1"
        return (winning_value, losing_value)

    def who_are_the_winners(self, data_pack, winning_value, bit_position):
        winners = []
        losers = []
        for i in range(len(data_pack)):
            if data_pack[i][bit_position] == winning_value:
                winners.append(data_pack[i])
            else:
                losers.append(data_pack[i])
        return winners, losers

    # -=-=-=-=-=- Day 4 -=-=-=-=-=-

    def get_data_for_day4(self):
        cards = []
        f = open('data/day4.data')
        big_text = ""
        for line in f:
            big_text += line
        chops = big_text.split("\n\n")
        for raw_card in chops:
            card = []
            rows = raw_card.split("\n")
            for row in rows:
                next_row = []
                for card_number in row.split(" "):
                    try:
                        next_row.append(int(card_number.strip()))
                    except ValueError:
                        pass
                card.append(next_row)
            cards.append(card)
        return cards

    def bingo_cards4(self):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.bingo_cards4()
        FIRST WIN! Card number 69 won on ping_pong_ball 4 with a score of 2496
        LAST WIN!  Card number 19 won on ping_pong_ball 61 with a score of 25925
        """
        ping_pong_balls = [76, 69, 38, 62, 33, 48, 81, 2, 64, 21, 80, 90, 29, 99, 37, 15, 93, 46,
                           75, 0, 89, 56, 58, 40, 92, 47, 8, 6, 54, 96, 12, 66, 83, 4, 70, 19, 17,
                           5, 50, 52, 45, 51, 18, 27, 49, 71, 28, 86, 74, 77, 11, 20, 84, 72, 23,
                           31, 16, 78, 91, 65, 87, 79, 73, 94, 24, 68, 63, 9, 88, 82, 30, 42, 60,
                           13, 67, 85, 44, 59, 7, 53, 22, 1, 26, 41, 61, 55, 43, 39, 3, 35, 25, 34,
                           57, 10, 14, 32, 97, 95, 36, 98]
        cards = self.get_data_for_day4()
        winning_cards = []
        no_wins_yet = True

        for ping_pong_ball in ping_pong_balls:
            for card in range(len(cards)):
                for row in range(len(cards[card])):
                    for card_number in range(len(cards[card][row])):
                        if cards[card][row][card_number] == ping_pong_ball:
                            # Change the matching cell to zero so it doesn't participate in sums:
                            cards[card][row][card_number] = 0
                        if self.check_for_winning_conditions(cards[card]) is True:
                            if no_wins_yet:
                                score = self.score_the_card(cards[card], ping_pong_ball)
                                print(f"FIRST WIN! Card number {card} won on ping_pong_ball"
                                      f" {ping_pong_ball} with a score of {score}")
                                no_wins_yet = False
                            if cards[card] not in winning_cards:
                                winning_cards.append(cards[card])
                            if len(winning_cards) == len(cards):
                                score = self.score_the_card(cards[card], ping_pong_ball)
                                print(f"LAST WIN!  Card number {card} won on ping_pong_ball"
                                      f" {ping_pong_ball} with a score of {score}")
                                return

    def score_the_card(self, winning_card, ping_pong_ball):
        sum_of_uncalled_numbers = 0
        for row in winning_card:
            for card_number in row:
                sum_of_uncalled_numbers += card_number
        return sum_of_uncalled_numbers * ping_pong_ball

    def check_for_winning_conditions(self, card):
        """A zero sum on any row is a win."""
        for row in card:
            if sum(row) == 0:  # horizontal is easily computed.
                return True

        for column_value in range(5):
            vertical = 0
            for row in card:
                vertical += row[column_value]
            if vertical == 0:
                return True

        return False

    # -=-=-=-=-=- Day 5 -=-=-=-=-=-

    def get_data_for_day5(self, filename, gridsize):
        data = []
        f = open(filename)
        for line in f:
            two_pieces = line.split(" -> ")
            indexs = []
            for each_coord in two_pieces:
                x_and_y = each_coord.split(",")
                each_pair = []
                for each_ in x_and_y:
                    each_pair.append(int(each_.strip()))
                indexs.append(each_pair)
            data.append(indexs)
        return data, gridsize

    def grid_overlap(self, filename, gridsize):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.grid_overlap('data/day5a.data', 10)
        12
        >>> elf_help.grid_overlap('data/day5.data', 1000)
        22083
        """
        input, grid = self.get_data_for_day5(filename, gridsize)
        # print(input)  # [[[0, 9], [5, 9]], [[8, 0], [0, 8]],... ]
        grid_field = []
        bound = grid - 1  # Exceeding the bounds will give an IndexError
        # Make a grid_field of gridsize x gridsize zeroes:
        for x in range(grid):
            y_values = []
            for y in range(grid):
                y_values.append(0)
            grid_field.append(y_values)

        # Now fill the grid_field with the line overlap values:
        for aa in input:  # each index pair: aa = [[0, 9], [5, 9]]
            delta_x, delta_y = self.get_deltas(aa)
            if delta_x == 0 or delta_y == 0:  # Vertical or Horizontal Line
                line_length = abs((aa[0][0] - aa[1][0]) + (aa[0][1] - aa[1][1])) + 1
                if delta_x < 0 or delta_y < 0:
                    aa = self.flip_the_direction(aa)
                    delta_x, delta_y = self.get_deltas(aa)
                for step in range(line_length):
                    # print(aa, delta_x, delta_y, line_length, step)
                    if delta_x == 0:  # | vertical line   [[7, 0], [7, 4]]
                        grid_field[min((aa[0][1] + step), bound)][aa[0][0]] += 1
                    if delta_y == 0:  # – horizontal line [[0, 9], [5, 9]]
                        grid_field[aa[1][1]][min((aa[0][0] + step), bound)] += 1
            # Now add Diagonals:
            if abs(delta_x) == abs(delta_y):  # slope = 45°, / or \ diagonal line
                line_length = abs(aa[0][0] - aa[1][0]) + 1
                if (delta_x < 0 and delta_y < 0) or (delta_x < 0 and delta_y > 0):
                    aa = self.flip_the_direction(aa)
                    delta_x, delta_y = self.get_deltas(aa)
                for step in range(line_length):
                    if (delta_x > 0 and delta_y > 0):  # \ slope line  [[0, 0], [8, 8]]
                        grid_field[min((aa[0][1] + step), bound)][
                            min((aa[0][0] + step), bound)] += 1
                    if (delta_x > 0 and delta_y < 0):  # / slope line  [[5, 5], [8, 2]]
                        grid_field[min((aa[0][1] - step), bound)][
                            min((aa[0][0] + step), bound)] += 1

        score = self.get_score(grid_field)
        return score

    def get_score(self, grid_field):
        score = 0
        for xx in grid_field:
            for yy in xx:
                if yy > 1:
                    score += 1
        return score

    def get_deltas(self, aa):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.get_deltas([[1, 2], [3, 4]])
        (2, 2)
        """
        delta_x = aa[1][0] - aa[0][0]
        delta_y = aa[1][1] - aa[0][1]
        return delta_x, delta_y

    def flip_the_direction(self, aa):
        """
        [[8, 8], [0, 0]] creates the same line as [[0, 0], [8, 8]]
        Let's use the same calculation for either.

        >>> elf_help = ElfSub()
        >>> elf_help.flip_the_direction([[1, 2], [3, 4]])
        [[3, 4], [1, 2]]
        """
        return [aa[1], aa[0]]

    # -=-=-=-=-=- Day 6 -=-=-=-=-=-

    def get_data_for_day6(self, filename):
        data = []
        f = open(filename)
        for line in f:
            for each_age in line.split(","):
                data.append(int(each_age))
        return data

    def lanternfish_spawning_cycle(self, filename, days):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.lanternfish_spawning_cycle('data/day6a.data', 18)
        26
        >>> elf_help.lanternfish_spawning_cycle('data/day6a.data', 80)
        5934
        >>> elf_help.lanternfish_spawning_cycle('data/day6.data', 80)
        375482
        """
        """  # Initial solution will take too long to run in part 2.
        data = self.get_data_for_day6(filename)
        for each_day in range(days):
            for zz in range(len(data)):
                if data[zz] > 0:
                    data[zz] -= 1
                else:
                    data[zz] = 6
                    data.append(8)
            print(each_day)
        return len(data)
        """
        data = self.get_data_for_day6(filename)
        fish_counts = {}
        for each_fish in data:
            fish_counts[each_fish] = fish_counts.get(each_fish, 0) + 1

        for each_day in range(days):
            # Save these values outside of the dict we're going to modify:
            previous_day_array = fish_counts.copy()
            for dd in range(9):
                if dd == 8:
                    fish_counts[dd] = previous_day_array.get(0, 0)
                elif dd == 6:
                    fish_counts[dd] = (previous_day_array.get(dd + 1, 0) +
                                       previous_day_array.get(0, 0))
                else:
                    fish_counts[dd] = previous_day_array.get(dd + 1, 0)

        return sum(fish_counts.values())

    # -=-=-=-=-=- Day 7 -=-=-=-=-=-

    def crab_sub_fuel_economization(self, filename):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.crab_sub_fuel_economization('data/day7a.data')
        168
        """
        data = self.get_data_for_day6(filename)
        fuel_usage_dict = {}
        horizontal_positions = len(data)
        for horizontal_position in range(max(data) + 1):
            fuel_cost = 0
            for ii in data:
                #  the first step costs 1, the second step costs 2, the third step costs 3, and so on.
                distance = abs(ii - horizontal_position)
                for dd in range(distance + 1):
                    fuel_cost += dd
            fuel_usage_dict[horizontal_position] = fuel_cost
            # print("Calculating", horizontal_position, "out of", max(data) + 1)
        return min(fuel_usage_dict.values())

    # -=-=-=-=-=- Day 8 -=-=-=-=-=-

    def day8_part1(self, filename):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.day8_part1('data/day8a.data')
        26
        >>> elf_help.day8_part1('data/day8.data')
        470
        """
        f = open(filename)
        counts_of_unique = 0
        for line in f:
            left_and_right = line.split("|")
            for word in left_and_right[1].strip().split(" "):
                if len(word) in [2, 3, 4, 7]:
                    counts_of_unique += 1
        return counts_of_unique

    def day8_part2(self, filename):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.day8_part2('data/day8a.data')
        61229
        >>> elf_help.day8_part2('data/day8.data')
        989396
        """
        nixie_tubes = {0: ['a', 'b', 'c', 'e', 'f', 'g'],
                       1: ['c', 'f'],
                       2: ['a', 'c', 'd', 'e', 'g'],
                       3: ['a', 'c', 'd', 'f', 'g'],
                       4: ['b', 'c', 'd', 'f'],
                       5: ['a', 'b', 'd', 'f', 'g'],
                       6: ['a', 'b', 'd', 'e', 'f', 'g'],
                       7: ['a', 'c', 'f'],
                       8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                       9: ['a', 'b', 'c', 'd', 'f', 'g']}

        right_side_total = 0

        f = open(filename)
        for line in f:
            # First create the answer_key from left_side data:
            one_line_of_left_words = []
            left_and_right = line.split("|")
            for word in left_and_right[0].strip().split(" "):
                one_line_of_left_words.append(word)
            answer_key = self.get_the_answer_key(one_line_of_left_words)

            right_number_as_string = ""
            # Now decode right_side using the answer_key:
            for word in left_and_right[1].strip().split(" "):
                build_one_digit = set()
                for letter in word:
                    for answer_key_letter in answer_key:
                        if answer_key[answer_key_letter] == set(letter):
                            build_one_digit.add(answer_key_letter)
                for nixie_tube_number in nixie_tubes:
                    if set(nixie_tubes[nixie_tube_number]) == build_one_digit:
                        right_number_as_string += str(nixie_tube_number)
            right_side_total += int(right_number_as_string)
        return right_side_total

    def get_the_answer_key(self, one_line_sorty):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.get_the_answer_key([['a', 'b', 'c', 'f', 'g'], \
                                         ['c', 'f', 'g'], \
                                         ['a', 'b', 'c', 'd', 'e', 'f', 'g'], \
                                         ['a', 'b', 'c', 'e', 'g'], ['f', 'g'], \
                                         ['a', 'b', 'c', 'd', 'e', 'g'], \
                                         ['a', 'e', 'f', 'g'], \
                                         ['a', 'b', 'c', 'e', 'f', 'g'], \
                                         ['a', 'b', 'c', 'd', 'f'], \
                                         ['b', 'c', 'd', 'e', 'f', 'g']])
        {'a': {'c'}, 'd': {'a'}, 'g': {'b'}, 'b': {'e'}, 'f': {'g'}, 'c': {'f'}, 'e': {'d'}}
        """
        known_lengths = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
        # unique lengths    1,       4,       7, 8
        # shared lengths 0,                6,       9
        # shared lengths2      2, 3,    5

        possible_values = {2: 1,  # length: possible values
                           3: 7,
                           4: 4,
                           5: [2, 3, 5],
                           6: [0, 6, 9],
                           7: 8}

        lengths_dict = {}  # structured like possible_values
        answer_dict = {}
        for number_array in one_line_sorty:
            if len(number_array) == 2:
                lengths_dict[1] = number_array
            elif len(number_array) == 3:
                lengths_dict[7] = number_array
            elif len(number_array) == 4:
                lengths_dict[4] = number_array
            elif len(number_array) == 5:
                len_five = lengths_dict.get(5, [])
                len_five.append(number_array)
                lengths_dict[5] = len_five
            elif len(number_array) == 6:
                len_six = lengths_dict.get(6, [])
                len_six.append(number_array)
                lengths_dict[6] = len_six
            elif len(number_array) == 7:
                lengths_dict[8] = number_array
        # lengths_dict = {1: ['f', 'g'],
        #                 4: ['a', 'e', 'f', 'g'],
        #                 5: [['a', 'b', 'c', 'f', 'g'],
        #                     ['a', 'b', 'c', 'e', 'g'],
        #                     ['a', 'b', 'c', 'd', 'f']],
        #                 6: [['a', 'b', 'c', 'd', 'e', 'g'],
        #                     ['a', 'b', 'c', 'e', 'f', 'g'],
        #                     ['b', 'c', 'd', 'e', 'f', 'g']],
        #                 7: ['c', 'f', 'g'],
        #                 8: ['a', 'b', 'c', 'd', 'e', 'f', 'g']}

        # A 7 ('acf') minus 1 ('cf') will give you 'a':
        answer_dict['a'] = set(lengths_dict[7]) - set(lengths_dict[1])  # 'a' for sure
        b_or_d = set(lengths_dict[4]) - set(lengths_dict[1])  # could be 'b' or 'd'

        counts_are_keys235 = self.three_item_handling(lengths_dict[5])
        """2: ['A',      'c', 'd', 'e',      'g'],  # Caps are KNOWN
           3: ['A',      'c', 'd',      'f', 'g'],
           5: ['A', 'b',      'd',      'f', 'g'],"""
        # 'a', 'd' and 'g' all are length = 3. And we already know 'a':
        d_or_g = set(counts_are_keys235[3]) - answer_dict['a']
        # 'd' is the shared item in b_or_d and d_or_g:
        answer_dict['d'] = d_or_g & b_or_d
        # 'g' falls apart because we know 'a' and 'd':
        answer_dict['g'] = d_or_g - answer_dict['d']
        # Now that we know 'd', we know 'b':
        answer_dict['b'] = b_or_d - answer_dict['d']

        counts_are_keys069 = self.three_item_handling(lengths_dict[6])
        """{0: ['A', 'B', 'c',      'e', 'f', 'G'],  # Caps are KNOWN
            6: ['A', 'B',      'D', 'e', 'f', 'G'],
            9: ['A', 'B', 'c', 'D',      'f', 'G']}"""
        # Union all KNOWN quantities:
        what_we_know = answer_dict['a'] | answer_dict['b'] | answer_dict['d'] | answer_dict['g']
        # All the other lengths of 3 are known. Only 'f' is left:
        answer_dict['f'] = set(counts_are_keys069[3]) - what_we_know
        c_or_e = set(counts_are_keys069[2]) - (what_we_know | answer_dict['f'])
        # Intersection. 1 'cf' and 4 'bcdf' both don't contain 'e'. Now we know 'c':
        answer_dict['c'] = c_or_e & set(lengths_dict[4]) & set(lengths_dict[1])
        answer_dict['e'] = c_or_e - answer_dict['c']  # 'e' is what's left over. Now we have all 7!

        return answer_dict

    def three_item_handling(self, a_list_of_3_lists):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.three_item_handling([['c', 'd', 'e', 'f', 'g'], \
                                          ['b', 'c', 'd', 'e', 'f'], \
                                          ['a', 'b', 'c', 'd', 'f']])
        {1: ['a', 'g'], 2: ['b', 'e'], 3: ['c', 'd', 'f']}
        """
        flatten_3_lists = [item for sublist in a_list_of_3_lists for item in sublist]

        counts_are_keys = {}
        for each_letter in 'abcdefg':
            letter_count = flatten_3_lists.count(each_letter)
            counts_are_keys.setdefault(letter_count, []).append(each_letter)

        return counts_are_keys

    # -=-=-=-=-=- Day 9 -=-=-=-=-=-

    def get_data_for_day9(self, filename):
        data = []
        f = open(filename)
        for line in f:
            data.append(line.strip())
        return data

    def day9_part1(self, filename):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.day9_part1('data/day9a.data')
        15
        >>> elf_help.day9_part1('data/day9.data')
        535
        """
        data = self.get_data_for_day9(filename)

        sum_of_low_points = 0
        for row_index, line in enumerate(data):
            len_chars = len(line)
            for char_index in range(len_chars):
                number = line[char_index]
                neighbors, _ = self.my_neighbors_are(row_index, char_index, len_chars, data)
                sum_of_low_points += self.evaluate_number(int(number), neighbors)
        return sum_of_low_points

    def my_neighbors_are(self, row_index, char_index, len_chars, data):
        len_rows = len(data)
        if row_index == 0 and char_index == 0:  # top left corner: 2 neighbors
            return [int(data[0][1]),
                    int(data[1][0])], [[0, 1], [1, 0]]
        elif row_index == 0 and char_index == len_chars - 1:  # top right corner: 2 neighbors
            return [int(data[0][char_index - 1]),
                    int(data[1][char_index])], [[0, char_index - 1], [1, char_index]]
        elif row_index == 0:  # top row, middle: 3 neighbors
            return [int(data[0][char_index - 1]),
                    int(data[1][char_index]),
                    int(data[0][char_index + 1])], [[0, char_index - 1], [1, char_index],
                                                    [0, char_index + 1]]
        elif row_index == len_rows - 1 and char_index == 0:  # bottom left corner: 2 neighbors
            return [int(data[row_index][1]),
                    int(data[row_index - 1][0])], [[row_index, 1], [row_index - 1, 0]]
        elif row_index == len_rows - 1 and char_index == len_chars - 1:  # bottom right corner: 2 neighbors
            return [int(data[row_index][char_index - 1]),
                    int(data[row_index - 1][char_index])], [[row_index, char_index - 1],
                                                            [row_index - 1, char_index]]
        elif row_index == len_rows - 1:  # bottom row, middle: 3 neighbors
            return [int(data[row_index][char_index - 1]),
                    int(data[row_index - 1][char_index]),
                    int(data[row_index][char_index + 1])], [[row_index, char_index - 1],
                                                            [row_index - 1, char_index],
                                                            [row_index, char_index + 1]]
        elif char_index == 0:  # middle left side: 3 neighbors
            return [int(data[row_index - 1][0]),
                    int(data[row_index][1]),
                    int(data[row_index + 1][0])], [[row_index - 1, 0], [row_index, 1],
                                                   [row_index + 1, 0]]
        elif char_index == len_chars - 1:  # middle right side: 3 neighbors
            return [int(data[row_index - 1][char_index]),
                    int(data[row_index][char_index - 1]),
                    int(data[row_index + 1][char_index])], [[row_index - 1, char_index],
                                                            [row_index, char_index - 1],
                                                            [row_index + 1, char_index]]
        else:  # middle of the pack: 4 neighbors
            return [int(data[row_index - 1][char_index]),
                    int(data[row_index][char_index - 1]),
                    int(data[row_index][char_index + 1]),
                    int(data[row_index + 1][char_index])], [[row_index - 1, char_index],
                                                            [row_index, char_index - 1],
                                                            [row_index, char_index + 1],
                                                            [row_index + 1, char_index]]

    def evaluate_number(self, number, neighbors):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.evaluate_number(9, [4, 3, 2, 1])
        0
        >>> elf_help.evaluate_number(1, [2, 2, 2, 2])
        2
        """
        risk_level = 0
        if number < min(neighbors):
            # Unsure if ties are in or out. For now, they're out.
            risk_level = number + 1
        return risk_level

    def day9_part2(self, filename):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.day9_part2('data/day9a.data')
        1134
        >>> elf_help.day9_part2('data/day9.data')
        1122700
        """
        data = self.get_data_for_day9(filename)

        basin_coordinates = []
        # try getting basin coordinates first:
        for row_index, line in enumerate(data):
            len_chars = len(line)
            for char_index in range(len_chars):
                number = line[char_index]
                neighbors, _ = self.my_neighbors_are(row_index, char_index, len_chars, data)
                if self.evaluate_number(int(number), neighbors) > 0:
                    basin_coordinates.append([row_index, char_index])

        basin_sizes = []
        for basin in basin_coordinates:
            self.neighbor_coordinates_in_basin = []  # Wipe it out.
            self.uh_oh_recursion(basin, len_chars, data)
            basin_sizes.append(len(self.neighbor_coordinates_in_basin))

        basin_sizes.sort()
        basin_top3_product = basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]
        return basin_top3_product

    def uh_oh_recursion(self, coordinates, len_chars, data):
        neighbor_values, neighbor_coordinates = self.my_neighbors_are(
            coordinates[0], coordinates[1], len_chars, data)
        for index, value in enumerate(neighbor_values):
            if neighbor_coordinates[index] in self.neighbor_coordinates_in_basin:
                pass  # Skip it; we already checked this one.
            elif value < 9:  # Coordinate is part of a basin.
                self.neighbor_coordinates_in_basin.append(neighbor_coordinates[index])
                self.uh_oh_recursion(neighbor_coordinates[index], len_chars, data)
            else:
                pass  # Skip it; dead end.

    # -=-=-=-=-=- Day 10 -=-=-=-=-=-

    def syntax_checker(self, filename):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.syntax_checker('data/day10a.data')
        (26397, ['[({([[{{', '({[<{(', '((((<{<{{', '<{[{[{{[[', '<{(['])
        >>> elf_help.autocomplete_tool(['[({([[{{', '({[<{(', '((((<{<{{', '<{[{[{{[[', '<{(['])
        288957
        >>> elf_help.syntax_checker('data/day10.data')[0]
        369105
        """
        data = self.get_data_for_day9(filename)  # Reuse some code.

        points = {")": 3,
                  "]": 57,
                  "}": 1197,
                  ">": 25137}
        illegals_count = {}
        incomplete_lines = []

        for line in data:
            self.first_illegal_char = None
            first_illegal_char = self.find_first_illegal_char(line)
            if first_illegal_char not in self.righties:
                incomplete_lines.append(first_illegal_char)
            illegals_count[first_illegal_char] = illegals_count.get(first_illegal_char, 0) + 1

        total_points = 0
        for illegal_char in illegals_count:
            if illegal_char in self.righties:
                total_points += points[illegal_char] * illegals_count[illegal_char]

        return total_points, incomplete_lines

    def find_first_illegal_char(self, line):
        """
        Look for the first right-side char, or closer:
        {([(<{}[<>[]}>{[]{[(<()>
        Look to the left for it’s mate.
        If mates, remove those two chars from the string and try again:
        {([(<{}[<>[]}>{[]{[(<()>  # Remove {}
        {([(<[<>[]}>{[]{[(<()>    # Remove <>
        {([(<[[]}>{[]{[(<()>      # Remove []
        {([(<[}>{[]{[(<()>        # Yuck! [}  Illegal Pairing. Stop loop and report '}'.
        """
        if all(char in self.lefties for char in line):
            self.first_illegal_char = line
            return self.first_illegal_char
        for index, char in enumerate(line):
            if self.first_illegal_char:
                return self.first_illegal_char
            if char in self.lefties:
                pass
            elif char in self.righties and char != self.partners[line[index - 1]]:
                self.first_illegal_char = char
                return self.first_illegal_char
            else:
                self.find_first_illegal_char(line[:index - 1] + line[index + 1:])

    def autocomplete_tool(self, incomplete_lines):
        """
        Incomplete lines don't have any incorrect characters - instead, they're missing some
        closing characters at the end of the line. To repair the navigation subsystem,
        you just need to figure out the sequence of closing characters that complete all
        open chunks in the line.
        """
        autocomplete_results = []
        for incomplete_line in incomplete_lines:
            autocomplete_result = ""
            incomplete_line_reversed = incomplete_line[::-1]
            for char in incomplete_line_reversed:
                autocomplete_result += self.partners[char]
            autocomplete_results.append(autocomplete_result)

        return self.score_autocomplete_results(autocomplete_results)

    def score_autocomplete_results(self, autocomplete_results):
        """
        Autocomplete tools are an odd bunch: the winner is found by sorting all of the
        scores and then taking the middle score.

        >>> elf_help = ElfSub()
        >>> elf_help.score_autocomplete_results(['}}]])})]', ')}>]})', '}}>}>))))', ']]}}]}]}>', '])}>'])
        288957
        """
        scores = []
        for completion_string in autocomplete_results:
            scores.append(self.score_one_completion_string(completion_string))
        scores.sort()
        index_to_hit = (len(scores) - 1) / 2  # 9 results...0-8 --> index=4
        return scores[int(index_to_hit)]

    def score_one_completion_string(self, completion_string):
        """
        For sample '])}>'
        Start with a total score of 0.
        Multiply the total score by 5 to get 0, then add the value of ] (2) to get a new total score of 2.
        Multiply the total score by 5 to get 10, then add the value of ) (1) to get a new total score of 11.
        Multiply the total score by 5 to get 55, then add the value of } (3) to get a new total score of 58.
        Multiply the total score by 5 to get 290, then add the value of > (4) to get a new total score of 294.

        >>> elf_help = ElfSub()
        >>> elf_help.score_one_completion_string('}}]])})]')
        288957
        >>> elf_help.score_one_completion_string(')}>]})')
        5566
        >>> elf_help.score_one_completion_string('}}>}>))))')
        1480781
        >>> elf_help.score_one_completion_string(']]}}]}]}>')
        995444
        >>> elf_help.score_one_completion_string('])}>')
        294
        """
        points = {")": 1,
                  "]": 2,
                  "}": 3,
                  ">": 4}
        total_score = 0
        multiplier = 5
        for i in range(len(completion_string)):
            total_score = (total_score * multiplier) + points[completion_string[i]]
        return total_score

    # -=-=-=-=-=- Day 11 -=-=-=-=-=-

    def get_data_for_day11(self, filename):
        data = []
        f = open(filename)
        for line in f:
            one_line_list = []
            for octopus in line:
                if octopus in '0123456789':
                    one_line_list.append(int(octopus))
            data.append(one_line_list)
        return data

    def octo_flash(self, filename, cycles):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.octo_flash('data/day11a.data', 10)
        204
        >>> elf_help.octo_flash('data/day11.data', 10)
        196
        >>> elf_help.octo_flash('data/day11.data', 400)
        364
        """
        data_pack = self.get_data_for_day11(filename)
        total_flashes = 0
        loop_number = 0
        for loop in range(cycles):
            loop_number += 1
            self.im_going_critical = []
            self.i_have_been_served = []
            data_pack = self.increment_all_cells(data_pack)
            while self.im_going_critical:
                for coordinate in self.im_going_critical:
                    neighbor_coordinates, _ = self.who_are_my_neighbors(data_pack, coordinate)
                    for neighbor_coordinate in neighbor_coordinates:
                        data_pack = self.increment_one_cell(data_pack, neighbor_coordinate)
                    self.i_have_been_served.append(coordinate)
                    self.im_going_critical.remove(coordinate)
            data_pack, score = self.score_this_grid(data_pack)
            if score == 100:
                return loop_number
            total_flashes += score
        return total_flashes

    def increment_all_cells(self, data_pack):
        for line_index in range(len(data_pack)):
            for value_index in range(len(data_pack[line_index])):
                data_pack = self.increment_one_cell(data_pack, [line_index, value_index])
        return data_pack

    def increment_one_cell(self, data_pack, coordinate):
        line_index, value_index = coordinate
        if data_pack[line_index][value_index] == 9:  # I'm going critical
            if coordinate not in self.im_going_critical and coordinate not in self.i_have_been_served:
                self.im_going_critical.append(coordinate)
        data_pack[line_index][value_index] += 1
        return data_pack

    def who_are_my_neighbors(self, data_pack, coordinate):
        """
        Includes Diagonals. Doesn't require defined boundaries of the data_pack.
        """
        upper_bound = len(data_pack[0])  # Just calculate it.
        lower_bound = -1  # Don't go off the grid
        line_index, value_index = coordinate

        line_index_up = line_index - 1 if line_index - 1 > lower_bound else 5000  # Definite Indexerror
        line_index_down = line_index + 1 if line_index + 1 < upper_bound else 5000  # Definite Indexerror
        value_index_left = value_index - 1 if value_index - 1 > lower_bound else 5000  # Definite Indexerror
        value_index_right = value_index + 1 if value_index + 1 < upper_bound else 5000  # Definite Indexerror

        square_addresses = [[line_index_up, value_index_left],
                            [line_index_up, value_index],
                            [line_index_up, value_index_right],
                            [line_index, value_index_left],
                            # [line_index, value_index,  # Paul Lynde, center square!
                            [line_index, value_index_right],
                            [line_index_down, value_index_left],
                            [line_index_down, value_index],
                            [line_index_down, value_index_right]]

        my_neighbor_coordinates = []
        my_neighbor_values = []
        for each_combo in square_addresses:
            try:
                line, value = each_combo
                data_pack[line][value]
                my_neighbor_values.append(data_pack[line][value])
                my_neighbor_coordinates.append([line, value])
            except IndexError:
                pass

        return my_neighbor_coordinates, my_neighbor_values

    def score_this_grid(self, data_pack):
        score = 0
        coordinates = self.coordinates_greater_than_9(data_pack)
        for coordinate in coordinates:
            line_index, value_index = coordinate
            data_pack[line_index][value_index] = 0
        score += len(coordinates)
        return data_pack, score

    def coordinates_greater_than_9(self, data_pack):
        coordinates = []
        for line_index in range(len(data_pack)):
            for value_index in range(len(data_pack[line_index])):
                if data_pack[line_index][value_index] > 9:
                    coordinates.append([line_index, value_index])
        return coordinates

    # -=-=-=-=-=- Day 12 -=-=-=-=-=-

    def get_data_for_day12(self, filename):
        paths = []
        caves = set()
        paths_dict = {}
        f = open(filename)
        for line in f:
            link = line.strip().split("-")
            if link[0] in ['start', 'end']:
                if link[0] == 'start':
                    paths.append(link)
                if link[0] == 'end':
                    paths.append([link[1], link[0]])
            elif link[1] in ['start', 'end']:
                if link[1] == 'start':
                    paths.append([link[1], link[0]])
                if link[1] == 'end':
                    paths.append(link)
            else:
                paths.append([link[0], link[1]])
                paths.append([link[1], link[0]])
            caves.add(link[0])
            caves.add(link[1])

        for cave in caves:
            routes = []
            for path in paths:
                if path[0] == cave:
                    routes.append(path[1])
            paths_dict[cave] = routes
        return paths_dict

    def day12(self, filename):
        self.cave_map = self.get_data_for_day12(filename)
        print(self.cave_map)
        found_paths = []
        # for i in range(2):
        count = self.find_all_paths('start', ['start'])
        # if a_path not in found_paths:
        #    found_paths.append(a_path)
        # print(count)

        """
        smol_caves = []
        for path in found_paths:
            for cave in path.split(","):
                if cave not in ['start', 'end'] and cave == cave.lower() and cave not in smol_caves:
                    smol_caves.append(cave)

        illegal_paths = []
        for path in found_paths:
            for cave in smol_caves:
                if path.count(cave) > 1 and path not in illegal_paths:
                    illegal_paths.append(path)

        # print(illegal_paths)

        for i in illegal_paths:
            found_paths.remove(i)

        return found_paths"""
        return count

    def find_all_paths(self, current_node, established_path):

        for next_cave in self.cave_map[current_node]:

            if next_cave not in established_path:
                self.find_all_paths(next_cave, established_path.append(next_cave))
            else:
                pass

        return self.cave_paths

    def make_a_path(self, paths):
        one_path = ['start']
        possible_values = paths.get('start')

        while 'end' not in one_path:
            next_key = choice(possible_values)
            one_path.append(next_key)
            possible_values = paths[next_key]

        return ','.join(one_path)

    # -=-=-=-=-=- Day 13 -=-=-=-=-=-

    def get_data_for_day13(self, filename):
        data_blob = ""
        f = open(filename)
        for line in f:
            data_blob += line

        dots = []
        two_blobs = data_blob.split("\n\n")
        for line in two_blobs[0].split("\n"):
            line_parts = line.split(",")
            dots.append([int(line_parts[0]), int(line_parts[1])])

        folding_instructions = []
        for line in two_blobs[1].split("\n"):
            line_parts = line.replace("fold along ", "").split("=")
            folding_instructions.append([line_parts[0], int(line_parts[1])])
        return dots, folding_instructions

    def transparent_paper_folding(self, filename):
        """
        >>> elf_help = ElfSub()
        >>> a = elf_help.transparent_paper_folding('data/day13.data')
        >>> print(a.strip())
        ##    ##      ####  ######    ##    ##  ########  ##    ##  ######      ####
        ##  ##          ##  ##    ##  ##  ##    ##        ##    ##  ##    ##  ##    ##
        ####            ##  ######    ####      ######    ##    ##  ######    ##
        ##  ##          ##  ##    ##  ##  ##    ##        ##    ##  ##    ##  ##  ####
        ##  ##    ##    ##  ##    ##  ##  ##    ##        ##    ##  ##    ##  ##    ##
        ##    ##    ####    ######    ##    ##  ########    ####    ######      ######
        """
        dots, folding_instructions = self.get_data_for_day13(filename)
        grid_map = self.put_dots_on_page(dots)
        for each_fold in folding_instructions:
            grid_map = self.fold_it(grid_map, each_fold[0], each_fold[1])
        # Answer is backwards so, I'm just going to make it print out nice:
        unlock_code = ""
        for each_row in grid_map:
            flipped_row = "".join(each_row[::-1])
            remove_noise = flipped_row.replace(".", "  ").replace("#", "##")
            unlock_code += f"{remove_noise.strip()}\n"
        return unlock_code

    def put_dots_on_page(self, dots):
        x_values = []
        y_values = []
        for dot in dots:
            x_values.append(dot[1])
            y_values.append(dot[0])
        x_dimension = max(x_values)
        y_dimension = max(y_values)

        grid_map = []
        for dd in range(x_dimension + 1):
            grid_map.append(['.'] * (y_dimension + 1))

        for coord in dots:
            grid_map[coord[1]][coord[0]] = "#"

        return grid_map

    def fold_it(self, grid_map, y_or_x, index_):
        if y_or_x == 'y':
            above_the_fold = grid_map[:index_]
            below_the_fold = grid_map[index_ + 1:]
            for lower_row in range(len(below_the_fold)):
                row_index_above = -1 if lower_row == 0 else (-lower_row - 1)
                new_above_row = self.merge_2_rows(
                    above_the_fold[row_index_above], below_the_fold[lower_row])
                above_the_fold[row_index_above] = new_above_row
            return above_the_fold
        else:
            left_side = []
            right_side = []
            for each_row in grid_map:
                left_side.append(each_row[:index_])
                right_side.append(each_row[index_ + 1:])
            for each_row in range(len(right_side)):
                new_right_row = []
                for hh in range(len(right_side[0])):
                    left_column_index = -1 if hh == 0 else (-hh - 1)
                    if right_side[each_row][hh] == "#" or (
                            left_side[each_row][left_column_index] == "#"):
                        new_right_row.append("#")
                    else:
                        new_right_row.append(".")
                right_side[each_row] = new_right_row
            return right_side

    def merge_2_rows(self, line_a, line_b):
        merged_row = []
        for jj in range(max(len(line_a), len(line_b))):
            if line_a[jj] == "#" or line_b[jj] == "#":
                merged_row.append("#")
            else:
                merged_row.append(".")
        return merged_row

    # -=-=-=-=-=- Day 14 -=-=-=-=-=-

    def get_data_for_day14(self, filename):
        data = {}
        f = open(filename)
        for line in f:
            line_pieces = line.strip().split(' -> ')
            data[line_pieces[0]] = line_pieces[1]
        return data

    def polymerization(self, filename, seed, growth_cycles):
        """
        After step 5, it has length 97; After step 10, it has length 3073.
        After step 10, B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times;
        taking the quantity of the most common element (B, 1749) and subtracting the quantity
        of the least common element (H, 161) produces 1749 - 161 = 1588.
        :param filename:
        :param seed:
        :param growth_cycles:
        :return:
        """
        pair_map = self.get_data_for_day14(filename)

        polymer_string = seed
        # polymer_counts = self.create_polymer_counts(polymer_string)
        # print(polymer_counts)
        for num_loop in range(growth_cycles):
            polymer_string, _, _ = self.insert_between_each(polymer_string, pair_map)
            # polymer_counts = self.create_polymer_counts(polymer_string)
            print(num_loop)
        # print(polymer_counts)
        """
        polymer_string = seed
        polymer_counts = self.create_polymer_counts(polymer_string)
        print(polymer_counts)
        for num_loop in range(5):
            polymer_string, _, _ = self.insert_between_each(polymer_string, pair_map)
            polymer_counts = self.exponential_sizes(polymer_counts, pair_map)
            print(polymer_counts)"""

        score = self.score_the_polymer(polymer_string, pair_map)
        return score

    def create_polymer_counts(self, polymer_string):
        polymer_counts = {}
        for index_ in range(len(polymer_string) - 1):
            before_letter = polymer_string[index_]
            after_letter = polymer_string[index_ + 1]
            polymer_counts[before_letter + after_letter] = polymer_counts.get(
                before_letter + after_letter, 0) + 1
        return polymer_counts

    def exponential_sizes(self, polymer_counts, pair_map):
        new_polymer_counts = {}
        for pair in polymer_counts:
            _, component1, component2 = self.insert_between_each(pair, pair_map)
            new_polymer_counts[component1] = new_polymer_counts.get(component1, 0) + 1
            new_polymer_counts[component2] = new_polymer_counts.get(component2, 0) + 1
        for key in polymer_counts:
            # if key in polymer_counts and key in new_polymer_counts:
            new_polymer_counts[key] += polymer_counts.get(key, 0)
        return new_polymer_counts

    @staticmethod
    def insert_between_each(polymer_string, pair_map):
        before_letter = ""
        middle_letter = ""
        after_letter = ""
        new_polymer_string = ""
        for index_ in range(len(polymer_string) - 1):
            before_letter = polymer_string[index_]
            after_letter = polymer_string[index_ + 1]
            middle_letter = pair_map[f"{polymer_string[index_]}{polymer_string[index_ + 1]}"]
            new_polymer_string += before_letter + middle_letter
        new_polymer_string += after_letter

        return new_polymer_string, before_letter + middle_letter, middle_letter + after_letter

    @staticmethod
    def score_the_polymer(polymer_string, pair_map):
        counts = []
        for letter in pair_map.values():
            counts.append(polymer_string.count(letter))
        return max(counts) - min(counts)

    # -=-=-=-=-=- Day 15: Maze traversal in a scored grid -=-=-=-=-=-

    # -=-=-=-=-=- Day 16: Just noodling around -=-=-=-=-=-
    def day16(self):
        packet = 'D2FE28'
        hexstring = "0110"
        print(bytes.fromhex(hexstring).decode('utf-16'))
        print(bytes.fromhex(hexstring).decode("ascii"))  # D2
        self.hex_2_bin('D2FE28')  # next cluster
        print('110100101111111000101000')  # Same as the example
        self.bin_2_int("0110")  # version 6
        self.bin_2_int("100")  # type 4
        self.bin_2_int("0111" + "1110" + "0101")  # 3 packets form the number 2021
        self.bin_2_int("011111100101")  # 2021
        self.hex_2_bin('38006F45291200')
        print(self.hex_2_bin(
            '38006F45291200') == b'00111000000000000110111101000101001010010001001000000000')  # False
        cluster = str(self.hex_2_bin('38006F45291200'))
        print(cluster)
        self.bin_2_int("0" + cluster[:3])  # version 1
        self.bin_2_int("0" + cluster[3:6])  # type 6
        self.bin_2_int('000000000011011')  # contain the length of the sub-packets in bits, 27.
        self.bin_2_int('11010001010')  # should be 10
        self.bin_2_int('0101001000100100')  # should be 20
        self.hex_2_bin('8A004A801A8002F478')

    def hex_2_bin(self, hex_string):
        a_bin = bin(int(hex_string, 16))[2:]
        print(a_bin)
        return a_bin

    def bin_2_int(self, binstring):
        an_int = int(binstring, 2)
        print(an_int)
        return an_int

    # -=-=-=-=-=- Day 17 -=-=-=-=-=-

    def day17(self, x_range, y_range, velocity_range):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.day17(x_range=[20, 30], y_range=[-10, -5], velocity_range=100)
        {'maximum_y_pos': 45, 'x_initial_vel': 6, 'y_initial_vel': 9, 'num_velocity_winners': 112}
        """
        best_so_far = {'maximum_y_pos': 0, 'x_initial_vel': 0, 'y_initial_vel': 0}
        velocity_winners = []
        for x_initial_vel in range(-velocity_range, velocity_range):
            for y_initial_vel in range(-velocity_range, velocity_range):
                trench_hits, coordinates_passed_thru = self.calculate_one_throw(
                    x_initial_vel, y_initial_vel, x_range, y_range)
                if trench_hits:
                    for coordinate in coordinates_passed_thru:
                        maximum_y_pos = coordinate[1]
                        if maximum_y_pos > best_so_far['maximum_y_pos']:
                            best_so_far['maximum_y_pos'] = maximum_y_pos
                            best_so_far['x_initial_vel'] = x_initial_vel
                            best_so_far['y_initial_vel'] = y_initial_vel
                    velocity_winners.append([x_initial_vel, y_initial_vel])
        best_so_far['num_velocity_winners'] = len(velocity_winners)
        return best_so_far

    def calculate_one_throw(self, x_initial_vel, y_initial_vel, x_range, y_range):
        coordinates_passed_thru = self.projectile_loop(
            x_initial_vel, y_initial_vel, x_range, y_range)
        trench_hits = self.check_for_trench_hits(coordinates_passed_thru, x_range, y_range)
        return trench_hits, coordinates_passed_thru

    def projectile_loop(self, x_initial_vel, y_initial_vel, x_range, y_range):
        overshoot = 100
        coordinates_passed_thru = [[0, 0]]
        x_velocity = x_initial_vel
        y_velocity = y_initial_vel
        x_pos = coordinates_passed_thru[-1][0]
        y_pos = coordinates_passed_thru[-1][1]
        while x_pos < x_range[1] + overshoot and y_pos > y_range[
            1] - overshoot:  # after that, you've missed it
            last_coordinate_visited = coordinates_passed_thru[-1]
            x_pos, x_velocity = self.x_dimension_throw(
                x_pos=last_coordinate_visited[0], x_velocity=x_velocity)
            y_pos, y_velocity = self.y_dimension_throw(
                y_pos=last_coordinate_visited[1], y_velocity=y_velocity)
            coordinates_passed_thru.append([x_pos, y_pos])
            # print(coordinates_passed_thru)
        return coordinates_passed_thru

    def check_for_trench_hits(self, coordinates_passed_thru, x_range, y_range):
        hits = []
        for one_coord in coordinates_passed_thru:
            if self.trench_hit(one_coord, x_range, y_range):
                hits.append(one_coord)
        return hits

    def trench_hit(self, one_coordinates, x_range, y_range):
        x_pos = one_coordinates[0]
        y_pos = one_coordinates[1]
        if x_range[0] <= x_pos <= x_range[1] and y_range[0] <= y_pos <= y_range[1]:
            return True
        else:
            return False

    def x_dimension_throw(self, x_pos, x_velocity):
        """The probe's x position increases by its x velocity.
        Due to drag, the probe's x velocity changes by 1 toward the value 0;
            that is, it decreases by 1 if it is greater than 0,
            increases by 1 if it is less than 0,
            or does not change if it is already 0.
        """
        x_pos += x_velocity
        if x_velocity > 0:
            x_velocity -= 1
        elif x_velocity < 0:
            x_velocity += 1
        elif x_velocity == 0:
            x_velocity += 0
        return x_pos, x_velocity

    def y_dimension_throw(self, y_pos, y_velocity):
        """
        The probe's y position increases by its y velocity.
        Due to gravity, the probe's y velocity decreases by 1.
        """
        y_pos += y_velocity
        y_velocity -= 1
        return y_pos, y_velocity

    # -=-=-=-=-=- Day 18 -=-=-=-=-=-

    # -=-=-=-=-=- Day 19 -=-=-=-=-=-

    # -=-=-=-=-=- Day 20 -=-=-=-=-=-

    # -=-=-=-=-=- Day 21 -=-=-=-=-=-

    def dirac_dice(self, player_1_position, player_2_position):
        """
        >>> elf_help = ElfSub()
        >>> elf_help.dirac_dice(4, 8)
        739785
        >>> elf_help.dirac_dice(2, 10)
        571032
        """
        self.current_roll_value = 0
        self.roll_counter = 0
        player_1_score = 0
        player_2_score = 0
        goal_score = 1000

        while player_1_score < goal_score and player_2_score < goal_score:
            roll_total = self.roll_deterministic_dice()
            player_1_position = self.move_player_pawn(player_1_position, roll_total)
            player_1_score += player_1_position
            # print(f"Player 1 rolls {roll_total} and moves to space {player_1_position} for a total score of {player_1_score}.")
            if player_1_score < goal_score:
                roll_total = self.roll_deterministic_dice()
                player_2_position = self.move_player_pawn(player_2_position, roll_total)
                player_2_score += player_2_position
                # print(f"Player 2 rolls {roll_total} and moves to space {player_2_position} for a total score of {player_2_score}.")

        return min(player_1_score, player_2_score) * self.roll_counter

    def move_player_pawn(self, start_position, roll_total):
        new_position = start_position + roll_total
        # The board resets at 10, the new position is the ones' place value:
        board_space = int(str(new_position)[-1])
        if board_space == 0:  # There is no zero'th space, it's space 10.
            board_space = 10
        return board_space

    def roll_deterministic_dice(self):
        rolls = [self.current_roll_value + 1,
                 self.current_roll_value + 2,
                 self.current_roll_value + 3]
        self.current_roll_value = rolls[-1]
        self.roll_counter += 3
        roll_total = sum(rolls)
        return roll_total

    def roll_quantum_die(self):
        return [1, 2, 3]

    def play_with_quantum_dice(self, player_1_position, player_2_position):
        player_1_score = 0
        player_2_score = 0
        goal_score = 21


if __name__ == "__main__":
    elf_help = ElfSub()
    answer = elf_help.play_with_quantum_dice(4, 8)
    print(answer)
