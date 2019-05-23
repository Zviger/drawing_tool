import sys


class DrawingTool:
    def __init__(self, strem=None):
        self.canvas = None
        self.width = 0
        self.height = 0
        self.stream = strem

    def create_canvas(self, width, height):
        self.width = width
        self.height = height
        self.canvas = [[0] * width for _ in range(height)]  # 0 - is nothing
        self.print_image()

    def print_image(self):
        saved_stream = sys.stdout
        if self.stream:
            sys.stdout = self.stream
        if self.canvas:
            print("-" * (self.width + 2))
            for row in self.canvas:
                print("|", end="")
                for point in row:
                    if point != 0:
                        print(point, end="")
                    else:
                        print(" ", end="")
                print("|")
            print("-" * (self.width + 2))
        else:
            print("Please create canvas first")
        sys.stdout = saved_stream

    def create_line(self, x1, y1, x2, y2, pr=True):
        if self.canvas:
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            if x1 == x2:
                for i in range(y1 - 1, y2):
                    self.canvas[i][x1 - 1] = "x"
            else:
                for i in range(x1 - 1, x2):
                    self.canvas[y1 - 1][i] = "x" \
                                             ""
            if pr:
                self.print_image()
        else:
            print("Please create canvas first")

    def create_rectangle(self, x1, y1, x2, y2, pr=True):
        if self.canvas:
            self.create_line(x1, y1, x2, y1, pr=False)
            self.create_line(x2, y1, x2, y2, pr=False)
            self.create_line(x2, y2, x1, y2, pr=False)
            self.create_line(x1, y2, x1, y1, pr=False)
            if pr:
                self.print_image()
        else:
            print("Please create canvas first")

    def bucket_fell(self, x, y, color, pr=True):
        self.color_nearest_pixel(x - 1, y - 1, self.canvas[y - 1][x - 1], color)
        if pr:
            self.print_image()

    def color_nearest_pixel(self, x, y, prev_color, new_color):
        points_stack = [(x, y)]
        while points_stack:
            _x, _y = points_stack.pop()
            if _x+1 < self.width and self.canvas[_y][_x+1] == prev_color:
                points_stack.append((_x + 1, _y))
            if _x - 1 >= 0 and self.canvas[_y][_x-1] == prev_color:
                points_stack.append((_x - 1, _y))
            if _y + 1 < self.height and self.canvas[_y + 1][_x] == prev_color:
                points_stack.append((_x, _y + 1))
            if _y - 1 >= 0 and self.canvas[_y - 1][_x] == prev_color:
                points_stack.append((_x, _y - 1))
            self.canvas[_y][_x] = new_color

    def parse_command_and_run(self, command):
        arguments = list(command.split(" "))
        if arguments[0].lower() == "c":
            self.create_canvas(int(arguments[1]), int(arguments[2]))
        if arguments[0].lower() == "l":
            self.create_line(int(arguments[1]), int(arguments[2]), int(arguments[3]), int(arguments[4]))
        if arguments[0].lower() == "r":
            self.create_rectangle(int(arguments[1]), int(arguments[2]), int(arguments[3]), int(arguments[4]))
        if arguments[0].lower() == "b":
            self.bucket_fell(int(arguments[1]), int(arguments[2]), arguments[3])

    def read_commands_from_file(self, file_name):
        with open(file_name) as file:
            for s in file:
                self.parse_command_and_run(s.rstrip())


if __name__ == "__main__":
    with open("output.txt", "w") as f:
        dt = DrawingTool(strem=f)
        dt.read_commands_from_file("input.txt")
