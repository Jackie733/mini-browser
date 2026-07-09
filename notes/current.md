# Current Status

## Chapter: 9 - Running Interactive Scripts

## Current concept: Event Handling

## Implemented

- Installed and imported `dukpy` for executing JavaScript.
- Added `src/runtime.js` as a small JavaScript runtime loaded before page scripts.
- Added `JSContext` to keep a per-tab JavaScript interpreter.
- Exported Python functions into JavaScript with `dukpy.export_function`.
- Added `console.log` support through the JavaScript runtime.
- Load external `<script src="...">` files during page load.
- Added `document.querySelectorAll` as the first DOM API exposed to JavaScript.
- Map Python DOM nodes to integer handles so JavaScript can refer to them.
- Wrap handles in JavaScript `Node` objects.
- Added `Node.getAttribute` by passing handles back from JavaScript to Python.
- Added JavaScript-side listener storage with `addEventListener`.
- Dispatch click, keydown, and submit events from Python into JavaScript.
- Run event listeners with `this` bound to the target `Node`.
- Added event objects with `preventDefault` support.
- Stop the browser's default action when JavaScript cancels an event.

## Previous chapter recap

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

- Continue Chapter 9 from DOM mutation.
- Re-render after JavaScript changes the page.
- Keep local HTML testing behind `python3 -m http.server`.

## Known Issues

- Links like `#click-handling` do not scroll within the current page yet.
  This is listed as a later Chapter 7 exercise.
