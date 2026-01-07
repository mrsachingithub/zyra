from app import create_app, db
from app.models import Music

app = create_app()

def add_music_tracks():
    tracks_to_add = [
        # User's English Tracks
        {
            'title': 'Stay', 'artist': 'The Kid LAROI & Justin Bieber', 
            'album': 'F*CK LOVE 3', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3',
            'cover_image': 'https://i.scdn.co/image/ab67616d0000b27341e31f6ea1d493dd77933ee5', 'is_premium': False
        },
        {
            'title': 'Circles', 'artist': 'Post Malone', 
            'album': 'Hollywood\'s Bleeding', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3',
            'cover_image': 'https://i.scdn.co/image/ab67616d0000b2739477c38533c0d5016e54ae29', 'is_premium': True
        },
        {
            'title': 'Love and Obsession', 'artist': 'Post Malone', 
            'album': 'International', 'url': 'https://drive.google.com/uc?export=download&id=1eHGAFYYWRl7VdwT9MfViFG0kxRCLLc7F',
            'cover_image': 'https://drive.google.com/uc?export=download&id=1JoDZ_Mqcpp_Kwu3oV8M447FyZCv_xr1B','is_premium': False
        },
        
        # 10 Hindi Songs
        {
            'title': 'Kesariya', 'artist': 'Arijit Singh', 
            'album': 'Brahmastra', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3',
            'cover_image': 'https://c.saavncdn.com/191/Kesariya-From-Brahmastra-Hindi-2022-20220717092820-500x500.jpg', 'is_premium': False, 'genre': 'Bollywood'
        },
        {
            'title': 'Raataan Lambiyan', 'artist': 'Jubin Nautiyal', 
            'album': 'Shershaah', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3',
            'cover_image': 'https://c.saavncdn.com/238/Shershaah-Hindi-2021-20210815121207-500x500.jpg', 'is_premium': True, 'genre': 'Bollywood'
        },
        {
            'title': 'Tum Hi Ho', 'artist': 'Arijit Singh', 
            'album': 'Aashiqui 2', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3',
            'cover_image': 'https://c.saavncdn.com/662/Aashiqui-2-Hindi-2013-500x500.jpg', 'is_premium': False, 'genre': 'Bollywood'
        },
        {
            'title': 'Kabira', 'artist': 'Tochi Raina', 
            'album': 'Yeh Jawaani Hai Deewani', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-13.mp3',
            'cover_image': 'https://c.saavncdn.com/001/Yeh-Jawaani-Hai-Deewani-Hindi-2013-500x500.jpg', 'is_premium': False, 'genre': 'Bollywood'
        },
        {
            'title': 'Apna Time Aayega', 'artist': 'Ranveer Singh', 
            'album': 'Gully Boy', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3',
            'cover_image': 'https://c.saavncdn.com/807/Gully-Boy-Hindi-2019-20190124151325-500x500.jpg', 'is_premium': True, 'genre': 'Hip Hop'
        },
        {
            'title': 'Dilbar', 'artist': 'Neha Kakkar', 
            'album': 'Satyameva Jayate', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3',
            'cover_image': 'https://c.saavncdn.com/202/Satyameva-Jayate-Hindi-2018-20180801-500x500.jpg', 'is_premium': False, 'genre': 'Dance'
        },
        {
            'title': 'Pasoori', 'artist': 'Ali Sethi', 
            'album': 'Coke Studio 14', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-16.mp3',
            'cover_image': 'https://c.saavncdn.com/152/Pasoori-Punjabi-2022-20220202153549-500x500.jpg', 'is_premium': False, 'genre': 'Indie'
        },
        {
            'title': 'Ranjha', 'artist': 'B Praak', 
            'album': 'Shershaah', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
            'cover_image': 'https://c.saavncdn.com/238/Shershaah-Hindi-2021-20210815121207-500x500.jpg', 'is_premium': True, 'genre': 'Bollywood'
        },
        {
            'title': 'Zaalima', 'artist': 'Arijit Singh', 
            'album': 'Raees', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
            'cover_image': 'https://c.saavncdn.com/004/Raees-Hindi-2017-500x500.jpg', 'is_premium': False, 'genre': 'Bollywood'
        },
        {
            'title': 'Chaiyya Chaiyya', 'artist': 'Sukhwinder Singh', 
            'album': 'Dil Se', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
            'cover_image': 'https://c.saavncdn.com/492/Dil-Se-Hindi-1998-20190603125213-500x500.jpg', 'is_premium': False, 'genre': 'Bollywood'
        },
        {
            'title': 'Chaleya', 'artist': 'Arijit Singh', 
            'album': 'Jawan', 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3',
            'cover_image': 'https://c.saavncdn.com/026/Chaleya-From-Jawan-Hindi-2023-20230814104054-500x500.jpg', 'is_premium': False, 'genre': 'Bollywood'
        }
    ]

    with app.app_context():
        # Scan local static/music directory
        import os
        import random
        from mutagen import File
        from mutagen.id3 import ID3, APIC
        
        local_music_dir = os.path.join(os.getcwd(), 'static', 'music')
        covers_dir = os.path.join(os.getcwd(), 'static', 'covers')
        if not os.path.exists(covers_dir):
            os.makedirs(covers_dir)

        if os.path.exists(local_music_dir):
            for filename in os.listdir(local_music_dir):
                if filename.lower().endswith(('.mp3', '.wav', '.ogg')):
                    file_path = os.path.join(local_music_dir, filename)
                    
                    # 1. Parse Filename: Title_-_Artist.mp3
                    # Replace underscores with spaces
                    clean_name = os.path.splitext(filename)[0]
                    
                    title = clean_name
                    artist = "Unknown Artist"
                    
                    if '_-_' in clean_name:
                        parts = clean_name.split('_-_', 1)
                        title = parts[0].replace('_', ' ').strip()
                        artist = parts[1].replace('_', ' ').strip()
                    else:
                        # Fallback if no separator found, just replace underscores
                        title = clean_name.replace('_', ' ')

                    # 2. Extract Embedded Cover Art using Mutagen
                    cover_image_url = 'https://placehold.co/500x500?text=Music' # Default
                    
                    try:
                        audio = File(file_path)
                        if audio and audio.tags:
                            # Look for APIC frame (ID3v2)
                            for tag in audio.tags.values():
                                if isinstance(tag, APIC):
                                    image_data = tag.data
                                    mime = tag.mime
                                    ext = 'jpg' if 'jpeg' in mime else 'png'
                                    
                                    # Create safe filename for cover
                                    safe_title = "".join(x for x in title if x.isalnum())
                                    cover_filename = f"{safe_title}_{int(os.path.getmtime(file_path))}.{ext}"
                                    cover_path = os.path.join(covers_dir, cover_filename)
                                    
                                    with open(cover_path, 'wb') as img_file:
                                        img_file.write(image_data)
                                    
                                    cover_image_url = f'/static/covers/{cover_filename}'
                                    # print(f"Extracted cover for {filename}")
                                    break
                    except Exception as e:
                        print(f"Could not extract metadata for {filename}: {e}")

                    # URL for static file
                    url = f'/static/music/{filename}'
                    
                    # Random Premium Status (approx 30% chance)
                    is_premium = random.choice([True, False, False])

                    tracks_to_add.append({
                        'title': title,
                        'artist': artist,
                        'album': 'Local Uploads',
                        'url': url,
                        'cover_image': cover_image_url,
                        'is_premium': is_premium,
                        'genre': 'Local'
                    })
                    print(f"Found local file: {title} by {artist} (Premium: {is_premium})")

        added_count = 0
        for track_data in tracks_to_add:
            # Check if track already exists by title and artist
            exists = Music.query.filter_by(
                title=track_data['title'], 
                artist=track_data['artist']
            ).first()

            if not exists:
                new_music = Music(
                    title=track_data['title'],
                    artist=track_data['artist'],
                    album=track_data.get('album'),
                    url=track_data['url'],
                    cover_image=track_data.get('cover_image'),
                    is_premium=track_data.get('is_premium', False),
                    genre=track_data.get('genre')
                )
                db.session.add(new_music)
                added_count += 1
                print(f"Added: {track_data['title']} by {track_data['artist']}")
        
        if added_count > 0:
            db.session.commit()
            print(f"Successfully added {added_count} new tracks.")
        else:
            print("No new tracks were added (all tracks already exist).")

if __name__ == '__main__':
    print("Starting music update...")
    add_music_tracks()
    print("Done.")