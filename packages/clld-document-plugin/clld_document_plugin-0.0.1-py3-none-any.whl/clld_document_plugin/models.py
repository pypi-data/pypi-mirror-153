from clld.db.meta import Base
from clld.db.models.common import IdNameDescriptionMixin
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from zope.interface import implementer
from clld_document_plugin.interfaces import IDocument


@implementer(IDocument)
class Document(Base, IdNameDescriptionMixin):
    chapter_no = Column(Integer)
    order = Column(String)

    following_pk = Column(Integer, ForeignKey("document.pk"))
    preceding_pk = Column(Integer, ForeignKey("document.pk"))
    preceding = relationship(
        "Document",
        innerjoin=True,
        foreign_keys=preceding_pk,
        uselist=False,
        remote_side="Document.pk",
        backref="following",
    )

    def __str__(self):
        if not self.chapter_no:
            return self.name
        return f"{self.chapter_no}. {self.name}"
