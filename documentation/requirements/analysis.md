# VITA ARS Version 1 Requirements Analysis


## 1. Problem Statements
1) Broad editing access can make the schedule inconsistent.
2) Clients sometimes erroneously schedule multiple appointments.
3) Clients must meet screening requirements.


## 2. Stakeholders
| Stakeholder | Role / Interest | Major Needs |
| ----------- | --------------- | ----------- |
| IRS | Local office efficacy | Ensure local VITA/TCE office manages client schedules effectively |
| IRS Partners | Operational efficacy | Ensure clients are scheduling meetings effectively and without duplicate appointments |
| VITA/TCE Volunteers | Time Efficiency | Ensure clients are properly scheduling appointments and arriving prepared |
| Clients | Receiving needed services | Receive proper and effective services |


## 3. Scope
| In Scope | Out of Scope / Future Version |
| -------- | ----------------------------- |
| Allow appointment scheduling through _____ | Non-English support |
| Automatically screen clients | Follow-up appointments |
| Reminder to not schedule multiple appointments | Client accounts |
| Delete appointment info after 3 years | Data encryption / PII |
| Admin, Volunteer logins | |


## 4. Functional Requirements

### FR01
**Appointment Limit**<br/>
Scheduling form should prompt the client to ensure that they have not already
had an appointment scheduled this year.

### FR02
**Contact Info**<br/>
Scheduling form should prompt the client for their name, zip code, and phone
number.

### FR03
**Screening**<br/>
Scheduling form should prevent client from scheduling an appointment unless
they verify that they meet the requirements of BR01.


## 5. Nonfunctional Requirements

### NFR01
Only authorized employees will be able to review and edit appointment data per
BR04.


## 6. Business Rules

### BR01
Criteria to receive services:
1) Less than $89'000 in household income, or
2) Over 65 years old, or
3) Vet with income limits

### BR02
No more than one appointment per household, per year. Additional appointments
will need to be scheduled in coordination with the Site Coordinator.

### BR03
Delete PII after 3 years.

### BR04
Site coordinator is the only person who can review the appointment list and edit
appointment info.

### BR05
To reschedule appointments, clients will first need to cancel their appointment
through the Site Coordinator, then schedule a new appointment.


## 7. Requirements Refinement Record
| Date | Statement / Requirement | Problem Found | Evidence / Reason | Revised Statement |
| ---- | ----------------------- | ------------- | ----------------- | ----------------- |
| 10/28/2026 | Document created ||||
| 10/29/2026 | Scope ||| Scope statements added |
| 10/29/2026 | Requirements ||| Requirements/Rules added |