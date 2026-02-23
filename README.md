# Instagram HTTP Request Scraper

## Overview

This module implements a low-level Instagram scraper using direct HTTP requests and reverse-engineered web APIs.

Instead of using a browser, it mimics how the Instagram web client communicates with backend services (Bootstrap + GraphQL + fallback HTML parsing).

The scraper extracts public profile and post data while attempting to behave like a real user through rotating identities, headers, and rate-control logic.

---

## Architecture

### Flow

1. Load identity (cookies, headers, proxy)
2. Fetch Bootstrap HTML page
3. Extract tokens (csrftoken, lsd, user_id)
4. Call internal GraphQL endpoints
5. Parse JSON response
6. Fallback to HTML/meta parsing if blocked
7. Store snapshot

---

## Components

### Token Extraction

Extracts dynamic session tokens required for authenticated GraphQL queries.

* csrftoken
* lsd token
* user_id

File:

```
client/token_extractor.py
```

---

### GraphQL Client

Sends internal Instagram queries such as:

* PolarisPostActionLoadPostQuery
* PolarisProfilePageContentQuery
* HoverCard queries

File:

```
client/graphql_client.py
```

---

### Identity Pool

Simulates multiple human users to avoid rate-limit detection.

Features:

* identity rotation
* scheduling (wake/sleep hours)
* health tracking
* failover retries

Files:

```
identity_pool/
```

---

### Failover Executor

Retries failed requests with different identities.

```
failover_executor.py
```

---

### HTML Fallback Parsers

When GraphQL is blocked, scraper extracts data from:

* bootstrap JSON
* meta tags
* structured HTML

Files:

```
parsers/profile_parser.py
parsers/post_parser.py
```

---

## Data Collected

### Profile

* username
* followers
* following
* posts
* bio (if available)
* category
* verification
* privacy status

### Post

* shortcode
* username
* caption
* likes
* comments
* media type
* media url

---

## Storage

Snapshots are saved chronologically:

```
data/
   profiles/<username>/<timestamp>.json
   posts/<shortcode>/<timestamp>.json
```

This enables historical tracking instead of overwriting data.

---

## Limitations

* Soft blocks possible
* Bio sometimes missing
* Requires fallback parsing
* Instagram changes API frequently

---

## Purpose

This scraper is designed for:

* learning reverse engineering
* understanding web client behavior
* building resilient scraping architecture
* collecting public analytics data

---

## Disclaimer

Only public data is collected.
No login bypassing or private data extraction is performed.
