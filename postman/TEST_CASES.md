# Regression test inventory

142 requests; one named test block per request. A test block may contain multiple assertions.

## API operations

| Method | Endpoint |
| --- | --- |
| POST | `/api/registration/` |
| POST | `/api/login/` |
| GET | `/api/email-check/` |
| GET | `/api/boards/` |
| POST | `/api/boards/` |
| GET | `/api/boards/{board_id}/` |
| PATCH | `/api/boards/{board_id}/` |
| DELETE | `/api/boards/{board_id}/` |
| POST | `/api/tasks/` |
| PATCH | `/api/tasks/{task_id}/` |
| DELETE | `/api/tasks/{task_id}/` |
| GET | `/api/tasks/assigned-to-me/` |
| GET | `/api/tasks/reviewing/` |
| GET | `/api/tasks/{task_id}/comments/` |
| POST | `/api/tasks/{task_id}/comments/` |
| DELETE | `/api/tasks/{task_id}/comments/{comment_id}/` |

## 01 - Fresh users and authentication

| No. | Test | Method | Expected status |
| --- | --- | --- | --- |
| 001 | Register fresh owner | POST | 201 |
| 002 | Register fresh creator | POST | 201 |
| 003 | Register fresh reviewer | POST | 201 |
| 004 | Register fresh outsider | POST | 201 |
| 005 | Log in as owner | POST | 200 |
| 006 | Log in as creator | POST | 200 |
| 007 | Log in as reviewer | POST | 200 |
| 008 | Log in as outsider | POST | 200 |
| 009 | Reject duplicate email | POST | 400 |
| 010 | Reject mismatched passwords | POST | 400 |
| 011 | Require registration fields | POST | 400 |
| 012 | Reject invalid registration email | POST | 400 |
| 013 | Reject weak password | POST | 400 |
| 014 | Normalize email domain during registration | POST | 201 |
| 015 | Reject duplicate with uppercase domain | POST | 400 |
| 016 | Reject duplicate with normalized domain | POST | 400 |
| 017 | Log in using normalized email | POST | 200 |
| 018 | Reject wrong password | POST | 400 |
| 019 | Reject unknown login email | POST | 400 |
| 020 | Require login fields | POST | 400 |
| 021 | Look up registered member | GET | 200 |
| 022 | Failed registrations did not create a user | GET | 404 |
| 023 | Require email query parameter | GET | 400 |
| 024 | Reject invalid lookup email | GET | 400 |
| 025 | Require lookup authentication | GET | 401 |
| 026 | Reject invalid lookup token | GET | 401 |

## 02 - Board creation, visibility and updates

| No. | Test | Method | Expected status |
| --- | --- | --- | --- |
| 027 | Create board with two members | POST | 201 |
| 028 | Owner lists own board without membership | GET | 200 |
| 029 | Member lists accessible board | GET | 200 |
| 030 | Outsider sees empty board list | GET | 200 |
| 031 | Require board list authentication | GET | 401 |
| 032 | Reject board with unknown member | POST | 400 |
| 033 | Reject empty board title | POST | 400 |
| 034 | Require board creation authentication | POST | 401 |
| 035 | Owner retrieves board without membership | GET | 200 |
| 036 | Member retrieves board | GET | 200 |
| 037 | Reject outsider board details | GET | 403 |
| 038 | Unknown board details return 404 | GET | 404 |
| 039 | Require board details authentication | GET | 401 |
| 040 | Owner changes only board title | PATCH | 200 |
| 041 | Member replaces membership | PATCH | 200 |
| 042 | Removed member cannot update board | PATCH | 403 |
| 043 | Invalid member rejects entire board update | PATCH | 400 |
| 044 | Rejected board update leaves title unchanged | GET | 200 |
| 045 | Owner removes all board members | PATCH | 200 |
| 046 | Require board update authentication | PATCH | 401 |
| 047 | Unknown board update returns 404 | PATCH | 404 |
| 048 | Restore title and original members | PATCH | 200 |
| 049 | Owner membership does not duplicate board | PATCH | 200 |
| 050 | Combined ownership and membership counted once | GET | 200 |
| 051 | Restore owner without membership | PATCH | 200 |

## 03 - Task creation and validation

| No. | Test | Method | Expected status |
| --- | --- | --- | --- |
| 052 | Member creates task | POST | 201 |
| 053 | Outsider cannot create task | POST | 403 |
| 054 | Owner without membership cannot create task | POST | 403 |
| 055 | Require task creation authentication | POST | 401 |
| 056 | Unknown task board returns 404 | POST | 404 |
| 057 | Reject outsider assignee_id | POST | 400 |
| 058 | Reject outsider reviewer_id | POST | 400 |
| 059 | Reject unknown assignee and reviewer | POST | 400 |
| 060 | Require mandatory task fields | POST | 400 |
| 061 | Reject whitespace task title | POST | 400 |
| 062 | Reject invalid status and priority | POST | 400 |
| 063 | Reject impossible due date | POST | 400 |
| 064 | Apply defaults to minimal task | POST | 201 |
| 065 | Accept explicit null assignments | POST | 201 |
| 066 | Only valid tasks exist in board details | GET | 200 |
| 067 | Board counters include created tasks | GET | 200 |

## 04 - Task updates, assignments and counters

| No. | Test | Method | Expected status |
| --- | --- | --- | --- |
| 068 | Change task title only | PATCH | 200 |
| 069 | Another member changes status and priority | PATCH | 200 |
| 070 | Counters reflect changed status and priority | GET | 200 |
| 071 | Reject moving task to another board | PATCH | 400 |
| 072 | Rejected move leaves task unchanged | GET | 200 |
| 073 | Outsider cannot update task | PATCH | 403 |
| 074 | Owner without membership cannot update task | PATCH | 403 |
| 075 | Require task update authentication | PATCH | 401 |
| 076 | Unknown task update returns 404 | PATCH | 404 |
| 077 | Reject outsider assignment on update: assignee_id | PATCH | 400 |
| 078 | Reject outsider assignment on update: reviewer_id | PATCH | 400 |
| 079 | Clear assignee without changing reviewer | PATCH | 200 |
| 080 | Restore assignee and clear reviewer | PATCH | 200 |
| 081 | Restore original task data | PATCH | 200 |
| 082 | Counters return to original values | GET | 200 |
| 083 | Remove reviewer from board | PATCH | 200 |
| 084 | Reject stale reviewer assignment on update | PATCH | 400 |
| 085 | Clear stale reviewer assignment | PATCH | 200 |
| 086 | Restore reviewer board membership | PATCH | 200 |
| 087 | Restore reviewer assignment | PATCH | 200 |

## 05 - Personal task lists

| No. | Test | Method | Expected status |
| --- | --- | --- | --- |
| 088 | List tasks for authenticated assignee | GET | 200 |
| 089 | Exclude users without assignee assignment | GET | 200 |
| 090 | Require authentication for assignee list | GET | 401 |
| 091 | List tasks for authenticated reviewer | GET | 200 |
| 092 | Exclude users without reviewer assignment | GET | 200 |
| 093 | Require authentication for reviewer list | GET | 401 |

## 06 - Comment creation, listing and validation

| No. | Test | Method | Expected status |
| --- | --- | --- | --- |
| 094 | Member creates first comment | POST | 201 |
| 095 | Another member reads comments | GET | 200 |
| 096 | Reject whitespace comment | POST | 400 |
| 097 | Require comment content | POST | 400 |
| 098 | Outsider cannot create comment | POST | 403 |
| 099 | Outsider cannot read comments | GET | 403 |
| 100 | Require comment creation authentication | POST | 401 |
| 101 | Require comment list authentication | GET | 401 |
| 102 | Cannot comment on unknown task | POST | 404 |
| 103 | Cannot list comments of unknown task | GET | 404 |
| 104 | Existing task without comments returns empty list | GET | 200 |
| 105 | Comment author comes from token, not body | POST | 201 |
| 106 | Only valid comments appear in chronological order | GET | 200 |
| 107 | Task comment counter increases | GET | 200 |

## 07 - Comment deletion and ID validation

| No. | Test | Method | Expected status |
| --- | --- | --- | --- |
| 108 | Task creator cannot delete another author comment | DELETE | 403 |
| 109 | Board owner cannot delete another author comment | DELETE | 403 |
| 110 | Require comment deletion authentication | DELETE | 401 |
| 111 | Comment cannot be deleted through wrong task | DELETE | 404 |
| 112 | Unknown comment deletion returns 404 | DELETE | 404 |
| 113 | Reject malformed comment ID | DELETE | 400 |
| 114 | Reject malformed task ID during comment deletion | DELETE | 400 |
| 115 | Authenticate before comment ID validation | DELETE | 401 |
| 116 | Author deletes own comment | DELETE | 204 |
| 117 | Repeated comment deletion returns 404 | DELETE | 404 |
| 118 | Other comment remains after deletion | GET | 200 |
| 119 | Task comment counter decreases | GET | 200 |

## 08 - Task deletion and cascading comments

| No. | Test | Method | Expected status |
| --- | --- | --- | --- |
| 120 | Create separate task for deletion | POST | 201 |
| 121 | Create comment on task to be deleted | POST | 201 |
| 122 | Assigned member cannot delete task they did not create | DELETE | 403 |
| 123 | Outsider cannot delete task | DELETE | 403 |
| 124 | Require task deletion authentication | DELETE | 401 |
| 125 | Reject malformed task ID | DELETE | 400 |
| 126 | Authenticate before task ID validation | DELETE | 401 |
| 127 | Task creator deletes own task | DELETE | 204 |
| 128 | Repeated task deletion returns 404 | DELETE | 404 |
| 129 | Task deletion also removes its comment | DELETE | 404 |
| 130 | Owner without membership deletes another user task | DELETE | 204 |
| 131 | Board counters reflect task deletion | GET | 200 |

## 09 - Board deletion, cascade and final cleanup

| No. | Test | Method | Expected status |
| --- | --- | --- | --- |
| 132 | Member cannot delete board | DELETE | 403 |
| 133 | Require board deletion authentication | DELETE | 401 |
| 134 | Owner deletes board | DELETE | 204 |
| 135 | Repeated board deletion returns 404 | DELETE | 404 |
| 136 | Deleted board cannot be retrieved | GET | 404 |
| 137 | Board deletion removes main task | PATCH | 404 |
| 138 | Board deletion removes minimal task | PATCH | 404 |
| 139 | Board deletion removes remaining comment | DELETE | 404 |
| 140 | Owner board list is empty after cleanup | GET | 200 |
| 141 | Assignee list is empty after cleanup | GET | 200 |
| 142 | Reviewer list is empty after cleanup | GET | 200 |
