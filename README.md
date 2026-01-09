# LIVE-SERVER

## demo imaes
<img width="407" height="780" alt="Screenshot 2026-01-09 212945" src="https://github.com/user-attachments/assets/04305d9e-dfe3-4931-b038-c00ec04e588e" />   <img width="415" height="790" alt="Screenshot 2026-01-09 212929" src="https://github.com/user-attachments/assets/ddf4d37c-f8dc-4996-985c-8cd11add8255" />


## Core Features:

1. **Device Preview Selector** - A GUI interface where users can:
   - Select an HTML file to preview
   - Choose from various device presets (Android/iOS device sizes)
   - Launch a live preview window

2. **Live Reload** - Automatically refreshes the preview when the HTML file is modified (using `watchdog`)

3. **Smart Window Control**:
   - Windows are non-resizable by default
   - Can be resized by holding Ctrl key (Windows-specific feature using `ctypes`)
   - Confirmation dialog on window close

4. **UI Framework** - Uses `ttkbootstrap` (themed tkinter) for a modern interface

## Key Components:

- **File watcher** - Monitors HTML file changes and triggers reload
- **Device presets** - Predefined mobile/tablet screen sizes
- **Window management** - Custom resize behavior and close handling
- **GUI selector** - Clean interface for file/device selection

## Workflow:
1. User selects HTML file and device preset
2. Application opens a fixed-size window simulating the chosen device
3. Live reload monitors file changes
4. Ctrl key enables temporary window resizing
5. Close confirmation prevents accidental closure

The app serves as a **mobile-first HTML preview tool** for developers, similar to browser dev tools' device simulation but as a standalone desktop application.
