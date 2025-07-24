"""
Moteur Vocal Avancé pour CyberSec AI Assistant
=============================================

Module de traitement vocal complet avec capacités de reconnaissance 
et synthèse vocale haute qualité pour la communication en temps réel.
"""

import asyncio
import threading
import queue
import io
import os
import wave
import json
import tempfile
from typing import Dict, List, Optional, Callable, Any, Union
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import numpy as np

# Audio processing
import pyaudio
import speech_recognition as sr
import pyttsx3
import librosa
import soundfile as sf
import noisereduce as nr
from scipy import signal
import webrtcvad

# Advanced TTS/STT services
try:
    from gtts import gTTS
    import azure.cognitiveservices.speech as speechsdk
    from google.cloud import speech as google_speech
    from google.cloud import texttospeech as google_tts
    import openai
    from elevenlabs import generate, Voice
except ImportError as e:
    print(f"Warning: Some advanced voice services unavailable: {e}")

from loguru import logger
from core.config import config


class VoiceQuality(Enum):
    """Qualité de la voix synthétisée"""
    BASIC = "basic"
    STANDARD = "standard"
    HIGH = "high"
    PREMIUM = "premium"


class EmotionalTone(Enum):
    """Ton émotionnel pour la voix"""
    NEUTRAL = "neutral"
    CONCERNED = "concerned"
    URGENT = "urgent"
    CALM = "calm"
    AUTHORITATIVE = "authoritative"
    REASSURING = "reassuring"


class Language(Enum):
    """Langues supportées"""
    FRENCH = "fr-FR"
    ENGLISH = "en-US"
    SPANISH = "es-ES"
    GERMAN = "de-DE"
    ITALIAN = "it-IT"


@dataclass
class VoiceSettings:
    """Configuration vocale"""
    language: Language = Language.FRENCH
    quality: VoiceQuality = VoiceQuality.HIGH
    tone: EmotionalTone = EmotionalTone.NEUTRAL
    speed: float = 1.0  # 0.5 à 2.0
    pitch: float = 1.0  # 0.5 à 2.0
    volume: float = 0.8  # 0.0 à 1.0
    voice_id: Optional[str] = None
    use_ssml: bool = True


@dataclass
class AudioSegment:
    """Segment audio traité"""
    data: np.ndarray
    sample_rate: int
    duration: float
    timestamp: datetime
    confidence: float = 0.0
    is_speech: bool = False
    noise_reduced: bool = False


class VoiceEngine:
    """
    Moteur vocal avancé pour communication haute qualité
    
    Fonctionnalités:
    - Reconnaissance vocale en temps réel multi-langue
    - Synthèse vocale émotionnelle de haute qualité
    - Réduction de bruit et amélioration audio
    - Détection d'activité vocale (VAD)
    - Support de multiples services cloud
    - Adaptation contextuelle du ton
    """
    
    def __init__(self):
        self.is_initialized = False
        self.is_listening = False
        self.is_speaking = False
        
        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        
        # Audio devices
        self.audio = None
        self.microphone = None
        self.speaker_stream = None
        
        # Recognition engines
        self.recognizer = sr.Recognizer()
        self.tts_engine = None
        
        # Voice Activity Detection
        self.vad = webrtcvad.Vad(2)  # Aggressivité moyenne
        
        # Queues for real-time processing
        self.audio_queue = queue.Queue()
        self.speech_queue = queue.Queue()
        self.synthesis_queue = queue.Queue()
        
        # Threading
        self.audio_thread = None
        self.processing_thread = None
        self.synthesis_thread = None
        
        # Callbacks
        self.speech_callback: Optional[Callable] = None
        self.synthesis_callback: Optional[Callable] = None
        self.error_callback: Optional[Callable] = None
        
        # Settings
        self.voice_settings = VoiceSettings()
        self.noise_threshold = 0.5
        
        # Services configuration
        self.azure_speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.azure_region = os.getenv("AZURE_REGION", "francecentral")
        self.google_credentials = os.getenv("GOOGLE_CREDENTIALS_PATH")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        
    async def initialize(self) -> bool:
        """Initialisation asynchrone du moteur vocal"""
        if self.is_initialized:
            return True
            
        logger.info("Initialisation du moteur vocal avancé...")
        
        try:
            # Initialisation PyAudio
            self.audio = pyaudio.PyAudio()
            
            # Configuration du microphone
            await self._setup_microphone()
            
            # Initialisation TTS local
            await self._setup_tts_engine()
            
            # Configuration des services cloud
            await self._setup_cloud_services()
            
            # Démarrage des threads de traitement
            await self._start_processing_threads()
            
            self.is_initialized = True
            logger.success("Moteur vocal initialisé avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du moteur vocal: {e}")
            return False
    
    async def _setup_microphone(self):
        """Configuration du microphone"""
        try:
            # Recherche du meilleur périphérique d'entrée
            device_info = None
            for i in range(self.audio.get_device_count()):
                info = self.audio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    device_info = info
                    break
            
            if not device_info:
                raise Exception("Aucun périphérique d'entrée audio trouvé")
            
            # Configuration optimale du microphone
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3
            
            logger.success(f"Microphone configuré: {device_info['name']}")
            
        except Exception as e:
            logger.error(f"Erreur configuration microphone: {e}")
            raise
    
    async def _setup_tts_engine(self):
        """Configuration du moteur TTS local"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configuration des propriétés vocales
            voices = self.tts_engine.getProperty('voices')
            
            # Sélection d'une voix française si disponible
            french_voice = None
            for voice in voices:
                if 'french' in voice.name.lower() or 'fr' in voice.id.lower():
                    french_voice = voice.id
                    break
            
            if french_voice:
                self.tts_engine.setProperty('voice', french_voice)
            
            # Configuration des paramètres
            self.tts_engine.setProperty('rate', 150)  # Vitesse de parole
            self.tts_engine.setProperty('volume', self.voice_settings.volume)
            
            logger.success("Moteur TTS local configuré")
            
        except Exception as e:
            logger.error(f"Erreur configuration TTS: {e}")
            raise
    
    async def _setup_cloud_services(self):
        """Configuration des services cloud pour TTS/STT avancés"""
        services_configured = []
        
        # Azure Speech Services
        if self.azure_speech_key:
            try:
                speech_config = speechsdk.SpeechConfig(
                    subscription=self.azure_speech_key,
                    region=self.azure_region
                )
                speech_config.speech_recognition_language = self.voice_settings.language.value
                speech_config.speech_synthesis_language = self.voice_settings.language.value
                services_configured.append("Azure Speech")
            except Exception as e:
                logger.warning(f"Azure Speech non configuré: {e}")
        
        # Google Cloud Speech
        if self.google_credentials:
            try:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.google_credentials
                services_configured.append("Google Cloud Speech")
            except Exception as e:
                logger.warning(f"Google Cloud Speech non configuré: {e}")
        
        # OpenAI Whisper/TTS
        if self.openai_api_key:
            try:
                openai.api_key = self.openai_api_key
                services_configured.append("OpenAI")
            except Exception as e:
                logger.warning(f"OpenAI non configuré: {e}")
        
        # ElevenLabs
        if self.elevenlabs_api_key:
            try:
                services_configured.append("ElevenLabs")
            except Exception as e:
                logger.warning(f"ElevenLabs non configuré: {e}")
        
        if services_configured:
            logger.info(f"Services cloud configurés: {', '.join(services_configured)}")
        else:
            logger.warning("Aucun service cloud configuré, utilisation des capacités locales uniquement")
    
    async def _start_processing_threads(self):
        """Démarrage des threads de traitement"""
        self.audio_thread = threading.Thread(target=self._audio_capture_loop, daemon=True)
        self.processing_thread = threading.Thread(target=self._audio_processing_loop, daemon=True)
        self.synthesis_thread = threading.Thread(target=self._synthesis_loop, daemon=True)
        
        self.audio_thread.start()
        self.processing_thread.start()
        self.synthesis_thread.start()
        
        logger.info("Threads de traitement audio démarrés")
    
    def _audio_capture_loop(self):
        """Boucle de capture audio en continu"""
        try:
            stream = self.audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            while self.is_listening:
                try:
                    # Capture d'un chunk audio
                    audio_data = stream.read(self.chunk_size, exception_on_overflow=False)
                    audio_array = np.frombuffer(audio_data, dtype=np.int16)
                    
                    # Détection d'activité vocale
                    is_speech = self._detect_speech(audio_data)
                    
                    if is_speech:
                        # Ajout à la queue de traitement
                        segment = AudioSegment(
                            data=audio_array,
                            sample_rate=self.sample_rate,
                            duration=len(audio_array) / self.sample_rate,
                            timestamp=datetime.now(),
                            is_speech=True
                        )
                        self.audio_queue.put(segment)
                        
                except Exception as e:
                    logger.error(f"Erreur capture audio: {e}")
                    
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            logger.error(f"Erreur boucle capture audio: {e}")
    
    def _detect_speech(self, audio_data: bytes) -> bool:
        """Détection d'activité vocale avec WebRTC VAD"""
        try:
            # WebRTC VAD nécessite des frames de 10, 20 ou 30ms
            frame_duration = 30  # ms
            frame_size = int(self.sample_rate * frame_duration / 1000)
            
            if len(audio_data) >= frame_size * 2:  # 2 bytes par sample (int16)
                frame = audio_data[:frame_size * 2]
                return self.vad.is_speech(frame, self.sample_rate)
            
            return False
            
        except Exception:
            # Fallback: analyse d'énergie simple
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            energy = np.sqrt(np.mean(audio_array.astype(np.float32) ** 2))
            return energy > self.noise_threshold * 1000
    
    def _audio_processing_loop(self):
        """Boucle de traitement et reconnaissance audio"""
        accumulated_audio = []
        silence_duration = 0
        max_silence = 2.0  # secondes
        
        while True:
            try:
                # Récupération d'un segment audio
                segment = self.audio_queue.get(timeout=1.0)
                
                if segment.is_speech:
                    # Réduction de bruit
                    cleaned_audio = self._reduce_noise(segment.data)
                    accumulated_audio.extend(cleaned_audio)
                    silence_duration = 0
                else:
                    silence_duration += segment.duration
                
                # Reconnaissance si silence détecté ou buffer plein
                if (silence_duration > max_silence and accumulated_audio) or len(accumulated_audio) > self.sample_rate * 10:
                    if accumulated_audio:
                        await self._process_speech(np.array(accumulated_audio))
                        accumulated_audio = []
                        silence_duration = 0
                        
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erreur traitement audio: {e}")
    
    def _reduce_noise(self, audio_data: np.ndarray) -> np.ndarray:
        """Réduction de bruit sur le signal audio"""
        try:
            # Conversion en float pour le traitement
            audio_float = audio_data.astype(np.float32) / 32768.0
            
            # Réduction de bruit avec noisereduce
            reduced = nr.reduce_noise(
                y=audio_float,
                sr=self.sample_rate,
                stationary=False,
                prop_decrease=0.8
            )
            
            # Reconversion en int16
            return (reduced * 32768.0).astype(np.int16)
            
        except Exception as e:
            logger.error(f"Erreur réduction bruit: {e}")
            return audio_data
    
    async def _process_speech(self, audio_data: np.ndarray):
        """Traitement et reconnaissance de la parole"""
        try:
            # Conversion en format WAV pour la reconnaissance
            audio_bytes = io.BytesIO()
            sf.write(audio_bytes, audio_data, self.sample_rate, format='WAV')
            audio_bytes.seek(0)
            
            # Reconnaissance avec le service le plus approprié
            text = await self._recognize_speech_premium(audio_bytes)
            
            if text and self.speech_callback:
                await self.speech_callback(text, datetime.now())
                
        except Exception as e:
            logger.error(f"Erreur reconnaissance vocale: {e}")
    
    async def _recognize_speech_premium(self, audio_io: io.BytesIO) -> Optional[str]:
        """Reconnaissance vocale avec services premium"""
        
        # Tentative avec Azure Speech (le plus précis)
        if self.azure_speech_key:
            try:
                result = await self._azure_speech_to_text(audio_io)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"Azure STT échoué: {e}")
        
        # Fallback: Google Cloud Speech
        if self.google_credentials:
            try:
                result = await self._google_speech_to_text(audio_io)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"Google STT échoué: {e}")
        
        # Fallback: OpenAI Whisper
        if self.openai_api_key:
            try:
                result = await self._openai_speech_to_text(audio_io)
                if result:
                    return result
            except Exception as e:
                logger.warning(f"OpenAI STT échoué: {e}")
        
        # Fallback final: SpeechRecognition local
        try:
            audio_io.seek(0)
            with sr.AudioFile(audio_io) as source:
                audio = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio, language=self.voice_settings.language.value)
        except Exception as e:
            logger.error(f"Reconnaissance locale échouée: {e}")
        
        return None
    
    async def _azure_speech_to_text(self, audio_io: io.BytesIO) -> Optional[str]:
        """Reconnaissance vocale avec Azure Speech Services"""
        try:
            speech_config = speechsdk.SpeechConfig(
                subscription=self.azure_speech_key,
                region=self.azure_region
            )
            speech_config.speech_recognition_language = self.voice_settings.language.value
            
            audio_io.seek(0)
            audio_config = speechsdk.audio.AudioConfig(stream=speechsdk.audio.PushAudioInputStream())
            
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            # Push audio data
            audio_config.stream.write(audio_io.read())
            audio_config.stream.close()
            
            result = speech_recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return result.text
            
        except Exception as e:
            logger.error(f"Erreur Azure STT: {e}")
        
        return None
    
    async def _google_speech_to_text(self, audio_io: io.BytesIO) -> Optional[str]:
        """Reconnaissance vocale avec Google Cloud Speech"""
        try:
            client = google_speech.SpeechClient()
            
            audio_io.seek(0)
            content = audio_io.read()
            
            audio = google_speech.RecognitionAudio(content=content)
            config = google_speech.RecognitionConfig(
                encoding=google_speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.sample_rate,
                language_code=self.voice_settings.language.value,
                enable_automatic_punctuation=True,
                use_enhanced=True
            )
            
            response = client.recognize(config=config, audio=audio)
            
            if response.results:
                return response.results[0].alternatives[0].transcript
                
        except Exception as e:
            logger.error(f"Erreur Google STT: {e}")
        
        return None
    
    async def _openai_speech_to_text(self, audio_io: io.BytesIO) -> Optional[str]:
        """Reconnaissance vocale avec OpenAI Whisper"""
        try:
            audio_io.seek(0)
            
            # Sauvegarde temporaire pour OpenAI
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_io.read())
                temp_path = temp_file.name
            
            try:
                with open(temp_path, 'rb') as audio_file:
                    transcript = openai.Audio.transcribe(
                        model="whisper-1",
                        file=audio_file,
                        language=self.voice_settings.language.value[:2]
                    )
                    return transcript.text
            finally:
                os.unlink(temp_path)
                
        except Exception as e:
            logger.error(f"Erreur OpenAI STT: {e}")
        
        return None
    
    def _synthesis_loop(self):
        """Boucle de synthèse vocale"""
        while True:
            try:
                # Récupération d'une demande de synthèse
                synthesis_request = self.synthesis_queue.get(timeout=1.0)
                
                text = synthesis_request.get('text')
                settings = synthesis_request.get('settings', self.voice_settings)
                callback = synthesis_request.get('callback')
                
                if text:
                    audio_data = self._synthesize_speech_premium(text, settings)
                    if audio_data and callback:
                        callback(audio_data)
                        
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erreur synthèse vocale: {e}")
    
    def _synthesize_speech_premium(self, text: str, settings: VoiceSettings) -> Optional[bytes]:
        """Synthèse vocale haute qualité"""
        
        # Tentative avec ElevenLabs (voix très naturelles)
        if self.elevenlabs_api_key and settings.quality == VoiceQuality.PREMIUM:
            try:
                return self._elevenlabs_text_to_speech(text, settings)
            except Exception as e:
                logger.warning(f"ElevenLabs TTS échoué: {e}")
        
        # Tentative avec Azure Speech (excellent pour le français)
        if self.azure_speech_key:
            try:
                return self._azure_text_to_speech(text, settings)
            except Exception as e:
                logger.warning(f"Azure TTS échoué: {e}")
        
        # Fallback: Google Cloud TTS
        if self.google_credentials:
            try:
                return self._google_text_to_speech(text, settings)
            except Exception as e:
                logger.warning(f"Google TTS échoué: {e}")
        
        # Fallback final: TTS local
        try:
            return self._local_text_to_speech(text, settings)
        except Exception as e:
            logger.error(f"TTS local échoué: {e}")
        
        return None
    
    def _elevenlabs_text_to_speech(self, text: str, settings: VoiceSettings) -> bytes:
        """Synthèse avec ElevenLabs (voix premium)"""
        try:
            # Sélection de la voix selon la langue et le ton
            voice_map = {
                Language.FRENCH: "Antoine" if settings.tone == EmotionalTone.AUTHORITATIVE else "Charlotte",
                Language.ENGLISH: "Adam" if settings.tone == EmotionalTone.AUTHORITATIVE else "Bella",
            }
            
            voice_name = voice_map.get(settings.language, "Charlotte")
            
            audio = generate(
                text=text,
                voice=Voice(voice_name),
                model="eleven_multilingual_v2"
            )
            
            return audio
            
        except Exception as e:
            logger.error(f"Erreur ElevenLabs: {e}")
            raise
    
    def _azure_text_to_speech(self, text: str, settings: VoiceSettings) -> bytes:
        """Synthèse avec Azure Speech Services"""
        try:
            speech_config = speechsdk.SpeechConfig(
                subscription=self.azure_speech_key,
                region=self.azure_region
            )
            
            # Sélection de la voix selon la langue et le ton
            voice_map = {
                Language.FRENCH: {
                    EmotionalTone.NEUTRAL: "fr-FR-DeniseNeural",
                    EmotionalTone.AUTHORITATIVE: "fr-FR-HenriNeural",
                    EmotionalTone.REASSURING: "fr-FR-EloiseNeural",
                    EmotionalTone.URGENT: "fr-FR-ClaudeNeural"
                },
                Language.ENGLISH: {
                    EmotionalTone.NEUTRAL: "en-US-JennyNeural",
                    EmotionalTone.AUTHORITATIVE: "en-US-GuyNeural",
                    EmotionalTone.REASSURING: "en-US-AriaNeural"
                }
            }
            
            voice_name = voice_map.get(settings.language, {}).get(settings.tone, "fr-FR-DeniseNeural")
            speech_config.speech_synthesis_voice_name = voice_name
            
            # Configuration SSML pour le contrôle émotionnel
            if settings.use_ssml:
                ssml_text = self._create_ssml(text, settings)
            else:
                ssml_text = text
            
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=None
            )
            
            result = synthesizer.speak_ssml_async(ssml_text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return result.audio_data
            
        except Exception as e:
            logger.error(f"Erreur Azure TTS: {e}")
            raise
        
        return None
    
    def _google_text_to_speech(self, text: str, settings: VoiceSettings) -> bytes:
        """Synthèse avec Google Cloud Text-to-Speech"""
        try:
            client = google_tts.TextToSpeechClient()
            
            synthesis_input = google_tts.SynthesisInput(text=text)
            
            # Configuration de la voix
            voice = google_tts.VoiceSelectionParams(
                language_code=settings.language.value,
                ssml_gender=google_tts.SsmlVoiceGender.FEMALE
            )
            
            # Configuration audio
            audio_config = google_tts.AudioConfig(
                audio_encoding=google_tts.AudioEncoding.LINEAR16,
                speaking_rate=settings.speed,
                pitch=settings.pitch,
                volume_gain_db=20 * np.log10(settings.volume) if settings.volume > 0 else -20
            )
            
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            logger.error(f"Erreur Google TTS: {e}")
            raise
    
    def _local_text_to_speech(self, text: str, settings: VoiceSettings) -> bytes:
        """Synthèse vocale locale avec pyttsx3"""
        try:
            # Configuration du moteur
            self.tts_engine.setProperty('rate', int(150 * settings.speed))
            self.tts_engine.setProperty('volume', settings.volume)
            
            # Sauvegarde temporaire
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            try:
                self.tts_engine.save_to_file(text, temp_path)
                self.tts_engine.runAndWait()
                
                with open(temp_path, 'rb') as f:
                    return f.read()
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"Erreur TTS local: {e}")
            raise
    
    def _create_ssml(self, text: str, settings: VoiceSettings) -> str:
        """Création de SSML pour contrôle émotionnel avancé"""
        
        # Mapping des tons émotionnels vers les styles SSML
        style_map = {
            EmotionalTone.NEUTRAL: "neutral",
            EmotionalTone.CONCERNED: "sad",
            EmotionalTone.URGENT: "excited",
            EmotionalTone.CALM: "calm",
            EmotionalTone.AUTHORITATIVE: "serious",
            EmotionalTone.REASSURING: "gentle"
        }
        
        style = style_map.get(settings.tone, "neutral")
        
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{settings.language.value}">
            <mstts:express-as style="{style}" styledegree="2">
                <prosody rate="{settings.speed:.1f}" pitch="{settings.pitch:.1f}" volume="{settings.volume:.1f}">
                    {text}
                </prosody>
            </mstts:express-as>
        </speak>
        """
        
        return ssml.strip()
    
    # Interface publique
    
    async def start_listening(self, callback: Callable[[str, datetime], None]):
        """Démarrage de l'écoute en continu"""
        if not self.is_initialized:
            await self.initialize()
        
        self.speech_callback = callback
        self.is_listening = True
        logger.info("Écoute vocale démarrée")
    
    def stop_listening(self):
        """Arrêt de l'écoute"""
        self.is_listening = False
        logger.info("Écoute vocale arrêtée")
    
    async def speak(self, text: str, settings: Optional[VoiceSettings] = None, 
                   callback: Optional[Callable] = None) -> bool:
        """Synthèse et lecture d'un texte"""
        if not text.strip():
            return False
        
        if not self.is_initialized:
            await self.initialize()
        
        settings = settings or self.voice_settings
        
        try:
            # Adaptation contextuelle du message
            adapted_text = self._adapt_message_for_security(text, settings.tone)
            
            # Ajout à la queue de synthèse
            synthesis_request = {
                'text': adapted_text,
                'settings': settings,
                'callback': callback or self._play_audio
            }
            
            self.synthesis_queue.put(synthesis_request)
            
            logger.info(f"Message en cours de synthèse: '{adapted_text[:50]}...'")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la synthèse: {e}")
            return False
    
    def _adapt_message_for_security(self, text: str, tone: EmotionalTone) -> str:
        """Adaptation du message selon le contexte de sécurité"""
        
        # Préfixes contextuels selon le ton
        prefixes = {
            EmotionalTone.URGENT: "ALERTE SÉCURITÉ: ",
            EmotionalTone.CONCERNED: "Attention: ",
            EmotionalTone.REASSURING: "Information: ",
            EmotionalTone.AUTHORITATIVE: "Directive sécurité: "
        }
        
        prefix = prefixes.get(tone, "")
        
        # Ajout d'emphases pour les mots-clés de sécurité
        security_keywords = [
            "menace", "vulnérabilité", "attaque", "malware", "intrusion",
            "critique", "urgent", "bloqué", "infecté", "compromis"
        ]
        
        adapted_text = text
        for keyword in security_keywords:
            if keyword in adapted_text.lower():
                adapted_text = adapted_text.replace(
                    keyword, 
                    f"<emphasis level='strong'>{keyword}</emphasis>"
                )
        
        return prefix + adapted_text
    
    def _play_audio(self, audio_data: bytes):
        """Lecture audio avec PyAudio"""
        try:
            if not audio_data:
                return
            
            # Ouverture du stream de sortie
            stream = self.audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.sample_rate,
                output=True
            )
            
            # Lecture des données audio
            chunk_size = 1024
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i:i + chunk_size]
                stream.write(chunk)
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            logger.error(f"Erreur lecture audio: {e}")
    
    async def set_voice_settings(self, settings: VoiceSettings):
        """Configuration des paramètres vocaux"""
        self.voice_settings = settings
        logger.info(f"Paramètres vocaux mis à jour: {settings.language.value}, {settings.quality.value}")
    
    async def get_available_voices(self) -> List[Dict[str, str]]:
        """Liste des voix disponibles"""
        voices = []
        
        # Voix locales
        if self.tts_engine:
            local_voices = self.tts_engine.getProperty('voices')
            for voice in local_voices:
                voices.append({
                    'id': voice.id,
                    'name': voice.name,
                    'language': getattr(voice, 'languages', ['unknown'])[0],
                    'service': 'local'
                })
        
        # Voix Azure (exemple)
        if self.azure_speech_key:
            azure_voices = [
                {'id': 'fr-FR-DeniseNeural', 'name': 'Denise (Français)', 'language': 'fr-FR', 'service': 'azure'},
                {'id': 'fr-FR-HenriNeural', 'name': 'Henri (Français)', 'language': 'fr-FR', 'service': 'azure'},
                {'id': 'en-US-JennyNeural', 'name': 'Jenny (English)', 'language': 'en-US', 'service': 'azure'},
            ]
            voices.extend(azure_voices)
        
        return voices
    
    def cleanup(self):
        """Nettoyage des ressources"""
        self.is_listening = False
        self.is_speaking = False
        
        if self.audio:
            self.audio.terminate()
        
        if self.tts_engine:
            self.tts_engine.stop()
        
        logger.info("Moteur vocal nettoyé")
    
    def __del__(self):
        """Destructeur"""
        self.cleanup()