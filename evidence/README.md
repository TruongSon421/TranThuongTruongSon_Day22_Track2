# Evidence Analysis — Day 22 Lab

## RAGAS Evaluation Results: V1 vs V2

### Score Comparison

| Metric | V1 (Concise) | V2 (Structured) | Winner |
|--------|-------------|-----------------|--------|
| Faithfulness | **0.9233** | 0.9184 | V1 |
| Answer Relevancy | 0.8639 | **0.8710** | V2 |
| Context Recall | **0.8500** | 0.8300 | V1 |
| Context Precision | 0.5917 | **0.5950** | V2 |

### Analysis: Why V1 Outperforms V2 on Faithfulness

**V1 (concise prompt) scored higher on faithfulness (0.923 vs 0.918) and context recall (0.85 vs 0.83).**

Several factors likely explain this:

1. **Conciseness reduces hallucination surface.** V1 constrains the model to 2–4 sentences, which limits the opportunity to introduce claims not supported by the retrieved context. V2's 3–5 sentence structure and multi-step instructions encourage longer answers, increasing the chance of adding ungrounded details.

2. **Context-first instruction.** V1's directive "Answer using ONLY the provided context" is more explicit about staying faithful to retrieved evidence. V2's structured format (identify facts → write answer) can inadvertently give the model more creative freedom.

3. **V2 leads on answer relevancy (0.871 vs 0.864)** — its step-by-step approach tends to produce more comprehensive answers that better address the full scope of the question. Similarly, V2 edges out on context precision (0.595 vs 0.592), suggesting its structured reasoning selects slightly more relevant context chunks.

### Conclusion

- **V1 is better for faithfulness and factual grounding** — preferred when accuracy is critical.
- **V2 is better for answer completeness and relevancy** — preferred when thoroughness matters more.
- For production RAG systems, a hybrid approach (concise grounding + structured reasoning) could yield the best of both.

### Bonus Qualification

- Faithfulness ≥ 0.9 for both versions: ✅ (V1=0.923, V2=0.918)
- Analysis comment in code: ✅

## Evidence Checklist

| File | Status |
|------|--------|
| `01_langsmith_traces.png` | ✅ LangSmith UI with ≥ 50 traces |
| `02_prompt_hub.png` | ✅ Prompt Hub showing 2 versions |
| `02_ab_routing_log.txt` | ✅ 50 queries, v1/v2 routing |
| `03_ragas_scores.png` | ✅ Comparison table screenshot |
| `03_ragas_report.json` | ✅ V1 + V2 scores |
| `04_pii_demo_log.txt` | ✅ PII detection results |
| `04_json_demo_log.txt` | ✅ JSON repair results |
| `README.md` (this file) | ✅ Analysis included |

*Link LangSmith 1 Tracec* : https://smith.langchain.com/public/dae895ea-471b-468d-82a9-d9764ba7b515/r