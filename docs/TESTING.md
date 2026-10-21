# Testing and Verification

[Project README](../README.md) ·
[Architecture](ARCHITECTURE.md) ·
[Data Model](DATA_MODEL.md) ·
[Authentication and Permissions](AUTH_AND_PERMISSIONS.md) ·
[Design Decisions](DESIGN_DECISIONS.md)

---

## Contents

- [Testing and Verification](#testing-and-verification)
  - [Contents](#contents)
  - [Testing Approach](#testing-approach)
  - [Recorded Results](#recorded-results)
  - [Postman Regression Suite](#postman-regression-suite)
    - [Files](#files)
    - [Coverage areas](#coverage-areas)
    - [Running the collection](#running-the-collection)
    - [Expected outcome](#expected-outcome)
  - [Test Data and Cleanup](#test-data-and-cleanup)
    - [Independent test accounts](#independent-test-accounts)
    - [Cleanup after success](#cleanup-after-success)
    - [Cleanup after failure](#cleanup-after-failure)
  - [Investigating Failures](#investigating-failures)
  - [Frontend Integration](#frontend-integration)
    - [Browser workflow](#browser-workflow)
  - [Administration Checks](#administration-checks)
    - [Inactive-user login check](#inactive-user-login-check)
  - [Static and Configuration Checks](#static-and-configuration-checks)
  - [Fresh Installation Verification](#fresh-installation-verification)
    - [Procedure](#procedure)
    - [Record the result](#record-the-result)
  - [Choosing Checks After Changes](#choosing-checks-after-changes)
  - [Limits of the Evidence](#limits-of-the-evidence)

---

## Testing Approach

KanMind combines API regression tests with browser integration checks,
Django checks and source review.

| Check | Purpose |
| --- | --- |
| Postman regression | Verify API behavior, response shapes, validation and permissions |
| Browser integration | Verify communication with the provided frontend and browser CORS behavior |
| Django Admin checks | Verify administration access and inspect related data |
| Django system checks | Detect supported configuration and model issues |
| Migration consistency | Detect model changes without corresponding migrations |
| Dependency checks | Detect incompatible installed package requirements |
| Source review | Review structure, documentation, conventions and method length |
| Fresh installation | Verify that another developer can start from the repository alone |

These checks provide different evidence. None replaces all the others.

## Recorded Results

| Area | Recorded result |
| --- | --- |
| Postman regression | 142 passed, 0 failed |
| Django system checks | No issues identified |
| Migration consistency | No changes detected |
| Git whitespace checks | No reported errors |
| Dependency consistency | No broken requirements found |
| Frontend integration | Authentication and board, task and comment workflows exercised |
| Fresh installation from the final README | Pending |
| Linux installation | Not yet practically verified |
| macOS installation | Not yet practically verified |

The regression result records a completed development run. It is not a live
CI status and does not automatically apply to later code changes.

## Postman Regression Suite

### Files

- [Collection](../postman/KanMind_Backend_Regression.postman_collection.json)
- [Collection instructions](../postman/README.md)
- [Complete test inventory](../postman/TEST_CASES.md)

The collection contains **142 requests and 142 named test blocks**.
A test block can contain multiple assertions.

It exercises all 16 implemented API operations.

### Coverage areas

| Folder | Main checks |
| --- | --- |
| 01 — Fresh users and authentication | Registration, login, email normalization and lookup |
| 02 — Board creation, visibility and updates | Ownership, membership, visibility and partial updates |
| 03 — Task creation and validation | Required fields, defaults, assignments and denied access |
| 04 — Task updates, assignments and counters | Partial updates, retained assignments and board statistics |
| 05 — Personal task lists | Assignee and reviewer filtering |
| 06 — Comment creation, listing and validation | Content validation, authorship, ordering and counts |
| 07 — Comment deletion and ID validation | Author permissions, parent-task matching and malformed IDs |
| 08 — Task deletion and cascading comments | Creator/owner permissions and dependent comment removal |
| 09 — Board deletion, cascade and final cleanup | Owner-only deletion and removal of dependent resources |

### Running the collection

1. Complete backend installation and apply migrations.
2. Start the development server.
3. Import the collection JSON file into Postman Desktop.
4. Open **KanMind Backend - Repeatable Regression**.
5. Select **No environment**.
6. Confirm `kmr_base_url` is `http://127.0.0.1:8000/api`.
7. Open the Collection Runner.
8. Select all 142 requests in their saved order.
9. Set iterations to one and use no data file.
10. Start the run.

Do not enter tokens or resource IDs manually.

The requests send explicit authorization headers. Their Postman authorization
setting is **No Auth** to avoid generating an additional header.

The suite depends on data created earlier in the same run. Running a middle
folder or sending an individual request is not equivalent to a complete run.

### Expected outcome

A successful full run reports:

```text
142 requests executed
142 test blocks passed
0 failed
```

Also check for network errors, skipped requests and early termination.
A partial run with no visible failed assertions is not sufficient evidence.

The assertion scripts stop the request sequence after a caught test failure.
This helps avoid misleading errors from later dependent requests.

## Test Data and Cleanup

### Independent test accounts

Each run generates unique credentials for five accounts:

- Board owner
- Task creator
- Reviewer
- Outsider
- Email normalization tester

The collection captures returned IDs and tokens for later requests.

Tokens and generated values use local run variables rather than being saved
into the collection or an environment.

Existing development accounts and hardcoded successful resource IDs are not
required.

Negative tests use `2147483647` as an expected nonexistent object ID.
That ID must not identify an existing record in the database being tested.

### Cleanup after success

The final folder deletes the test board and checks the removal of dependent
tasks and comments.

The five generated users remain because the API has no user deletion endpoint.

### Cleanup after failure

An early failure can leave the run's board, tasks and comments in place.
This state can help explain the failure.

If manual cleanup is needed:

1. Identify the run through its generated `kmr.` email addresses.
2. Identify its board through the corresponding owner.
3. Delete only that run's board and related test data.
4. Remove its generated users if desired.

Protected relationships can prevent deleting users while their boards,
created tasks or authored comments remain.

Do not delete unrelated users or development fixtures.

## Investigating Failures

Record the first failing request:

| Information | Example |
| --- | --- |
| Request name | Reject malformed comment ID |
| Method and path | `DELETE /api/tasks/{task_id}/comments/abc/` |
| Expected status | `400` |
| Actual status | Status returned by the server |
| Response body | Relevant JSON or error text |
| Assertion message | The failed condition reported by Postman |
| Backend output | Relevant error or traceback, if present |

Remove tokens and passwords before sharing results.

Check the following before changing application code:

- Is the backend running from the intended project and virtual environment?
- Were all migrations applied?
- Did the collection start at its first request?
- Was the correct base URL used?
- Did an earlier request fail to create required data?
- Does the request use the intended user's token?
- Does the expected result match the API contract?

Do not change an expected status simply to make a failing test pass.

After correcting a failure, start a new complete run. The generated credentials
allow the new run to create independent accounts.

## Frontend Integration

Postman verifies HTTP behavior but does not enforce browser CORS rules.

Use the provided frontend separately with:

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5501`

Use a dedicated test account and board for destructive checks.

### Browser workflow

1. Register or log in.
2. Open the dashboard and inspect the board-list request.
3. Create a board.
4. Retrieve its details.
5. Add the required members, including the owner if they will create tasks.
6. Create a task with an assignee and reviewer.
7. Change the task status.
8. Create a comment.
9. Delete the comment as its author.
10. Delete the task as its creator or board owner.
11. Delete the board as its owner.

Inspect both the interface and the browser's Network panel.

Check that:

- Requests reach the expected API routes.
- Successful responses contain the expected data.
- Protected requests send the authorization header.
- The browser accepts the configured CORS response.
- Deleted resources disappear from the interface.
- HTTP 204 responses have an empty body.

After changing board membership, refresh the page if assignment selectors
still show the previous members.

The integration workflow above was exercised during development.
It does not replace the more detailed permission checks in Postman.

## Administration Checks

Django Admin provides a separate interface for maintenance and inspection.

Check that:

- A created superuser can log in using email.
- Users, boards, tasks and comments are available in Admin.
- Object labels are readable.
- Related-object selections work.
- Board ordering is consistent.

### Inactive-user login check

The regression collection cannot deactivate a user because the API does not
provide that operation.

For a manual check:

1. Create a dedicated regular test user.
2. Confirm that the user can log in.
3. Disable that user's `is_active` flag in Admin.
4. Repeat login with the same credentials.
5. Expect HTTP 400 with the invalid-credentials response.
6. Restore the user's active status if the account is still needed.

Use a separate administrator account for this check.

Admin changes do not automatically execute API serializer validation.
Take care when modifying relationships used by subsequent API tests.

## Static and Configuration Checks

Run these commands from the backend directory with its virtual environment
activated:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python -m pip check
git diff --check
```

| Command | What it establishes |
| --- | --- |
| `manage.py check` | Django reports no issues covered by its system checks |
| `makemigrations --check --dry-run` | Model changes do not require an uncommitted migration |
| `pip check` | Installed dependencies satisfy their declared requirements |
| `git diff --check` | The current diff has no reported whitespace errors |

These commands do not establish complete runtime correctness or full
PEP 8 compliance.

Source review additionally checks:

- Small methods with one responsibility
- The project's maximum method length of 14 lines
- Explicit serializer fields
- Declared permission classes
- Dynamic filtering in `get_queryset()`
- English documentation
- Import organization and formatting
- Absence of leftover debug prints and commented-out implementation code

Documentation review also checks relative links, command examples and
consistency with the actual implementation.

## Fresh Installation Verification

This is a separate acceptance check for the repository and setup guide.

Use a new checkout in a separate directory. Keep the existing development
installation intact.

### Procedure

1. Clone the intended submission revision.
2. Record its commit hash with `git rev-parse HEAD`.
3. Follow the README instructions for the operating system.
4. Create a new virtual environment.
5. Install the pinned requirements.
6. Create `.env` from `.env.example` and generate a new secret key.
7. Apply committed migrations to create a new database.
8. Run the configuration and dependency checks.
9. Create an administrator and verify admin login.
10. Start the backend.
11. Run the complete Postman regression collection.
12. Verify frontend access using the documented origin.

Do not copy the development database, virtual environment, tokens or `.env`
into the fresh installation.

If another backend is already using port 8000, stop that server before
starting the fresh installation. This prevents accidentally testing the old
process.

### Record the result

Record:

- Operating system and shell
- Python version
- Tested commit hash
- Any setup deviations
- System-check and migration results
- Complete Postman result
- Admin and frontend observations

Only mark an operating system as verified after actually completing its
installation checks.

Windows development use does not by itself prove that the final README
works from a clean checkout.

## Choosing Checks After Changes

| Change | Relevant verification |
| --- | --- |
| Documentation only | Review wording, examples, links and formatting |
| Serializer validation | Relevant successful and invalid requests |
| Permissions | Allowed and denied requests with different users |
| Queryset filtering | Visibility, empty results and duplicate prevention |
| Response representation | Exact keys, types, nested values and counts |
| Model relationships | Migration review and affected data/deletion behavior |
| Authentication | Registration, login and protected-request behavior |
| CORS settings | Browser request from the intended frontend origin |
| Dependencies or setup | Dependency checks and fresh installation |
| Final behavioral release | Complete regression run and relevant integration checks |

After a focused fix, check the behavior it affects. Run the complete regression
suite for the final behavioral revision.

Pure documentation changes do not require repeating every API test unless
they reveal an implementation discrepancy.

## Limits of the Evidence

The recorded results do not establish:

- Source-code test coverage
- A guaranteed score on the instructor's undisclosed tests
- Behavior under concurrent duplicate requests
- Load capacity or production performance
- Production security readiness
- Verified Linux or macOS installation
- Every possible administrative or manually edited database state

HTTP 500 scenarios are not deliberately induced as part of the required
assessment tests.

Unexpected HTTP 500 responses during ordinary requests are still defects
to investigate and correct.

A Postman test block passing means its assertions passed for that run.
It is not evidence that every possible input or state has been tested.

---

[Back to contents](#contents) · [Project README](../README.md)