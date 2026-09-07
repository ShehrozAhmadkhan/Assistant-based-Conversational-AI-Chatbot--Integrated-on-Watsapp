Multi-Turn Conversation Implementation

## Kya kiya
- save_entry() function ko parameter-based banaya (global hata diya)
  - Seekha: list mutable hai, .append() in-place kaam karta hai,
    lekin slicing (history[-chat:]) naya object banata hai jo
    return + reassign kiye bina bahar reflect nahi hota
- Poori logic ko while loop mein daala for real multi-turn testing

## Test kiya
- Real PDF (company policy) se paragraph use kiya
- Q1: "After hours call ke baad kitna break milta hai?" — sahi jawab mila
- Q2 (incomplete/follow-up): "Agar wo call midnight-6am ke darmiyan ho to?"
  — bot ne "wo" ko sahi context (after hours call) se samjha, sahi jawab diya

## Result
- Multi-turn conversation memory + query reformulation + retrieval
  end-to-end successfully kaam kar raha hai