from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from .models import db, User, Estate, Event, Post, Comment, Project

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return jsonify({'status': 'ok', 'message': 'Flask app is running'})

# USER ROUTES
@main_bp.route('/api/user', methods=['GET'])
def api_get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'phone': user.phone,
        'estate_id': user.estate_id,
        'created_at': user.created_at.isoformat()
    } for user in users])

@main_bp.route('/api/user/<int:user_id>', methods=['GET'])
def api_get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'phone': user.phone,
        'estate_id': user.estate_id,
        'created_at': user.created_at.isoformat()
    })

@main_bp.route('/api/user', methods=['POST'])
def api_create_user():
    data = request.get_json()
    required_fields = ['username', 'email', 'password', 'full_name']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        full_name=data['full_name'],
        phone=data.get('phone'),
        estate_id=data.get('estate_id')
    )
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'phone': user.phone,
            'estate_id': user.estate_id,
            'created_at': user.created_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create user', 'message': str(e)}), 500

@main_bp.route('/api/user/<int:user_id>', methods=['PATCH'])
def api_update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'phone' in data:
        user.phone = data['phone']
    if 'estate_id' in data:
        user.estate_id = data['estate_id']

    try:
        db.session.commit()
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'phone': user.phone,
            'estate_id': user.estate_id,
            'created_at': user.created_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user', 'message': str(e)}), 500

@main_bp.route('/api/user/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'User {user_id} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete user', 'message': str(e)}), 500

# ESTATE ROUTES
@main_bp.route('/api/estate', methods=['GET'])
def api_get_estates():
    estates = Estate.query.all()
    return jsonify([{
        'id': estate.id,
        'name': estate.name,
        'address': estate.address,
        'description': estate.description,
        'created_at': estate.created_at.isoformat()
    } for estate in estates])

@main_bp.route('/api/estate/<int:estate_id>', methods=['GET'])
def api_get_estate_by_id(estate_id):
    estate = Estate.query.get_or_404(estate_id)
    return jsonify({
        'id': estate.id,
        'name': estate.name,
        'address': estate.address,
        'description': estate.description,
        'created_at': estate.created_at.isoformat()
    })

@main_bp.route('/api/estate', methods=['POST'])
def api_create_estate():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing name field'}), 400

    estate = Estate(
        name=data['name'],
        address=data.get('address'),
        description=data.get('description')
    )
    
    try:
        db.session.add(estate)
        db.session.commit()
        return jsonify({
            'id': estate.id,
            'name': estate.name,
            'address': estate.address,
            'description': estate.description,
            'created_at': estate.created_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create estate', 'message': str(e)}), 500

@main_bp.route('/api/estate/<int:estate_id>', methods=['PATCH'])
def api_update_estate(estate_id):
    estate = Estate.query.get_or_404(estate_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' in data:
        estate.name = data['name']
    if 'address' in data:
        estate.address = data['address']
    if 'description' in data:
        estate.description = data['description']

    try:
        db.session.commit()
        return jsonify({
            'id': estate.id,
            'name': estate.name,
            'address': estate.address,
            'description': estate.description,
            'created_at': estate.created_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update estate', 'message': str(e)}), 500

@main_bp.route('/api/estate/<int:estate_id>', methods=['DELETE'])
def api_delete_estate(estate_id):
    estate = Estate.query.get_or_404(estate_id)
    try:
        db.session.delete(estate)
        db.session.commit()
        return jsonify({'message': f'Estate {estate_id} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete estate', 'message': str(e)}), 500

# EVENT ROUTES
@main_bp.route('/api/event', methods=['GET'])
def api_get_events():
    events = Event.query.all()
    return jsonify([{
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'date': event.date.isoformat(),
        'location': event.location,
        'estate_id': event.estate_id,
        'creator_id': event.creator_id,
        'created_at': event.created_at.isoformat(),
        'attendees': [user.id for user in event.attendees]
    } for event in events])

@main_bp.route('/api/event/<int:event_id>', methods=['GET'])
def api_get_event_by_id(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'date': event.date.isoformat(),
        'location': event.location,
        'estate_id': event.estate_id,
        'creator_id': event.creator_id,
        'created_at': event.created_at.isoformat(),
        'attendees': [user.id for user in event.attendees]
    })

@main_bp.route('/api/event', methods=['POST'])
def api_create_event():
    data = request.get_json()
    if not data or not all(field in data for field in ['name', 'date', 'creator_id']):
        return jsonify({'error': 'Missing required fields'}), 400

    event = Event(
        name=data['name'],
        description=data.get('description'),
        date=data['date'],
        location=data.get('location'),
        estate_id=data.get('estate_id'),
        creator_id=data['creator_id']
    )
    
    try:
        db.session.add(event)
        if 'attendees' in data and isinstance(data['attendees'], list):
            for user_id in data['attendees']:
                user = User.query.get(user_id)
                if user:
                    event.attendees.append(user)
        db.session.commit()
        return jsonify({
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'date': event.date.isoformat(),
            'location': event.location,
            'estate_id': event.estate_id,
            'creator_id': event.creator_id,
            'created_at': event.created_at.isoformat(),
            'attendees': [user.id for user in event.attendees]
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create event', 'message': str(e)}), 500

@main_bp.route('/api/event/<int:event_id>', methods=['PATCH'])
def api_update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' in data:
        event.name = data['name']
    if 'description' in data:
        event.description = data['description']
    if 'date' in data:
        event.date = data['date']
    if 'location' in data:
        event.location = data['location']
    if 'estate_id' in data:
        event.estate_id = data['estate_id']
    if 'attendees' in data and isinstance(data['attendees'], list):
        event.attendees = []
        for user_id in data['attendees']:
            user = User.query.get(user_id)
            if user:
                event.attendees.append(user)

    try:
        db.session.commit()
        return jsonify({
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'date': event.date.isoformat(),
            'location': event.location,
            'estate_id': event.estate_id,
            'creator_id': event.creator_id,
            'created_at': event.created_at.isoformat(),
            'attendees': [user.id for user in event.attendees]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update event', 'message': str(e)}), 500

@main_bp.route('/api/event/<int:event_id>', methods=['DELETE'])
def api_delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': f'Event {event_id} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete event', 'message': str(e)}), 500

# PROJECT ROUTES
@main_bp.route('/api/project', methods=['GET'])
def api_get_projects():
    projects = Project.query.all()
    return jsonify([{
        'id': project.id,
        'project_name': project.project_name,
        'description': project.description,
        'estate_id': project.estate_id,
        'creator_id': project.creator_id,
        'state': project.state,
        'cost_estimates': project.cost_estimates,
        'created_at': project.created_at.isoformat(),
        'contributors': [user.id for user in project.contributors]
    } for project in projects])

@main_bp.route('/api/project/<int:project_id>', methods=['GET'])
def api_get_project_by_id(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({
        'id': project.id,
        'project_name': project.project_name,
        'description': project.description,
        'estate_id': project.estate_id,
        'creator_id': project.creator_id,
        'state': project.state,
        'cost_estimates': project.cost_estimates,
        'created_at': project.created_at.isoformat(),
        'contributors': [user.id for user in project.contributors]
    })

@main_bp.route('/api/project', methods=['POST'])
def api_create_project():
    data = request.get_json()
    if not data or not all(field in data for field in ['project_name', 'creator_id']):
        return jsonify({'error': 'Missing required fields'}), 400

    project = Project(
        project_name=data['project_name'],
        description=data.get('description'),
        estate_id=data.get('estate_id'),
        creator_id=data['creator_id'],
        state=data.get('state', True),
        cost_estimates=data.get('cost_estimates')
    )
    
    try:
        db.session.add(project)
        if 'contributors' in data and isinstance(data['contributors'], list):
            for user_id in data['contributors']:
                user = User.query.get(user_id)
                if user:
                    project.contributors.append(user)
        db.session.commit()
        return jsonify({
            'id': project.id,
            'project_name': project.project_name,
            'description': project.description,
            'estate_id': project.estate_id,
            'creator_id': project.creator_id,
            'state': project.state,
            'cost_estimates': project.cost_estimates,
            'created_at': project.created_at.isoformat(),
            'contributors': [user.id for user in project.contributors]
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create project', 'message': str(e)}), 500

@main_bp.route('/api/project/<int:project_id>', methods=['PATCH'])
def api_update_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'project_name' in data:
        project.project_name = data['project_name']
    if 'description' in data:
        project.description = data['description']
    if 'estate_id' in data:
        project.estate_id = data['estate_id']
    if 'state' in data:
        project.state = data['state']
    if 'cost_estimates' in data:
        project.cost_estimates = data['cost_estimates']
    if 'contributors' in data and isinstance(data['contributors'], list):
        project.contributors = []
        for user_id in data['contributors']:
            user = User.query.get(user_id)
            if user:
                project.contributors.append(user)

    try:
        db.session.commit()
        return jsonify({
            'id': project.id,
            'project_name': project.project_name,
            'description': project.description,
            'estate_id': project.estate_id,
            'creator_id': project.creator_id,
            'state': project.state,
            'cost_estimates': project.cost_estimates,
            'created_at': project.created_at.isoformat(),
            'contributors': [user.id for user in project.contributors]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update project', 'message': str(e)}), 500

@main_bp.route('/api/project/<int:project_id>', methods=['DELETE'])
def api_delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': f'Project {project_id} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete project', 'message': str(e)}), 500

# POST ROUTES
@main_bp.route('/api/post', methods=['GET'])
def api_get_posts():
    posts = Post.query.all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author_id': post.author_id,
        'estate_id': post.estate_id,
        'created_at': post.created_at.isoformat()
    } for post in posts])

@main_bp.route('/api/post/<int:post_id>', methods=['GET'])
def api_get_post_by_id(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author_id': post.author_id,
        'estate_id': post.estate_id,
        'created_at': post.created_at.isoformat()
    })

@main_bp.route('/api/post', methods=['POST'])
def api_create_post():
    data = request.get_json()
    if not data or not all(field in data for field in ['title', 'content', 'author_id']):
        return jsonify({'error': 'Missing required fields'}), 400

    post = Post(
        title=data['title'],
        content=data['content'],
        author_id=data['author_id'],
        estate_id=data.get('estate_id')
    )
    
    try:
        db.session.add(post)
        db.session.commit()
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author_id': post.author_id,
            'estate_id': post.estate_id,
            'created_at': post.created_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create post', 'message': str(e)}), 500

@main_bp.route('/api/post/<int:post_id>', methods=['PATCH'])
def api_update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'estate_id' in data:
        post.estate_id = data['estate_id']

    try:
        db.session.commit()
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author_id': post.author_id,
            'estate_id': post.estate_id,
            'created_at': post.created_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update post', 'message': str(e)}), 500

@main_bp.route('/api/post/<int:post_id>', methods=['DELETE'])
def api_delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': f'Post {post_id} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete post', 'message': str(e)}), 500

# COMMENT ROUTES
@main_bp.route('/api/comment', methods=['GET'])
def api_get_comments():
    comments = Comment.query.all()
    return jsonify([{
        'id': comment.id,
        'content': comment.content,
        'author_id': comment.author_id,
        'post_id': comment.post_id,
        'created_at': comment.created_at.isoformat()
    } for comment in comments])

@main_bp.route('/api/comment/<int:comment_id>', methods=['GET'])
def api_get_comment_by_id(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'author_id': comment.author_id,
        'post_id': comment.post_id,
        'created_at': comment.created_at.isoformat()
    })

@main_bp.route('/api/comment', methods=['POST'])
def api_create_comment():
    data = request.get_json()
    if not data or not all(field in data for field in ['content', 'author_id', 'post_id']):
        return jsonify({'error': 'Missing required fields'}), 400

    comment = Comment(
        content=data['content'],
        author_id=data['author_id'],
        post_id=data['post_id']
    )
    
    try:
        db.session.add(comment)
        db.session.commit()
        return jsonify({
            'id': comment.id,
            'content': comment.content,
            'author_id': comment.author_id,
            'post_id': comment.post_id,
            'created_at': comment.created_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create comment', 'message': str(e)}), 500

@main_bp.route('/api/comment/<int:comment_id>', methods=['PATCH'])
def api_update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'content' in data:
        comment.content = data['content']

    try:
        db.session.commit()
        return jsonify({
            'id': comment.id,
            'content': comment.content,
            'author_id': comment.author_id,
            'post_id': comment.post_id,
            'created_at': comment.created_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update comment', 'message': str(e)}), 500

@main_bp.route('/api/comment/<int:comment_id>', methods=['DELETE'])
def api_delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    try:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': f'Comment {comment_id} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete comment', 'message': str(e)}), 500