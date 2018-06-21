from config import env
from lxml import etree
from pathlib import Path
import psycopg2


def main():
    connection = psycopg2.connect("dbname={dbname} user={user}".format(dbname=env.DB_DATABASE, user=env.DB_USERNAME))
    cursor = connection.cursor()

    root = etree.Element("documents")

    cursor.execute("""
    SELECT DISTINCT  D4.id as "Dokument_CensusID", D4.name as "Dokument_Name", M.id as "Monument_CensusID", M.label_name as "Monument_Label"
    FROM census.cs_document D2, census.cs_document D3, census.cs_document D4, census.cs_monument M, census.cs_monument__document LinkTable
    WHERE D2.fk_father_id = 10165743
    AND D3.fk_father_id = D2.id
    AND D4.fk_father_id = D3.id
    AND LinkTable.lk_document_id = D4.id
    AND M.id = LinkTable.lk_monument_id
    ORDER BY "Dokument_Name" ASC;
    """)

    # get all documents as tuples
    docs = prepare_docs(cursor.fetchall())

    for doc_id in docs:
        xml = doc_to_xml(doc_id, docs[doc_id])
        root.append(xml)

    cursor.close()
    connection.close()

    write_output(root)

def prepare_docs(documents) -> dict:
    """
    Prepare a dictionary that group entries by the document id
    :param documents:
    :return: dict
    """
    docs = {}
    for doc in documents:
        id = doc[0]
        if id not in docs:
            docs[id] = [doc]
        else:
            docs[id].append(doc)

    return docs


def doc_to_xml(doc_id, documents) -> etree.Element:

    document = etree.Element("document")

    census_id = etree.Element("census-id")
    census_id.text = str(doc_id)

    name = etree.Element("name")
    name.text = documents[0][1]

    monuments = etree.Element("monuments")
    for doc in documents:
        monument = etree.Element("monument")

        monument_id = etree.Element("census-id")
        monument_id.text = str(doc[2])

        monument_label = etree.Element("label")
        monument_label.text = doc[3]

        monument.append(monument_id)
        monument.append(monument_label)

        monuments.append(monument)

    document.append(census_id)
    document.append(name)
    document.append(monuments)

    return document


def write_output(root):

    filepath = Path(__file__).parent / ".." / "out" / "text-export.xml"
    with open(filepath, "w") as outfile:
        outfile.write('<?xml version="1.0" encoding="utf-8"?>\n')
        outfile.write(etree.tostring(root, pretty_print=True).decode("utf-8"))

main()
