import os
from datetime import timedelta
from typing import List

from curses_playlist.platform_defs import KEY_BACKSPACE
from curses_playlist.video_file import VideoFile
from curses_playlist.video_store import VideoStore


class GUIState:
    """
    Represents the internal state and exposes methods to change it coherently.
    """

    INPUT = 1
    CMD = 2
    NAVIGATE_PLAYLIST = 3
    MOVE_PLAYLIST_ENTRIES = 4

    PLAY = 5
    WRITE = 6

    mode_str = {
        INPUT: "[INPUT: ENTER - add | ESC - CMD]",
        CMD: "[CMD: m - mod | q | w | p - play | r - reset]",
        NAVIGATE_PLAYLIST: "[PL-NAV: m - move | d - del]",
        MOVE_PLAYLIST_ENTRIES: "[PL-MOV: m - nav | d - del]",
    }

    def __init__(self, all_files: List[VideoFile]):
        self.all_files = all_files
        self._init()

    def _init(self):
        """
        Does actual init. Useful for resetting state.
        """
        # for controller
        self.mode = None
        self.set_mode(GUIState.INPUT)

        self.search_str = ""
        self.history = [""]
        self.current_history_idx = 0
        self.candidate_files = self.all_files

        # for playlist
        self.play_list = []
        self.selected_line = -1
        self.exit_GUI = False

        self.gui_requests = []

        self.cand_offset = 0
        self.cand_rotate_counter = 0

    def gui_request(self, request):
        self.gui_requests.append(request)

    def set_mode(self, mode):
        # guards.
        if mode == self.NAVIGATE_PLAYLIST and not self.play_list:
            return

        self.mode = mode
        self.mode_str = GUIState.mode_str[mode]

    def update_search_str(self, c):
        if c == KEY_BACKSPACE:
            self.search_str = self.search_str[:-1]
        else:
            self.search_str += chr(c)

        self.cand_offset = 0
        self.cand_rotate_counter = 0
        self.update_candidate_files()

    def reset_search_str(self):
        self.search_str = ""
        self.cand_offset = 0
        self.cand_rotate_counter = 0
        self.candidate_files = self.all_files

    def update_candidate_files(self):
        words = self.search_str.split(" ")
        self.candidate_files = [
            f for f in self.all_files if all(w.lower() in f.path.lower() for w in words)
        ]

    def add_candidate(self, idx):
        """Adds self.candidate_files[idx] to self.play_list
        Args:
            idx: index
        """

        if len(self.candidate_files) > idx:
            self.play_list.append(self.candidate_files[idx])
            self.history.append(self.search_str)
            self.reset_search_str()

    def add_all_candidates(self):
        self.play_list.append([el.path for el in self.candidate_files])
        self.history.append(self.search_str)
        self.reset_search_str()

    def get_candidate_files(self):
        return self.candidate_files

    def get_total_play_duration(self) -> str:
        durations = [el.duration for el in self.play_list]
        acc = timedelta(seconds=0)
        for el in durations:
            if el:
                acc += el

        minutes = acc.total_seconds() // 60
        seconds = int(acc.total_seconds() - minutes * 60)

        return f"({minutes:0.0f}:{seconds:02d})"

    def playlist_cursor_up(self):
        if self.selected_line > 0:
            self.selected_line -= 1
            if self.mode == self.MOVE_PLAYLIST_ENTRIES:
                self.swap(self.selected_line + 1, self.selected_line)
        else:
            if not self.mode == self.MOVE_PLAYLIST_ENTRIES:
                self.selected_line = len(self.play_list) - 1

    def playlist_cursor_down(self):
        if self.selected_line == len(self.play_list) - 1:
            if not self.mode == self.MOVE_PLAYLIST_ENTRIES:
                self.selected_line = 0
        else:
            self.selected_line += 1
            if self.mode == self.MOVE_PLAYLIST_ENTRIES:
                self.swap(self.selected_line - 1, self.selected_line)

    def swap(self, idx_1, idx_2):
        self.play_list[idx_1], self.play_list[idx_2] = (
            self.play_list[idx_2],
            self.play_list[idx_1],
        )

    def toggle_playlist_mode(self):
        if self.mode == GUIState.NAVIGATE_PLAYLIST:
            self.set_mode(GUIState.MOVE_PLAYLIST_ENTRIES)
        elif self.mode == GUIState.MOVE_PLAYLIST_ENTRIES:
            self.set_mode(GUIState.NAVIGATE_PLAYLIST)

    def remove_selected_line_from_playlist(self):
        self.play_list.pop(self.selected_line)
        if self.selected_line > len(self.play_list) - 1:
            self.selected_line = len(self.play_list) - 1

        if not self.play_list:
            self.selected_line = -1
            self.set_mode(GUIState.INPUT)

    def history_up(self):

        if self.history:
            self.current_history_idx -= 1
            self.current_history_idx = self.current_history_idx % len(self.history)
            self.search_str = self.history[self.current_history_idx]
            self.update_candidate_files()

    def history_down(self):

        if self.history:
            self.current_history_idx += 1
            self.current_history_idx = self.current_history_idx % len(self.history)
            self.search_str = self.history[self.current_history_idx]
            self.update_candidate_files()

    def restore_from_playlist(self, playlist_path: str, video_store: VideoStore):

        # parse playlist
        if os.path.exists(playlist_path):
            with open(playlist_path, "r") as f:

                group_add = False
                for line in f.readlines():
                    if "# group_start" in line:
                        tmp_acc = []
                        group_add = True

                    elif "# group_end" in line:
                        self.play_list.append(tmp_acc)
                        group_add = False

                    # line contains actual VideoFile
                    else:
                        stripped = os.path.relpath(line.strip(), os.getcwd())
                        cur_vf = video_store.retrieve_video_file(stripped)

                        if cur_vf is not None:
                            if group_add:
                                tmp_acc.append(cur_vf)
                            else:
                                self.play_list.append(cur_vf)

    def reset_state(self):
        self._init()
