from PIL import Image
import numpy as np
import random as random


class Map:
    def __init__(self):
        self.elevations = []
        self.lowest = 10000
        self.highest = 0
        self.colored_map = []
        self.coords = []
        self.width = ''
        self.height = ''
        self.map = ''
        self.map_trails = ''
        self.paths = []
        self.worst = ''
        self.best = ''

    # This is essentially the main function
    def build_map(self):
        """
        This is the main function that is called when wanting to create a map.
        """
        choice = input('Would you like the small or large map?').lower()
        if choice == 'small':
            self.build_map_data('elevation_small.txt')
            self.set_high_and_low()
            self.build_map_colors()
            self.color_map()
            self.find_paths()
            self.draw_trails()
            # self.display_map()
            self.display_map_trails()
        elif choice == 'large':
            self.build_map_data('elevation_large.txt')
            self.set_high_and_low()
            self.build_map_colors()
            self.color_map()
            self.find_paths()
            self.draw_trails()
            # self.display_map()
            self.display_map_trails()
        else:
            print('Seems you have mistyped something')
            self.build_map()

    def display_map(self):
        self.map.show()

    def display_map_trails(self):
        self.map_trails.show()

    def build_map_data(self, file):
        with open(file) as elevation_map:
            rows = elevation_map.read().splitlines()
            for row in rows:
                row = row.split()
                for i in range(len(row)):
                    row[i] = int(row[i])
                self.elevations.append(row)
        self.width = len(self.elevations)
        self.height = len(self.elevations[0])

    def set_high_and_low(self):
        for row in self.elevations:
            for number in row:
                if number > self.highest:
                    self.highest = number
                elif number < self.lowest:
                    self.lowest = number

    def build_map_colors(self):
        """
        Using: (elevation of the given number - lowest elevation) / (lowest elevation - highest elevation)
        Skeleton: (0, 0, 0, percent)
        """
        self.map = Image.new(
            'RGBA', (self.width, self.height), (0, 0, 0, 255))
        for row in self.elevations:
            for number in row:
                base = (number - self.lowest) / \
                    (self.highest - self.lowest)
                base = base * 255
                base = round(base)
                self.colored_map.append((base, base, base, 255))

    def color_map(self):
        count = 0
        for y in range(len(self.elevations)):
            for x in range(len(self.elevations[y])):
                self.map.putpixel((x, y), (self.colored_map[count]))
                self.coords.append((x, y, self.elevations[x][y]))
                count += 1
        self.map.save('map.png')

    def find_paths(self):
        """
        This will be my pathfinder generator and will loop through every starting position with the x position being 0.
        """
        starting_points = [item for item in self.coords if item[0] == 0]
        rand = starting_points[299]  # random.choice(starting_points)
        hiker = Pathfinder(self)
        path, score = hiker.find_path(rand)
        self.paths.append([score, path])
        # for start in starting_points:
        #     hiker = Pathfinder(self)
        #     path, score = hiker.find_path(start)
        #     path_score = [score, path]
        #     self.paths.append(path_score)
        self.best = self.paths[0]
        self.worst = self.paths[0]
        for score in self.paths:
            # Going for the best one
            if self.best[0] < score[0]:
                self.best = score
            # Going for the worst
            elif self.worst[0] > score[0]:
                self.worst = score

    def draw_trails(self):
        """
        With the draw path, using the self.paths, we will loop through and give the path to the draw path to put our trails onto the map
        """
        self.map_trails = self.map
        for trail in self.paths:
            self.draw_path(trail[1])
        self.draw_path(self.worst[1], (250, 0, 0, 255))
        self.draw_path(self.best[1], (0, 255, 0, 255))

    def draw_path(self, path, color=(0, 255, 0, 255)):
        for point in path:
            if type(point) != int:
                self.map_trails.putpixel((point[0], point[1]), color)
        self.map_trails.save('map_trails.png')


class Pathfinder:
    def __init__(self, the_journ):
        # Inside joke between Kerry and I
        self.map = the_journ
        self.elevation_change = []
        self.path = []
        self.remaining = []

    def find_path(self, start_point):
        """
        This will create the line on the map for you, given best starting position
        """
        trail = []
        current = start_point
        self.remaining = self.map.coords[:]
        # This would be the x in the map
        while current[0]+1 < self.map.width:
            # Choices will be the list of tuples
            options, self.remaining = self.next_step(current, self.remaining)
            best_choice = None
            for choice in options:
                diff = abs(choice[2] - current[2])
                if best_choice == None:
                    best_choice = choice
                elif choice[2] == best_choice[2]:
                    best_choice = random.choice([choice, best_choice])
                elif diff > abs((best_choice[2] - current[2])):
                    best_choice = choice
            trail.append(best_choice)
            current = best_choice
        # After we have found the path, we will check the sum of the trail
        score = sum([elevation[2] for elevation in trail])
        return trail, score

    def next_step(self, current, remaining):
        """
        Looks in the maps tuple elevations and checks for what is available
        Returns a list of 3 options
        """
        options = []
        for option in remaining:
            if option[1] == current[1]+1 and option[0] == current[0]+1:
                options.append(option)
            elif option[1] == current[1] and option[0] == current[0]+1:
                options.append(option)
            elif option[1] == current[1]-1 and option[0] == current[0]+1:
                options.append(option)
        remaining = [path for path in remaining if current[0] < path[0]]
        return options, remaining


# Start it up!!! ----------------------------
small_map = Map()
small_map.build_map()
