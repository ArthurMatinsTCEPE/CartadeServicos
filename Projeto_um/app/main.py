import streamlit as st
import hmac

def verificar_senha():
    """Retorna `True` se o usuário tiver a senha correta."""

    def formulario_login():
        """Formulário com widgets para coletar as informações do usuário"""
        with st.form("Credenciais"):
            st.text_input("Nome de usuário", key="usuario")
            st.text_input("Senha", type="password", key="senha")
            st.form_submit_button("Entrar", on_click=senha_inserida)

    def senha_inserida():
        """Verifica se a senha inserida pelo usuário está correta."""
        if st.session_state["usuario"] in st.secrets["senhas"] and hmac.compare_digest(
            st.session_state["senha"],
            st.secrets.senhas[st.session_state["usuario"]],
        ):
            st.session_state["senha_correta"] = True
            del st.session_state["senha"]  # Não armazena o nome de usuário ou senha.
            del st.session_state["usuario"]
        else:
            st.session_state["senha_correta"] = False

    # Retorna True se o nome de usuário + senha for validado.
    if st.session_state.get("senha_correta", False):
        return True

    # Exibe os campos para nome de usuário + senha.
    formulario_login()
    if "senha_correta" in st.session_state:
        st.error("😕 Usuário desconhecido ou senha incorreta")
    return False

# Verifique a senha antes de mostrar o conteúdo principal
if not verificar_senha():
    st.stop()

# O aplicativo Streamlit principal começa aqui
st.title("Bem-vindo ao Aplicativo")

if st.button("Enviar um relatório novo"):
    st.switch_page("pages/Enviar_documento.py")

if st.button("Visualizar relatórios antigos"):
    st.switch_page("pages/Visualizar_documento.py")
    
