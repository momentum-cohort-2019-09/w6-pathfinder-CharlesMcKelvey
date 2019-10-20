# A two-dimensional array that will have it much like a coordinate sheet
# Row being Y, Column (index of row) being X
from PIL import Image
# Figure out what you want
import numpy as np
import random as random
# np.loadtext(file, dtype=int)
# using np.subtract(map_color_array, lowest)
# using np.divide(map_color_array, diff_between_low_high)
# using np.multiply(map_color_array, 255)


class Map:
    def __init__(self):
        self.elevations = []
        self.lowest = 10000
        self.highest = 0
        self.colored_map = []
        self.coords = []  # This will be designed [ (x,y,elevation) ]
        # Each time we go through to check for the path, we would go through, looking for a y that is up 1, the same, or down 1 while also moving to the right by 1.
        self.width = ''
        self.height = ''
        self.map = ''
        self.map_trails = ''
        # Paths will be a list of my paths that I have taken. Initially it will just be one but then I will have all of them starting at the left most edge (600 for small, 1200 for large).
        # Listed with a score and the path
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
        # self.map.show()

    def find_paths(self):
        """
        This will be my pathfinder generator and will loop through every starting position with the x position being 0.
        """
        starting_points = [item for item in self.coords if item[0] == 0]
        # score_and_path = []
        # count = 0
        test = random.choice(starting_points)
        hiker = Pathfinder(self)
        path, score = hiker.find_path(test)
        path_score = [score, path]
        self.paths.append(path_score)
        # for start in starting_points:
        #     hiker = Pathfinder(self)
        #     path, score = hiker.find_path(start)
        #     path_score = [score, path]
        #     self.paths.append(path_score)
        # Find the best score in score_and_path
        self.best = self.paths[0]
        self.worst = self.paths[0]
        # Saving both worst and best and will print both. One being red, the other blue
        # best/worst structure: (score, [path])
        # Needed path to highlight specific path
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
        # point = ( x, y, elevation ) path = [ point, point, point, etc. ]
        for point in path:
            if type(point) != int:  # for the score that is passed in
                self.map_trails.putpixel((point[0], point[1]), color)
        self.map_trails.save('map_trails.png')


class Pathfinder:
    def __init__(self, the_journ):
        # Inside joke between Kerry and I
        self.map = the_journ
        # This will be a list of all the elevations that will be summed up at the end to calculate scores
        self.elevation_change = []
        # This will be the list of the full tuple (x, y, elevation) as a way to check where the pathfinder has been
        self.path = []
        # This will be what parts of the map are left for the pathfinder to go through
        self.remaining = []

    def find_path(self, start_point):
        """
        This will create the line on the map for you, given best starting position
        """
        # Should append a coordinate for the map. x[0] and y[1] elevation[2] will need to be accessed in a loop. You could, wherever you are, search through the list to find that, then do math, such as x+1 and then loop through such that y+1 y+0 y-1 is gained. and use those to get the tuple that matches that so you have the elevation. Once there, calculate difference in elevation, grab the lowest absolute value difference and add to sum, while also replacing the current coordinate of the pathfinder position.
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
                # By this point, the error would have gone away
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
        # How do we grab specifically the 3 options
        # append the tuples of choices to this and then return it
        # Checking that the x is 1 above the current location
        # That it grabs the y if it is -1 or 0 or +1 from the current
        # option[1] should be the y of the tuple
        # option = ( x, y, elevation )
        options = []
        for option in remaining:
            if option[1] == current[1]+1 and option[0] == current[0]+1:
                options.append(option)
            elif option[1] == current[1] and option[0] == current[0]+1:
                options.append(option)
            elif option[1] == current[1]-1 and option[0] == current[0]+1:
                options.append(option)
        remaining = [path for path in remaining if current[0] < path[0]]
        # options = [option for option in self.map.coords if option[0] == current[0]+1 and (option[1]+1 == current[1]+1 or option[1] == current[1] or option[1]-1 == current[1]-1)]
        return options, remaining


# Start it up!!! ----------------------------
small_map = Map()
small_map.build_map()

# large_map = Map()
# large_map.build_map('elevation_large.txt')
# large_map.set_high_and_low()
# large_map.color_map()

# im = Image.new('RGB', (600, 600))
# im.save('output.png')
# im.show()
# get_elevation_map('elevation_small.txt')
# get_elevation_map('elevation_large.txt')

# small_map = Map(get_elevation_map('elevation_small.txt'))
# large_map = Map(get_elevation_map('elevation_large.txt'))
