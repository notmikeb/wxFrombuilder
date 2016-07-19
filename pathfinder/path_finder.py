import pygame
import sys
import operator


WIDTH, HEIGHT = 620, 496

BLACK       = (  0,   0,   0)
WHITE       = (255, 255, 255)
GREY        = (229, 228, 226)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
GRAY        = ( 95,  95,  95)
LIGHT_BLUE  = (224, 255, 255)
LIGHT_GREEN = (144, 238, 144)
DARK_BLUE   = (171, 205, 239)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Path Finder')

pygame.init()


class Board:
    def __init__(self):
        self.rows, self.cols = 16,30

        self.cell_size = 30

        self.grid = list()
        self.fill_grid()
        self.add_adj_nodes()

        self.root_set = set()
        self.goal_set = set()

        self.font = pygame.font.SysFont('comic sans', 12)

    def fill_grid(self):
        """Instance every cell of the grid"""

        for row_margin, row in enumerate(range(self.rows)):
            self.grid.append([])

            for col_margin, col in enumerate(range(self.cols)):
                x = col*self.cell_size + col_margin
                y = row*self.cell_size + row_margin

                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                cell = Cell(row, col, rect)

                if row == 7 and col == 3:
                    cell.root = True
                    self.root = cell
                elif row == 7 and col == 16:
                    cell.goal = True
                    self.goal = cell

                self.grid[row].append(cell)

    def add_adj_nodes(self):
        """Add adjacent nodes attributes to each cell of grid"""

        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if x-1 >= 0:
                    cell.above = self.grid[x-1][y]
                if y+1 < len(self.grid[0]):
                    cell.right = self.grid[x][y+1]
                if x+1 < len(self.grid):
                    cell.below = self.grid[x+1][y]
                if y-1 >= 0:
                    cell.left = self.grid[x][y-1]

    def draw_grid(self):
        """Draw each cell on the screen"""

        screen.fill(GREY)

        for row in self.grid:
            for cell in row:
                if cell.root:
                    color = GREEN
                elif cell.goal:
                    color = RED
                elif cell.value:
                    color = DARK_BLUE
                elif cell.visited:
                    color = LIGHT_BLUE
                elif cell.f:
                    color = LIGHT_GREEN
                elif cell.wall:
                    color = GRAY
                else:
                    color = WHITE

                pygame.draw.rect(screen, color, cell.rect)

                x, y = cell.rect.x, cell.rect.y

                if cell.g:
                    self.draw_score(x + 2, y + 2, cell.g)
                if cell.h:
                    self.draw_score(x + 18, y + 2, cell.h)
                if cell.f:
                    self.draw_score(x + 2, y + self.cell_size - 10, cell.f)

    def draw_score(self, x, y, score):
        """Draw the g, h and f score values, right on the evaluated cell"""

        screen.blit(self.font.render('{}'.format(score), 1, BLACK), (x, y))

    def return_cell(self):
        """Return an istanced cell based on the mouse position"""

        pos = pygame.mouse.get_pos()

        x = pos[1] // (self.cell_size+1)
        y = pos[0] // (self.cell_size+1)

        return self.grid[x][y]

    def toggle_wall(self, is_wall):
        """Add/Remove a wall in the grid"""

        cell = self.return_cell()

        if not cell.root and not cell.goal:
            if is_wall and cell.wall:
                cell.wall = False
            elif not is_wall and not cell.wall:
                cell.wall = True

    def drag(self, is_root, is_goal):
        """Drag a root/goal cell around the grid"""

        cell = self.return_cell()

        if is_root:
            self.root_set.add(cell)
            if len(self.root_set) > 2:
                print("More than 2 ", len(self.root_set))
            if len(self.root_set) > 1:
                for root_cell in self.root_set:
                    if root_cell is not cell:
                        root_cell.root = False
                        self.root_set.remove(root_cell)
                        break

            cell.root = True
            self.root = cell

        elif is_goal:
            self.goal_set.add(cell)

            if len(self.goal_set) > 1:
                for goal_cell in self.goal_set:
                    if goal_cell is not cell:
                        goal_cell.goal = False
                        self.goal_set.remove(goal_cell)
                        break

            cell.goal = True
            self.goal = cell

    def return_adj_nodes(self, node):
        """Return a list of adjacent nodes"""

        return [node.above, node.right, node.below, node.left]

    def dfs(self):
        """Depth First Search Algorithm"""

        stack = [self.root]

        while stack:
            node = stack[-1]

            if node.goal:
                return True

            if not node.visited:
                node.visited = True

            for adj_node in self.return_adj_nodes(node):
                if adj_node and not adj_node.visited and not adj_node.wall:
                    stack.append(adj_node)
                    break
            else:
                stack.pop()

        return False

    def a_star(self):
        """A* algorithm."""

        stack = [self.root]

        while stack:
            # Take the node with the lowest f score value in the stack
            node = min(stack, key=operator.attrgetter('f'))

            if node == self.goal:
                return True

            # Remove the current node from the stack, and mark it as visited
            index = stack.index(node)
            stack.pop(index)
            node.visited = True

            for adj_node in self.return_adj_nodes(node):
                if adj_node and not adj_node.visited and not adj_node.wall:
                    cost = node.g + self.heuristic(node, adj_node)

                    if adj_node not in stack or cost < adj_node.g:
                        adj_node.parent = node
                        adj_node.g = cost
                        adj_node.h = self.heuristic(adj_node, self.goal)
                        adj_node.f = adj_node.g + adj_node.h

                        if adj_node not in stack:
                            stack.append(adj_node)

        return False

    def heuristic(self, root, goal):
        """Return the value of the distance from the root to the goal node
           using Manhattan heuristic"""

        dx = abs(root.row - goal.row)
        dy = abs(root.col - goal.col)

        return dx + dy
    def reset_path(self):
        """ set the path's g h f"""
        for i in self.grid:
            for y in i:
                y.g = 0
                y.h = 0
                y.f = 0
                y.parent = None
                y.visited = False


    def show_path(self):
        """Show the best path found"""

        node = self.goal

        while node.parent:
            node.parent.value = 1
            node = node.parent


class Cell:
    def __init__(self, row, col, rect):
        self.row, self.col = row, col
        self.rect = rect

        self.root = self.goal = False
        self.wall = False

        self.below = self.right = self.above = self.left = None

        self.visited = False
        self.g = self.h = self.f = 0
        self.parent = None

        self.value = 0

    def __repr__(self):
        return '<Cell in position ({}, {}) wall={} visited={}>'.format(
            self.row, self.col, self.wall, self.visited
        )


def run():
    board = Board()

    is_pressed = is_root = is_goal = is_wall = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = board.return_cell()

                # Left mouse button
                if event.button == 1:
                    is_pressed = True

                    is_root = True if cell.root else False
                    is_goal = True if cell.goal else False

                    if not cell.root and not cell.goal:
                        is_wall = True if cell.wall else False
            elif event.type == pygame.MOUSEBUTTONUP:
                is_pressed = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_9:
                    board.reset_path()

                if event.key == 32 or event.key == pygame.K_0:
                    # clear the value
                    board.reset_path()
                    if board.a_star():
                        #board.show_path()
                        pass
                    else:
                        print('No path found.')

        if is_pressed:
            if is_root or is_goal:
                board.drag(is_root, is_goal)
            else:
                board.toggle_wall(is_wall)

        board.draw_grid()

        pygame.display.update()


if __name__ == '__main__':
    run()