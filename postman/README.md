# KanMind Backend Regression Collection

A separate, repeatable Postman collection for the KanMind backend project.
The original development collection is not modified.

## What this collection does

The collection contains **142 requests and 142 named test blocks** in nine
ordered folders. A test block can contain several assertions. All 16 API
operations implemented in this project are exercised.

Each run creates five unique test accounts: owner, creator, reviewer, outsider,
and one account for email normalization. It creates its own board, tasks and
comments. Successful responses supply the IDs and tokens used by later requests.
Existing development fixtures are not used.

The final folder deletes the board and verifies that its remaining tasks and
comments are gone. The five user accounts remain because the documented API has
no user deletion endpoint. A failed run may also leave its test board and children.

This is a project regression suite, not a copy of the instructor's undisclosed
tests. A successful run does not establish source-code coverage or guarantee a
particular score on those tests. HTTP 500 scenarios are not intentionally induced.

## Files

- `KanMind_Backend_Regression.postman_collection.json`: import this file.
- `TEST_CASES.md`: request order, expected statuses and endpoint inventory.
- `ANLEITUNG_DE.md`: short German walkthrough.
- `STATIC_VALIDATION.txt`: checks performed on the collection before delivery.

## Prerequisites

- The backend and migrations are installed using the project's setup instructions.
- The latest implemented endpoints and fixes are available.
- Postman Desktop is installed.
- The Django development server is running.

For the current Windows project, run these commands in CMD:

```bat
cd /d C:\Users\Bastian\kanmind-backend
.venv\Scripts\activate.bat
python manage.py runserver
```

Keep that terminal open during the run. The collection does not install packages,
change the backend source, run migrations or start the server.

## Import and configuration

1. Extract the ZIP archive.
2. In Postman, choose **Import** and select the collection JSON file.
3. Open **KanMind Backend - Repeatable Regression**.
4. Select **No environment**.
5. Check the collection variable `kmr_base_url`:
   `http://127.0.0.1:8000/api` (no trailing slash).

No token, password or resource ID needs to be entered manually. All authenticated
requests include an explicit `Authorization: Token ...` header. Request auth is
set to **No Auth** to avoid generating a second authorization header.

Use the default variable name and prefix. An environment or runner data file with
the same variables can override configuration, so neither is needed here.

## Run the collection

1. Open the Collection Runner for this collection.
2. Select **all 142 requests** and keep their saved order.
3. Set **Iterations** to **1** and use no data file.
4. Run the collection.
5. Record the executed request count, passed tests and failed tests.

Expected outcome on a matching backend: **142 requests executed, 142 test blocks
passed, 0 failed**. This expected result still requires a real run against the
backend; the delivered static checks do not establish it.

Do not start a middle folder or use individual **Send** operations for this suite.
Its runtime variables depend on earlier requests in the same collection run.
Keep the original development collection for individual manual requests.

Each assertion block catches a failure, calls `pm.execution.setNextRequest(null)`
and rethrows the error. The runner then stops after the current request. This
prevents later dependent requests from producing misleading follow-up failures.
Use one iteration so there is no subsequent iteration to restart the sequence.
Network failures or runner-level errors must also be investigated; never treat a
partial run as a successful full run.

## How variables work

The first request's pre-request script creates unique email addresses, a password
and a due date 30 days in the future. It uses a generated GUID to distinguish runs.

For example, after creating a board, its response test stores the returned ID:

```javascript
pm.variables.set("kmr_board_id", data.id);
```

Later requests address that board using:

```text
{{kmr_base_url}}/boards/{{kmr_board_id}}/
```

IDs are inserted as numbers in JSON bodies. Email addresses and passwords are
inserted as strings. Tokens and resource IDs are local run variables, not written
to an environment or to the collection's saved variable list. The shipped JSON
contains no real tokens or saved response examples.

The numeric value `2147483647` is used only as an expected nonexistent object ID
in negative tests. It must not identify a real record in the development database.
All successful operations and cleanup use IDs captured from this run.

## Reading and changing a test

Open a request's response script to inspect the checks. The script names its
purpose, asserts the HTTP status, parses JSON where appropriate, and checks
response fields or state. Helpers such as `user`, `task` and `summary` are included
directly in the scripts that use them; there is no downloaded test library,
external script execution or hidden background API request.

Response-shape checks distinguish the documented representations:

- Board list/create: counts and `owner_id`.
- Board details: `members` and nested `tasks`.
- Board update: `owner_data` and `members_data`.
- Task create/personal lists: `board` and `comments_count` included.
- Task update: neither `board` nor `comments_count` included.
- Task inside board details: `comments_count`, without `board`.
- Comment: `id`, `created_at`, `author`, `content`.
- Successful deletion: HTTP 204 and an empty response body.

An intentional negative test can include unsupported or invalid input fields.
For example, the comment-author test tries to spoof the author and checks that
the authenticated user is used instead. It is not an example request for normal
frontend use.

## If a test fails

Record the first failed request's number and name, expected/actual status and
response body. Share those details without tokens or passwords. Do not change an
expected status simply to turn a failed test green; compare the API specification,
implementation and test setup first.

After fixing a problem, start a complete new run. Unique emails prevent duplicate
registration errors from the previous run. Cleanup does not run after an early
failure, which preserves the failed state for inspection.

To remove leftovers, use Django Admin and identify the run by its generated
`kmr.` email addresses and its board owner. Delete the run's board first, then its
test users if desired. Do not delete unrelated users or development fixtures.
Protected foreign keys can prevent user deletion while related objects remain.

## Scope that remains separate

- **Inactive login:** requires setting a user's `is_active` flag in Django Admin;
  the documented API does not expose that operation. Check active login succeeds,
  deactivate that same test user, expect login rejection, then reactivate it.
- **Browser/CORS and frontend behavior:** use the separate frontend integration
  checks; Postman does not enforce browser CORS rules.
- **Definition of Done:** code style, documentation, method length, English
  README, clean installation, repository contents and secret exclusion still
  need their own review.
- **Concurrent duplicate registration and performance:** not tested by this
  sequential regression run.

Several exploratory tests from the original collection are consolidated here.
This collection has no dependency on manually created admin fixtures, previous
request execution, fixed user IDs or hardcoded existing tokens.

## Save with the backend later

After the first successful real run, the collection and its documentation can be
stored under a backend repository folder such as `postman/`. Keep exported files
free of saved live tokens, credentials and response examples. Record the actual
run result separately; do not relabel the static validation report as a live test.

## Postman references

- [Local variables and scope](https://learning.postman.com/docs/tests-and-scripts/write-scripts/postman-sandbox-reference/pm-variables/)
- [Collection execution workflows](https://learning.postman.com/docs/tests-and-scripts/running-collections/building-workflows/)
