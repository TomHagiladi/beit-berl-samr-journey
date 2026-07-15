# -*- coding: utf-8 -*-
"""Deploy updated Firestore rules to ono-health-gallery.
2026-07-15: add the six samr_* collections for the Beit Berl SAMR journey
(meeting 2, special-education team). The full LIVE ruleset was fetched first
with fetch_rules.py and is preserved below VERBATIM (submissions + all zpd_*);
the samr_* blocks are appended with the same security posture:
public read + create-only with field validation, no update/delete.

Rollback: re-release the previous ruleset
projects/ono-health-gallery/rulesets/c487edd9-5a11-4b60-9993-0b4cf599fae2
(source also saved in tools/rules_backup.txt; old rulesets are retained by Firebase).
"""
import json
import os
import urllib.request

TOKEN = os.environ["GTOKEN"].strip()
PROJECT = "projects/ono-health-gallery"
API = "https://firebaserules.googleapis.com/v1"

NEW_RULES = """rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /submissions/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.url is string
                    && request.resource.data.url.size() <= 500;
      allow update, delete: if false;
    }

    match /zpd_takeaways/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.text is string
                    && request.resource.data.text.size() > 0
                    && request.resource.data.text.size() <= 8000;
      allow update, delete: if false;
    }

    match /zpd_products/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.text is string
                    && request.resource.data.text.size() > 0
                    && request.resource.data.text.size() <= 60000
                    && request.resource.data.format is string
                    && request.resource.data.format.size() <= 60;
      allow update, delete: if false;
    }

    match /zpd_reflections/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.understood is string
                    && request.resource.data.understood.size() <= 20000
                    && request.resource.data.unclear is string
                    && request.resource.data.unclear.size() <= 20000;
      allow update, delete: if false;
    }

    match /zpd_progress/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.stage is int
                    && request.resource.data.stage >= 0
                    && request.resource.data.stage <= 5;
      allow update, delete: if false;
    }

    match /zpd_choices/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.qs is list
                    && request.resource.data.qs.size() <= 7;
      allow update, delete: if false;
    }

    match /zpd_admin/{id} {
      allow read: if true;
      allow create: if request.resource.data.kind == 'reset';
      allow update, delete: if false;
    }

    match /samr_reflections/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.understood is string
                    && request.resource.data.understood.size() <= 20000
                    && request.resource.data.unclear is string
                    && request.resource.data.unclear.size() <= 20000;
      allow update, delete: if false;
    }

    match /samr_pairs/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.qs is list
                    && request.resource.data.qs.size() <= 7
                    && request.resource.data.text is string
                    && request.resource.data.text.size() > 0
                    && request.resource.data.text.size() <= 4000;
      allow update, delete: if false;
    }

    match /samr_products/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.lesson is string
                    && request.resource.data.lesson.size() > 0
                    && request.resource.data.lesson.size() <= 8000
                    && request.resource.data.upgrade is string
                    && request.resource.data.upgrade.size() > 0
                    && request.resource.data.upgrade.size() <= 8000
                    && request.resource.data.rung is string
                    && request.resource.data.rung.size() > 0
                    && request.resource.data.rung.size() <= 40;
      allow update, delete: if false;
    }

    match /samr_mirror/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.rung is string
                    && request.resource.data.rung.size() <= 40
                    && request.resource.data.text is string
                    && request.resource.data.text.size() > 0
                    && request.resource.data.text.size() <= 2000;
      allow update, delete: if false;
    }

    match /samr_progress/{id} {
      allow read: if true;
      allow create: if request.resource.data.name is string
                    && request.resource.data.name.size() > 0
                    && request.resource.data.name.size() <= 80
                    && request.resource.data.stage is int
                    && request.resource.data.stage >= 0
                    && request.resource.data.stage <= 5;
      allow update, delete: if false;
    }

    match /samr_admin/{id} {
      allow read: if true;
      allow create: if request.resource.data.kind == 'reset';
      allow update, delete: if false;
    }
  }
}
"""

def call(method, url, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {TOKEN}",
        "x-goog-user-project": "ono-health-gallery",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

# 1. create the new ruleset
ruleset = call("POST", f"{API}/{PROJECT}/rulesets", {
    "source": {"files": [{"name": "firestore.rules", "content": NEW_RULES}]}
})
new_name = ruleset["name"]
print("new ruleset:", new_name)

# 2. point the live cloud.firestore release at it
release = call("PATCH", f"{API}/{PROJECT}/releases/cloud.firestore", {
    "release": {
        "name": f"{PROJECT}/releases/cloud.firestore",
        "rulesetName": new_name,
    }
})
print("release now:", release["rulesetName"])
print("DEPLOYED OK")
