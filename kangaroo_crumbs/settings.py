from kangaroo.settings import TEMPLATES

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "kangaroo_crumbs.context_processors.breadcrumbs",
)
