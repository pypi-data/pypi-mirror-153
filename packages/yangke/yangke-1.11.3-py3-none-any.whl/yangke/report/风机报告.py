from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape


def fill_document(doc):
    with doc.create(Section('A section')):
        doc.append('Some regular text and some')

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters:$&#{}')


if __name__ == "__main__":
    doc = Document('basic')
    fill_document(doc)
    doc.generate_pdf(clean_tex=False)
    doc.generate_tex()
