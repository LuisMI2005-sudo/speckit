# Investigación y decisiones

**Fecha**: 2026-10-26

- Decisión: SQLite con reserva atómica y clave única por tarea/fecha. Motivo:
  coordinar pestañas y perfiles. Alternativa descartada: solo almacenamiento del
  navegador, que no coordina perfiles. [Transacciones SQLite](https://www.sqlite.org/lang_transaction.html).
- Decisión: resultado incierto antes de llamar al navegador; confirmar por token.
  Motivo: no existe transacción conjunta entre el SO y SQLite. Fracaso conocido
  permite reintentar; cierre incierto no. No se promete exactamente una visualización.
- Decisión: service worker y showNotification tras consentimiento. Motivo:
  soportar el mecanismo requerido por navegadores móviles compatibles. Alternativa:
  constructor Notification, insuficiente en muchos móviles.
  [Notificaciones](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/showNotification).
- Decisión: instante del dispositivo y zona IANA convertidos con zoneinfo/tzdata.
  Motivo: no confundir un día de calendario con 24 horas ni usar la zona del servidor.
  [Zoneinfo](https://docs.python.org/3.12/library/zoneinfo.html).
- Decisión: pytest-playwright, registro real del service worker y frontera de entrega
  controlada para pruebas reproducibles. Alternativa: comprobar solo API, insuficiente.
  [Service workers y pruebas](https://playwright.dev/python/docs/service-workers).
- Decisión: implementar la base necesaria en el mismo proyecto, conservando el
  alcance de la especificación 001; esta dependencia está autorizada por FR-012 de 002.

No quedan investigaciones bloqueantes. Los permisos y presentación dependen del
navegador y SO; no confundir una solicitud aceptada con una notificación leída.
