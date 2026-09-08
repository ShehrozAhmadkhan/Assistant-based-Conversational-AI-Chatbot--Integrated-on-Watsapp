# Day 5 — Guardrails (Out-of-Scope Detection)

## Kya seekha
- Guardrails: bot ko apni limits pehchanni sikhana, taake wo har
  sawaal ka jawab dene ki koshish na kare (hallucination avoid karna)
- Approach: Pinecone similarity score check karna (top match ka score)
  - Agar score < 0.3 (threshold), matlab koi bhi chunk truly relevant nahi
  - LLM ko call hi nahi karte, seedha "out of domain" bol dete hain

## Bugs fix kiye
- `len(db_query.matches == 0)` galat tha — bracket placement issue
  - Sahi: `len(db_query.matches) == 0`
- List ko `== 0` se compare nahi kar sakte, `len()` use karna zaroori hai

## Design decision
- Out-of-scope Q&A history mein save NAHI karte — history clean/relevant
  rehti hai, future reformulation confuse nahi hoti

## Test
- "How is the weather today?" → "This question is out of my domain!"
  (successfully rejected, no hallucination)