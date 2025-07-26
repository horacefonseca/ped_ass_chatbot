# 🏥 Guía de Pruebas en Google Colab

## 📋 Pasos para probar el chatbot después de sincronizar

### 1. **Sincronizar con GitHub**
```bash
git add .
git commit -m "Add testing files and improvements 🤖"
git push origin main
```

### 2. **Abrir Google Colab**
- Ve a [colab.research.google.com](https://colab.research.google.com)
- Selecciona **GitHub** como fuente
- Busca tu repositorio: `usuario/ped_ass_chatbot`
- Abre el archivo: `Colab_Testing_Notebook.ipynb`

### 3. **Ejecutar las pruebas**

#### **Opción A: Notebook Completo (Recomendado)**
1. Ejecuta todas las celdas en orden
2. Sigue las instrucciones en pantalla
3. Prueba el chat interactivo

#### **Opción B: Script de Pruebas Rápidas**
```python
# En una celda de Colab:
!git clone https://github.com/tu-usuario/ped_ass_chatbot.git
%cd ped_ass_chatbot
!pip install chatterbot chatterbot_corpus pytz

# Ejecutar pruebas automáticas
exec(open('colab_test_runner.py').read())
```

### 4. **Pruebas que se ejecutarán**

#### ✅ **Pruebas Automáticas:**
- **Flujo de reservas**: Proceso completo de agendar cita
- **Sistema FAQs**: Respuestas a preguntas frecuentes  
- **Manejo de errores**: Respuestas a entradas inválidas
- **Navegación**: Comandos menu/back/quit

#### 🎯 **Escenarios de Prueba:**

**1. Reserva de Cita Completa:**
```
Usuario: "hello"
Bot: [Muestra menú principal]

Usuario: "appointment" 
Bot: [Lista doctores disponibles]

Usuario: "Aguilar"
Bot: [Muestra fechas disponibles]

Usuario: "25/07/2025"
Bot: [Muestra horarios disponibles]

Usuario: "10:00 AM"
Bot: [Solicita nombre del paciente]

Usuario: "Maria Rodriguez"
Bot: [Solicita confirmación]

Usuario: "yes"
Bot: [Confirma cita exitosamente]
```

**2. Consultas FAQ:**
```
Usuario: "faqs"
Bot: [Muestra opciones de FAQ]

Usuario: "hours"
Bot: [Horarios de la clínica]

Usuario: "location"  
Bot: [Dirección y ubicación]
```

**3. Información de Doctores:**
```
Usuario: "3" (información clínica)
Bot: [Detalles de doctores y especialidades]
```

### 5. **Resultados Esperados**

#### 🟢 **Funcionalidades que deben funcionar:**
- ✅ Reserva de citas médicas
- ✅ Consulta de disponibilidad de doctores
- ✅ FAQs sobre la clínica
- ✅ Navegación entre menús
- ✅ Manejo de errores graceful
- ✅ Validación de fechas y horarios
- ✅ Prevención de citas duplicadas

#### 📊 **Métricas de Éxito:**
- **Tasa de éxito de reservas**: >90%
- **Respuestas FAQ correctas**: >95%
- **Manejo de errores**: 100%
- **Navegación fluida**: 100%

### 6. **Doctores Disponibles para Pruebas**

| Doctor | Especialidad | Días | Horarios |
|--------|--------------|------|----------|
| **Dr. Aguilar** | Pediatría General | L, M, V | 8AM-4PM |
| **Dr. Chacon** | Alergias | M, J | 9AM-5PM |
| **Dr. Villalobos** | Medicina Adolescente | M | 8AM-4PM |
| **Dr. Irias** | Neonatología | M, M, J, V | 10AM-4PM |

### 7. **Comandos Útiles para Pruebas**

#### **Navegación:**
- `menu` - Volver al menú principal
- `back` - Regresar al paso anterior  
- `quit` - Salir del chatbot

#### **Reservas rápidas:**
- `appointment` o `1` - Reservar cita
- `any` - Cualquier doctor disponible
- `Aguilar` / `Chacon` / `Villalobos` / `Irias` - Doctor específico

#### **Información:**
- `faqs` o `2` - Preguntas frecuentes
- `hours` - Horarios de atención
- `location` - Ubicación de la clínica
- `contact` - Información de contacto

### 8. **Solución de Problemas**

#### **Si hay errores de instalación:**
```python
!pip install --upgrade chatterbot
!pip install chatterbot-corpus==1.2.0
!pip install pytz
```

#### **Si el bot no responde correctamente:**
```python
# Reiniciar el bot
bot.current_state = "MAIN_MENU"
bot.current_booking = {}
```

#### **Para debugging:**
```python
# Ver estado actual del bot
print(f"Estado: {bot.current_state}")
print(f"Reserva actual: {bot.current_booking}")

# Ver citas programadas
print(f"Citas: {bot.scheduler.appointments}")
```

### 9. **Personalización para tu Clínica**

Para adaptar a tu clínica real, modifica:

1. **Información de doctores** en `initialize_doctors()`
2. **FAQs** en el diccionario `faqs`
3. **Datos de la clínica** en `show_clinic_info()`
4. **Horarios y días** según tu disponibilidad

### 10. **Próximos Pasos**

#### **Para Producción:**
- [ ] Conectar con base de datos real
- [ ] Integrar con sistema de citas existente
- [ ] Agregar autenticación de usuarios
- [ ] Implementar notificaciones por email/SMS
- [ ] Configurar logging y monitoreo

#### **Para Expandir Funcionalidades:**
- [ ] Recordatorios automáticos de citas
- [ ] Reprogramación de citas
- [ ] Historiales médicos básicos
- [ ] Integración con WhatsApp/Telegram
- [ ] Sistema de pagos

---

## 🎉 ¡Listo para Probar!

Tu chatbot está completamente funcional y listo para ser probado en Google Colab. 

**💡 Consejo**: Ejecuta primero las pruebas automáticas para verificar que todo funciona, luego usa el modo interactivo para explorar todas las funcionalidades.

---

**📞 Contacto de la Clínica (Demo):**
- **Nombre:** Pediatric Associates Doral
- **Dirección:** 9655 NW 41st Street, Doral, FL
- **Teléfono:** +1-305-436-1563
- **Horarios:** Lunes-Viernes 8AM-5PM