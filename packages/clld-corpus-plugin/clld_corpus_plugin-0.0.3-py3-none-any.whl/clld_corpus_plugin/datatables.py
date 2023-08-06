from clld.web.datatables.base import DataTable
from clld.web.datatables.base import LinkCol, Col
from clld.web.datatables.sentence import Sentences, AudioCol
from clld_corpus_plugin.models import Text


class CountCol(Col):
    def __init__(self, dt, name, **kw):
        Col.__init__(self, dt, name, **kw)

    def format(self, item):
        return item.part_count


class Texts(DataTable):
    def col_defs(self):
        return [
            Col(self, "id"),
            LinkCol(self, "name"),
            CountCol(self, "Parts", bSortable=False, bSearchable=False),
        ]


class SentencesWithAudio(Sentences):
    def col_defs(self):
        return super().col_defs() + [AudioCol(self, "audio")]
