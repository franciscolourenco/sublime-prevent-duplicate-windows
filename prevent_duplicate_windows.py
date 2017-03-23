"""Prevent Duplicate Windows.

Sublime Text 3 package to prevent duplicate windows from being opened.
Instead, switch to the corresponding, existing window.

[duplicate window]
1. window with the same folders has an existing one

"""
import os
import time
import sublime
import sublime_plugin
from subprocess import Popen, PIPE


class PreventDuplicateWindows(sublime_plugin.EventListener):

    # using on_new without async, the window does't have any folders yet
    def on_new_async(self, view):
        # if a single file is opened in a new window, view doesn't contain a view. api bug?
        current_window = view.window() or sublime.windows()[-1]
        # if a single file is opened, view might not contain a file name. api bug?
        current_file = view.file_name() or current_window.active_view().file_name()
        current_folders = current_window.folders()

        # dont do anything if we have an empty buffer on a new window
        if not current_file and not current_window:
            return

        # loop through all windows except current one
        for existing_window in sublime.windows()[:-1]:
            existing_folders = existing_window.folders()
            # folders need to match
            if existing_folders == current_folders:
                # if the folders are empty, then the files need to match
                if existing_folders or current_file == existing_window.active_view().file_name():
                    # close current window
                    current_window.run_command('close_window')
                    # switch window unless current window is the right one
                    if existing_window != sublime.windows()[-1]:
                        self.focus(existing_window)
                    return

    def focus(self, window_to_move_to):
        active_view = window_to_move_to.active_view()
        active_group = window_to_move_to.active_group()

        # In Sublime Text 2 if a folder has no open files in it the active view
        # will return None. This tries to use the actives view and falls back
        # to using the active group

        # Calling focus then the command then focus again is needed to make this
        # work on Windows
        if active_view is not None:
            window_to_move_to.focus_view(active_view)
            window_to_move_to.run_command(
                'focus_neighboring_group')
            window_to_move_to.focus_view(active_view)

        elif active_group is not None:
            window_to_move_to.focus_group(active_group)
            window_to_move_to.run_command(
                'focus_neighboring_group')
            window_to_move_to.focus_group(active_group)

        if sublime.platform() == 'osx':
            self._osx_focus()
        elif sublime.platform() == 'linux':
            self._linux_focus(window_to_move_to)


    def _osx_focus(self):
        name = 'Sublime Text'
        if int(sublime.version()) < 3000:
            name = 'Sublime Text 2'

        # This is some magic. I spent many many hours trying to find a
        # workaround for the Sublime Text bug. I found a bunch of ugly
        # solutions, but this was the simplest one I could figure out.
        #
        # Basically you have to activate an application that is not Sublime
        # then wait and then activate sublime. I picked "Dock" because it
        # is always running in the background so it won't screw up your
        # command+tab order. The delay of 1/60 of a second is the minimum
        # supported by Applescript.
        cmd = """
        tell application "System Events"
            activate application "Dock"
            delay 1/60
            activate application "%s"
        end tell""" % name

        Popen(['/usr/bin/osascript', "-e", cmd],
              stdout=PIPE, stderr=PIPE)

    # Focus a Sublime window using wmctrl. wmctrl takes the title of the window
    # that will be focused, or part of it.
    def _linux_focus(self, window_to_move_to):
        window_variables = window_to_move_to.extract_variables()

        if 'project_base_name' in window_variables:
            window_title = window_variables['project_base_name']
        elif 'folder' in window_variables:
            window_title = os.path.basename(
                window_variables['folder'])

        try:
            Popen(["wmctrl", "-a", window_title + ") - Sublime Text"],
                  stdout=PIPE, stderr=PIPE)
        except FileNotFoundError:
            msg = "`wmctrl` is required by GotoWindow but was not found on " \
                  "your system. Please install it and try again."
            sublime.error_message(msg)
