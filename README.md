# PARZIVAL---BOT-para-TikTok-Live.
Un bot robusto para leer comentarios en Live de TikTok con voz humana.

# 🚀 PARZIVAL - BOT para TikTok live.

**PARZIVAL** es un bot robusto diseñado para leer comentarios de TikTok Live en tiempo real utilizando síntesis de voz (TTS). A diferencia de otros bots, PARZIVAL utiliza un sistema de **aislamiento de procesos** para evitar que el motor de voz se congele durante transmisiones con mucho tráfico.

## ✨ Características Únicas
- **Estabilidad Total:** Usa subprocesos independientes para la voz, evitando bloqueos del programa principal.
- **Sistema VIP:** Prioridad de lectura para usuarios específicos.
- **Anti-Spam:** Control de cooldown por usuario para evitar saturación.
- **Auto-Reconexión:** Se mantiene conectado incluso si hay micro-cortes de internet.

## 🛠️ Instalación

1. Clona este repositorio o descarga el archivo `parzival_bot.py`.
   
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   
3. Cambia el nombre de usuario en la linea 58 del archivo `parzival_bot.py`
   USUARIO = "tu_usuario_sin_@" # TU USUARIO SIN EL @
   
4. Cambia el nombre de VIP_USERS en la linea 59 del archivo `parzival_bot.py`
   VIP_USERS = {"USUARIO_1", "USUARIO_2"}   # USUARIOS SIN @ set → búsqueda O(1)
   
5. Ejecuta el bot con el siguiente comando:
   python parzival_bot.py



📜 Créditos y Desarrollo

Concepto, Testing y Dirección de Proyecto: parzival14as.

Asistencia en Desarrollo: Co-programado con IA (claude).

Inspiración: Optimizado para la comunidad de creadores de contenido (Live TikTok) que buscan estabilidad y ligereza.

Nota: Este software se proporciona de forma gratuita y con fines educativos.
