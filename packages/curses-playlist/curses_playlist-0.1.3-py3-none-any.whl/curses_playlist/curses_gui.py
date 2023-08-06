import collections
import curses
import os


class MyCursesGUI(object):
    """Main class for interactive mode.
    Displays the 'state' (GUIState) and forwards keypresses to the controller.
    """

    def __init__(self, controller):
        os.environ.setdefault("ESCDELAY", "25")  # std. delay is 1000ms!
        self.controller = controller
        self.state = self.controller.state

        self.playlist_wnd = None
        self.candidates_wnd = None
        self.input_wnd = None
        self.status_wnd = None

    def start(self):
        print("starting up curses")
        curses.wrapper(self.main_loop)  # main-loop, activates "curses console" mode
        print("curses session ended.")

    def main_loop(self, stdscr):
        """Function to be called by curses.wrapper()
        Does this in infinite loop:
        -grab keypress
        -update state
        -draw GUI

        Args:
            stdscr: ref to standard screen
        """
        stdscr.clear()
        stdscr.refresh()

        # create windows
        self.candidates_wnd = Candlist()
        self.playlist_wnd = Playlist()
        self.input_wnd = InputWnd()
        self.status_wnd = InputWnd(loc_y=curses.LINES - 1)
        self.update()

        while not self.state.exit_GUI:
            c = stdscr.getch()

            # debug: display pressed key
            # print("KEY NAME : %s - %i\n" % (chr(c), c))
            # return

            self.controller.key_pressed(c)
            self.update()

    def update(self):

        # process gui_requests
        while self.state.gui_requests:
            request = self.state.gui_requests.pop()

            if (
                request == "candlist_left"
                and len(self.state.candidate_files) > self.candidates_wnd.num_lines
            ):
                self.candidates_wnd.rotate_candlist(-1, self.state)
            elif (
                request == "candlist_right"
                and len(self.state.candidate_files) > self.candidates_wnd.num_lines
            ):
                self.candidates_wnd.rotate_candlist(1, self.state)

        # update gui
        self.status_wnd.update(self.state.mode_str)
        self.candidates_wnd.update(self.state)
        self.playlist_wnd.update(self.state)
        self.input_wnd.update(self.state.search_str)


class InputWnd(object):
    """Displays query string. Or other things."""

    def __init__(self, loc_y=0, num_lines=1):
        self.wnd = curses.newwin(
            num_lines, curses.COLS, loc_y, 0
        )  # nlines, ncols, begin_y, begin_x
        self.num_lines = num_lines
        self.loc_y = loc_y

    def update(self, text):
        self.wnd.clear()
        self.wnd.addnstr(0, 0, text, curses.COLS - 1)
        self.wnd.refresh()


class Candlist(object):
    """Display files that match the current query."""

    def __init__(self, loc_y=12, num_lines=11):

        self.wnd = curses.newwin(
            num_lines, curses.COLS, loc_y, 0
        )  # nlines, ncols, begin_y, begin_x
        self.num_lines = num_lines
        self.loc_y = loc_y

    def rotate_candlist(self, direction, state):

        # guard: don't rotate over 0
        if direction == -1 and state.cand_offset == 0:
            return

        # guard: don't rotate over end of list
        if direction == 1 and state.cand_offset + self.num_lines - 1 > len(
            state.candidate_files
        ):
            return

        state.cand_rotate_counter += direction
        d = collections.deque(state.candidate_files)
        d.rotate(-direction * (self.num_lines - 1))
        state.candidate_files = list(d)
        state.cand_offset = state.cand_rotate_counter * (self.num_lines - 1)

    def update(self, state):

        self.wnd.clear()
        for idx in range(min(self.num_lines - 1, len(state.candidate_files))):

            real_idx = state.cand_offset + idx

            if 0 <= real_idx < len(state.candidate_files):
                self.wnd.addnstr(
                    idx,
                    0,
                    "%i: (%i / %i) %s"
                    % (
                        idx + 1 if idx != 9 else 0,
                        real_idx + 1,
                        len(state.candidate_files),
                        state.candidate_files[idx],
                    ),
                    curses.COLS - 1,
                )

        self.wnd.addnstr(
            self.num_lines - 1,
            0,
            f"{len(state.candidate_files)} files  |  duration {state.get_total_play_duration()}",
            curses.COLS - 1,
        )
        self.wnd.refresh()


class Playlist:
    """Display selected files. Supports reordering and deletion."""

    def __init__(self, loc_y=1, num_lines=10):

        self.wnd = curses.newwin(
            num_lines, curses.COLS, loc_y, 0
        )  # nlines, ncols, begin_y, begin_x
        self.num_lines = num_lines
        self.loc_y = loc_y

    def update(self, state):

        self.wnd.clear()
        for idx in range(min(self.num_lines, len(state.play_list))):

            if idx == state.selected_line:
                self.wnd.addnstr(
                    idx,
                    0,
                    "%i: %s" % (idx, state.play_list[idx]),
                    curses.COLS - 1,
                    curses.A_BOLD,
                )
            else:
                self.wnd.addnstr(
                    idx, 0, "%i: %s" % (idx, state.play_list[idx]), curses.COLS - 1
                )
        self.wnd.refresh()
