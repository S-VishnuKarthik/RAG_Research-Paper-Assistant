import streamlit as st


# 🔥 HEADER
def render_header():
    st.markdown(
        """
        <h1 style="text-align:center;">📄 Smart Research Paper Assistant</h1>
        <p style="text-align:center;color:#94a3b8;">
        Advanced RAG System for Research Paper Analysis
        </p>
        """,
        unsafe_allow_html=True
    )


# 🔥 FILE UPLOADER
def render_file_uploader():
    return st.file_uploader(
        "📥 Upload Research Papers",
        type="pdf",
        accept_multiple_files=True
    )


# 🔥 PROCESS BUTTON
def render_process_button():
    return st.button("⚡ Process PDFs")


# 🔥 QUERY INPUT
def render_query_input():
    return st.text_input("💬 Ask your question")


# 🔥 ANSWER CARD
def render_answer(answer):
    st.markdown("### 🤖 Answer")
    st.markdown(
        f"""
        <div class="answer-box">
        {answer}
        </div>
        """,
        unsafe_allow_html=True
    )


# 🔥 SOURCES DISPLAY
def render_sources(chunks, limit=5):
    with st.expander("📚 Sources & Citations"):
        for c in chunks[:limit]:
            st.markdown(
                f"""
                <div class="source-card">
                <b>📄 {c['source']} | Page {c['page']} | {c.get('section','unknown')}</b><br>
                {c['content'][:300]}...
                </div>
                """,
                unsafe_allow_html=True
            )


# 🔥 METRICS PANEL
def render_metrics(response_time, chunk_count):
    col1, col2 = st.columns(2)

    with col1:
        st.metric("⚡ Response Time", f"{response_time:.2f}s")

    with col2:
        st.metric("📊 Chunks Used", chunk_count)


# 🔥 DEBUG PANEL
def render_debug_info(q_type, processed, retrieved, filtered, reranked):
    with st.expander("🔍 Debug Info"):
        st.write("Query Type:", q_type)
        st.write("Enhanced Query:", processed["enhanced_query"])
        st.write("Constraints:", processed["constraints"])
        st.write("Retrieved:", len(retrieved))
        st.write("After Filtering:", len(filtered))
        st.write("After Reranking:", len(reranked))


# 🔥 STATUS MESSAGES
def render_success(msg):
    st.success(f"✅ {msg}")


def render_error(msg):
    st.error(f"❌ {msg}")


def render_info(msg):
    st.info(f"ℹ️ {msg}")


# 🔥 EMPTY STATE
def render_empty():
    st.info("📂 Upload PDFs and start asking questions!")