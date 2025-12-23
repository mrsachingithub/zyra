from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Music, Plan, Subscription, Payment
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/login')
def login_page():
    return render_template('login.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/api/music', methods=['GET'])
@jwt_required()
def get_music():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check subscription
    is_premium = False
    if user.subscription and user.subscription.is_active:
        is_premium = True
    
    # Filter music based on subscription
    if is_premium:
        music_list = Music.query.all()
    else:
        music_list = Music.query.filter_by(is_premium=False).all()
        
    return jsonify([m.to_dict() for m in music_list])

@main_bp.route('/api/plans', methods=['GET'])
def get_plans():
    plans = Plan.query.all()
    return jsonify([p.to_dict() for p in plans])

@main_bp.route('/api/subscribe', methods=['POST'])
@jwt_required()
def subscribe():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    plan_id = data.get('plan_id')
    
    user = User.query.get(current_user_id)
    plan = Plan.query.get(plan_id)
    
    if not plan:
        return jsonify({'error': 'Plan not found'}), 404
        
    # Create Payment Record
    payment = Payment(
        user_id=user.id,
        plan_id=plan.id,
        amount=plan.price,
        currency='INR',
        status='completed'
    )
    db.session.add(payment)

    # Create or update subscription
    if user.subscription:
        sub = user.subscription
        sub.plan_id = plan.id
        sub.start_date = datetime.utcnow()
        sub.end_date = datetime.utcnow() + timedelta(days=plan.duration_days)
        sub.status = 'active'
    else:
        sub = Subscription(
            user_id=user.id,
            plan_id=plan.id,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=plan.duration_days),
            status='active'
        )
        db.session.add(sub)
    
    db.session.commit()
    
    return jsonify({'message': f'Subscribed to {plan.name} successfully', 'subscription': sub.to_dict()})

@main_bp.route('/api/search', methods=['GET'])
def search_music():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    # Case insensitive search
    results = Music.query.filter(
        (Music.title.ilike(f'%{query}%')) | 
        (Music.artist.ilike(f'%{query}%')) |
        (Music.album.ilike(f'%{query}%'))
    ).all()
    
    return jsonify([m.to_dict() for m in results])

@main_bp.route('/api/music/<int:music_id>/like', methods=['POST'])
@jwt_required()
def like_music(music_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    music = Music.query.get(music_id)
    
    if not music:
        return jsonify({'error': 'Music not found'}), 404
        
    if music not in user.liked_songs:
        user.liked_songs.append(music)
        db.session.commit()
        
    return jsonify({'message': 'Song liked'})

@main_bp.route('/api/music/<int:music_id>/like', methods=['DELETE'])
@jwt_required()
def unlike_music(music_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    music = Music.query.get(music_id)
    
    if not music:
        return jsonify({'error': 'Music not found'}), 404
        
    if music in user.liked_songs:
        user.liked_songs.remove(music)
        db.session.commit()
        
    return jsonify({'message': 'Song unliked'})

@main_bp.route('/api/me/liked', methods=['GET'])
@jwt_required()
def get_liked_songs():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    # Using lazy='dynamic' allows filtering but simplified here
    liked = user.liked_songs.all()
    return jsonify([m.to_dict() for m in liked])
