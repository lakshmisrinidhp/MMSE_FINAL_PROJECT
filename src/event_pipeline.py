# event_pipeline.py

# Classes for Event Request Management
class EventRequest:
    def __init__(self, event_type, date, preferences):
        self.event_type = event_type
        self.date = date
        self.preferences = preferences
        self.status = "Pending"

class EventPipeline:
    def __init__(self):
        self.requests = []

    def create_event_request(self, event_type, date, preferences):
        request = EventRequest(event_type, date, preferences)
        self.requests.append(request)
        return request

    def get_pending_requests(self):
        """Retrieve all pending event requests for approval."""
        return [request for request in self.requests if request.status == "Pending"]

class SeniorCustomerService:
    @staticmethod
    def approve_event_request(request):
        request.status = "Approved"

    @staticmethod
    def reject_event_request(request):
        request.status = "Rejected"


# Classes for Financial Request Management
class FinancialRequest:
    def __init__(self, amount, reason):
        self.amount = amount
        self.reason = reason
        self.status = "Pending"

class FinancialPipeline:
    def __init__(self):
        self.requests = []

    def submit_financial_request(self, amount, reason):
        request = FinancialRequest(amount, reason)
        self.requests.append(request)
        return request

    def get_pending_requests(self):
        """Retrieve all pending financial requests for review."""
        return [request for request in self.requests if request.status == "Pending"]

class FinancialManager:
    @staticmethod
    def approve_financial_request(request):
        request.status = "Budget Approved"

    @staticmethod
    def reject_financial_request(request):
        request.status = "Budget Rejected"



# Classes for Task Distribution
class Task:
    def __init__(self, description, deadline, assigned_team, event_type):
        self.description = description
        self.deadline = deadline
        self.assigned_team = assigned_team
        self.status = "Not Started"
        self.event_type = event_type

class TaskPipeline:
    def __init__(self):
        self.tasks = []

    def assign_task(self, description, deadline, assigned_team, event_type):
        task = Task(description, deadline, assigned_team, event_type)
        self.tasks.append(task)
        print(f"Assigned task for event '{event_type}': {description}, deadline: {deadline}, team: {assigned_team}")
        return task


    def view_task_status(self, description):
        for task in self.tasks:
            if task.description == description:
                return task.status
        return "Task not found"
    
    def start_task(self, description):
        for task in self.tasks:
            if task.description == description:
                task.status = "Ongoing"
                return f"Task '{description}' is now Ongoing."
        return "Task not found"

    def complete_task(self, description):
        for task in self.tasks:
            if task.description == description:
                task.status = "Completed"
                return f"Task '{description}' is now Completed."
        return "Task not found"
    
    def get_tasks_by_team(self, team):
        """Retrieve tasks assigned to a specific team."""
        return [task for task in self.tasks if task.assigned_team == team]


# Classes for Staff Recruitment
class StaffRequest:
    def __init__(self, position, urgency, requesting_department):
        self.position = position
        self.urgency = urgency
        self.requesting_department = requesting_department
        self.status = "Pending"

class RecruitmentPipeline:
    def __init__(self):
        self.requests = []

    def request_new_staff(self, position, urgency, requesting_department):
        request = StaffRequest(position, urgency, requesting_department)
        self.requests.append(request)
        return request

    def get_pending_requests(self):
        """Retrieve all pending recruitment requests for HR review."""
        return [request for request in self.requests if request.status == "Pending"]

class RecruitmentManager:
    @staticmethod
    def approve_request(request):
        request.status = "Approved"

    @staticmethod
    def reject_request(request):
        request.status = "Rejected"
