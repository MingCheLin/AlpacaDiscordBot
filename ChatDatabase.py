import sqlite3

# load the chat history info to make alpaca model remember chat history
def load_chat_history(channel_id: int) -> str:
    con = sqlite3.connect("./src/chatHistory.db")

    cur = con.cursor()
    res = cur.execute("SELECT chatHistory FROM IdAndChat WHERE ID = ?", (channel_id,)).fetchone()
    if res:
        con.close()
        return res[0]
    cur.execute("INSERT INTO IdAndChat VALUES (?, ?)", (channel_id, None))
    con.commit()
    con.close()
    return 

# update chat history into database
def update_chat_history(channel_id: int, prompt: str):
    con = sqlite3.connect("./src/chatHistory.db")
    cur = con.cursor()
    cur.execute("UPDATE IdAndChat SET chatHistory = ? WHERE ID = ?", (prompt, channel_id))
    con.commit()
    con.close()
    return

# reset the chat history of certain channel
def reset(channel_id: str):
    update_chat_history(channel_id, "")
    return
