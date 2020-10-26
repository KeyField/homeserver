
# KeyField Homeserver

KeyField reference Homeserver

## What is a Homeserver?

The KeyField homeserver provides the same functions that other chat services provide: it relays information between users and stores long-term data so that each client device doesn't need to store an entire copy of history.

Notably a homeserver is a user's primary method for ensuring information reaches that user. When a user chooses or hosts their own homeserver they are trusting that server only enough to make it's best effort to send messages where they need to go.

The homeserver does this by relaying content between it's users, or if the users are on different homeservers then the federation comes into play and the user's homeserver will try as hard as it can to deliver the message to the other user's homeserver.

## How does it work?

This homeserver implementation is written in Python using Flask and MongoDB (MongoEngine).

It operates entirely over HTTP methods in order to make it as accessible to clients and users as possible. Using the standard transport allows servers to employ common reverse proxies and existing high-availability systems.

## Project Status

Pre-production, nothing here is complete yet, it's mostly scaffolding and hacks until the v1 API is finalized.

### Is it any good?

No, not yet.
