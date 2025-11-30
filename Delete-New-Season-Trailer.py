#/bin/python3 /volume2/docker/config/Test.py
#!/usr/bin/env python3
"""
Plex Episode 00 Cleanup Script
Connects to Plex, finds TV shows with "New Season" label,
and deletes episode 00 from the latest season.
"""

from plexapi.server import PlexServer
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Plex server configuration
PLEX_URL = 'http://localhost:32400'  # Change to your Plex server URL
PLEX_TOKEN = 'YOUR_PLEX_TOKEN_HERE'  # Replace with your Plex token

# Script configuration
LABEL_NAME = 'New Season'  # The label to search for on TV shows
REPORT_MODE = False  #True will report only, change to False to actually delete episodes

def get_plex_token_instructions():
    """Print instructions for finding Plex token"""
    print("\nTo find your Plex token:")
    print("1. Sign in to Plex Web App")
    print("2. Play any media item")
    print("3. Click the three dots (...) and select 'Get Info'")
    print("4. Click 'View XML'")
    print("5. Look for 'X-Plex-Token' in the URL")
    print("   Example: ...?X-Plex-Token=YOUR_TOKEN_HERE\n")

def connect_to_plex():
    """Connect to Plex server"""
    try:
        plex = PlexServer(PLEX_URL, PLEX_TOKEN)
        logger.info(f"Connected to Plex server: {plex.friendlyName}")
        return plex
    except Exception as e:
        logger.error(f"Failed to connect to Plex: {e}")
        return None

def find_shows_with_label(plex, label_name):
    """Find all TV shows with the specified label"""
    shows_with_label = []
    
    try:
        # Get all TV show libraries
        for section in plex.library.sections():
            if section.type == 'show':
                logger.info(f"Scanning library: {section.title}")
                
                # Get all shows in this library
                for show in section.all():
                    # Check if show has the target label
                    labels = [label.tag for label in show.labels]
                    if label_name in labels:
                        shows_with_label.append(show)
                        logger.info(f"Found show with '{label_name}' label: {show.title}")
        
        return shows_with_label
    
    except Exception as e:
        logger.error(f"Error finding shows: {e}")
        return []

def delete_episode_00_from_latest_season(show, report_mode=True):
    """Delete episode 00 from the latest season of a show"""
    try:
        # Get all seasons, sorted by season number
        seasons = sorted(show.seasons(), key=lambda s: s.seasonNumber, reverse=True)
        
        if not seasons:
            logger.warning(f"No seasons found for {show.title}")
            return
        
        # Get the latest season (highest season number)
        latest_season = seasons[0]
        logger.info(f"Latest season for {show.title}: Season {latest_season.seasonNumber}")
        
        # Find episode 00 in this season
        for episode in latest_season.episodes():
            if episode.episodeNumber == 0:
                logger.info(f"Found episode 00 in {show.title} - Season {latest_season.seasonNumber}")
                logger.info(f"Episode title: {episode.title}")
                logger.info(f"File path: {episode.media[0].parts[0].file if episode.media else 'Unknown'}")
                
                # Delete the episode only if not in report mode
                if report_mode:
                    logger.info(f"[REPORT MODE] Would delete episode 00 from {show.title} - Season {latest_season.seasonNumber}")
                else:
                    try:
                        episode.delete()
                        logger.info(f"Successfully deleted episode 00 from {show.title} - Season {latest_season.seasonNumber}")
                    except Exception as e:
                        logger.error(f"Failed to delete episode: {e}")
                
                return
        
        logger.info(f"No episode 00 found in latest season of {show.title}")
    
    except Exception as e:
        logger.error(f"Error processing {show.title}: {e}")

def main():
    """Main function"""
    logger.info("Starting Plex Episode 00 Cleanup Script")
    logger.info(f"Looking for shows with label: '{LABEL_NAME}'")
    
    # Log the current mode
    if REPORT_MODE:
        logger.info("*** RUNNING IN REPORT MODE - NO DELETIONS WILL OCCUR ***")
    else:
        logger.warning("*** RUNNING IN DELETE MODE - EPISODES WILL BE DELETED ***")
    
    # Check if token is set
    if PLEX_TOKEN == 'YOUR_PLEX_TOKEN_HERE':
        logger.error("Please set your Plex token in the script")
        get_plex_token_instructions()
        return
    
    # Connect to Plex
    plex = connect_to_plex()
    if not plex:
        return
    
    # Find shows with the specified label
    shows = find_shows_with_label(plex, LABEL_NAME)
    
    if not shows:
        logger.info(f"No shows found with '{LABEL_NAME}' label")
        return
    
    logger.info(f"Found {len(shows)} show(s) with '{LABEL_NAME}' label")
    
    # Process each show
    for show in shows:
        logger.info(f"\nProcessing: {show.title}")
        delete_episode_00_from_latest_season(show, REPORT_MODE)
    
    logger.info("\nScript completed")
    if REPORT_MODE:
        logger.info("To actually delete episodes, set REPORT_MODE = False in the script")

if __name__ == "__main__":
    main()
