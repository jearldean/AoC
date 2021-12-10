# Beginning Advent of Code 2021. This looks fun.
from pprint import pprint


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


if __name__ == "__main__":
    elf_help = ElfSub()
    total_points, incomplete_lines = elf_help.syntax_checker('data/day10.data')
    total_score = elf_help.autocomplete_tool(incomplete_lines)
    print(total_score)
