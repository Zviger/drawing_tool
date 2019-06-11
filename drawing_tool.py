import sys


class DrawingTool:
    def __init__(self, stream=None):
        self.canvas = None
        self.width = 0
        self.height = 0
        self.stream = stream

    def create_canvas(self, width, height):
        self.width = width
        self.height = height
        self.canvas = [[" "] * width for _ in range(height)]
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
                    print(point, end="")
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
                    self.canvas[y1 - 1][i] = "x"
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
        if self.canvas:
            self.color_nearest_pixel(x - 1, y - 1, self.canvas[y - 1][x - 1], color)
            if pr:
                self.print_image()
        else:
            print("Please create canvas first")

    def color_nearest_pixel(self, x, y, prev_color, new_color):
        deltas = (-1, 0, 1, 0)
        points_stack = [(x, y)]
        while points_stack:
            _x, _y = points_stack.pop()
            for i in range(4):
                dx = deltas[i]
                dy = deltas[i - 1]
                if self._is_ok(_x + dx, _y + dy) and self.canvas[_y + dy][_x + dx] == prev_color:
                    points_stack.append((_x + dx, _y + dy))
            self.canvas[_y][_x] = new_color

    def parse_command_and_run(self, com_and_arg):
        com_and_arg = list(com_and_arg.split(" "))
        c = com_and_arg[0].lower()
        if c == "b":
            self.bucket_fell(*map(int, com_and_arg[1:-1]), com_and_arg[-1])
        else:
            arguments = list(map(int, com_and_arg[1:]))
            if c == "c":
                self.create_canvas(*arguments)
            elif c == "l":
                self.create_line(*arguments)
            elif c == "r":
                self.create_rectangle(*arguments)
            elif c == "b":
                self.bucket_fell(*arguments)

    def read_commands_from_file(self, file_name):
        with open(file_name) as file:
            for s in file:
                self.parse_command_and_run(s.rstrip())

    def _is_ok(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        else:
            return False


if __name__ == "__main__":
    with open("output.txt", "w") as f:
        dt = DrawingTool()
        dt.read_commands_from_file("input.txt")
