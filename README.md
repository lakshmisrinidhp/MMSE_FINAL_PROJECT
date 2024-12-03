# Swedish Event Planners (SEP) Management System

## Overview
This project is a comprehensive Event Management System designed for Swedish Event Planners (SEP). It provides role-based dashboards and functionalities for managing events, financial approvals, task assignments, recruitment, and more. The system ensures a streamlined workflow across all departments.

---

## Features
- **Role-Based Access:** Custom dashboards for different roles.
- **Event Management:** Request creation, approval, and tracking.
- **Financial Management:** Budget approval and tracking.
- **Task Assignment:** Assign tasks to sub-teams and track progress.
- **Recruitment Management:** Recruitment requests and job publishing.
- **User-Friendly UI:** Intuitive dashboards for efficient task handling.

---

## Actors and Credentials

| **Role**                 | **Username**             | **Password**       |
|--------------------------|--------------------------|--------------------|
| Customer Service         | `customer_service`       | `password123`      |
| Senior Customer Service  | `senior_customer_service`| `password456`      |
| Financial Manager        | `financial_manager`      | `password345`      |
| Admin Manager            | `admin_manager`          | `password678`      |
| Service Manager          | `service_manager`        | `password901`      |
| Production Manager       | `production_manager`     | `password789`      |
| HR Manager               | `hr_manager`             | `password012`      |
| Subteam Leader           | `subteam_leader`         | `password234`      |

---

## Setup Instructions

```bash
# 1. Clone the Repository
git clone https://github.com/your-repo/SEP_Project.git
cd SEP_Project

# 2. Set up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Navigate to the Source Directory
cd src

# 5. Run the Application
python app.py
