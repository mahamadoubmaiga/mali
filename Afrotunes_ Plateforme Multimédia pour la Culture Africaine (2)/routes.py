from flask import render_template, session, redirect, url_for, make_response, request
from functools import wraps
from app_init import app, db
from translations import translations
from models.music import Artist, Album, Track
from models.video import Video

def with_sidebar(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return render_template(f.__name__.replace('_route', '.html'), with_sidebar=True)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user', {}).get('is_admin'):
            return redirect(url_for('landing_route'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def landing_route():
    lang = session.get('lang', 'en')
    return render_template("landing.html", with_sidebar=False, translations=translations[lang])

@app.route("/change-language/<lang>")
def change_language(lang):
    if lang in translations:
        session['lang'] = lang
    return redirect(request.referrer or url_for('landing_route'))

@app.route("/profile")
def profile_route():
    return render_template("profile.html", with_sidebar=True)

@app.route("/music")
def music_route():
    artists = Artist.query.all()
    return render_template("music.html", with_sidebar=True, artists=artists)

@app.route("/videos")
def videos_route():
    videos = Video.query.all()
    return render_template("videos.html", with_sidebar=True, videos=videos)

@app.route("/admin")
@admin_required
def admin_route():
    return render_template("admin.html", with_sidebar=True)

@app.route("/admin/add-artist", methods=['POST'])
@admin_required
def admin_add_artist():
    name = request.form.get('name')
    genre = request.form.get('genre')
    description = request.form.get('description')
    image_url = request.form.get('image_url')
    
    artist = Artist(name=name, genre=genre, description=description, image_url=image_url)
    db.session.add(artist)
    db.session.commit()
    
    return redirect(url_for('admin_route'))

@app.route("/admin/add-video", methods=['POST'])
@admin_required
def admin_add_video():
    title = request.form.get('title')
    description = request.form.get('description')
    video_url = request.form.get('video_url')
    genre = request.form.get('genre')
    thumbnail_url = request.form.get('thumbnail_url')
    
    video = Video(title=title, description=description, video_url=video_url,
                  genre=genre, thumbnail_url=thumbnail_url)
    db.session.add(video)
    db.session.commit()
    
    return redirect(url_for('admin_route'))

@app.route("/logout", methods=['POST'])
def logout_route():
    session.clear()
    return redirect(url_for('landing_route'))