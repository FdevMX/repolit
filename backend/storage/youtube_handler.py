import os
import re
import streamlit as st
import yt_dlp
from urllib.parse import urlparse, parse_qs

def is_youtube_url(url):
    """Verifica si una URL es de YouTube."""
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    match = re.match(youtube_regex, url)
    return match is not None

def get_youtube_video_id(url):
    """Extrae el ID de video de una URL de YouTube."""
    # Para URLs de formato youtu.be/ID
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
     
    # Para URLs de formato youtube.com/watch?v=ID
    parsed_url = urlparse(url)
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            query = parse_qs(parsed_url.query)
            return query['v'][0] if 'v' in query else None
    return None

# Función cacheada para extraer stream de audio
@st.cache_data(ttl=3600, show_spinner=False)  # Caché de 1 hora
def get_cached_youtube_audio_stream(url):
    """
    Versión cacheada de la extracción de stream de audio.
    Usa el decorador de Streamlit para almacenar resultados.
    """
    # Seleccionar formato de calidad media
    format_selection = 'bestaudio[abr<=96]/worstaudio'
    
    ydl_opts = {
        'format': format_selection,
        'noplaylist': True,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            audio_url = info_dict.get('url')
            title = info_dict.get('title', 'Título no disponible')
            duration = info_dict.get('duration_string', 'N/A')
            
            if not audio_url:
                return None
            
            return {
                "url": audio_url, 
                "title": title, 
                "duration": duration
            }
    
    except Exception as e:
        st.error(f"Error al extraer audio: {str(e)}")
        return None

def get_youtube_audio_stream(url):
    """
    Obtiene la URL directa del stream de audio de un video de YouTube.
    Usa caché para evitar extracciones repetidas.
    """
    # Inicializar el diccionario de caché en session_state si no existe
    if 'youtube_audio_cache' not in st.session_state:
        st.session_state.youtube_audio_cache = {}
    
    # Obtener el ID del video para usarlo como clave en la caché
    video_id = get_youtube_video_id(url)
    if not video_id:
        st.error("No se pudo extraer el ID del video.")
        return None
    
    # Verificar si ya tenemos este video en caché
    if video_id in st.session_state.youtube_audio_cache:
        # st.success("✅ Usando versión en caché")
        return st.session_state.youtube_audio_cache[video_id]
    
    # Si no está en caché, usar la función cacheada
    result = get_cached_youtube_audio_stream(url)
    
    # Guardar en nuestra caché manual
    if result:
        st.session_state.youtube_audio_cache[video_id] = result
    
    return result

def extract_audio_from_youtube(url, user_id):
    """Prepara una URL de YouTube para reproducción de solo audio."""
    try:
        # Verificar si es una URL de YouTube válida
        if not is_youtube_url(url):
            st.error("La URL proporcionada no parece ser de YouTube.")
            return None
        
        # Obtener ID del video
        video_id = get_youtube_video_id(url)
        if not video_id:
            st.error("No se pudo extraer el ID del video de YouTube.")
            return None
        
        # En vez de descargar, solo guardamos la información necesaria
        file_info = {
            "url": url,
            "is_external": True,
            "filename": f"youtube_audio_{video_id}",
            "content_type": "url",
            "media_type": "audio",
            "video_id": video_id
        }
        
        return file_info
    
    except Exception as e:
        st.error(f"Error al procesar URL de YouTube: {str(e)}")
        return None

def get_youtube_embed_url(url, audio_only=False):
    """
    Convierte una URL de YouTube en una URL embedible.
    """
    video_id = get_youtube_video_id(url)
    if not video_id:
        return None

    # URL base para embed
    embed_url = f"https://www.youtube.com/embed/{video_id}"

    # Si solo queremos audio, añadimos parámetros para optimizar reproducción de audio
    if audio_only:
        # Parámetros que minimizan la experiencia visual
        embed_url += "?showinfo=0&controls=1&autohide=1&disablekb=1&fs=0&modestbranding=1&iv_load_policy=3"
    
    return embed_url