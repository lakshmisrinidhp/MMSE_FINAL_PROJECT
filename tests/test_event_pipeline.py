import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from event_pipeline import (
    EventPipeline, SeniorCustomerService, FinancialPipeline,
    FinancialManager, TaskPipeline, RecruitmentPipeline, RecruitmentManager
)

# EventPipeline Tests
def test_create_event_request():
    pipeline = EventPipeline()
    event = pipeline.create_event_request("Conference", "2023-11-01", {"location": "Stockholm"})
    assert event in pipeline.requests
    assert event.status == "Pending"

def test_approve_event_request():
    pipeline = EventPipeline()
    event = pipeline.create_event_request("Workshop", "2023-11-02", {"location": "Gothenburg"})
    SeniorCustomerService.approve_event_request(event)
    assert event.status == "Approved"

def test_reject_event_request():
    pipeline = EventPipeline()
    event = pipeline.create_event_request("Seminar", "2023-11-03", {"location": "Malmo"})
    SeniorCustomerService.reject_event_request(event)
    assert event.status == "Rejected"


# FinancialPipeline Tests
def test_submit_financial_request():
    pipeline = FinancialPipeline()
    request = pipeline.submit_financial_request(5000, "Venue booking")
    assert request in pipeline.requests
    assert request.status == "Pending"

def test_approve_financial_request():
    pipeline = FinancialPipeline()
    request = pipeline.submit_financial_request(3000, "Catering")
    FinancialManager.approve_financial_request(request)
    assert request.status == "Approved"

def test_reject_financial_request():
    pipeline = FinancialPipeline()
    request = pipeline.submit_financial_request(1500, "Decorations")
    FinancialManager.reject_financial_request(request)
    assert request.status == "Rejected"


# TaskPipeline Tests
def test_assign_task():
    pipeline = TaskPipeline()
    task = pipeline.assign_task("Setup stage", "2023-11-05", "Production Team")
    assert task in pipeline.tasks
    assert task.status == "Not Started"

def test_start_task():
    pipeline = TaskPipeline()
    task = pipeline.assign_task("Test AV Equipment", "2023-11-06", "Tech Team")
    pipeline.start_task(task.description)
    assert task.status == "Ongoing"

def test_complete_task():
    pipeline = TaskPipeline()
    task = pipeline.assign_task("Arrange seating", "2023-11-07", "Logistics Team")
    pipeline.complete_task(task.description)
    assert task.status == "Completed"


# RecruitmentPipeline Tests
def test_request_new_staff():
    pipeline = RecruitmentPipeline()
    request = pipeline.request_new_staff("Photographer", "High", "Marketing")
    assert request in pipeline.requests
    assert request.status == "Pending"

def test_approve_recruitment_request():
    pipeline = RecruitmentPipeline()
    request = pipeline.request_new_staff("Security Guard", "Medium", "Security")
    RecruitmentManager.approve_request(request)
    assert request.status == "Approved"

def test_reject_recruitment_request():
    pipeline = RecruitmentPipeline()
    request = pipeline.request_new_staff("Usher", "Low", "Customer Service")
    RecruitmentManager.reject_request(request)
    assert request.status == "Rejected"
