SELECT I.transcription
FROM census.cs_document_inscription as I, census.cs_document_inscription__attribute__doc_inscr_type as IType
WHERE I.lk_document_id = 10172091
  AND IType.lk_document_inscription_id = I.id
  AND IType.lk_attribute_id = 10006614;