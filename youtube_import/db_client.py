"""
Database Client for YouTube to Odoo eLearning import using direct SQL connection
"""

import psycopg2
import psycopg2.extras
import logging
import sys
import os
import json

# Handle imports whether run as a module or directly as a script
if __name__ == "__main__":
    # When run directly, use absolute imports
    sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    import youtube_import.conf as conf
else:
    # When imported as a module, use relative imports
    from . import conf

logger = logging.getLogger(__name__)
logging.basicConfig(level=getattr(logging, conf.LOG_LEVEL))

class DBClient:
    """Client for interacting with Odoo eLearning via direct SQL queries"""
    
    def __init__(self, host=None, port=None, db=None, user=None, password=None):
        """Initialize database connection parameters"""
        self.host = host or conf.ODOO.get("host", "localhost")
        self.port = port or conf.ODOO.get("port", 5432)
        self.db = db or conf.ODOO.get("db")
        self.user = user or conf.ODOO.get("username")
        self.password = password or conf.ODOO.get("password")
        self.conn = None
        self.cursor = None
        self.default_lang = conf.DEFAULT_LANG
        
    def connect(self):
        """Establish connection to the database"""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.db,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            logger.info(f"Connected to database {self.db}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            return False
    
    def disconnect(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Disconnected from database")
    
    def execute_query(self, query, params=None):
        """Execute a SQL query with parameters"""
        if not self.conn or self.conn.closed:
            if not self.connect():
                return False
        
        try:
            self.cursor.execute(query, params or ())
            return True
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            self.conn.rollback()
            return False
    
    def fetch_all(self, query, params=None):
        """Execute a query and fetch all results"""
        if not self.execute_query(query, params):
            return []
        
        try:
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Fetch error: {str(e)}")
            return []
    
    def fetch_one(self, query, params=None):
        """Execute a query and fetch one result"""
        if not self.execute_query(query, params):
            return None
        
        try:
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Fetch error: {str(e)}")
            return None
    
    def commit(self):
        """Commit the current transaction"""
        if self.conn and not self.conn.closed:
            self.conn.commit()
    
    def format_multilang_field(self, text):
        """Format text as a JSON object for multilingual fields"""
        return json.dumps({self.default_lang: text})
    
    def check_if_course_exists(self, youtube_id):
        """Check if a course with this YouTube playlist ID already exists"""
        query = f"""
            SELECT id FROM {conf.SLIDE_CHANNEL_TABLE}
            WHERE source_id = %s
        """
        result = self.fetch_one(query, (youtube_id,))
        return result['id'] if result else None
    
    def check_course_exists(self, course_id):
        """Check if a course exists by its ID"""
        query = f"""
            SELECT id FROM {conf.SLIDE_CHANNEL_TABLE}
            WHERE id = %s
        """
        result = self.fetch_one(query, (course_id,))
        return result is not None
    
    def create_course(self, playlist_data):
        """Create a new course from YouTube playlist data"""
        # Prepare course data
        current_timestamp = 'NOW()'
        
        # Format multilingual fields as JSON
        name_json = self.format_multilang_field(playlist_data['title'])
        description_json = self.format_multilang_field(playlist_data['description'])
        
        query = f"""
            INSERT INTO {conf.SLIDE_CHANNEL_TABLE} (
                name,
                description,
                create_date,
                write_date,
                is_published,
                visibility,
                channel_type,
                enroll
            ) VALUES (
                %s, %s, {current_timestamp}, {current_timestamp}, true, 'public', 'training', 'public'
            )
            RETURNING id
        """
        
        params = (
            name_json,
            description_json
        )
        
        if self.execute_query(query, params):
            course_id = self.cursor.fetchone()[0]
            self.commit()
            logger.info(f"Created new course with ID {course_id}")
            return course_id
        return None
    
    def create_slide(self, video_data, course_id):
        """Create a new slide from YouTube video data"""
        current_timestamp = 'NOW()'
        
        # Format multilingual fields as JSON
        name_json = self.format_multilang_field(video_data['title'])
        description_json = self.format_multilang_field(video_data['description'])
        
        # YouTube URL format
        video_url = f"https://www.youtube.com/watch?v={video_data['youtube_id']}"
        
        query = f"""
            INSERT INTO {conf.SLIDE_SLIDE_TABLE} (
                name,
                description,
                channel_id,
                create_date,
                write_date,
                is_published,
                slide_category,
                url,
                sequence,
                source_type
            ) VALUES (
                %s, %s, %s, {current_timestamp}, {current_timestamp}, true, 'video', %s, %s, 'local_file'
            )
            RETURNING id
        """
        
        params = (
            name_json,
            description_json,
            course_id,
            video_url,
            video_data['position']
        )
        
        if self.execute_query(query, params):
            slide_id = self.cursor.fetchone()[0]
            self.commit()
            logger.info(f"Created new slide with ID {slide_id}")
            return slide_id
        return None
    
    def create_slides_bulk(self, video_data_list):
        """Create multiple slides in a single database transaction"""
        if not video_data_list:
            return 0
            
        current_timestamp = 'NOW()'
        slides_created = 0
        
        try:
            # Start a transaction
            if not self.conn or self.conn.closed:
                if not self.connect():
                    return 0
                    
            # Prepare the bulk insert query
            query = f"""
                INSERT INTO {conf.SLIDE_SLIDE_TABLE} (
                    name,
                    description,
                    channel_id,
                    create_date,
                    write_date,
                    is_published,
                    slide_category,
                    url,
                    sequence,
                    source_type
                ) VALUES %s
                RETURNING id
            """
            
            # Prepare the values for bulk insert
            value_tuples = []
            template = f"(%s, %s, %s, {current_timestamp}, {current_timestamp}, true, 'video', %s, %s, 'local_file')"
            
            for video in video_data_list:
                # Format multilingual fields as JSON
                name_json = self.format_multilang_field(video['title'])
                description_json = self.format_multilang_field(video['description'])
                
                # YouTube URL format
                video_url = f"https://www.youtube.com/watch?v={video['youtube_id']}"
                
                value_tuples.append((
                    name_json, 
                    description_json,
                    video['course_id'],
                    video_url,
                    video['position']
                ))
            
            # Execute the bulk insert with psycopg2's execute_values
            from psycopg2.extras import execute_values
            execute_values(
                self.cursor, 
                query, 
                value_tuples,
                template=template,
                page_size=100  # Process in batches of 100
            )
            
            # Get the number of rows affected
            slides_created = len(self.cursor.fetchall())
            
            # Commit the transaction
            self.commit()
            logger.info(f"Bulk created {slides_created} slides in a single transaction")
            
            return slides_created
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error during bulk insert: {str(e)}")
            return 0