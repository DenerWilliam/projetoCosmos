#!/usr/bin/env python3
"""
Script to import markdown tutorials into Odoo Knowledge module.
Run this script from the host machine.
"""

import os
import sys
import xmlrpc.client

# Configuration
URL = "http://localhost:16069"
DB = "devel"
USERNAME = "admin"
PASSWORD = "admin"

# Tutorial files to import
TUTORIALS = [
    {
        "file": "/home/dener/Documentos/Escodoo/projetoCosmos/playwright-screenshots/tutoriais/01-crm-lead.md",
        "name": "Tutorial: CRM - Criacao de Lead",
        "category": "Tutoriais",
    },
    {
        "file": "/home/dener/Documentos/Escodoo/projetoCosmos/playwright-screenshots/tutoriais/02-helpdesk-ticket.md",
        "name": "Tutorial: Helpdesk - Criacao de Ticket",
        "category": "Tutoriais",
    },
    {
        "file": "/home/dener/Documentos/Escodoo/projetoCosmos/playwright-screenshots/tutoriais/03-faturamento.md",
        "name": "Tutorial: Faturamento - Emissao de Nota",
        "category": "Tutoriais",
    },
    {
        "file": "/home/dener/Documentos/Escodoo/projetoCosmos/playwright-screenshots/tutoriais/04-contatos.md",
        "name": "Tutorial: Contatos - Cadastro de Cliente",
        "category": "Tutoriais",
    },
    {
        "file": "/home/dener/Documentos/Escodoo/projetoCosmos/playwright-screenshots/tutoriais/05-projetos.md",
        "name": "Tutorial: Projetos - Gestao de Entregas",
        "category": "Tutoriais",
    },
    {
        "file": "/home/dener/Documentos/Escodoo/projetoCosmos/playwright-screenshots/tutoriais/06-excluir-contato.md",
        "name": "Tutorial: Contatos - Exclusao de Contato",
        "category": "Tutoriais",
    },
]


def authenticate():
    """Authenticate with Odoo and return uid and models proxy."""
    common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
    uid = common.authenticate(DB, USERNAME, PASSWORD, {})
    if not uid:
        print("ERROR: Authentication failed!")
        sys.exit(1)
    print(f"Authenticated as user ID: {uid}")
    models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
    return uid, models


def create_category(uid, models, category_name):
    """Create or get the category for tutorials."""
    # Check if category exists
    category = models.execute_kw(
        DB,
        uid,
        PASSWORD,
        "document.page",
        "search_read",
        [[["name", "=", category_name], ["type", "=", "category"]]],
        {"fields": ["id", "name"], "limit": 1},
    )

    if category:
        print(f"Category '{category_name}' exists with ID: {category[0]['id']}")
        return category[0]["id"]

    # Create category
    category_id = models.execute_kw(
        DB,
        uid,
        PASSWORD,
        "document.page",
        "create",
        [{"name": category_name, "type": "category"}],
    )
    print(f"Created category '{category_name}' with ID: {category_id}")
    return category_id


def import_tutorial(uid, models, tutorial, category_id):
    """Import a single tutorial into Knowledge."""
    # Read markdown file
    with open(tutorial["file"], encoding="utf-8") as f:
        markdown_content = f.read()

    # Check if page already exists
    existing = models.execute_kw(
        DB,
        uid,
        PASSWORD,
        "document.page",
        "search_read",
        [[["name", "=", tutorial["name"]]]],
        {"fields": ["id"], "limit": 1},
    )

    if existing:
        # Update existing page
        page_id = existing[0]["id"]
        models.execute_kw(
            DB,
            uid,
            PASSWORD,
            "document.page",
            "write",
            [[page_id], {"markdown_content": markdown_content}],
        )
        print(f"Updated: {tutorial['name']} (ID: {page_id})")
    else:
        # Create new page
        page_id = models.execute_kw(
            DB,
            uid,
            PASSWORD,
            "document.page",
            "create",
            [
                {
                    "name": tutorial["name"],
                    "type": "content",
                    "parent_id": category_id,
                    "markdown_content": markdown_content,
                    "draft_name": "Initial import",
                    "draft_summary": "Imported from tutorial markdown files",
                }
            ],
        )
        print(f"Created: {tutorial['name']} (ID: {page_id})")

    return page_id


def main():
    print("=" * 60)
    print("Importing Tutorials to Odoo Knowledge")
    print("=" * 60)

    # Authenticate
    uid, models = authenticate()

    # Create/get category
    category_id = create_category(uid, models, "Tutoriais")

    # Import each tutorial
    print("\nImporting tutorials...")
    for tutorial in TUTORIALS:
        if os.path.exists(tutorial["file"]):
            import_tutorial(uid, models, tutorial, category_id)
        else:
            print(f"WARNING: File not found: {tutorial['file']}")

    print("\n" + "=" * 60)
    print("Import completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
