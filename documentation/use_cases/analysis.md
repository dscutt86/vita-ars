# Use Case Analysis


## 1. Actor Analysis
| Role / External System | Actor and/or Stakeholder? | Primary / Supporting | Interaction and/or Interest? |
| ---------------------- | ------------------------- | -------------------- | ---------------------------- |
| Coordinator | Both | Primary | Management of Schedule and Appointments |
| Volunteer | Stakeholder | Primary | Provide Services Per Schedule and Appointments |
| Client | Both | Primary | Reserve Appointments |


## 2. Use Cases
| Candidate Use Case | Primary Actor | Related FR's | Actor Goal/Value |
| ------------------ | ------------- | ------------ | ------------ |
| View Schedule and Appointments | Coordinator | FR11, FR13 | Manage schedule |
| Maintain Schedule and Appointments | Coordinator | FR12, FR14, FR15 | Manage schedule |
| Enforce One-Household Rule | Coordinator | FR11 | Manage schedule |
| Access Reservation System and Schedule | Client | FR01, FR03 | Request services |
| Screen for and Reserve Appointment | Client | FR02, FR03, FR04, FR05, FR07 | Request services |
| Review and Cancel Reservation | Client | FR06, FR08, FR09, FR10, FR16 | Request services |


## 3. Use Case Example - Reserve Appointment
1. Primary Actor: Client
2. Goal: Successfully reserve an appointment.
3. Related FR's: FR01, FR02, FR03, FR04, FR05, FR07
4. Related BR's: BR01-BR06, BR08, BR10, BR12, BR13
5. Workflow
| Condition | Use Case Branch |
| --------- | --------------- |
| Success Workflow | Client goes to appointment reservation portal, online. |
|| Client clicks "Screen for an Appointment". |
|| HTTPS request generated and sent to the server to load screening page. |
|| Screening page template sent to client as response to request. |
|| Client answers screening questions and submits answers as HTTPS request. |
|| Server receives request and approves valid screening results. |
|| Server pulls open appointment slots in the schedule from the database. |
|| Appointment reservation page template loaded. |
|| Template and schedule data sent to client as response to request. |
|| Client enters first name, last name, zip code, and phone number into form. |
|| Client selects open appointment slot on in-page calendar. |
|| Client submits data as HTTPS request to server. |
|| Server validates reservation and saves it in the database. |
|| Server generates and sends confirmation code to client as response to request. |
|| Client receives confirmation and code for their appointment. |
| Candidate Does Not Pass Screening | Server receives request and denies failed screening results. |
|| Failed screening template sent to client as response to request. |
|| Client receives message that screening failed. |


## 4. NFR Check
| NFR | Use Case/Goal Affected | Testable? What is needed? |
| --- | ---------------------- | ------------------------- |
| NFR01 | Ease of Use | Access Reservation System |
| NFR02 | Server Responds Promptly | Acess Reservation System |
| NFR03 | PII | View Schedule and Appointments |
| NFR04 | PII Collection Limits | Screen For and Reserve Appointment |
| NFR05 | Admin Privilege Protections | View Schedule and Appointments |
| NFR06 | Concurrent Reservation Handling | Screen For and Reserve Appointment |
| NFR07 | Persistent Information Retention | Review and Cancel Reservation |