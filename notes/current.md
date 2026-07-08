# Current Status

## Chapter: 8 - Sending Information to Servers

## Current concept: Receiving POST requests

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
- Renamed the default stylesheet to `browser.css`.
- Added default styles for `input` and `button`.
- Added `InputLayout` for rendering text inputs and simple buttons.
- Added inline layout handling for `input` and `button` elements.
- Added `should_paint` filtering to avoid double-painting form controls.
- Added focus tracking for page `<input>` elements.
- Split keyboard input between browser chrome and page content.
- Added input editing by updating the focused node's `value`.
- Re-render page content after input edits or focus changes.
- Draw a text cursor inside the focused input.
- Added HTTP POST support with request payloads.
- Added form submission from `<button>` clicks.
- Collect named input values from forms and URL-encode submitted data.
- Added a simple guest book server in `src/server.py`.
- Parse HTTP GET and POST requests on the server.
- Decode submitted form bodies and update server-side guest book state.
- Return generated HTML responses for guest book and 404 pages.

## Next to do

- Run the toy browser against `http://localhost:8000/`.
- Implement fragment links later if desired.

## Known Issues

- Links like `#click-handling` do not scroll within the current page yet.
  This is listed as a later Chapter 7 exercise.
