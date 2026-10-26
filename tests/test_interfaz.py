"""Navegador real; la frontera de entrega del SO se controla explícitamente."""
from datetime import datetime, timezone
import json
import pytest
from playwright.sync_api import expect

@pytest.fixture(params=[360,1280])
def vista(browser,servidor,request):
    contexto=browser.new_context(viewport={'width':request.param,'height':900},timezone_id='America/La_Paz')
    contexto.add_init_script("""
      window.permisoPrueba='default'; window.avisosPrueba=[]; window.solicitudesPrueba=0;
      Object.defineProperty(Notification,'permission',{get:()=>window.permisoPrueba});
      Notification.requestPermission=async()=>{window.solicitudesPrueba++; return window.permisoPrueba='granted'};
      ServiceWorkerRegistration.prototype.showNotification=async function(titulo,opciones){
        if(window.falloPrueba) throw new Error('Fallo conocido');
        window.avisosPrueba.push({titulo,...opciones});
      };
    """)
    pagina=contexto.new_page()
    pagina.clock.install(time=datetime(2026,10,27,19,tzinfo=timezone.utc))
    pagina.goto(servidor)
    expect(pagina.get_by_role('heading',name='Tu agenda académica')).to_be_visible()
    pagina.wait_for_function('window.recordatorios && window.recordatorios.lista')
    yield pagina
    contexto.close()

def activar(pagina):
    pagina.get_by_role('button',name='Activar recordatorios').click()
    expect(pagina.locator('#estado-recordatorios')).to_contain_text('disponibles')

def test_permiso_solo_tras_gesto_y_disposicion(vista):
    assert vista.evaluate('window.solicitudesPrueba')==0
    activar(vista)
    assert vista.evaluate('window.solicitudesPrueba')==1
    assert vista.evaluate('!!navigator.serviceWorker.controller')
    assert vista.evaluate('document.documentElement.scrollWidth <= innerWidth')
    vista.get_by_label('Nombre de materia').fill('Historia')
    vista.get_by_label('Color de materia').select_option('verde')
    vista.get_by_role('button',name='Guardar materia').click()
    expect(vista.locator('#catalogo')).to_contain_text('Historia')

def test_veinte_avisos_y_repeticiones(vista,tarea,cliente):
    for i in range(20): tarea(titulo=f'Tarea {i}')
    tarea(estado='completada'); tarea(fecha='2026-10-27')
    activar(vista)
    vista.wait_for_function('window.avisosPrueba.length===20')
    avisos=vista.evaluate('window.avisosPrueba')
    assert all('Contenido privado' not in str(d) for d in avisos)
    assert all('Cálculo I' in d['body'] for d in avisos)
    for _ in range(10): vista.evaluate('window.recordatorios.evaluar()')
    assert len(vista.evaluate('window.avisosPrueba'))==20
    vista.reload(); vista.wait_for_function('window.recordatorios && window.recordatorios.lista')
    activar(vista)
    vista.evaluate('window.recordatorios.evaluar()')
    assert vista.evaluate('window.avisosPrueba')==[]

def test_denegado_revocado_y_fallo(vista,tarea,cliente):
    tarea()
    vista.evaluate("window.permisoPrueba='denied'")
    vista.evaluate('window.recordatorios.evaluar()')
    expect(vista.locator('#estado-recordatorios')).to_contain_text('denegado')
    assert vista.evaluate('window.avisosPrueba')==[]
    vista.evaluate("window.permisoPrueba='granted';window.falloPrueba=true")
    vista.evaluate('window.recordatorios.evaluar()')
    expect(vista.locator('#error-recordatorios')).to_contain_text('No se pudo emitir')
    assert cliente.get('/api/recordatorios').json()[0]['resultado']=='no_emitido'
    vista.evaluate('window.falloPrueba=false')
    vista.evaluate('window.recordatorios.evaluar()')
    assert len(vista.evaluate('window.avisosPrueba'))==1
    vista.evaluate("window.permisoPrueba='denied'")
    vista.evaluate('window.recordatorios.evaluar()')
    expect(vista.locator('#estado-recordatorios')).to_contain_text('denegado')

def test_calendario_y_timer(vista,tarea):
    tarea()
    vista.clock.set_fixed_time(datetime(2026,10,27,12,59,59,tzinfo=timezone.utc))
    activar(vista)
    vista.evaluate('window.recordatorios.evaluar()')
    assert vista.evaluate('window.avisosPrueba')==[]
    vista.clock.set_fixed_time(datetime(2026,10,27,13,0,0,tzinfo=timezone.utc))
    vista.clock.run_for(30001)
    vista.wait_for_function('window.avisosPrueba.length===1')

def test_agenda_completado_filtros_y_borrado(vista):
    vista.get_by_label('Nombre de materia').fill('Álgebra')
    vista.get_by_label('Color de materia').select_option('azul')
    vista.get_by_role('button',name='Guardar materia').click()
    expect(vista.locator('#catalogo')).to_contain_text('Álgebra')
    vista.get_by_label('Título de tarea').fill('Resolver ejercicios')
    vista.get_by_label('Fecha de entrega').fill('2026-10-28')
    vista.get_by_role('button',name='Guardar tarea').click()
    expect(vista.locator('#listado')).to_contain_text('Resolver ejercicios')
    expect(vista.locator('#listado')).to_contain_text('Urgente')
    vista.get_by_role('button',name='Completar Resolver ejercicios').click()
    expect(vista.locator('#listado')).to_contain_text('Completada')
    vista.get_by_label('Filtrar por estado').select_option('pendiente')
    expect(vista.locator('#listado')).to_contain_text('No hay tareas para estos filtros')
    vista.get_by_role('button',name='Borrar Álgebra').click()
    vista.get_by_role('button',name='Confirmar borrado').click()
    expect(vista.locator('#aviso')).to_contain_text('No puedes borrar una materia con tareas')

def test_dos_contextos_y_resultado_incierto(vista,tarea,cliente,browser,servidor):
    tarea()
    activar(vista)
    vista.wait_for_function('window.avisosPrueba.length===1')
    otro=browser.new_context(permissions=['notifications'],timezone_id='America/La_Paz')
    otro.add_init_script("""window.avisosPrueba=[];
      ServiceWorkerRegistration.prototype.showNotification=async function(...x){window.avisosPrueba.push(x)};""")
    pagina=otro.new_page(); pagina.clock.install(time=datetime(2026,10,27,19,tzinfo=timezone.utc))
    pagina.goto(servidor); pagina.wait_for_function('window.recordatorios && window.recordatorios.lista')
    pagina.evaluate('window.recordatorios.evaluar()')
    assert pagina.evaluate('window.avisosPrueba')==[]
    otro.close()

def test_capacidad_ausente_no_bloquea(browser,servidor):
    c=browser.new_context()
    c.add_init_script("Object.defineProperty(window,'Notification',{value:undefined})")
    p=c.new_page();p.goto(servidor)
    expect(p.locator('#estado-recordatorios')).to_contain_text('no disponibles')
    expect(p.get_by_role('button',name='Guardar materia')).to_be_enabled()
    c.close()
