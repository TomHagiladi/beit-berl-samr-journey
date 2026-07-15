# Rollback pointer (2026-07-15)
Previous live ruleset (before samr_* were added):
projects/ono-health-gallery/rulesets/c487edd9-5a11-4b60-9993-0b4cf599fae2
To roll back: PATCH releases/cloud.firestore back to that rulesetName
(see deploy_rules.py for the API call shape). rules_backup.txt holds the
CURRENT deployed source (refreshed on every fetch_rules.py run).
