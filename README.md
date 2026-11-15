# Engineering Knowledge RAG

The first lab uses the bottleneck idea from the book *The Goal* to ask whether faster cutting increases output when assembly is already at capacity. The three Markdown notes describe a fictional line and measure physical output in finished units per hour.

The notebook shows six sections you can inspect separately. Partition the notes, chunk by heading, embed and index the chunks, retrieve evidence with a source filter when needed, and optionally generate an answer with citations.

## What I learned

- **Partitioning and chunking serve different purposes.** Partitioning identifies elements such as headings and paragraphs. Chunking groups those elements into passages for retrieval. Keeping the source filename and heading with each chunk makes the retrieved text easier to trace back to the notes.
- 
- **Embeddings make similarity search possible.** Chroma embeds both the stored passages and the question. Inspecting the stored text, metadata, and vectors helped me connect the original notes to what the collection actually contains. A smaller cosine distance indicates a closer vector match; I still need to read the passage to decide whether it answers the question.
- 
- **Source filters change the search scope.** Comparing the full-corpus search with a search restricted to the bottleneck note shows two separate decisions: metadata filtering selects eligible chunks, and vector similarity ranks them.
- 
- **Retrieval and answer generation need separate checks.** I can inspect the retrieved evidence before calling Ollama. That helps distinguish missing evidence from a model that misinterprets evidence it received. In this example, faster Cutting still leaves Assembly limiting output to 40 finished units per hour.
- **A citation does not guarantee a supported answer.** During testing, the model refused despite relevant passages and also produced an incorrect conclusion with a citation. Asking for before/after values and allowing direct conclusions helped in one observed run, but I still need to verify each claim against its cited passage.

This lab gives me a small, inspectable starting point. I have not yet established reliability across a larger corpus or a repeatable set of evaluation questions.

## Run in VS Code

Use Python 3.12 and the VS Code Python and Jupyter extensions. From the repository root, run the following.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --group notebook
code .
```

Open [01-markdown-to-rag.ipynb](notebooks/01-markdown-to-rag.ipynb), select the `.venv` Python kernel, and run the cells in order. Package installation requires internet access. The first run may also download model files. Chroma creates the embeddings locally, and the collection lasts for the current kernel session.

## Check the evidence

The expected passage is **Faster cutting with the same bottleneck** in [`01-bottleneck-throughput.md`](data/sample/01-bottleneck-throughput.md). Cutting goes from 60 to 75 units per hour, while Assembly caps the line at 40 finished units per hour. Compare the full-corpus query with the same question filtered to this file.

## Generate an answer

If you have Ollama running, set `ollama_model` in the last cell to the exact name of an installed model. Use `ollama list` on the Ollama host to see its models. The cell uses `http://127.0.0.1:11434` by default. For a remote server, change `ollama_base_url` to its reachable Ollama API address. Section 6 sends the filtered passages from Section 5. Check the answer against those numbered excerpts.

## Troubleshoot answer generation

For Ollama running in a Docker container named `ollama`, run these on the server:

```bash
docker exec ollama ollama list
docker exec -it ollama ollama run qwen2.5-coder:14b "Tell me one fun fact about the Roman Empire."
docker exec ollama ollama ps
```

The generation command checks that the model responds; it does not verify factual accuracy. In our test, `ollama ps` reported `100% GPU`.

From the notebook machine, check API access with `curl --max-time 10 http://<ollama-host>:11434/api/tags`, replacing `<ollama-host>` with the server address. Connect to Tailscale first if that address is on your tailnet. Port `3000` served our Open WebUI interface; sending the notebook's `/api/chat` request there returned HTTP 405. Use the Ollama API on port `11434`.

If generation is slow, remember that `stream=False` displays the answer only after completion; the request timeout is 180 seconds. After editing the function or settings, rerun the entire last cell. If no passages reached Section 6, rerun Section 5. Inspect the actual inputs with:

```python
print(question)
print(format_evidence(filtered_evidence))
```

During testing, the model both refused despite relevant evidence and gave an incorrect conclusion with a citation. The final prompt permits direct conclusions across sentences and asks for before/after values. It produced the correct 40 finished units per hour conclusion in the observed run, but citations were not attached to every factual claim. Treat that as one passing answer, not a reliability guarantee. A citation must support the claim, not merely appear in the response.

## Use your own notes

Keep the example questions and add one of your own. For a private corpus, put a few Markdown files in `data/private/` and point `corpus_dir` there. Update the source filter to match the new filename. Git ignores files under `data/` except the three sample notes. Clear notebook outputs before committing after a run with private notes.

## References

- [Markdown partitioning](https://docs.unstructured.io/open-source/core-functionality/partitioning#partition-md) and [chunking by title](https://docs.unstructured.io/open-source/core-functionality/chunking)
- [Chroma embedding functions](https://docs.trychroma.com/docs/embeddings/embedding-functions) and [metadata-filtered queries](https://docs.trychroma.com/docs/querying-collections/query-and-get)
- [Ollama chat endpoint](https://docs.ollama.com/api/chat)
