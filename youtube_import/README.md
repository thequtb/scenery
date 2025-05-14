# YouTube to Odoo eLearning Importer

This module imports YouTube playlists from a specified channel directly into Odoo's eLearning module as courses.

## Requirements

- Python 3.6+
- Odoo with eLearning module installed
- PostgreSQL database access
- YouTube Data API v3 key

## Installation

1. Install required packages using requirements.txt:

```bash
pip install -r requirements.txt
```

2. Update the `conf.py` file with your YouTube API key and database connection settings.

## Features

- Imports all playlists from a YouTube channel as Odoo eLearning courses with their videos
- Import a single playlist as an Odoo eLearning course with all its videos
- Each video in a playlist becomes a slide in the course
- Uses bulk database operations for efficient video imports
- Handles YouTube API pagination for large playlists
- Detailed logging

## Usage

### Import an entire channel:

```bash
# Run as a module (recommended)
python -m youtube_import.youtube --channel "Channel Name"

# Or run the script directly
python youtube_import/youtube.py --channel "Channel Name"
```

This creates courses for each playlist and adds all videos as slides in a single bulk operation.

Or with a specific channel ID:

```bash
python -m youtube_import.youtube --channel "UCxxxxxxxxx"
```

### Import a single playlist:

```bash
python -m youtube_import.youtube --playlist "PLxxxxxxxx"
```

This creates a course and adds all videos from the playlist in a single bulk operation.

You can also specify an API key directly:

```bash
python -m youtube_import.youtube --channel "Channel Name" --api-key "YOUR_API_KEY"
```

### Finding a Playlist ID

To get a YouTube playlist ID:

1. Open the playlist in YouTube
2. Look at the URL in your browser: `https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxx`
3. The part after `list=` is your playlist ID (always starts with "PL")

## Odoo Database Tables

This module interacts with the following Odoo eLearning tables:

1. `slide_channel` - For courses (from YouTube playlists)
2. `slide_slide` - For slides (from YouTube videos)

No table creation is needed as these are standard Odoo eLearning module tables.

## Technical Notes

- Uses direct SQL connections to the Odoo database for better performance
- Uses bulk database operations to efficiently insert all videos at once
- Creates courses with public visibility by default
- Sets each video as a 'video' type slide in Odoo
- Preserves video sequence from YouTube playlist
- Course URL is generated from the playlist title