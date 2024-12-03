from event_pipeline import EventPipeline, SeniorCustomerService, FinancialPipeline, FinancialManager, TaskPipeline, RecruitmentPipeline, RecruitmentManager

# Initialize pipeline objects
event_pipeline = EventPipeline()
financial_pipeline = FinancialPipeline()
task_pipeline = TaskPipeline()
recruitment_pipeline = RecruitmentPipeline()

def create_event_request():
    event_type = input("Enter event type (e.g., Conference, Workshop): ")
    date = input("Enter event date (YYYY-MM-DD): ")
    preferences = input("Enter preferences (e.g., food:vegan, music:jazz): ")
    preferences_dict = dict([pref.split(":") for pref in preferences.split(",")])
    event = event_pipeline.create_event_request(event_type, date, preferences_dict)
    print(f"Event '{event.event_type}' created with status: {event.status}")

def start_task():
    description = input("Enter task description to start: ")
    result = task_pipeline.start_task(description)
    print(result)

def complete_task():
    description = input("Enter task description to complete: ")
    result = task_pipeline.complete_task(description)
    print(result)

def view_task_status():
    description = input("Enter task description to view status: ")
    status = task_pipeline.view_task_status(description)
    print(f"Task status: {status}")

def approve_or_reject_event():
    event_type = input("Enter the event type to approve/reject: ")
    request = next((req for req in event_pipeline.requests if req.event_type == event_type), None)
    if request:
        decision = input("Approve (A) or Reject (R) this event? ").strip().upper()
        if decision == "A":
            SeniorCustomerService.approve_event_request(request)
        elif decision == "R":
            SeniorCustomerService.reject_event_request(request)
        print(f"Event '{request.event_type}' status: {request.status}")
    else:
        print("Event request not found.")

def submit_financial_request():
    amount = float(input("Enter financial amount: "))
    reason = input("Enter reason for request: ")
    request = financial_pipeline.submit_financial_request(amount, reason)
    print(f"Financial request submitted with status: {request.status}")

def approve_or_reject_financial_request():
    reason = input("Enter reason for the financial request to approve/reject: ")
    request = next((req for req in financial_pipeline.requests if req.reason == reason), None)
    if request:
        decision = input("Approve (A) or Reject (R) this financial request? ").strip().upper()
        if decision == "A":
            FinancialManager.approve_financial_request(request)
        elif decision == "R":
            FinancialManager.reject_financial_request(request)
        print(f"Financial request '{request.reason}' status: {request.status}")
    else:
        print("Financial request not found.")

def assign_task():
    description = input("Enter task description: ")
    deadline = input("Enter task deadline (YYYY-MM-DD): ")
    team = input("Enter assigned team (e.g., Decorations Team): ")
    task = task_pipeline.assign_task(description, deadline, team)
    print(f"Task '{task.description}' assigned to {task.assigned_team} with status: {task.status}")

def view_task_status():
    description = input("Enter task description to view status: ")
    status = task_pipeline.view_task_status(description)
    print(f"Task status: {status}")

def request_new_staff():
    position = input("Enter position for recruitment: ")
    urgency = input("Enter urgency level (High, Medium, Low): ")
    department = input("Enter requesting department: ")
    request = recruitment_pipeline.request_new_staff(position, urgency, department)
    print(f"Staff request for '{position}' submitted with status: {request.status}")

def approve_or_reject_staff_request():
    position = input("Enter position for the staff request to approve/reject: ")
    request = next((req for req in recruitment_pipeline.requests if req.position == position), None)
    if request:
        decision = input("Approve (A) or Reject (R) this staff request? ").strip().upper()
        if decision == "A":
            RecruitmentManager.approve_request(request)
        elif decision == "R":
            RecruitmentManager.reject_request(request)
        print(f"Staff request for '{request.position}' status: {request.status}")
    else:
        print("Staff request not found.")

def main():
    while True:
        print("\nSEP Management System")
        print("1. Create Event Request")
        print("2. Approve/Reject Event Request")
        print("3. Submit Financial Request")
        print("4. Approve/Reject Financial Request")
        print("5. Assign Task to Sub-Team")
        print("6. Start Task")
        print("7. Complete Task")
        print("8. View Task Status")
        print("9. Request New Staff")
        print("10. Approve/Reject Staff Request")
        print("11. Exit")

        choice = input("Select an option (1-11): ").strip()

        if choice == "1":
            create_event_request()
        elif choice == "2":
            approve_or_reject_event()
        elif choice == "3":
            submit_financial_request()
        elif choice == "4":
            approve_or_reject_financial_request()
        elif choice == "5":
            assign_task()
        elif choice == "6":
            start_task()
        elif choice == "7":
            complete_task()
        elif choice == "8":
            view_task_status()
        elif choice == "9":
            request_new_staff()
        elif choice == "10":
            approve_or_reject_staff_request()
        elif choice == "11":
            print("Exiting SEP Management System.")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()