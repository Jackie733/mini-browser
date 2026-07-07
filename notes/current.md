# Current Status

## Chapter: 7 - Handling Buttons and Links

## Current concept: Editable address bar navigation

## Implemented

- Split inline text into `LineLayout` and `TextLayout` objects.
- Bound left mouse clicks to the browser click handler.
- Hit-test click coordinates against the layout tree.
- Resolve and load links from clicked `<a href>` elements.
- Split page state into `Tab` and window/chrome state into `Browser`.
- Added browser chrome with a tab bar, new-tab button, URL bar, and back button.
- Added per-tab history and back navigation.
- Added URL string rendering for the address bar.
- Added address bar focus, keyboard input, cursor drawing, and Enter-to-navigate.

## Next to do

- Implement fragment links later if desired.

## Known Issues

- Links like `#click-handling` do not scroll within the current page yet.
  This is listed as a later Chapter 7 exercise.
