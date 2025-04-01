import streamlit as st
from datetime import datetime
from frontend.components.sidebar_public_component import show_sidebar_public
from backend.data.category_data import get_categories
from backend.data.publication_data import get_publication_by_id
from backend.storage.file_handler import get_file_path
from streamlit_pdf_viewer import pdf_viewer
from PyPDF2 import PdfReader
from PIL import Image
import os
import base64
import mimetypes


def format_date(date_str):
    if not date_str:
        return ""
    try:
        date_obj = datetime.fromisoformat(str(date_str).replace('Z', '+00:00'))
        return date_obj.strftime("%d de %B de %Y")
    except:
        return str(date_str)

def view_public_appsview():
    try:
        # Obtener categorías para el sidebar
        categories = get_categories()
        show_sidebar_public(categories)

        # Crear layout de tres columnas para centrar el contenido
        left_col, main_col, right_col = st.columns([1, 3, 1])

        with main_col:
            # Botón para volver
            if st.button("← Volver", key="back_button"):
                st.query_params.clear()
                st.session_state.vista = "public_apps"
                st.rerun()

            # Obtener ID de la publicación
            pub_id = st.query_params.get('id')
            if not pub_id:
                st.error("No se especificó ninguna publicación")
                st.session_state.vista = "public_apps"
                st.rerun()
                return

            # Obtener detalles de la publicación
            publication = get_publication_by_id(pub_id)
            if not publication:
                st.error("La publicación no existe o ha sido eliminada")
                return

            # Verificar si la publicación es pública
            if not publication.get('is_public', False):
                st.error("Esta publicación no está disponible")
                return

            # Mostrar la publicación
            st.title(publication['title'])

            # Información básica en dos columnas
            info_col1, info_col2 = st.columns([3, 1])

            with info_col1:
                # Contenedor de información básica con mejor espaciado
                info_container = st.container()
                with info_container:
                    st.markdown("""
                        <style>
                            .tag-wrapper {
                                display: flex;
                                align-items: center;
                                gap: 8px;
                                margin: 0.5rem 0;
                            }
                            .publication-info p {
                                margin-bottom: 0.5rem;
                                line-height: 1.6;
                            }
                            .tag-container {
                                display: inline-flex;
                                flex-wrap: wrap;
                                gap: 8px;
                                margin: 8px 0;
                            }
                            .publication-tag {
                                background-color: #FF8A8C;
                                color: #000000;
                                padding: 4px 12px;
                                border-radius: 16px;
                                font-size: 0.9em;
                                display: inline-block;
                            }
                            .info-label {
                                font-weight: bold;
                                color: #333;
                                margin-right: 8px;
                                flex-shrink: 0;
                            }
                            .info-divider {
                                margin: 1rem 0;
                                border-bottom: 1px solid #eee;
                            }
                        </style>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                        <div class="publication-info">
                            <p><span class="info-label">Categoría:</span> {publication['category_name']}</p>
                            <p><span class="info-label">Autor:</span> {publication.get('author_name', 'Desconocido')}</p>
                            <p><span class="info-label">Fecha de creación:</span> {format_date(publication['created_at'])}</p>
                            <p><span class="info-label">Última actualización:</span> {format_date(publication['updated_at'])}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # Etiquetas mejoradas en línea
                    if publication.get('tags'):
                        tags_html = "".join([
                            f'<span class="publication-tag">{tag["name"]}</span>'
                            for tag in publication['tags']
                        ])
                        st.markdown(f"""
                            <div class="tag-wrapper">
                                <span class="info-label">Etiquetas:</span>
                                <div class="tag-container">
                                    {tags_html}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

            # 6. Descripción
            st.markdown("""
                <div style='margin: 1rem 0 0.5rem 0;'>
                    <h3 style='color: #1f1f1f; margin-bottom: 0.5rem;'>Descripción</h3>
                    <div style='height: 1px; background: #eee; margin-bottom: 0.5rem;'></div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div style='line-height: 1.5; color: #333; padding-left: 0.25rem;'>
                    {publication['description']}
                </div>
            """, unsafe_allow_html=True)

            # Manejo de archivos
            if publication.get("file_url"):
                st.markdown("""
                    <div style='margin: 2rem 0 1rem 0;'>
                        <h3 style='color: #1f1f1f; margin-bottom: 1rem;'>Archivo adjunto</h3>
                        <div style='height: 1px; background: #eee; margin-bottom: 1rem;'></div>
                    </div>
                """, unsafe_allow_html=True)

                try:
                    file_path = get_file_path(publication["file_url"])
                    file_type = publication["file_type"]

                    if os.path.exists(file_path):
                        # Manejo de imágenes
                        if file_type.startswith("image/"):
                            image = Image.open(file_path)
                            st.image(image, caption=publication["file_name"])

                        # Manejo de video
                        elif file_type.startswith("video/"):
                            st.video(file_path)

                        # Manejo de audio
                        elif file_type.startswith("audio/"):
                            st.audio(file_path)

                        # Manejo de PDFs
                        elif file_type == "application/pdf":
                            with open(file_path, "rb") as pdf_file:
                                pdf_data = pdf_file.read()
                                st.download_button(
                                    label="📥 Descargar PDF",
                                    data=pdf_data,
                                    file_name=publication["file_name"],
                                    mime="application/pdf",
                                )

                            # Visor de PDF
                            try:
                                pdf = PdfReader(file_path)
                                total_pages = len(pdf.pages)
                                st.caption(f"Documento PDF - {total_pages} páginas")

                                with open(file_path, "rb") as f:
                                    base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                                    pdf_display = f"""
                                        <iframe 
                                            src="data:application/pdf;base64,{base64_pdf}" 
                                            width="100%" 
                                            height="800"
                                            style="border: 1px solid #ddd; border-radius: 4px;"
                                            type="application/pdf"
                                        ></iframe>
                                    """
                                    st.markdown(pdf_display, unsafe_allow_html=True)

                            except Exception as pdf_error:
                                st.error(f"Error al mostrar el PDF: {str(pdf_error)}")

                        # Otros tipos de archivo
                        else:
                            with open(file_path, "rb") as file:
                                st.download_button(
                                    label=f"📥 Descargar {publication['file_name']}",
                                    data=file,
                                    file_name=publication["file_name"],
                                    mime=file_type,
                                )
                except Exception as e:
                    st.error(f"Error al cargar el archivo: {str(e)}")

        # Botón para volver con estilo
        st.markdown("""
            <div style='margin: 2rem 0;'>
                <div style='height: 1px; background: #eee; margin-bottom: 1rem;'></div>
            </div>
        """, unsafe_allow_html=True)
        
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
        with btn_col2:
            if st.button("← Volver", key="back_button_one", use_container_width=True):
                st.query_params.clear()
                st.session_state.vista = "public_apps"
                st.rerun()
                
        

    except Exception as e:
        st.error(f"Error al cargar la publicación: {str(e)}")
