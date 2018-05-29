"""
=== Module Description ===
This module contains the code to run the treemap visualisation program.
It is responsible for initializing an instance of AbstractTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import pygame
from tree_data import FileSystemTree
from population import PopulationTree


# Screen dimensions and coordinates
ORIGIN = (0, 0)
WIDTH = 880
HEIGHT = 500
FONT_HEIGHT = 30                       # The height of the text display.
TREEMAP_HEIGHT = HEIGHT - FONT_HEIGHT  # The height of the treemap display.

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'


def run_visualisation(tree):
    """Display an interactive graphical display of the given tree's treemap.

    @type tree: AbstractTree
    @rtype: None
    """
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Render the initial display of the static treemap.
    render_display(screen, tree, '')

    # Start an event loop to respond to events.
    event_loop(screen, tree)


def render_display(screen, tree, text):
    """Render a treemap and text display to the given screen.

    Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
    screen vertically into the treemap and text comments.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @type text: str
        The text to render.
    @rtype: None
    """
    # First, clear the screen
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, 0, WIDTH, HEIGHT))

    tree_map = tree.generate_treemap((0, 0, WIDTH, TREEMAP_HEIGHT))

    for tree_rect in tree_map:
        # tree_rect[0] has format (x, y, width, height)
        # tree_rect[1] has format (int, int, int) which refers to colour.
        pygame.draw.rect(screen, tree_rect[1], tree_rect[0])

    _render_text(screen, text)

    # This must be called *after* all other pygame functions have run.
    pygame.display.flip()


def _render_text(screen, text):
    """Render text at the bottom of the display.

    @type screen: pygame.Surface
    @type text: str
    @rtype: None
    """
    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    text_surface = font.render(text, 1, pygame.color.THECOLORS['white'])

    # Where to render the text_surface
    text_pos = (0, HEIGHT - FONT_HEIGHT + 4)
    screen.blit(text_surface, text_pos)


def event_loop(screen, tree):
    """Respond to events (mouse clicks, key presses) and update the display.

    Note that the event loop is an *infinite loop*: it continually waits for
    the next event, determines the event's type, and then updates the state
    of the visualisation or the tree itself, updating the display if necessary.
    This loop ends when the user closes the window.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @rtype: None
    """
    # We strongly recommend using a variable to keep track of the currently-
    # selected leaf (type AbstractTree | None).
    # But feel free to remove it, and/or add new variables, to help keep
    # track of the state of the program.
    selected_leaf = None
    rect0 = (0, 0, WIDTH, TREEMAP_HEIGHT)
    curr_rect = (0, 0, 0, 0)
    # type of <curr_rect> is (int, int, int, int).
    text = ''

    while True:
        treemap = tree.generate_treemap(rect0)  # Update the treemap.
        # Wait for an event
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return

        if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
            # This is the left click mouse event.
            x, y = event.pos
            if selected_leaf is not None:
                # Convert the <selected_leaf> to its rectangle representation.
                # curr_rect has format: (x, y, width, height).
                curr_rect = tree.convert_to_rect(rect0, selected_leaf)[0]

            for t_rect in treemap:
                # <t_rect> is the rectangle representation of leaf in <tree>.
                # NOTICE that t_rect has format ((x, y, width, height), color)
                # Format of t_rect[0] is (x, y, width, height).
                mouse_check = locate_rect(x, y, t_rect)
                # <mouse_check> is the marker that indicates if the mouse is
                # inside the current rectangle.

                if selected_leaf is None:
                    if mouse_check:
                        selected_leaf = tree.get_leaf(rect0, t_rect[0])
                        # Now, selected_leaf refer to a FileSystemTree object.
                        text = generate_text(selected_leaf)
                        render_display(screen, tree, text)
                        break

                else:
                    if (curr_rect[0] <= x < (curr_rect[0] + curr_rect[2])) and \
                            (curr_rect[1] <= y < (curr_rect[1] + curr_rect[3])):
                        # Change the currently-selected rectangle to
                        # unseletected stage.
                        selected_leaf = None
                        text = ''
                        render_display(screen, tree, text)
                        break

                    elif mouse_check:
                        # change the selection of rectangle.
                        selected_leaf = tree.get_leaf(rect0, t_rect[0])
                        text = generate_text(selected_leaf)
                        render_display(screen, tree, text)
                        break

        if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 3):
            # Right click the pygame display and delete the leaf coresponding to
            # the rectangle user clicked on.
            # There are two cases: 1. the rectangle being clicked on is not the
            # currently_selected rectangle.
            # 2. the rectangle being clicked on is the currently_selected one.

            # First, we need to locate the rectangle clicked by the user.

            x, y = event.pos
            if selected_leaf is not None:
                # Convert the <selected_leaf> to its rectangle representation.
                # curr_rect has format: (x, y, width, height).
                curr_rect = tree.convert_to_rect(rect0, selected_leaf)[0]

            for t_rect in treemap:
                # <t_rect> is the rectangle representation of leaf in <tree>.
                # NOTICE that t_rect has format ((x, y, width, height), color)
                # Format of t_rect[0] is (x, y, width, height).
                mouse_check = locate_rect(x, y, t_rect)

                if mouse_check and (t_rect[0] != curr_rect):
                    # Delete the rectanlge being click on and does not affect
                    # the <selected_leaf> and the text shown on the screen.

                    # <tree.get_leaf(rect0, t_rect[0])> is the leaf
                    # we want to delele.
                    tree.complete_leaf_deletion(tree.get_leaf(rect0, t_rect[0]))
                    # We mutate the tree here.
                    render_display(screen, tree, text)

                elif mouse_check and (t_rect[0] == curr_rect):
                    # Delete the rectanlge being click on and change the
                    # <selected_leaf> to None and no text is shown.
                    selected_leaf = None
                    text = ''
                    tree.complete_leaf_deletion(tree.get_leaf(rect0, t_rect[0]))
                    render_display(screen, tree, text)

        if (event.type == pygame.KEYUP) and (selected_leaf is not None):
            # Perform the relative operation when the user releases a 'Up arrow'
            # or 'Down arrow' key.
            key_up(event, screen, tree, selected_leaf)


def run_treemap_file_system(path):
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a file or folder.

    @type path: str
    @rtype: None
    """
    file_tree = FileSystemTree(path)
    run_visualisation(file_tree)


def run_treemap_population():
    """Run a treemap visualisation for World Bank population data.

    @rtype: None
    """
    pop_tree = PopulationTree(True)
    run_visualisation(pop_tree)


def locate_rect(x, y, t_rect):
    """Return True if the mouse inside the current rectangle <t_rect>.

    @type x: int
        x coordinate of the mouse cursor.
    @type y: int
        y coordinate of the mouse cursor.
    @type t_rect: ((int, int, int, int), (int, int, int))
        This is the rectangle representation of leaf in <tree>,
        which is currently looped through,
        and it has format ((x, y, width, height), color).
    @rtype: bool
    """
    marker1 = t_rect[0][0] <= x < (t_rect[0][0] + t_rect[0][2])
    marker2 = t_rect[0][1] <= y < (t_rect[0][1] + t_rect[0][3])
    return marker1 and marker2


def generate_text(selected_leaf):
    """Return the text which should be displayed along the bottom of the window.
    Showing the name and data_size of the currently selected rectangle.

    @type selected_leaf: AAbstractTree
    @rtype: str
    """
    data_size = '(' + str(selected_leaf.data_size) + ')'
    return selected_leaf.get_separator() + ' ' + data_size


def key_up(event, screen, tree, selected_leaf):
    """Perform the relative operation when the user releases a 'Up arrow'
    or 'Down arrow' key.

    @type event: pygame.event.EventType
    @type screen: pygame.Surface
    @type tree: AbstractTree
    @type selected_leaf: AbstractTree
    """
    if event.key == pygame.K_UP:
        selected_leaf.increase_size()
        text = generate_text(selected_leaf)
        render_display(screen, tree, text)

    elif event.key == pygame.K_DOWN:
        selected_leaf.decrease_size()
        text = generate_text(selected_leaf)
        render_display(screen, tree, text)


if __name__ == '__main__':
    # To check your work for Tasks 1-4, try uncommenting the following function
    # call, with the '' replaced by a path like
    # 'C:\\Users\\David\\Documents\\csc148\\assignments' (Windows) or
    # '/Users/dianeh/Documents/courses/csc148/assignments' (OSX)
    PATH = 'C:\\Users\\User\\Desktop\\UofT\\csc148\\assignments\\a1'
    run_treemap_file_system(PATH)

    # To check the work for Task 5, uncomment the following function call.
    # run_treemap_population()
