import streamlit as st
import pikepdf
import io

# Configuração da página
st.set_page_config(page_title="Desbloqueador de Faturas", page_icon="🔓")

st.title("🔓 Removedor de Senha de PDF")
st.markdown("""
Esta aplicação remove a proteção de senha de suas faturas de forma segura. 
O arquivo é processado em memória e não fica salvo no servidor.
""")

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha a fatura em PDF", type="pdf")

if uploaded_file is not None:
    # Campo para a senha
    # Dica: Você pode definir um valor padrão no 'value' se suas faturas seguirem um padrão
    senha = st.text_input("Digite a senha do PDF:", type="password")
    
    if st.button("Desbloquear PDF"):
        if not senha:
            st.warning("Por favor, insira a senha.")
        else:
            try:
                # Carregar o PDF da memória
                with pikepdf.open(uploaded_file, password=senha) as pdf:
                    # Criar um buffer para salvar o PDF desbloqueado
                    output_buffer = io.BytesIO()
                    pdf.save(output_buffer)
                    output_buffer.seek(0)
                    
                    st.success("PDF desbloqueado com sucesso!")
                    
                    # Botão de download
                    st.download_button(
                        label="Baixar PDF sem senha",
                        data=output_buffer,
                        file_name=f"desbloqueado_{uploaded_file.name}",
                        mime="application/pdf"
                    )
            except pikepdf.PasswordError:
                st.error("Senha incorreta. Verifique e tente novamente.")
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")

st.divider()
st.caption("Desenvolvido para automação de processos de Controladoria.")
