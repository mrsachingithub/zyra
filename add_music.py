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
        }
    ]

    with app.app_context():
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