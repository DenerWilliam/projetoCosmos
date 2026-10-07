{
    "name": "Cosmos Advisors Setup",
    "version": "16.0.1.0.0",
    "category": "Extra Tools",
    "summary": "Configuração inicial para Cosmos Advisors",
    "description": """
        Configura a instância Odoo com os dados da Cosmos Advisors:
        - Dados da empresa
        - Cores da marca
        - Formato brasileiro
    """,
    "author": "Escodoo",
    "website": "https://escodoo.com.br",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "crm",
        "hr",
        "project",
    ],
    "data": [
        "data/cosmos_data.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
