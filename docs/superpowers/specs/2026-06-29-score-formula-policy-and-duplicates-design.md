# Versioned Scoring Formula And Duplicate Review Design

## Context

The HR performance system currently calculates monthly raw work scores from six business tables:

- `Orders`
- `Cutovers`
- `Posts`
- `Routine`
- `Faulty`
- `Bonuses`

`scores.views.updateScoreOfWorkers()` writes raw monthly category totals into `Scores`. Ranking then uses `getJixiao()` to turn those raw category scores into a final work score. The current active ranking formula is a hard cap style:

- project score is not compressed
- special bonus score is not compressed
- orders + cutovers + faulty + routine are capped at 40

There is also an older exponential compression function, `getJixiao2021()`, where a category approaches a configured maximum as work quantity increases:

```python
cap * (1 - exp(-lambda_value * raw_score))
```

The new requirement is to let superusers configure ranking formulas through the Django admin, keep historical rankings stable by formula effective month, support future annual ranking, and reduce duplicate submissions without blocking legitimate work.

## Goals

1. Let superusers choose the ranking formula from the admin.
2. Let superusers configure compression behavior per work category.
3. Support both compressed and uncompressed scoring.
4. Apply formula changes by effective month so historical rankings remain stable.
5. Store monthly ranking snapshots with formula parameters for future annual ranking and audit.
6. Detect likely duplicate work submissions.
7. Allow duplicate-looking work to proceed only when an approver explicitly confirms it.

## Non-Goals

1. This design does not add the annual ranking page yet.
2. This design does not rebuild the existing business tables.
3. This design does not force duplicate submission blocking at user submission time.
4. This design does not add multi-participant fields to `Cutovers`; the current `Cutovers` model only has `pj_leader`.

## Data Model

### `ScoreFormulaPolicy`

Create this model in `scores.models`.

Purpose: represent one versioned ranking formula.

Fields:

- `name`: human-readable policy name, such as `2026下半年绩效公式`
- `effective_year`: integer
- `effective_month`: integer, 1-12
- `ranking_formula`: choice field
  - `legacy_cap40`
  - `compressed_sum`
  - `raw_sum`
- `is_active`: boolean
- `notes`: text, optional
- `created_at`
- `updated_at`

Rules:

- Only active policies are candidates for ranking.
- The active policy for a target month is the active policy with the latest effective year/month less than or equal to the target year/month.
- If no policy exists, create or fall back to a default `legacy_cap40` policy.
- Superusers manage policies in Django admin.

### `ScoreCategoryRule`

Create this model in `scores.models`.

Purpose: configure how each category contributes under a policy.

Fields:

- `policy`: foreign key to `ScoreFormulaPolicy`
- `category`: choice field
  - `posts`
  - `orders`
  - `cutovers`
  - `bonuses`
  - `routine`
  - `faulty`
- `algorithm`: choice field
  - `none`
  - `exponential`
  - `hard_cap`
- `cap`: float, default `0`
- `lambda_value`: float, default `0`
- `weight`: float, default `1`

Rules:

- Unique constraint: `policy + category`.
- `none`: `raw_score * weight`
- `hard_cap`: `min(raw_score, cap) * weight`
- `exponential`: `cap * (1 - exp(-lambda_value * raw_score)) * weight`
- For `legacy_cap40`, category rules may exist for documentation, but the legacy calculation is applied as a whole formula for compatibility with current behavior.

### `ScoreRankingSnapshot`

Create this model in `scores.models`.

Purpose: preserve the monthly ranking result and the formula used to generate it.

Fields:

- `worker_name`
- `score_year`
- `score_month`
- raw category scores:
  - `raw_posts`
  - `raw_orders`
  - `raw_cutovers`
  - `raw_bonuses`
  - `raw_faulty`
  - `raw_routine`
- final category scores:
  - `final_posts`
  - `final_orders`
  - `final_cutovers`
  - `final_bonuses`
  - `final_faulty`
  - `final_routine`
- `work_score`
- `democracy_score`
- `total_score`
- `rank`
- `policy`: foreign key to `ScoreFormulaPolicy`, nullable with `SET_NULL`
- `policy_snapshot`: JSON field containing policy and category rule values used at calculation time
- `created_at`
- `updated_at`

Rules:

- Unique constraint: `worker_name + score_year + score_month`.
- Regenerating the same month updates the existing snapshot.
- Historical snapshots keep their `policy_snapshot` even if the policy is later edited.
- Future annual ranking can aggregate snapshots instead of recomputing from mutable formula settings.

### Duplicate Review Fields On `WorkApplication`

Add these fields to `accounts.models.WorkApplication`:

- `duplicate_status`: choice field
  - `none`
  - `suspected`
  - `confirmed_duplicate`
  - `overridden`
- `duplicate_checked_at`
- `duplicate_signature`
- `duplicate_override_reason`
- `duplicate_override_by`: foreign key to `User`, nullable

Purpose: store duplicate detection status and human override audit trail.

## Formula Behavior

### Formula Selection

Create a formula service, for example `scores/services/formulas.py`.

Core functions:

- `get_policy_for_period(year, month)`
- `build_policy_snapshot(policy)`
- `calculate_category_score(raw_score, rule)`
- `calculate_work_score(score, policy)`
- `generate_ranking_snapshots(year, month, worker_names=None)`

`get_policy_for_period()` chooses the active policy by effective month. This keeps older months stable.

### Formula Types

#### `legacy_cap40`

Compatibility formula matching current `getJixiao()` behavior:

```python
ocfr = orders + cutovers + faulty + routine
work_score = min(ocfr, 40) + posts + bonuses
```

Final category scores for the snapshot should be transparent:

- `posts`: raw posts
- `bonuses`: raw bonuses
- `orders`, `cutovers`, `faulty`, `routine`: retain raw category values in `final_*` or proportionally allocate the capped combined score

Decision for this project: store raw values in `final_*` for `legacy_cap40`, and store the capped combined result in `work_score`. This avoids creating artificial category numbers that do not currently exist.

#### `raw_sum`

No compression:

```python
work_score = posts + orders + cutovers + bonuses + faulty + routine
```

Each `final_*` equals its raw category score.

#### `compressed_sum`

Each category applies its `ScoreCategoryRule`, then sums:

```python
final_category = apply_rule(raw_category, category_rule)
work_score = sum(final_categories)
```

This supports examples such as:

- cutovers compressed
- orders compressed
- projects uncompressed
- bonuses uncompressed

### Default Policy

The migration or a data setup helper should create a default policy equivalent to current behavior:

- name: `当前兼容公式`
- effective date: early enough to cover current historical data, for example `2000-01`
- `ranking_formula`: `legacy_cap40`
- active: true

This prevents rankings from changing immediately after deployment.

## Ranking Snapshot Flow

Replace direct ranking construction in `scores.views.index()` with snapshot generation.

Flow:

1. Determine target ranking period with `current_period()`.
2. Call `updateScoreOfWorkers(year, month, worker_names)` to refresh raw `Scores`.
3. Call `generate_ranking_snapshots(year, month, worker_names)`.
4. `generate_ranking_snapshots()`:
   - loads `Scores` rows for the period
   - gets the active policy
   - calculates work score from raw category scores
   - applies democracy score for the period
   - sorts by total score
   - writes or updates `ScoreRankingSnapshot`
5. `scores/index.html` reads ranking rows from snapshots, not from ad hoc in-memory tuples.

This provides a durable monthly ranking result that can support annual ranking later.

## Duplicate Detection

Create a duplicate service, for example `accounts/services/duplicates.py`.

Core functions:

- `build_duplicate_signature(application)`
- `find_duplicate_candidates(application)`
- `update_duplicate_status(application)`
- `approval_requires_duplicate_override(application)`

### Signature

Build a normalized signature using:

- work type
- work number if present
- normalized title
- work date if present
- applicant
- score

The signature is stored on `WorkApplication.duplicate_signature`.

### Candidate Checks

Check likely duplicates against:

1. `WorkApplication`
   - same `work_type`
   - same non-empty `work_num`, or
   - same normalized title and same work date, or
   - same applicant, work type, score, and work date
2. Materialized business tables
   - `Orders.orders_num`
   - `Cutovers.cutover_num`
   - relevant title/date combinations for tables without a unique business number

Exact number matches are high risk. Title/date matches are medium risk.

### Submission Flow

At dashboard submission time:

1. Save the application as pending.
2. Run duplicate detection.
3. Mark `duplicate_status` as `suspected` if candidates are found.
4. Show the user a warning in workflow history.

Submission is not blocked.

### Approval Flow

On approval page:

1. Show duplicate candidates and risk reason.
2. If high-risk duplicate exists, require:
   - checkbox: confirmed not duplicate
   - text reason in `duplicate_override_reason`
3. If missing override confirmation, do not approve.
4. If override provided:
   - set `duplicate_status = overridden`
   - set `duplicate_override_by = request.user`
   - save the reason
   - proceed with materializing the business table record
5. If the approver rejects because it is duplicate:
   - set `duplicate_status = confirmed_duplicate`
   - set status rejected

## Admin Experience

### Formula Policy Admin

Add admin pages:

- `ScoreFormulaPolicyAdmin`
- inline `ScoreCategoryRuleInline`
- `ScoreRankingSnapshotAdmin`

Only superusers can add/change/delete policies and rules.

Recommended admin list display:

- policy name
- formula type
- effective year/month
- active status
- updated time

### Work Application Admin

Enhance `WorkApplicationAdmin`:

- show `duplicate_status`
- search by `work_num`, title, applicant
- read-only generated business table reference remains visible
- bulk approval must respect duplicate override rules for high-risk duplicates; if a selected item requires override, skip it and show an admin message

## Migration And Compatibility

Migrations should:

1. Create formula policy/rule/snapshot models.
2. Add duplicate fields to `WorkApplication`.
3. Create a default compatibility policy.

Existing `Scores` rows remain valid as raw scores. Existing rankings can be regenerated into snapshots on demand by visiting the scores page or by a management command.

Optional management command:

```bash
python manage.py rebuild_ranking_snapshots --year 2026
```

This command can be added in a later phase if needed for annual reporting.

## Testing Strategy

Use Django tests with the project venv.

Required tests:

1. Formula selection:
   - policy effective in July does not affect June
   - latest active policy before target month is selected
2. Formula calculation:
   - `legacy_cap40` matches current behavior
   - `raw_sum` does not compress
   - `compressed_sum` applies exponential rule
3. Snapshot generation:
   - creates one snapshot per worker/month
   - stores raw category scores
   - stores policy snapshot JSON
   - updates existing snapshot on regeneration
4. Duplicate detection:
   - same work number marks application as suspected
   - submission is allowed
   - high-risk suspected duplicate cannot be approved without override reason
   - duplicate override allows approval and stores override audit fields
5. Regression:
   - existing score page still renders
   - default policy keeps current ranking behavior

Commands:

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py test accounts scores
```

## Implementation Boundaries

Keep the implementation focused:

- Do not redesign the scores UI beyond showing policy/snapshot information where useful.
- Do not add the annual ranking page in this phase.
- Do not change business table schemas except migrations required by formula and duplicate review models.
- Keep formula logic out of views; use services.
- Keep duplicate logic out of templates; templates only display the results and submit override fields.

## Open Follow-Up For Later

Annual ranking needs a separate decision:

- annual total score as sum of monthly `total_score`
- annual score as sum of monthly `work_score` plus annual democracy average
- annual ranking points based on each monthly rank

This design stores enough monthly snapshot data to support any of those choices later.
