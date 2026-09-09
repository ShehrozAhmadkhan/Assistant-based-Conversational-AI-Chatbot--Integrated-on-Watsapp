def save_history(user_question,assistant_answer,entries,history):
    history.append({"role":"user","content":user_question})
    history.append({"role":"assistant","content":assistant_answer})

    chat = entries*2
    if len(history) < chat:
        history = history[-10:]
    return history
