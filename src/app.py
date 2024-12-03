from flask import Flask, render_template, request, redirect, url_for, session, flash
from event_pipeline import EventPipeline, SeniorCustomerService, FinancialPipeline, FinancialManager, TaskPipeline, RecruitmentPipeline, RecruitmentManager

app = Flask(__name__, template_folder="../templates")  # Explicitly set the path to templates folder
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Initialize backend logic
event_pipeline = EventPipeline()
financial_pipeline = FinancialPipeline()
task_pipeline = TaskPipeline()
recruitment_pipeline = RecruitmentPipeline()

# Sample users with roles
users = {
    "customer_service": {"password": "password123", "role": "customer_service"},
    "senior_customer_service": {"password": "password456", "role": "senior_customer_service"},
    "production_manager": {"password": "password789", "role": "production_manager"},
    "hr_manager": {"password": "password012", "role": "hr_manager"},
    "financial_manager": {"password": "password345", "role": "financial_manager"},
    "admin_manager": {"password": "password678", "role": "admin_manager"},
    "service_manager": {"password": "password901", "role": "service_manager"},
    "subteam_leader": {"password": "password234", "role": "subteam_leader"}
}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            flash('Login successful!', 'success')
            
            # Redirect to dashboard based on role
            role_redirects = {
                'customer_service': 'customer_dashboard',
                'senior_customer_service': 'senior_dashboard',
                'production_manager': 'production_manager_dashboard',
                'hr_manager': 'hr_dashboard',
                'financial_manager': 'financial_dashboard',
                'admin_manager': 'admin_dashboard',
                'service_manager': 'service_manager_dashboard',
                'subteam_leader': 'subteam_leader_dashboard'
            }
            return redirect(url_for(role_redirects.get(user['role'])))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Customer Service - Create Event Requests
@app.route('/customer_dashboard')
def customer_dashboard():
    if session.get('role') != 'customer_service':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    return render_template('customer_dashboard.html')

@app.route('/create_event', methods=['POST'])
def create_event():
    if session.get('role') != 'customer_service':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    event_type = request.form['event_type']
    date = request.form['date']
    preferences = request.form['preferences']
    preferences_dict = dict([pref.split(":") for pref in preferences.split(",")])
    event_pipeline.create_event_request(event_type, date, preferences_dict)
    flash("Event created successfully!", "success")
    return redirect(url_for('customer_dashboard'))

# Senior Customer Service (SCS) - View and Approve/Reject Event Requests
@app.route('/senior_dashboard')
def senior_dashboard():
    if session.get('role') != 'senior_customer_service':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    # Fetch only events with "Pending" status
    pending_events = [event for event in event_pipeline.requests if event.status == "Pending"]
    return render_template('senior_dashboard.html', pending_events=pending_events)


@app.route('/process_event_decision', methods=['POST'])
def process_event_decision():
    if session.get('role') != 'senior_customer_service':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    event_type = request.form['event_type']
    decision = request.form['decision']
    
    # Find the event in the pipeline and update its status
    event = next((event for event in event_pipeline.requests if event.event_type == event_type), None)
    if event:
        if decision == "approve":
            SeniorCustomerService.approve_event_request(event)
            message = f"Event '{event_type}' approved successfully."
        elif decision == "reject":
            SeniorCustomerService.reject_event_request(event)
            message = f"Event '{event_type}' rejected successfully."
        else:
            message = "Invalid decision."
    else:
        message = "Event not found."

    # Update pending events and refresh the dashboard
    pending_events = event_pipeline.get_pending_requests()
    return render_template('senior_dashboard.html', pending_events=pending_events, message=message)



@app.route('/view_event_requests')
def view_event_requests():
    if session.get('role') != 'senior_customer_service':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    return render_template('view_event_requests.html', requests=event_pipeline.requests)

@app.route('/approve_event/<event_type>')
def approve_event(event_type):
    if session.get('role') != 'senior_customer_service':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    request = next((req for req in event_pipeline.requests if req.event_type == event_type), None)
    if request:
        SeniorCustomerService.approve_event_request(request)
        flash(f"Event '{event_type}' approved successfully.", "success")
    else:
        flash("Event not found.", "danger")
    return redirect(url_for('view_event_requests'))

@app.route('/reject_event/<event_type>')
def reject_event(event_type):
    if session.get('role') != 'senior_customer_service':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    request = next((req for req in event_pipeline.requests if req.event_type == event_type), None)
    if request:
        SeniorCustomerService.reject_event_request(request)
        flash(f"Event '{event_type}' rejected successfully.", "success")
    else:
        flash("Event not found.", "danger")
    return redirect(url_for('view_event_requests'))

# Financial Manager (FM) - Submit, View, and Approve Budget Requests
@app.route('/financial_dashboard')
def financial_dashboard():
    if session.get('role') != 'financial_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    # Fetch events that are approved by Senior Customer Service but not yet processed by Financial Manager
    approved_events = [event for event in event_pipeline.requests if event.status == "Approved"]
    return render_template('financial_dashboard.html', approved_events=approved_events)

@app.route('/process_financial_decision', methods=['POST'])
def process_financial_decision():
    if session.get('role') != 'financial_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    event_type = request.form['event_type']
    decision = request.form['decision']
    
    # Find the event and update status based on decision
    event = next((event for event in event_pipeline.requests if event.event_type == event_type), None)
    if event:
        if decision == "approve":
            FinancialManager.approve_financial_request(event)
            message = f"Budget for event '{event_type}' has been approved."
        else:
            FinancialManager.reject_financial_request(event)
            message = f"Budget for event '{event_type}' has been rejected."
    else:
        message = "Event not found or already processed."

    # Fetch updated list of approved events for Financial Manager
    approved_events = [event for event in event_pipeline.requests if event.status == "Approved"]
    return render_template('financial_dashboard.html', approved_events=approved_events, message=message)


@app.route('/submit_budget_request', methods=['POST'])
def submit_budget_request():
    if session.get('role') != 'financial_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    amount = request.form['amount']
    reason = request.form['reason']
    financial_pipeline.submit_financial_request(amount, reason)
    flash("Budget request submitted successfully!", "success")
    return redirect(url_for('financial_dashboard'))

@app.route('/approve_budget/<reason>', methods=['POST'])
def approve_budget(reason):
    if session.get('role') != 'financial_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    request = next((req for req in financial_pipeline.requests if req.reason == reason), None)
    if request:
        FinancialManager.approve_financial_request(request)
        flash(f"Budget for '{reason}' approved.", "success")
    else:
        flash("Budget request not found", "danger")
    return redirect(url_for('financial_dashboard'))

# Admin Manager (AM) - Final Approval of Event Requests
@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    # Fetch events that have been approved by Financial Manager
    budget_approved_events = [event for event in event_pipeline.requests if event.status == "Budget Approved"]
    return render_template('admin_dashboard.html', budget_approved_events=budget_approved_events)

@app.route('/process_final_approval', methods=['POST'])
def process_final_approval():
    if session.get('role') != 'admin_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    event_type = request.form['event_type']
    
    # Find the event in the pipeline and update its status to "Final Approved"
    event = next((event for event in event_pipeline.requests if event.event_type == event_type), None)
    if event:
        event.status = "Final Approved"
        message = f"Event '{event_type}' has been given final approval."
    else:
        message = "Event not found or already processed."

    # Refresh the list of events pending final approval
    budget_approved_events = [event for event in event_pipeline.requests if event.status == "Budget Approved"]
    return render_template('admin_dashboard.html', budget_approved_events=budget_approved_events, message=message)




# Service Manager (SM) - View and Assign Tasks
@app.route('/service_manager_dashboard')
def service_manager_dashboard():
    if session.get('role') != 'service_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    # Fetch events with "Final Approved" status
    final_approved_events = [event for event in event_pipeline.requests if event.status == "Final Approved"]
    tasks = task_pipeline.tasks  # Get all tasks for display
    return render_template('service_manager_dashboard.html', final_approved_events=final_approved_events, tasks=tasks)

@app.route('/assign_task', methods=['POST'])
def assign_task():
    if session.get('role') != 'service_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    # Retrieve data from the form
    event_type = request.form['event_type']
    task_description = request.form['task_description']
    deadline = request.form['deadline']
    sub_team = request.form['sub_team']
    
    # Assign task using the pipeline
    task_pipeline.assign_task(task_description, deadline, sub_team, event_type)
    flash(f"Task '{task_description}' assigned to {sub_team} for event '{event_type}'.", "success")
    
    # Fetch all tasks for rendering
    tasks = task_pipeline.tasks
    return render_template('assign_task.html', tasks=tasks)


@app.route('/submit_recruitment_request', methods=['POST'])
def submit_recruitment_request():
    if session.get('role') != 'service_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    position = request.form['position']
    urgency = request.form['urgency']
    
    # Submit recruitment request
    recruitment_pipeline.request_new_staff(position, urgency, "Service")
    flash(f"Recruitment request for '{position}' submitted with urgency '{urgency}'.", "success")
    return redirect(url_for('service_manager_dashboard'))


# Production Manager - View Tasks and Update Status
@app.route('/production_manager_dashboard')
def production_manager_dashboard():
    if session.get('role') != 'production_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    # Get tasks assigned to the production team
    tasks = task_pipeline.get_tasks_by_team("Production")
    
    # Retrieve all recruitment requests submitted by the Service Manager
    recruitment_requests = recruitment_pipeline.requests
    return render_template('production_manager_dashboard.html', tasks=tasks, recruitment_requests=recruitment_requests)

@app.route('/update_task_status_pm', methods=['POST'])
def update_task_status_pm():
    if session.get('role') != 'production_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    task_description = request.form['task_description']
    new_status = request.form['new_status']
    
    # Update the task's status in the TaskPipeline
    task = next((t for t in task_pipeline.tasks if t.description == task_description), None)
    if task:
        task.status = new_status
        flash(f"Task '{task_description}' status updated to '{new_status}'.", "success")
    else:
        flash("Task not found", "danger")
    return redirect(url_for('production_manager_dashboard'))



# Subteam Leader - View and Update Task Status
@app.route('/subteam_leader_dashboard')
def subteam_leader_dashboard():
    if session.get('role') != 'subteam_leader':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    # Fetch tasks assigned to the Subteam Leader’s team
    team = session.get('username')  # Assuming username represents the team leader
    tasks = task_pipeline.get_tasks_by_team(team)
    return render_template('subteam_leader_dashboard.html', tasks=tasks)

@app.route('/update_task_status', methods=['POST'])
def update_task_status():
    if session.get('role') != 'subteam_leader':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    task_description = request.form['task_description']
    new_status = request.form['new_status']
    
    # Find and update the task’s status
    task = next((t for t in task_pipeline.tasks if t.description == task_description), None)
    if task:
        task.status = new_status
        flash(f"Task '{task_description}' status updated to '{new_status}'.", "success")
    else:
        flash("Task not found", "danger")
    return redirect(url_for('subteam_leader_dashboard'))


# HR Manager - Manage Recruitment
@app.route('/hr_dashboard')
def hr_dashboard():
    if session.get('role') != 'hr_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))

    # Fetch pending recruitment requests
    recruitment_requests = recruitment_pipeline.get_pending_requests()
    return render_template('hr_manager_dashboard.html', recruitment_requests=recruitment_requests)

# Route to publish job advertisement
@app.route('/publish_job', methods=['POST'])
def publish_job():
    if session.get('role') != 'hr_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    position = request.form['position']
    urgency = request.form['urgency']
    recruitment_pipeline.request_new_staff(position, urgency, "HR")
    flash("Job advertisement published successfully.", "success")
    return redirect(url_for('hr_dashboard'))

# Route to process recruitment requests
@app.route('/process_recruitment_request', methods=['POST'])
def process_recruitment_request():
    if session.get('role') != 'hr_manager':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('login'))
    
    position = request.form['position']
    decision = request.form['decision']
    request = next((r for r in recruitment_pipeline.requests if r.position == position), None)
    
    if request:
        if decision == "approve":
            RecruitmentManager.approve_request(request)
            flash(f"Recruitment request for '{position}' has been approved.", "success")
        elif decision == "reject":
            RecruitmentManager.reject_request(request)
            flash(f"Recruitment request for '{position}' has been rejected.", "danger")
    else:
        flash("Recruitment request not found.", "danger")

    return redirect(url_for('hr_dashboard'))


    # Refresh the page with message
    pending_events = [event for event in event_pipeline.requests if event.status == "Pending"]
    return render_template('senior_dashboard.html', pending_events=pending_events, message=message)


if __name__ == '__main__':
    app.run(debug=True)
