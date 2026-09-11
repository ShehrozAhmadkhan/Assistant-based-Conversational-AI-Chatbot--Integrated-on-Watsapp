# Day 7 — Exception Handling + Prompt Fixes

## Kya kiya
- Har API call (embedding, Pinecone query, LLM call) ko try-except mein wrap kiya
- Bug fix: if/if ki jagah if/elif (warna dono blocks ek hi iteration mein chal jate)
- Bug fix: history[-10:] hardcoded tha, history[-max_chat:] kiya
- Guardrail wapas add kiya (score < 0.5 threshold, pehle 0.3 tha - update kiya)
- Prompt mein explicit instruction add ki: language match karo (english/roman urdu), 
  hindi words na use karo, sirf clean answer do (question/context repeat na karo)

## Test results (real catalog data ke sath)
- Q1: "Bachelor's ke liye kitne credit hours?" -> 138 credit hours, accurate answer
- Q2 (follow-up): "Agar kam ho jayein to?" -> sahi context (part-time student) samjha
- Q3 (guardrail): "Cricket match kaun jeeta?" -> sahi reject hua

## Status
Core AskUni engine (RAG + Memory + Guardrails + Error Handling) 
fully functional hai real data ke sath.