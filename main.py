# Beginning Advent of Code 2021. This looks fun.

class ElfSub:
    """Help the elves deliver Santa's gifts via submarine."""

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
