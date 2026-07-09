# Current Status

## Chapter: 10 - Keeping Data Private

## Current concept: read through CSRF nonces; next section is SameSite Cookies

## Implemented

- Added a browser-side `COOKIE_JAR`.
- Send stored cookies back with later requests to the same host.
- Store `Set-Cookie` response headers in the cookie jar.
- Added server-side session tokens and a `SESSIONS` dictionary.
- Added guest book login accounts and a login form.
- Store the logged-in user in server-side session data.
- Only show the guest book posting form to logged-in users.
- Record the username with each guest book entry.
- Added minimal JavaScript `XMLHttpRequest` support.
- Exported `XMLHttpRequest_send` from Python to the JavaScript runtime.
- Added `URL.origin()` and enforce same-origin checks for XHR.
- Added CSRF nonce generation in the guest book form.
- Reject guest book posts with a missing or mismatched nonce.

## Previous chapter recap

- Chapter 9 added the JavaScript runtime bridge, DOM handles, event listeners,
  event cancellation, `innerHTML`, and guest book client-side validation.

## Next to do

- Read and implement SameSite Cookies.
- Parse cookie parameters from `Set-Cookie`.
- Pass request referrer context so the browser can decide when to send
  `SameSite=Lax` cookies.

## Known Issues

- The toy browser stores only one cookie per host.
- Session tokens and nonces use `random.random`, which is not secure enough for
  real applications.
- Each session currently has only one active nonce, so opening two posting forms
  can invalidate the older one.
- Links like `#click-handling` do not scroll within the current page yet.
  This is listed as a later Chapter 7 exercise.
