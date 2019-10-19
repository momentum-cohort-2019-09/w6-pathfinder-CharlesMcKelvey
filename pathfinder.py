# A two-dimensional array that will have it much like a coordinate sheet
# Row being Y, Column (index of row) being X
from PIL import Image
# Figure out what you want
import numpy as np
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
        self.image = ''
        # Pathfinders will be a list of my paths that I have taken. Initially it will just be one but then I will have all of them starting at the left most edge (600 for small, 1200 for large).
        self.pathfinders = []

    def build_map_data(self, file):
        with open(file) as elevation_map:
            rows = elevation_map.read().splitlines()
            for row in rows:
                row = row.split()
                self.elevations.append(row)
        self.width = len(self.elevations)
        self.height = len(self.elevations[0])

    def set_high_and_low(self):
        for row in self.elevations:
            for number in row:
                if int(number) > self.highest:
                    self.highest = int(number)
                elif int(number) < self.lowest:
                    self.lowest = int(number)

    def build_map_colors(self):
        """
        Using: (elevation of the given number - lowest elevation) / (lowest elevation - highest elevation)
        Skeleton: (0, 0, 0, percent)
        """
        self.image = Image.new(
            'RGBA', (self.width, self.height), (0, 0, 0, 255))
        # Need to use putpixel to place the specific elevations in
        for row in self.elevations:
            for number in row:
                base = (int(number) - self.lowest) / \
                    (self.highest - self.lowest)
                base = base * 255
                base = round(base)
                self.colored_map.append((base, base, base, 255))

    def color_map(self):
        # This part is suppoed to color the map
        # The count is used to traverse the colored_map list and grab each point that is created as we go.
        count = 0
        for y in range(len(self.elevations)):
            for x in range(len(self.elevations[y])):
                self.image.putpixel((x, y), (self.colored_map[count]))
                self.coords.append((x, y, self.elevations[x][y]))
                count += 1
        self.image.save('map.png')
        self.image.show()

    def build_map(self):
        """
        This is the main function that is called when wanting to create a map.
        """
        # Choosing between big and small map
        choice = input('Would you like the small or large map?').lower()
        if choice == 'small':
            self.build_map_data('elevation_small.txt')
            self.set_high_and_low()
            self.build_map_colors()
            self.color_map()
        elif choice == 'large':
            self.build_map_data('elevation_large.txt')
            self.set_high_and_low()
            self.build_map_colors()
            self.color_map()
        else:
            print('Seems you have mistyped something')
            self.build_map()

    def find_paths(self):
        """
        This will be my pathfinder generator and will loop through every starting position with the x position being 0. 
        """
        starting_points = [item for item in self.coords if item[0] == 0]
        print(starting_points)


class Pathfinder:
    def __init__(self, map):
        self.map = map
        # This will be a list of all the elevations that will be summed up at the end to calculate scores
        self.path = []

    def find_path(self, start_point):
        """
        This will create the line on the map for you, given best starting position
        """
        # Should append a coordinate for the map. x[0] and y[1] elevation[2] will need to be accessed in a loop. You could, wherever you are, search through the list to find that, then do math, such as x+1 and then loop through such that y+1 y+0 y-1 is gained. and use those to get the tuple that matches that so you have the elevation. Once there, calculate difference in elevation, grab the lowest absolute value difference and add to sum, while also replacing the current coordinate of the pathfinder position.


# Start it up!!! ----------------------------
small_map = Map()
small_map.build_map()
small_map.find_paths()

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
