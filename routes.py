from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from models import User, Event, RSVP
from forms import RegistrationForm, LoginForm, EventForm, RSVPForm
from datetime import datetime
import logging

# Home route
@app.route('/')
def index():
    upcoming_events = Event.query.filter(Event.start_time >= datetime.utcnow()).order_by(Event.start_time).limit(5).all()
    return render_template('index.html', events=upcoming_events)

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Login failed. Please check email and password.', 'danger')
    
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Event routes
@app.route('/events')
def events_list():
    events = Event.query.filter(Event.start_time >= datetime.utcnow()).order_by(Event.start_time).all()
    return render_template('events_list.html', title='Events', events=events)

@app.route('/calendar')
def calendar():
    return render_template('index.html', title='Calendar')

@app.route('/api/events')
def api_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    
    rsvp_form = None
    user_rsvp = None
    
    if current_user.is_authenticated:
        rsvp_form = RSVPForm()
        user_rsvp = RSVP.query.filter_by(user_id=current_user.id, event_id=event.id).first()
        if user_rsvp:
            rsvp_form.status.data = user_rsvp.status
    
    rsvp_counts = {
        'attending': RSVP.query.filter_by(event_id=event.id, status='attending').count(),
        'maybe': RSVP.query.filter_by(event_id=event.id, status='maybe').count(),
        'declined': RSVP.query.filter_by(event_id=event.id, status='declined').count()
    }
    
    return render_template('event_detail.html', title=event.title, event=event, 
                          rsvp_form=rsvp_form, user_rsvp=user_rsvp, rsvp_counts=rsvp_counts)

@app.route('/event/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            location=form.location.data,
            user_id=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('event_detail', event_id=event.id))
    
    return render_template('create_event.html', title='Create Event', form=form)

@app.route('/event/<int:event_id>/rsvp', methods=['POST'])
@login_required
def rsvp_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = RSVPForm()
    
    if form.validate_on_submit():
        rsvp = RSVP.query.filter_by(user_id=current_user.id, event_id=event.id).first()
        
        if rsvp:
            rsvp.status = form.status.data
            flash('Your RSVP has been updated!', 'success')
        else:
            rsvp = RSVP(user_id=current_user.id, event_id=event.id, status=form.status.data)
            db.session.add(rsvp)
            flash('Your RSVP has been recorded!', 'success')
        
        db.session.commit()
    
    return redirect(url_for('event_detail', event_id=event.id))

@app.route('/event/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if event.user_id != current_user.id:
        abort(403)  # Forbidden
    
    db.session.delete(event)
    db.session.commit()
    
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('events_list'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
