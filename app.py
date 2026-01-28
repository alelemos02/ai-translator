import streamlit as st
from translator import process_text

# Page Configuration
st.set_page_config(
    page_title="AI Translation Agent v1.0.3",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for a better look
st.markdown("""
<style>
    /* Styling for the code blocks to look like text boxes but keep copy button */
    .stCode {
        font-family: "Source Sans Pro", sans-serif !important;
    }
    
    /* Target the code element inside the block to ensure sans-serif */
    code {
        font-family: "Source Sans Pro", sans-serif !important;
        white-space: pre-wrap !important; /* Allow wrapping */
    }
    
    .stChatInput textarea {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for Settings
with st.sidebar:
    st.header("Configurações")
    st.caption("Versão: v1.0.3 🚀 (Reloaded)")
    
    target_language = st.selectbox(
        "Idioma de Destino",
        [
            "Inglês (US)",
            "Português (Brasil)",
            "Espanhol",
            "Francês",
            "Alemão",
            "Italiano",
            "Chinês (Mandarim)",
            "Japonês",
            "Russo",
            "Árabe"
        ],
        index=0
    )
    
    st.markdown("---")
    
    improve_mode = st.checkbox(
        "✨ Melhorar texto e traduzir",
        value=True,
        help="Se ativado, a IA irá reescrever o texto original para torná-lo mais fluido e profissional antes de traduzir."
    )
    
    # Add a reset button to clear chat history
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Accept user input
if prompt := st.chat_input("Digite ou cole aqui o texto para tradução..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Traduzindo..."):
            result = process_text(prompt, target_language, improve_mode)
            
            if "error" in result:
                error_msg = f"❌ Ocorreu um erro: {result['error']}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                # Construct the response content
                response_content = f"**Idioma Detectado:** `{result.get('detected_language', 'Desconhecido')}`\n\n"
                
                if improve_mode and result.get("improved_text"):
                    response_content += f"""**✍️ Original Melhorado:**
```text
{result['improved_text']}
```
"""
                
                response_content += f"""**🔄 Tradução ({target_language}):**
```text
{result['translated_text']}
```
"""
                
                st.markdown(response_content)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_content})
