from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for Event attendees (many-to-many)
event_attendees = db.Table('event_attendees',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

# Association table for Project contributors (many-to-many, optional)
project_contributors = db.Table('project_contributors',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    estate_id = db.Column(db.Integer, db.ForeignKey('estate.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    events = db.relationship('Event', backref='creator', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    projects = db.relationship('Project', backref='creator', lazy=True)  # Projects created by user
    contributed_projects = db.relationship('Project', secondary='project_contributors',
                                          backref='contributors', lazy='dynamic')  # Projects user contributes to

    def __repr__(self):
        return f"<User {self.username}>"

class Estate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    residents = db.relationship('User', backref='estate', lazy=True)
    events = db.relationship('Event', backref='estate', lazy=True)
    projects = db.relationship('Project', backref='estate', lazy=True)  # Projects in this estate

    def __repr__(self):
        return f"<Estate {self.name}>"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    estate_id = db.Column(db.Integer, db.ForeignKey('estate.id'), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    attendees = db.relationship('User', secondary='event_attendees', backref='attending_events', lazy='dynamic')

    def __repr__(self):
        return f"<Event {self.name}>"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    estate_id = db.Column(db.Integer, db.ForeignKey('estate.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f"<Post {self.title}>"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Comment by User {self.author_id} on Post {self.post_id}>"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    estate_id = db.Column(db.Integer, db.ForeignKey('estate.id'), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    state = db.Column(db.Boolean, default=True, nullable=False)  # True=active/ongoing, False=inactive/completed
    cost_estimates = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    estate = db.relationship('Estate', backref='projects', lazy=True)
    creator = db.relationship('User', backref='created_projects', lazy=True)  # Renamed to avoid conflict

    def __repr__(self):
        return f"<Project {self.project_name}>"
