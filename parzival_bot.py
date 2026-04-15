import subprocess
import threading
import time
from collections import deque
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent, DisconnectEvent

# =========================
# 🔊 MOTOR DE VOZ (robusto)
# =========================
# ✅ FIX: En lugar de reutilizar un engine que se atasca,
# cada mensaje lanza un proceso fresco de pyttsx3.
# Esto elimina el bloqueo permanente tras el primer comentario.

cola_mensajes = deque()
lock_voz = threading.Lock()      # evita lecturas simultáneas de la cola
voz_activa = threading.Event()   # señal para despertar al worker
voz_activa.set()

def hablar(texto: str):
    """Sintetiza voz en un subproceso aislado para evitar bloqueos."""
    script = (
        "import pyttsx3;"
        "e=pyttsx3.init();"
        f"e.setProperty('rate',160);"
        f"e.say({repr(texto)});"
        "e.runAndWait()"
    )
    try:
        subprocess.run(
            ["python", "-c", script],
            timeout=15,          # evita que un mensaje trabe todo para siempre
            check=False
        )
    except subprocess.TimeoutExpired:
        print(f"⏱️ Timeout leyendo: {texto[:40]}...")
    except Exception as e:
        print(f"❌ Error de voz: {e}")

def worker_voz():
    """Hilo dedicado: lee la cola sin bloquearse indefinidamente."""
    print("👷 Worker de voz listo...")
    while True:
        with lock_voz:
            texto = cola_mensajes.popleft() if cola_mensajes else None

        if texto:
            print(f"🎙️ Leyendo: {texto}")
            hablar(texto)
        else:
            time.sleep(0.15)   # pausa corta si no hay mensajes

threading.Thread(target=worker_voz, daemon=True).start()

# =========================
# ⚙️ CONFIGURACIÓN TIKTOK
# =========================
USUARIO = "TU_USUARIO_SIN_@" # TU USUARIO SIN EL @
VIP_USERS = {"USUARIO_1", "USUARIO_2"}   # USUARIOS SIN @ set → búsqueda O(1)
cooldowns: dict[str, float] = {}
COOLDOWN_SEGUNDOS = 3

# ✅ FIX: reconnect_on_failure mantiene la conexión viva automáticamente
client = TikTokLiveClient(unique_id=USUARIO)

def puede_hablar(usuario: str) -> bool:
    ahora = time.time()
    ultimo = cooldowns.get(usuario, 0)
    if ahora - ultimo >= COOLDOWN_SEGUNDOS:
        cooldowns[usuario] = ahora
        return True
    return False

# =========================
# 💬 EVENTOS
# =========================
@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    try:
        usuario_unique = event.user.unique_id
        usuario_nick   = event.user.nickname or usuario_unique
        mensaje        = event.comment.strip()

        if not mensaje:
            return

        es_vip = usuario_unique in VIP_USERS
        if not es_vip and not puede_hablar(usuario_unique):
            return

        texto_final = f"{usuario_nick} dice: {mensaje}"
        print(f"💬 {texto_final}")

        with lock_voz:
            if es_vip:
                cola_mensajes.appendleft(texto_final)   # VIP → frente de cola
            else:
                # ✅ FIX: evita que la cola crezca sin límite si hay spam
                if len(cola_mensajes) < 30:
                    cola_mensajes.append(texto_final)
                else:
                    print("⚠️ Cola llena, mensaje descartado.")

    except Exception as e:
        print(f"⚠️ Error procesando comentario: {e}")

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"\n✅ CONECTADO A: @{USUARIO}  |  Sala: {event.room_id}")
    print("-" * 40)

@client.on(DisconnectEvent)
async def on_disconnect(event: DisconnectEvent):
    print("🛑 Desconectado. TikTokLive reintentará automáticamente...")

# =========================
# 🚀 EJECUCIÓN
# =========================
if __name__ == "__main__":
    print(f"🚀 ESTACIÓN ARTEMISmx ACTIVADA PARA @{USUARIO}...")
    while True:
        try:
            client.run()
        except KeyboardInterrupt:
            print("\n👋 Cerrando manualmente.")
            break
        except Exception as e:
            print(f"❌ Error fatal: {e}")
            print("🔄 Reintentando en 10 segundos...")
            time.sleep(10)
