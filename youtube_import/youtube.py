"""
YouTube API Client for importing playlists as Odoo eLearning courses
"""

import os
import googleapiclient.discovery
import googleapiclient.errors
import logging
import argparse
from datetime import datetime
import sys
import os

# Handle imports whether run as a module or directly as a script
if __name__ == "__main__":
    # When run directly, use absolute imports
    sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    import youtube_import.conf as conf
    from youtube_import.db_client import DBClient
else:
    # When imported as a module, use relative imports
    from . import conf
    from .db_client import DBClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=getattr(logging, conf.LOG_LEVEL))

class YouTubeImporter:
    """Client for importing YouTube playlists as Odoo eLearning courses"""
    
    def __init__(self, api_key=None):
        """Initialize YouTube API client"""
        self.api_key = api_key or conf.YOUTUBE_API_KEY
        self.youtube = None
        self.db_client = DBClient()
        
    def connect(self):
        """Connect to YouTube API and database"""
        try:
            # YouTube API setup
            api_service_name = "youtube"
            api_version = "v3"
            self.youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey=self.api_key)
            logger.info("Connected to YouTube API")
            
            # Connect to database
            if not self.db_client.connect():
                logger.error("Failed to connect to database")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to YouTube API: {str(e)}")
            return False
    
    def get_channel_id(self, channel_name_or_id):
        """Get channel ID from channel name or ID"""
        if not self.youtube:
            if not self.connect():
                return None
        
        # Check if input is already a channel ID
        if channel_name_or_id.startswith('UC'):
            return channel_name_or_id
            
        try:
            # Search for channel by name
            request = self.youtube.search().list(
                part="snippet",
                q=channel_name_or_id,
                type="channel",
                maxResults=1
            )
            response = request.execute()
            
            if not response.get('items'):
                logger.error(f"No channel found for: {channel_name_or_id}")
                return None
                
            return response['items'][0]['id']['channelId']
            
        except Exception as e:
            logger.error(f"Error getting channel ID: {str(e)}")
            return None
    
    def get_playlist_details(self, playlist_id):
        """Get details for a specific playlist by ID"""
        if not self.youtube:
            if not self.connect():
                return None
        
        try:
            request = self.youtube.playlists().list(
                part="snippet,contentDetails",
                id=playlist_id,
                maxResults=1
            )
            response = request.execute()
            
            if not response.get('items'):
                logger.error(f"No playlist found with ID: {playlist_id}")
                return None
                
            return response['items'][0]
            
        except Exception as e:
            logger.error(f"Error getting playlist details: {str(e)}")
            return None
    
    def get_channel_playlists(self, channel_id):
        """Get all playlists for a channel"""
        if not self.youtube:
            if not self.connect():
                return []
                
        try:
            playlists = []
            next_page_token = None
            
            while True:
                request = self.youtube.playlists().list(
                    part="snippet,contentDetails",
                    channelId=channel_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                playlists.extend(response.get('items', []))
                next_page_token = response.get('nextPageToken')
                
                if not next_page_token:
                    break
                    
            logger.info(f"Found {len(playlists)} playlists for channel {channel_id}")
            return playlists
            
        except Exception as e:
            logger.error(f"Error getting channel playlists: {str(e)}")
            return []
    
    def get_playlist_videos(self, playlist_id):
        """Get all videos in a playlist"""
        if not self.youtube:
            if not self.connect():
                return []
                
        try:
            videos = []
            next_page_token = None
            
            while True:
                request = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                videos.extend(response.get('items', []))
                next_page_token = response.get('nextPageToken')
                
                if not next_page_token:
                    break
                    
            logger.info(f"Found {len(videos)} videos in playlist {playlist_id}")
            return videos
            
        except Exception as e:
            logger.error(f"Error getting playlist videos: {str(e)}")
            return []
    
    def import_playlist_as_course(self, playlist):
        """Import a playlist as an Odoo eLearning course with all its videos using bulk insert"""
        
        # Create course data from playlist
        playlist_data = {
            'youtube_id': playlist['id'],
            'title': playlist['snippet']['title'],
            'description': playlist['snippet']['description']
        }
        
        # Create the course
        course_id = self.db_client.create_course(playlist_data)
        if not course_id:
            logger.error(f"Failed to create course for playlist: {playlist['id']}")
            return None
            
        # Get videos from the playlist
        videos = self.get_playlist_videos(playlist['id'])
        if not videos:
            logger.warning(f"No videos found in playlist: {playlist['id']}")
            return course_id
        
        # Prepare video data for bulk insert
        video_data_list = []
        for video in videos:
            snippet = video['snippet']
            content_details = video['contentDetails']
            
            video_data = {
                'youtube_id': content_details['videoId'],
                'title': snippet['title'],
                'description': snippet['description'],
                'position': snippet['position'],
                'course_id': course_id
            }
            video_data_list.append(video_data)
        
        # Bulk insert all videos
        slides_created = self.db_client.create_slides_bulk(video_data_list)
        logger.info(f"Bulk imported {slides_created} videos for playlist {playlist['id']} as course with ID {course_id}")
        
        return course_id
    
    def import_single_playlist(self, playlist_id):
        """Import a single playlist as an Odoo eLearning course"""
        logger.info(f"Importing single playlist: {playlist_id}")
        
        # Get playlist details
        playlist = self.get_playlist_details(playlist_id)
        if not playlist:
            logger.error(f"Failed to get details for playlist: {playlist_id}")
            return False
            
        # Import the playlist as a course
        course_id = self.import_playlist_as_course(playlist)
        return course_id is not None
    
    def import_channel(self, channel_name_or_id):
        """Import all playlists from a channel as Odoo eLearning courses"""
        channel_id = self.get_channel_id(channel_name_or_id)
        if not channel_id:
            logger.error(f"Could not find channel ID for: {channel_name_or_id}")
            return False
            
        logger.info(f"Importing channel: {channel_id}")
        
        # Get all playlists
        playlists = self.get_channel_playlists(channel_id)
        if not playlists:
            logger.warning(f"No playlists found for channel: {channel_id}")
            return False
            
        # Import each playlist as a course
        courses_created = 0
        for playlist in playlists:
            course_id = self.import_playlist_as_course(playlist)
            if course_id:
                courses_created += 1
                
        logger.info(f"Imported {courses_created} courses from channel {channel_id}")
        return courses_created > 0
    
    def cleanup(self):
        """Clean up connections"""
        self.db_client.disconnect()
        logger.info("Cleanup complete")

def main():
    parser = argparse.ArgumentParser(description='Import YouTube playlists as Odoo eLearning courses')
    
    # Create argument groups
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--channel', help='Channel name or ID to import')
    action_group.add_argument('--playlist', help='Playlist ID to import as a course with all videos')
    
    # API key option
    parser.add_argument('--api-key', help='YouTube API key (overrides config)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize the importer
    importer = YouTubeImporter(api_key=args.api_key)
    
    try:
        if not importer.connect():
            logger.error("Failed to connect. Aborting import.")
            return 1
            
        # Process based on selected action
        if args.channel:
            success = importer.import_channel(args.channel)
            
        elif args.playlist:
            success = importer.import_single_playlist(args.playlist)
            
        else:
            logger.error("No action specified")
            return 1
            
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.info("Operation canceled by user")
        return 1
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1
        
    finally:
        importer.cleanup()

if __name__ == "__main__":
    sys.exit(main())