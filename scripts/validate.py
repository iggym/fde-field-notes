#!/usr/bin/env python3
"""Validation script for FDE Field Notes build and metadata."""
import json
import re
import sys
from pathlib import Path


def validate_metadata():
    """Validate metadata.json schema and content."""
    try:
        metadata = json.loads(Path("metadata.json").read_text())
    except json.JSONDecodeError as e:
        print(f"metadata.json is not valid JSON: {e}")
        return False

    # Validate site object
    if "site" not in metadata:
        print("Missing 'site' object in metadata.json")
        return False

    site = metadata["site"]
    for field in ["base_url", "title", "description"]:
        if field not in site:
            print(f"Missing 'site.{field}' in metadata.json")
            return False

    # Validate articles
    if "articles" not in metadata:
        print("Missing 'articles' array in metadata.json")
        return False

    if not metadata["articles"]:
        print("No articles found in metadata.json")
        return False

    required_fields = ["id", "slug", "title", "hook", "path", "date", "status", "pillar", "tags", "reading_time_minutes"]
    valid_pillars = ["deployment-practice", "customer-judgment", "discovery-scoping", "internal-advocacy", "market-comp", "role-craft"]

    for i, article in enumerate(metadata["articles"]):
        slug = article.get("slug", f"unknown (index {i})")

        # Check required fields
        for field in required_fields:
            if field not in article:
                print(f"Article '{slug}': missing '{field}'")
                return False

        # Validate ID format
        id_parts = article["id"].split("-", 1)
        if len(id_parts) != 2 or len(id_parts[0]) != 8:
            print(f"Article '{slug}': ID '{article['id']}' must be YYYYMMDD-slug format")
            return False

        # Validate date format
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", article["date"]):
            print(f"Article '{slug}': date '{article['date']}' must be YYYY-MM-DD")
            return False

        # Validate pillar
        if article["pillar"] not in valid_pillars:
            print(f"Article '{slug}': unknown pillar '{article['pillar']}'")
            return False

        # Validate tags
        if not isinstance(article.get("tags"), list):
            print(f"Article '{slug}': tags must be a list")
            return False

        if not article["tags"]:
            print(f"Article '{slug}': tags list is empty")
            return False

        if "fde" not in article["tags"]:
            print(f"Article '{slug}': missing 'fde' tag")
            return False

    print(f"Metadata valid: {len(metadata['articles'])} articles")
    return True


def validate_meta_tags():
    """Check all articles have required SEO meta tags."""
    metadata = json.loads(Path("metadata.json").read_text())

    required_meta = {
        "description": r'<meta name="description"',
        "canonical": r'<link rel="canonical"',
        "og:type": r'<meta property="og:type"',
        "og:title": r'<meta property="og:title"',
        "twitter:card": r'<meta name="twitter:card"',
        "json-ld": r'<script type="application/ld\+json"',
    }

    all_valid = True
    for article in metadata["articles"]:
        if article["status"] != "published":
            continue

        slug = article["slug"]
        path = Path(article["path"])

        if not path.exists():
            print(f"Missing file: {article['path']}")
            all_valid = False
            continue

        content = path.read_text()
        missing = [name for name, pattern in required_meta.items() if not re.search(pattern, content)]

        if missing:
            print(f"{slug}: missing meta tags: {', '.join(missing)}")
            all_valid = False
        else:
            print(f"{slug}: all meta tags present")

    return all_valid


def validate_html_structure():
    """Check articles have required semantic HTML elements."""
    metadata = json.loads(Path("metadata.json").read_text())

    all_valid = True
    for article in metadata["articles"]:
        if article["status"] != "published":
            continue

        slug = article["slug"]
        path = Path(article["path"])

        if not path.exists():
            continue

        content = path.read_text()

        checks = {
            "h1": r"<h1[^>]*>",
            "footer": r"<footer[^>]*>",
        }

        missing = [name for name, pattern in checks.items() if not re.search(pattern, content)]

        if missing:
            print(f"{slug}: missing elements: {', '.join(missing)}")

    return all_valid


def main():
    """Run all validations."""
    print("=== FDE Field Notes Validation ===\n")

    all_valid = True

    print("Validating metadata.json...")
    if not validate_metadata():
        all_valid = False
    print()

    print("Checking SEO meta tags...")
    if not validate_meta_tags():
        all_valid = False
    print()

    print("Validating HTML structure...")
    validate_html_structure()
    print()

    if all_valid:
        print("All validations passed!")
        return 0
    else:
        print("Some validations failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
