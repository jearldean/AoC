# Beginning Advent of Code 2021. This looks fun.

class ElfSub:
    """Help the elves deliver Santa's gifts via submarine."""

    ox = "0b"  # I only vote for winners in my pack
    co = "0b"  # I only vote for losers in my pack

    def __init__(self):
        """ Might init instance variables in the future: self.things = things """

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


e = ElfSub()
e.bingo_cards4()
