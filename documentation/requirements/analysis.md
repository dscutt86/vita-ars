# VITA ARS Version 1 Requirements Analysis


## 1. Problem Statements
1) Broad editing access can make the schedule inconsistent.
2) Clients sometimes erroneously schedule multiple appointments.
3) Clients must meet screening requirements.


## 2. Stakeholders
| Stakeholder | Role / Interest | Major Needs |
| ----------- | --------------- | ----------- |
| IRS Partners | Manage Appointments | Be able to edit appointments |
||| Be able to cancel appointments |
||| Be able to over-ride rules/requirements that would disallow multiple appointments |
| VITA/TCE Volunteers | View Appointments | Be able to view appointments |
| Clients | Schedule an Appointment | Be able to easily schedule an appointment |
||| Be prompted to ensure they do not schedule more than one appointment per year |
||| Be asked a series of questions ensuring they meet the criteria for service |


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
**Streamlined Portal**<br/>
The system shall provide one consistent reservation scheduling channel for clients and
mobile site partners

### FR02
**Screening Info**<br/>
The system shall collect preliminary screening answers and determine whether the
household is eligible.

### FR03
**View Openings**<br/>
The system shall allow an eligible household to view available appointments by location,
date, and time, and remaining capacity.

### FR04
**Data Collected**<br/>
The system shall collect the client's full name, phone number, and ZIP code before
creating a reservation.

### FR05
**Appointment Saving**<br/>
The system shall create and save a confirmed appointment for a selected available hourly
block.

### FR06
**Unique Confirmation Number**<br/>
The system shall generate a unique confirmation number and display the confirmed
location, date, and appointment time after finishing reservation.

### FR07
**Screening Explanation**<br/>
The system shall provide explanation messages when screening or booking is unsuccessful,
including ineligible screening, incomplete information, closed booking, or full capacity.

### FR08
**Reservation Retrieval by Confirmation Number**<br/>
The system shall allow clients to retrieve their own appointments using given
confirmation numbers.

### FR09
**Reservation Retrieval by Client Info**<br/>
The system shall allow clients to retrieve their own appointments using their full name,
phone number, and ZIP code.

### FR10
**Cancelations**<br/>
The system shall allow clients to cancel eligible appointments.

### FR11
**View Full Site Schedule**<br/>
The system shall allow site coordinators to view appointment lists by location and date,
including suspected duplicate flags.

### FR12
**Edit Client Information**<br/>
The system shall allow the site coordinator to correct a client's contact information.

### FR13
**Appointment Lists**<br/>
The system shall allow the site coordinator to generate and print appointment lists
including appointment time, client full name, and phone number.

### FR14
**Schedule Management**<br/>
The system shall allow the site coordinator to create, update, or close service
schedules, including locations, dates, and appointment blocks.

### FR15
**Capacity Management**<br/>
The system shall allow the site coordinator to adjust appointment capacity for a service
block.

### FR16
**Schedule Locking**<br/>
Booking closes and locks for an entire site/service date 24 hours before its first appointment block.


## 5. Nonfunctional Requirements

### NFR01
**Ease of Use**<br/>
The website shall be easy to navigate and usable on smartphones and desktop computers.
The V1 client interface shall be in English.

### NFR02
**Server Responds Promptly**<br/>
Appointment availability, screening results, and confirmations shall respond promptly
under ordinary site usage.

### NFR03
**PII Protection**<br/>
Public appointment listings shall never disclose other clients' names, contact
information, or screening details.

### NFR04
**PII Collection Limits**<br/>
The system shall collect only the information needed for screening and scheduling. V1
shall not require Social Security numbers, street addresses, or uploaded taxpayer
documents.

### NFR05
**Admin Privilege Protections**<br/>
Protected client and staff operations shall be checked by the server. A user must not
gain access merely by changing an appointment ID or claiming another role.

### NFR06
**Concurrent Reservation Handling**<br/>
Concurrent reservation requests must not cause capacity violations or conflicting
records. Database transactions shall prevent partial saves.

### NFR07
**Persistent Information Retention**<br/>
Confirmed appointments, cancellations, and authorized schedule changes shall remain
available after a normal application restart.



## 6. Business Rules

### BR01
**One Appointment Per Household**<br/>
Each household is permitted one and only one appointment across the program, regardless
of the booking channel or service location.

### BR02
**Household Definition**<br/>
One household appointment covers the taxpayer, spouse, and dependents. Spouses filing
Married Filing Separately are still covered by one appointment, even if two returns are
prepared.

### BR03
**Screening Requirement**<br/>
A household must complete and pass preliminary screening before selecting an appointment.

### BR04
**Household Income Limit**<br/>
The general income eligibility limit is $89,000 or less in prior-year household gross
income, based on the Hartwick VITA site's stated policy.

### BR05
**Income Excemptions**<br/>
Seniors age 65 or older, veterans, active military personnel, and individuals with
disabilities qualify for an exemption from the general income limit.

### BR06
**No Scheduling Priority**<br/>
All eligible households have equal appointment priority. No specific group have earlier
scheduling priority.

### BR07
**Appointment Expectations**<br/>
Each appointment lasts one hour and includes the taxpayer interview, return preparation,
and quality review.

### BR08
**Capacity**<br/>
The standard capacity is eight households per one-hour appointment block, subject to
authorized adjustments.

### BR09
**Site-Specific Service Schedules**<br/>
Appointment dates and hours must follow the approved campus, Saturday library, and Friday
mobile-service schedules, which have been described on the shared documents.

### BR10
**Reservation Requirements**<br/>
A new reservation may be confirmed only for an open service date, an available block, and
an eligible household.

### BR11
**Capacity Limit**<br/>
The number of confirmed appointments must never exceed the block's authorized capacity,
including when multiple booking channels submit requests simultaneously.

### BR12
**Available Capacity Calculation**<br/>
Available capacity is calculated from active booked appointments.

### BR13
**Household Identity Limitations**<br/>
Name, phone number, and ZIP code, individually or together, are not sufficient to
establish a unique household identity.

### BR14
**Cancelation Requirement**<br/>
Clients may cancel an appointment at least 24 hours before its scheduled start time.

### BR15
**Time Slot Release Upon Cancelation**<br/>
A successful cancellation immediately releases one place after the cancellation is saved.
The cancelled appointment record remains in the database.

### BR16
**Service Block Management Limit**<br/>
A service block containing booked appointments cannot be silently moved or deleted.


## 7. Requirements Refinement Record
| Date | Statement / Requirement | Problem Found | Evidence / Reason | Revised Statement |
| ---- | ----------------------- | ------------- | ----------------- | ----------------- |
| 10/28/2026 | Document created ||||
| 10/29/2026 | Scope ||| Scope statements added |
| 10/29/2026 | Requirements ||| Requirements/Rules added |
| 10/6/2026 | Stakeholders | Stakeholder interests/needs not clear | Needs should be clearly defined | Refined stakeholder interests/needs |
| 11/11/2026 | Functional Requirements ||| Category fully replaced by class composite |
| 11/11/2026 | Non-Functional Requirements ||| Category fully replaced by class composite |
| 11/11/2026 | Business Rules ||| Category fully replaced by class composite |