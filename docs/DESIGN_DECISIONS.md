# Design Decisions

[Project README](../README.md) ·
[Architecture](ARCHITECTURE.md) ·
[Data Model](DATA_MODEL.md) ·
[Authentication and Permissions](AUTH_AND_PERMISSIONS.md) ·
[Testing](TESTING.md)

---

## Contents

- [Design Decisions](#design-decisions)
  - [Contents](#contents)
  - [Purpose](#purpose)
  - [1. Implement the Provided API Contract](#1-implement-the-provided-api-contract)
  - [2. Separate Domain Apps and API Code](#2-separate-domain-apps-and-api-code)
  - [3. Use a Custom Email-Based User](#3-use-a-custom-email-based-user)
  - [4. Use DRF Token Authentication](#4-use-drf-token-authentication)
  - [5. Separate Input and Response Serializers](#5-separate-input-and-response-serializers)
  - [6. Combine Permissions with Relationship Validation](#6-combine-permissions-with-relationship-validation)
  - [7. Keep Ownership and Membership Independent](#7-keep-ownership-and-membership-independent)
  - [8. Make Partial Updates Explicit](#8-make-partial-updates-explicit)
  - [9. Calculate Counts from Relationships](#9-calculate-counts-from-relationships)
  - [10. Define Deletion Behavior Explicitly](#10-define-deletion-behavior-explicitly)
  - [11. Group Related Writes in Transactions](#11-group-related-writes-in-transactions)
  - [12. Use SQLite and Environment Configuration](#12-use-sqlite-and-environment-configuration)
  - [13. Test with Independent Postman Data](#13-test-with-independent-postman-data)
  - [14. Keep the Implementation Direct](#14-keep-the-implementation-direct)
  - [When to Revisit These Decisions](#when-to-revisit-these-decisions)

---

## Purpose

This document explains how the implemented choices support the project's
requirements and what their practical limits are.

It describes the current implementation. Alternative approaches mentioned
here are trade-offs, not a claim that every alternative was prototyped.

## 1. Implement the Provided API Contract

**Decision:** Match the required routes, methods, field names, response
representations and status codes.

The frontend is provided separately. Its requests and response handling
depend on a compatible backend.

Consequently, response shapes intentionally differ between operations.
For example, board updates return `owner_data` and `members_data`, while
board details return `owner_id`, `members` and `tasks`.

**Consequence:** Consistency with the contract takes priority over making
every endpoint return an identical representation.

Changing a field name or adding an operation requires checking the contract
and frontend expectations first.

## 2. Separate Domain Apps and API Code

**Decision:** Organize the project into `auth_app`, `boards_app` and
`tasks_app`, with API code inside each app's `api/` directory.

This makes the main business areas easy to locate and follows the course's
structural conventions.

Models and administration remain at app level. Serializers, API views,
permissions and API routes remain together under `api/`.

Comments belong to `tasks_app` because they depend on tasks and are accessed
through task URLs. Separate comment view and serializer files keep their
implementation navigable.

**Trade-off:** Apps still depend on shared models and serializers. They are
logical modules within one Django application, not independent services.

## 3. Use a Custom Email-Based User

**Decision:** Extend `AbstractUser`, remove `username` and use a unique
email address as `USERNAME_FIELD`.

This supports email-based authentication while retaining Django's password,
permission and administration infrastructure.

A custom manager handles regular user and superuser creation. Dedicated
admin forms support the custom account fields.

**Consequence:** Relationships reference `settings.AUTH_USER_MODEL`, and
runtime code uses `get_user_model()` where appropriate.

The custom user was introduced before the initial database migration.
Replacing the user model after a project already contains data would require
a separate migration plan.

Registration normalizes the email domain before checking uniqueness.
This prevents the previously observed mismatch between validation and
manager-level normalization.

**Limit:** Domain normalization does not make every email lookup
case-insensitive.

## 4. Use DRF Token Authentication

**Decision:** Use DRF's database-backed token authentication for the API.

It supplies the token response expected by registration and login and works
with both the provided frontend and Postman.

Protected requests use:

```http
Authorization: Token <token>
```

Login retrieves or creates the user's token. It does not issue a new token
on every successful login.

**Trade-off:** The project has no token refresh, logout or revocation API.
Client-side logout alone does not invalidate the stored token.

Django Admin continues to use its separate session authentication.

## 5. Separate Input and Response Serializers

**Decision:** Use dedicated serializers where accepted input and returned
data have different structures.

Task input accepts user IDs. Task responses contain nested user objects.
Board input accepts member IDs, while its output varies by operation.

Separate serializers make editable fields and output fields explicit.
They also prevent response-only fields from becoming writable through a
shared serializer.

Task response serializers reuse `BoardTaskSerializer` where their fields
overlap.

**Trade-off:** There are more serializer classes to maintain. Their purpose
is to represent actual contract differences rather than hypothetical future
variations.

## 6. Combine Permissions with Relationship Validation

**Decision:** Use permission classes for access to existing objects and
serializer validation for submitted relationships.

An existing task can be checked through its board during object lookup.
A task being created does not yet exist, so its submitted board is resolved
and checked in the write serializer.

The serializer also checks whether selected assignees and reviewers belong
to that board.

**Consequence:** Declaring an object permission on a view is not sufficient
to protect creation or filter every item in a list.

Board and personal task lists apply their own queryset filters. Comment
creation explicitly checks access to the parent task.

These checks have different responsibilities and must remain coordinated.

## 7. Keep Ownership and Membership Independent

**Decision:** Represent board ownership with a foreign key and membership
with a separate many-to-many relationship.

Ownership identifies who controls board deletion. Membership identifies
participation for task creation, task updates and comment access.

This permits an owner to manage a board without automatically participating
in its tasks.

**Consequence:** Owners who want to create or update tasks must also be
members. The frontend may require a refresh after membership changes.

Task deletion and comment deletion use their own relationships:
creator or board owner for tasks, author for comments.

There is no general rule that a board owner may perform every operation.

## 8. Make Partial Updates Explicit

**Decision:** Use PATCH with `partial=True` and distinguish omitted fields
from explicit `null` values.

An omitted assignment preserves the current user.
An explicit `null` clears the assignment.

The task serializer validates the effective assignments after combining
submitted and retained values. This prevents an unrelated update from
silently accepting a retained assignment to a former member.

**Trade-off:** Removing a member can leave an assignment that blocks later
task updates. A permitted user must clear it, replace it or restore membership.

The board membership update does not silently rewrite task assignments.

**Additional decision:** Prevent moving a task to another board through PATCH.

Moving a task would affect membership checks, assignments and access to its
comments. The current API rejects that change rather than implementing an
implicit transfer workflow.

## 9. Calculate Counts from Relationships

**Decision:** Produce board statistics and task comment counts through
queryset annotations.

This keeps counts connected to the underlying records. No separate counter
needs updating whenever a task, membership or comment changes.

Board counts use distinct aggregation to avoid inflation when joins include
multiple relationships.

Related users, members and tasks are loaded with `select_related()` and
`prefetch_related()` where used by the response serializers.

**Trade-off:** Aggregations and related-object loading have a database cost.
The project has not established performance limits through load testing.

Persistent counters or caching would require a demonstrated need and a
strategy for keeping values correct.

## 10. Define Deletion Behavior Explicitly

**Decision:** Use relationship-specific deletion rules.

- `CASCADE` removes dependent tasks and comments.
- `SET_NULL` permits optional assignments to be cleared on user deletion.
- `PROTECT` prevents deleting users referenced as owners, creators or authors.

Deleting a board removes its contained work, but does not delete the users
who participated in it.

**Consequence:** User cleanup may be blocked by protected relationships.
The API does not expose user deletion.

These rules preserve the distinction between deleting a resource, removing
membership and deleting an account.

## 11. Group Related Writes in Transactions

**Decision:** Wrap selected creation and update operations in
`transaction.atomic`.

For example, registration creates a user and token together. Board writes
can update both the board and its membership links.

If an exception escapes the atomic block, its database changes are rolled
back.

**Limit:** Transactions do not replace input validation or access checks.
They also do not automatically solve every concurrent-request conflict.

The regression collection tests sequential behavior, not concurrency.

## 12. Use SQLite and Environment Configuration

**Decision:** Use SQLite for local persistence and `.env` for local settings.

SQLite meets the project's local setup requirements without requiring a
separate database service.

The repository includes migrations and `.env.example`, while excluding the
database and actual `.env`.

Dependencies are pinned in `requirements.txt` to make the Python environment
reproducible.

**Trade-off:** The recorded working environment is Windows. Linux and macOS
installation instructions still require practical verification.

The current configuration is intended for local development and assessment.
Production operation would require a separate configuration and review.

## 13. Test with Independent Postman Data

**Decision:** Maintain a repeatable regression collection that creates its
own accounts, boards, tasks and comments.

Later requests use IDs and tokens returned by earlier requests.
The collection does not depend on manually prepared development fixtures.

This makes permission checks repeatable across owner, creator, reviewer
and outsider accounts.

**Trade-off:** The collection must run in its saved order. Successful cleanup
removes its board and related objects, but five generated users remain.

A failed run may preserve additional data for investigation.

The recorded result is 142 passed and 0 failed. This is not a measurement
of source-code coverage or a guarantee about undisclosed assessment tests.

## 14. Keep the Implementation Direct

**Decision:** Use Django models, DRF serializers, permissions and views
directly for the current application scope.

The project does not introduce a separate repository or service layer.
The ORM already provides database access, and the existing operations fit
within small, focused methods.

Framework behavior is reused where it matches the contract. Explicit
methods handle special response shapes and additional validation.

English docstrings explain responsibilities. The project convention limits
functions and methods to 14 lines.

**Trade-off:** Keeping methods short must not obscure the execution path.
Additional abstractions should solve an observed problem, such as duplicated
workflows or growing coordination logic.

## When to Revisit These Decisions

| Change in requirements | Decision to review |
| --- | --- |
| Production operation | Secrets, hosts, HTTPS, logging, database and token lifecycle |
| Concurrent or high-volume usage | Transactions, constraints, query behavior and database choice |
| Task transfer between boards | Assignment validation, comment access and transfer permissions |
| Automated membership cleanup | Whether to clear or replace assignments when membership changes |
| API contract changes | Routes and operation-specific serializers |
| More complex business workflows | Whether a dedicated service layer improves clarity |
| Automated test execution | How to integrate regression checks into a repeatable CI process |

These are review triggers, not features already implemented.

---

[Back to contents](#contents) · [Project README](../README.md)