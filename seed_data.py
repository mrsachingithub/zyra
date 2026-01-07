from app import create_app, db
from app.models import User, Plan, Music
from werkzeug.security import generate_password_hash
import os

app = create_app()

def seed():
    with app.app_context():
        # db.drop_all() and db.create_all() are REMOVED.
        # We rely on Flask-Migrate for table creation.
        # This script now only adds data if it's missing (Safe to run on every deploy).
        
        # 1. Plans
        if not Plan.query.first():
            plans = [
                Plan(name='Free', price=0, duration_days=30, features='Shuffle Play'),
                Plan(name='Premium', price=119, duration_days=30, features='Ad-free, High Quality, Offline'),
                Plan(name='Family', price=179, duration_days=30, features='6 Accounts, Block Explicit')
            ]
            db.session.bulk_save_objects(plans)
            print("Plans created.")

        # 2. Admin User
        if not User.query.filter_by(username='admin').first():
            admin_pwd = os.environ.get('ADMIN_PASSWORD', 'admin123') # Fallback for local dev if not set
            admin = User(username='admin', email='admin@zyra.com', role='admin')
            admin.set_password(admin_pwd)
            db.session.add(admin)
            print(f"Admin user created (admin/{'*' * len(admin_pwd)}).")

        # 3. Music
        if not Music.query.first():
            music_list = [
                Music(title='Midnight City', artist='M83', album='Hurry Up, We\'re Dreaming', 
                      url='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3', 
                      cover_image='https://i.scdn.co/image/ab67616d0000b273295966a34dc236528d259837', is_premium=True),
                Music(title='Blinding Lights', artist='The Weeknd', album='After Hours', 
                      url='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3', 
                      cover_image='https://i.scdn.co/image/ab67616d0000b2738863bc11d2aa12b54f5aeb36', is_premium=True),
                Music(title='Levitating', artist='Dua Lipa', album='Future Nostalgia', 
                      url='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3', 
                      cover_image='https://i.scdn.co/image/ab67616d0000b273bd26ede1ae69327010d49946', is_premium=False),
                Music(title='Heat Waves', artist='Glass Animals', album='Dreamland', 
                      url='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3', 
                      cover_image='https://i.scdn.co/image/ab67616d0000b273974d9ec55bdf47a1dfa151b6', is_premium=False),
                Music(title='Love and Obsession', artist='Post Malone', album='International', 
                      url='https://drive.google.com/uc?export=download&id=1eHGAFYYWRl7VdwT9MfViFG0kxRCLLc7F', 
                      cover_image='https://drive.google.com/uc?export=download&id=1JoDZ_Mqcpp_Kwu3oV8M447FyZCv_xr1B', is_premium=False)      
            ]
            db.session.bulk_save_objects(music_list)
            print("Music tracks added.")
            
        db.session.commit()
        print("Seeding complete.")

if __name__ == '__main__':
    seed()
