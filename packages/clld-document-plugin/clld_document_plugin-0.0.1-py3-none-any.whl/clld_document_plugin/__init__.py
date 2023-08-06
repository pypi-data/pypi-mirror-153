"""Top-level package for clld-document-plugin."""
from clld_document_plugin import interfaces
from clld_document_plugin import models
from clld_document_plugin import datatables

__author__ = "Florian Matter"
__email__ = "florianmatter@gmail.com"
__version__ = "0.0.1"


def includeme(config):

    config.registry.settings["mako.directories"].insert(
        1, "clld_document_plugin:templates"
    )
    config.add_static_view("clld-document-plugin-static", "clld_document_plugin:static")

    config.register_resource(
        "document", models.Document, interfaces.IDocument, with_index=True
    )

    config.register_datatable("documents", datatables.Documents)
