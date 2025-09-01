# relic

Problem: 
I write and save so many notes and random links all around my devices - phone, laptop, desktop - across different platforms (browser bookmarks, Telegram Saved Messages, Obsidian, Teams Drafts, Journals). Half the time I don't remember the content I've saved.

Solution:
A living knowledge base that knows what I've saved, when I save it, and why I saved it in context of what I was currently doing at the time.

Tech:

Fusion of 2 types of data:
- Active notarization - I specifically chose to write about/ save this piece of content.
- Passive context - I was looking at these X other tabs at work/ home when I decided to create a note.

Data producers exist on the device-side. These "collectors" are installed or accessed per device.
- Webapp for quickloggings
- Browser extension for tracking passive context

## Implementation

- [x] Prepared webapp for quicklogging with auth
- [x] Prepared backend self-hosted server for receiving data event across internet
- [x] 

## Usage
Run using

    docker-compose down --volumes --remove-orphans && docker-compose up --build

Visit `http://localhost:8080/` - enter client_id and api_key set in `.env`

 
 Run the server side consumer (hub) on local script for testing

    uv run core/pipeline/main.py --network localhost