"""Read-only inspection helpers for the Chroma notebook."""


def inspect_collection(collection, *, limit=10, offset=0, source=None):
    """Print chunks, source metadata, and a preview of each embedding."""
    print("Collection:", collection.name)
    print("Stored chunks:", collection.count())

    data = collection.get(
        limit=limit,
        offset=offset,
        where={"source": source} if source is not None else None,
        include=["documents", "metadatas", "embeddings"],
    )
    if not data["ids"]:
        print("No matching chunks.")
        return

    for chunk_id, document, metadata, embedding in zip(
        data["ids"],
        data["documents"],
        data["metadatas"],
        data["embeddings"],
        strict=True,
    ):
        metadata = metadata or {}
        print("\n" + "=" * 70)
        print("ID:", chunk_id)
        print("Source:", metadata.get("source", ""))
        print("Heading:", metadata.get("heading", ""))
        print("Vector dimensions:", len(embedding))
        print("First 8 vector values:", embedding[:8])
        print("\nStored text:\n")
        print(document)
