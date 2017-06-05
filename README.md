# Sublime Prevent Duplicate Windows


<p>
  <img src="https://img.shields.io/github/release/aristidesfl/sublime-prevent-duplicate-windows.svg" alt="Release version">
  <img src="https://img.shields.io/badge/stability-stable-green.svg" alt="Stability: Stable">
  <img src="https://img.shields.io/packagecontrol/dm/Prevent%20Duplicate%20Windows.svg" alt="Package Control">
  <img src="https://img.shields.io/badge/license-MIT-lightgray.svg" alt="License: MIT">
</p>

Sublime Text 3 package to prevent duplicate windows.
This may happen frequently if you use the command line utility `subl`.
Instead it switches to the corresponding, existing window.
This packages has a very small footprint.

[duplicate window]
1. window with the same folders / files has an existing one


## Install

Please use [Package Control](https://sublime.wbond.net/installation) to install this package. This will ensure that the package will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html) and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available packages.

1. When the package list appears, type `prevent duplicate`. Among the entries you should see `Prevent Duplicate Windows`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Caveats

This package also prevents multiple workspaces with the same folders from being open in different windows side by side.
This limitation results from not being able to identify which workspace is open.
You can still switch between workspaces in the same window using "Quick Switch Project...".
