from config import env
from lxml import etree
from pathlib import Path
import psycopg2
import csv


def read_record_list():
    """
    Read all records from a file
    :return:
    """
    filepath = Path(__file__).parent / ".." / "doc" / "Strada-Einzelbaende-IDs.csv"
    records = []
    with open(filepath, "r") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter="\t")
        for entry in csvreader:
            records.append(entry)

    return records


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


def doc_to_xml(doc_id, documents, transcription_list) -> etree.Element:
    """
    Transform SQL document list to xml element
    :param doc_id:
    :param documents:
    :return:
    """
    # Create <document/> node for the census document
    document = etree.Element("document")

    # Create <census-id/> node for for the document id
    census_id = etree.Element("census-id")
    census_id.text = str(doc_id)

    # Create <name>document-name</name>
    name = etree.Element("name")
    name.text = documents[0][1]

    # Create container for monuments <monuments/>
    monuments = etree.Element("monuments")
    for doc in documents:
        # Create <monument/>
        monument = etree.Element("monument")

        # Create <census-id>monument-id</census-id>
        monument_id = etree.Element("census-id")
        monument_id.text = str(doc[2])

        # Create <label>monument-label</label>
        monument_label = etree.Element("label")
        monument_label.text = doc[3]

        # Insert content nodes into monument node
        monument.append(monument_id)
        monument.append(monument_label)

        # Append monument node into list of monuments node
        monuments.append(monument)

    # Create container for transcriptions <transcriptions/>
    transcriptions = etree.Element("transcriptions")
    for script in transcription_list:
        # create <transcription>
        transcription = etree.Element("transcription")

        # Create <inscription/>
        inscription = etree.Element("inscription")
        inscription.text = script

        # Create <inscription type>
        inscription_type = etree.Element("inscription-type")
        inscription_type.text = "coin legend"

        transcription.append(inscription)
        transcription.append(inscription_type)
        transcriptions.append(transcription)

    # Append document information and list of monuments and transcriptions to documents node
    document.append(census_id)
    document.append(name)
    document.append(monuments)
    document.append(transcriptions)

    return document


def write_output(root, record_id):
    """
    Write output to file
    :param root: xml root
    :return: None
    """
    filename = record_id + ".xml"

    filepath = Path(__file__).parent / ".." / "out" / filename
    with open(filepath, "w") as outfile:
        outfile.write('<?xml version="1.0" encoding="utf-8"?>\n')
        outfile.write(etree.tostring(root, pretty_print=True).decode("utf-8"))


def fetch_documents(cursor, record_id, level=1):
    """
    Fetch all documents related to the parent document
    :param cursor: Database Cursor
    :param record_id: Parent Record ID
    :param level: Nesting Level
    :return: All records related to the record_id
    """
    query = """
            SELECT DISTINCT  D2.id as "Dokument_CensusID", D2.name as "Dokument_Name", M.id as "Monument_CensusID", M.label_name as "Monument_Label"
            FROM census.cs_document D2, census.cs_monument M, census.cs_monument__document LinkTable
            WHERE D2.fk_father_id = {record_id}
            AND LinkTable.lk_document_id = D2.id
            AND M.id = LinkTable.lk_monument_id
            ORDER BY "Dokument_Name" ASC;
            """

    if level == 2:
        query = """
                SELECT DISTINCT  D3.id as "Dokument_CensusID", D3.name as "Dokument_Name", M.id as "Monument_CensusID", M.label_name as "Monument_Label"
                FROM census.cs_document D2, census.cs_document D3, census.cs_monument M, census.cs_monument__document LinkTable
                WHERE D2.fk_father_id = {record_id}
                AND D3.fk_father_id = D2.id
                AND LinkTable.lk_document_id = D3.id
                AND M.id = LinkTable.lk_monument_id
                ORDER BY "Dokument_Name" ASC;        
                """

    elif level == 3:
        query = """
                SELECT DISTINCT  D4.id as "Dokument_CensusID", D4.name as "Dokument_Name", M.id as "Monument_CensusID", M.label_name as "Monument_Label"
                FROM census.cs_document D2, census.cs_document D3, census.cs_document D4, census.cs_monument M, census.cs_monument__document LinkTable
                WHERE D2.fk_father_id = {record_id}
                AND D3.fk_father_id = D2.id
                AND D4.fk_father_id = D3.id
                AND LinkTable.lk_document_id = D4.id
                AND M.id = LinkTable.lk_monument_id
                ORDER BY "Dokument_Name" ASC;
                """

    query = query.format(record_id=record_id)
    cursor.execute(query)
    return cursor.fetchall()


def fetch_transcriptions(cursor, documents):
    """
    Fetch all transcriptions for a list of documents
    :param cursor: Database cursor
    :param documents: List of documents
    :return: All transcriptions for all documents
    """
    # Create a base query
    base_query = """
            SELECT I.transcription
            FROM census.cs_document_inscription as I, census.cs_document_inscription__attribute__doc_inscr_type as IType
            WHERE I.lk_document_id = {document_id}
            AND IType.lk_document_inscription_id = I.id
            AND IType.lk_attribute_id = 10006614;
            """

    # Filter all unique document ids to query later
    doc_ids = set([doc[0] for doc in documents])
    transcriptions = {}

    # For each unique document id
    for doc_id in doc_ids:

        # Create empty list for id
        if doc_id not in transcriptions:
            transcriptions[doc_id] = []

        # Fetch all transcriptions for a given document id
        query = base_query.format(document_id=doc_id)
        cursor.execute(query)
        results = cursor.fetchall()

        # Append it the indexed cdocument list
        if len(results) > 0:
            transcriptions[doc_id].extend([transcription[0] for transcription in results])

    return transcriptions


def main():
    parent_records = read_record_list()

    # Open the database connection
    connection = psycopg2.connect("dbname={dbname} user={user}".format(dbname=env.DB_DATABASE, user=env.DB_USERNAME))
    cursor = connection.cursor()

    for record in parent_records:

        if record["census_id"] == "" or record["nesting_level"] == "":
            continue

        # Get all documents and monuments
        documents = fetch_documents(cursor, int(record["census_id"]), int(record["nesting_level"]))

        if len(documents) == 0:
            continue

        # Get all transcriptions for all documents
        transcriptions = fetch_transcriptions(cursor, documents)

        # Create a root <documents/> element that should contain all child documents
        root = etree.Element("documents")

        # get all documents as tuples
        docs = prepare_docs(documents)

        for doc_id in docs:
            xml = doc_to_xml(doc_id, docs[doc_id], transcriptions[doc_id])
            root.append(xml)

        write_output(root, record["census_id"])

    cursor.close()
    connection.close()


main()
