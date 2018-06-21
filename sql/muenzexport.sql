SELECT DISTINCT  D4.id as "Dokument_CensusID", D4.name as "Dokument_Name", M.id as "Monument_CensusID", M.label_name as "Monument_Label"
FROM census.cs_document D2, census.cs_document D3, census.cs_document D4, census.cs_monument M, census.cs_monument__document LinkTable
WHERE D2.fk_father_id = 10165743
AND D3.fk_father_id = D2.id
AND D4.fk_father_id = D3.id
AND LinkTable.lk_document_id = D4.id
AND M.id = LinkTable.lk_monument_id
ORDER BY "Dokument_Name" ASC;