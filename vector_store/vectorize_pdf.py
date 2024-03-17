from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import uuid
from pinecone import Pinecone
import glob

embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
INDEX_NAME = "homeassist"
# Namespace for UUID
NAMESPACE = uuid.UUID('6ba7b812-9dad-11d1-80b4-00c04fd430c8')
pc = Pinecone()
index = pc.Index(INDEX_NAME)

# Process all PDFs in the raw_materials dir
pdf_paths = glob.glob("./raw_materials/*.pdf")
for file_path in pdf_paths:
    print(file_path)

    # https://medium.com/@felix.lu07/how-to-run-text-embeddings-on-a-pdf-and-upload-to-pinecone-vector-database-0c74af2288c8
    pdf_loader = PyPDFLoader(file_path)

    documents = pdf_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100)
    split_documents = text_splitter.split_documents(documents)

    # We will follow the approach of UPSERT with Pinecone
    pc_upsert_list = []
    for split in split_documents:
        # https://python.langchain.com/docs/integrations/text_embedding/openai
        embedding = embedder.embed_query(str(split))
        metadata = {
            "source": split.metadata["source"],
            "page": split.metadata["page"],
            "text": split.page_content
        }

        pc_upsert_list.append(
            {"id": str(uuid.uuid5(NAMESPACE, split.page_content)),
                "values": embedding,
             "metadata": metadata}
        )

    # Vector dictionary needs the extra required fields: ['id', 'values']
    index.upsert(
        vectors=pc_upsert_list
    )
