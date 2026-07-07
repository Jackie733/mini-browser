# Current Status

## Chapter: 7 - Handling Buttons and Links

## Current concept: Click handling for links

## Implemented

- Split inline text into `LineLayout` and `TextLayout` objects.
- Bound left mouse clicks to the browser click handler.
- Hit-test click coordinates against the layout tree.
- Resolve and load links from clicked `<a href>` elements.

## Next to do

- Implement fragment links later if desired.

## Known Issues

- Links like `#click-handling` do not scroll within the current page yet.
  This is listed as a later Chapter 7 exercise.
