# Instagram Stealth Browser Scraper

## Overview

This module implements a stealth scraping system using a real browser.

Instead of reverse-engineering APIs, it simulates an actual human browsing Instagram.
The scraper runs a real Chrome instance with stored login cookies and extracts data from the rendered page DOM.

This approach bypasses:

* API blocks
* GraphQL restrictions
* missing bio issues
* soft limits

---

## Core Principle

Instagram trusts **behavior**, not requests.

So this scraper does:
Human behavior → Real rendering → DOM extraction

Not:
Direct HTTP → Blocked API → Missing data

---

## Architecture

### Flow

1. Launch undetected Chrome browser
2. Load saved login cookies
3. Open profile/post page
4. Wait for React hydration
5. Extract rendered data
6. Store timestamp snapshot

---

## Modules

### Browser Controller

Creates stealth browser instance with automation fingerprints removed.

```
stealth_browser/browser.py
```

Uses:

* undetected_chromedriver
* real Chrome profile
* anti-automation flags

---

### Login Manager

User logs in manually once.
Cookies saved for future automated sessions.

```
stealth_browser/login.py
stealth_browser/session_cookies.json
```

---

### Cookie Loader

Injects saved authenticated session into browser.

```
stealth_browser/cookie_store.py
```

---

### Profile Scraper

Extracts:

* followers
* following
* posts
* bio

From rendered DOM after page load.

```
stealth_browser/profile_scraper.py
```

---

### Post Scraper

Extracts:

* caption
* likes
* comments
* media

```
stealth_browser/post_scraper.py
```

---

## Data Storage

Snapshots stored chronologically:

```
data/
   profiles/<username>/<timestamp>.json
   posts/<shortcode>/<timestamp>.json
```

This creates a historical dataset.

---

## Advantages

* Works on private UI-protected fields
* Stable against API changes
* Retrieves fully rendered data
* Bio and dynamic elements available
* Closest to real user behavior

---

## Limitations

* Slower than HTTP scraper
* Requires logged-in account
* Requires Chrome installation

---

## Use Cases

* social analytics dataset
* engagement tracking
* growth monitoring
* influencer research
* OSINT learning

---

## Important Note

The browser only reads publicly visible information visible to a logged-in user.
No security protections are bypassed.

---

## Recommended Usage

Run periodically to build historical datasets:

Example:

```
python main.py --file input/urls.txt
```

---

## Summary

HTTP Scraper → reverse engineering
Stealth Scraper → behavior simulation

Both together create a resilient multi-layer scraping system.
