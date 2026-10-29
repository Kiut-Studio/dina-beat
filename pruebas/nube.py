# Prueba de la nube (☁️ cuenta de Google y desafíos con resultado automático) con una nube FALSA:
# cada "teléfono" es un navegador aparte y todos comparten este diccionario de Python en vez de Firebase.
# Servidor en el puerto 8766, como las otras pruebas.
import asyncio,json
from playwright.async_api import async_playwright
import os; SP=os.path.dirname(os.path.abspath(__file__))+'/'
NUBE={}
def mock(op,path,data):
  if op=='get': return NUBE.get(path)
  if op=='set':
    d=json.loads(json.dumps(data['d']))
    if data.get('m') and isinstance(NUBE.get(path),dict): NUBE[path]={**NUBE[path],**d}
    else: NUBE[path]=d
    return True
  if op=='since':
    pre=path+'/';return [{'id':k[len(pre):],'data':v} for k,v in NUBE.items() if k.startswith(pre) and '/' not in k[len(pre):] and v.get(data['f'],0)>data['v']]
  if op in('list','top','count'):
    pre=path+'/';L=[{'id':k[len(pre):],'data':v} for k,v in NUBE.items() if k.startswith(pre) and '/' not in k[len(pre):]]
    if op=='top': return sorted(L,key=lambda r:-r['data'].get(data['f'],0))[:data['n']]
    if op=='count': return sum(1 for r in L if r['data'].get(data['f'],0)>data['v'])
    return L
  if op=='del': NUBE.pop(path,None);return True
  return None
MOCK='''window.CLOUD_MOCK={
  onUser:cb=>{cb(JSON.parse(localStorage.getItem('mockUser')||'null'))},
  google:async()=>{const u={uid:window.MOCK_UID,anon:false,name:'Leandro Casco',email:'leandro@ejemplo.com',photo:''};localStorage.setItem('mockUser',JSON.stringify(u));return u},
  anon:async()=>{const u={uid:'anon-'+Math.random().toString(36).slice(2,8),anon:true};localStorage.setItem('mockUser',JSON.stringify(u));return u},
  out:async()=>{localStorage.removeItem('mockUser')},
  get:p=>window.mockCloud('get',p,null),set:(p,d,m)=>window.mockCloud('set',p,{d,m:!!m}),list:p=>window.mockCloud('list',p,null),
  top:(p,f,n)=>window.mockCloud('top',p,{f,n}),count:(p,f,v)=>window.mockCloud('count',p,{f,v}),del:p=>window.mockCloud('del',p,null),since:(p,f,v)=>window.mockCloud('since',p,{f,v})};'''
async def phone(b,uid,errs):
  ctx=await b.new_context(viewport={'width':360,'height':640})
  await ctx.expose_function('mockCloud',mock)
  await ctx.add_init_script(f"window.FORCE_SS=1;window.MOCK_UID={json.dumps(uid)};"+MOCK)
  pg=await ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
  await pg.goto('http://localhost:8766/#prueba');await pg.wait_for_timeout(600);return ctx,pg
WIN='''async(i)=>{SS.startStage(i);await new Promise(r=>setTimeout(r,300));for(const n of SS.notes){n.st=1;n.off=0.01}SS.cnt.p=SS.notes.length;SS.finish(true);await new Promise(r=>setTimeout(r,1000));SS.toMenu()}'''
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);errs=[]
    # 📱 arranque con un guardado que ya usó la nube (ranking, salas): no tiene que haber errores (en la 0.19 de prueba, canRank se usaba antes de existir)
    c0=await b.new_context();await c0.add_init_script('''if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem("sofiSilbato.v1",JSON.stringify({best:[5000,0,0],stars:[3,0,0],open:2,name:"Leandro",cloud:1,rk:[{best:5000,pos:2,down:1},{},{}],salas:{abc123:{song:"Etapa 1 · Tranqui",at:Date.now(),own:1,me:4000,pos:2,count:3,top:{n:"Deisy",s:7000}}},newRes:2,songs:[],set:{}}))}''')
    p0=await c0.new_page();e0=[];p0.on('pageerror',lambda e:e0.append(str(e)))
    await p0.goto('http://localhost:8766/');await p0.wait_for_timeout(1500);await p0.reload();await p0.wait_for_timeout(1500)
    print('arranque con guardado de la nube: errores',e0,'· menú',await p0.evaluate('()=>document.querySelector(".st[data-i=\'0\'] span").innerText.replace(/\\n/g," ")'));await c0.close()
    # 📱 A: juega sin cuenta, compone una canción y después entra con Google
    ca,a=await phone(b,'G1',errs)
    await a.evaluate(WIN,0)
    await a.evaluate('()=>{SS.save.songs.unshift({id:"cA",name:"La de A",bpm:100,drums:true,notes:Array(64).fill(null).map((x,i)=>i%4?null:60)});SS.save.set.lat=120;SS.save.name="Leandro"}')
    await a.click('#cfgB');await a.click('#acctB');await a.wait_for_timeout(300);await a.click('#gIn');await a.wait_for_timeout(1500)
    await a.screenshot(path=SP+'m_cuenta.png')
    nube1=NUBE.get('jugadores/G1',{});pa=[k for k in NUBE if k.startswith('jugadores/G1/partidas/')]
    print('A entra: en la nube estrellas',nube1.get('beat',{}).get('stars'),'· canciones',[s['name'] for s in nube1.get('beat',{}).get('songs',[])],'· ajuste de ritmo sube?', 'lat' in nube1.get('beat',{}).get('set',{}),'· partidas',len(pa),'· botón',await a.inner_text('#acctB') if not await a.evaluate('()=>document.getElementById("cfg").hidden') else (await a.evaluate('()=>SS.cloud.google')))
    # 📱 B: otro teléfono con su propio progreso (etapa 2 desbloqueada y otro récord), entra con la misma cuenta
    cb_,bb=await phone(b,'G1',errs)
    await bb.evaluate('()=>{const s=SS.save;s.best=[0,7777,0];s.stars=[0,2,0];s.open=2;s.songs=[{id:"cB",name:"La de B",bpm:110,drums:false,notes:Array(64).fill(null).map((x,i)=>i%2?null:64)}];s.set.lat=40;localStorage.setItem("sofiSilbato.v1",JSON.stringify(s))}')
    await bb.reload();await bb.wait_for_timeout(500)
    await bb.click('#cfgB');await bb.click('#acctB');await bb.wait_for_timeout(300);await bb.click('#gIn');await bb.wait_for_timeout(1500)
    rb=await bb.evaluate('async()=>{await SS.openHist("plays");return [SS.save.best,SS.save.stars,SS.save.open,SS.save.songs.map(s=>s.name),SS.save.set.lat,SS.histRows.length]}')
    print('B entra y se junta: récords',rb[0],'estrellas',rb[1],'etapas',rb[2],'canciones',rb[3],'ritmo propio de B',rb[4],'partidas bajadas',rb[5])
    # ⚔️ B desafía desde una partida guardada; C (sin cuenta) lo juega y el resultado le llega solo a B
    await bb.evaluate('()=>document.querySelector("#histList [data-h]").click()');await bb.wait_for_timeout(300)
    link=await bb.evaluate('''async()=>{const x=SS.histRows[0];const R=Object.assign({},x.r,{n:"Leandro"});const id=await (async()=>{const r=await SS.cloudLoad();return 1})();
      let url='';await new Promise(res=>{const orig=navigator.clipboard&&navigator.clipboard.writeText;document.getElementById('plDare').click();setTimeout(res,1500)});
      return {msg:document.getElementById('plMsg').textContent,salas:Object.entries(SS.save.salas||{}).sort((x,y)=>y[1].at-x[1].at).map(x=>x[0])}}''')
    did=link['salas'][0] if link['salas'] else None
    dz=NUBE.get('desafios/'+str(did),{})
    print('B desafía: código',did,'· en la nube de',dz.get('de'),'puntaje',dz.get('s'),'· notas',len(dz.get('t',[])))
    R=dict(dz);R.pop('de',None);R.pop('at',None);R['id']=did
    url=await bb.evaluate('async(R)=>location.origin+location.pathname+"#reto="+await SS.packReto(R)',R)
    cc,c=await phone(b,'G9',errs)
    await c.goto('about:blank');await c.goto(url);await c.wait_for_timeout(900)
    await c.fill('#retoName','Sofi');await c.click('#retoGo');await c.wait_for_timeout(500)
    await c.evaluate('()=>{SS.notes.forEach((n,i)=>{if(i%3){n.st=1;n.off=0.02}else n.st=2});SS.cnt.p=SS.notes.filter(n=>n.st===1).length;SS.finish(true)}');await c.wait_for_timeout(2500)
    res=[(k,v.get('n'),v.get('s')) for k,v in NUBE.items() if k.startswith('desafios/'+str(did)+'/resultados/')]
    print('C juega sin cuenta: resultado en la nube',res)
    await bb.evaluate('async()=>{SS.toMenu();await SS.checkResults(true)}');await bb.wait_for_timeout(800)
    av=await bb.evaluate('()=>[SS.save.newRes,document.getElementById("histB").innerText.replace(/\\n/g," ")]')
    await bb.evaluate('async()=>{await SS.openHist("duels")}');await bb.wait_for_timeout(500)
    du=await bb.evaluate('()=>[...document.querySelectorAll("#histList .part")].map(e=>e.innerText.replace(/\\n/g," "))')
    await bb.screenshot(path=SP+'m_duelos_nube.png')
    print('B ve el resultado: aviso',av,'· duelos',du,'· aviso después',await bb.evaluate('()=>SS.save.newRes'))
    # 📱 una partida jugada en B aparece en A al reabrir (sin esperar 12 horas)
    await bb.evaluate('async()=>{SS.toMenu();SS.startStage(1);await new Promise(r=>setTimeout(r,300));for(const n of SS.notes){n.st=1;n.off=0.01}SS.cnt.p=SS.notes.length;SS.score=1234;SS.finish(true);await new Promise(r=>setTimeout(r,1500));SS.toMenu()}')
    await a.reload();await a.wait_for_timeout(2500)
    print('partida de B en A al reabrir:',await a.evaluate('async()=>{await SS.openHist("plays");return SS.histRows.some(x=>x.score===1234)}'))
    await a.evaluate('()=>SS.toMenu()')
    # 🌎 ranking de la etapa 1 y fantasmas: A (Leandro, 5.000) y N (Nora, 6.000), los dos con cuenta
    PLAY='''async([i,sc])=>{SS.startStage(i);await new Promise(r=>setTimeout(r,300));for(const n of SS.notes){n.st=1;n.off=0.01}SS.cnt.p=SS.notes.length;SS.score=sc;SS.finish(true);await new Promise(r=>setTimeout(r,1500))}'''
    await a.evaluate('()=>SS.toMenu()');await a.evaluate(PLAY,[0,5000])
    ra=await a.evaluate('()=>[document.getElementById("resVs").innerText,JSON.stringify(SS.save.rk[0])]')
    cn,nn=await phone(b,'G2',errs)
    await nn.evaluate('()=>{SS.save.name="Nora";SS.save.char="nora"}');await nn.click('#cfgB');await nn.click('#acctB');await nn.wait_for_timeout(200);await nn.click('#gIn');await nn.wait_for_timeout(1200)
    await nn.evaluate('()=>SS.toMenu()');await nn.evaluate(PLAY,[0,6000])
    await a.evaluate('async()=>{SS.toMenu();await SS.rankRefresh(true);await SS.rankTop(0,true);SS.toMenu()}');await a.wait_for_timeout(300)
    menu=await a.evaluate('()=>document.querySelector(".st[data-i=\'0\'] span").innerText.replace(/\\n/g," ")')
    g=await a.evaluate('()=>(SS.stageGhosts(0)||[]).map(r=>r.n+":"+r.s)')
    await a.evaluate('async()=>{SS.histRows;await SS.openHist("rank")}');await a.wait_for_timeout(500)
    rk=await a.evaluate('()=>[...document.querySelectorAll("#histList .part")].map(e=>e.innerText.replace(/\\n/g," "))')
    await a.screenshot(path=SP+'m_ranking.png')
    await a.evaluate('()=>SS.toMenu()');await a.evaluate('()=>SS.startStage(0)');await a.wait_for_timeout(300)
    gj=await a.evaluate('()=>SS.ghosts.map(g=>g.n)');await a.evaluate('()=>SS.toMenu()')
    print('ranking: A al terminar',ra,'· menú de A',menu,'· fantasmas para A',g,'· tabla',rk,'· jugando con',gj)
    # 🏆 sala: A desafía (enlace corto); C y D sin cuenta la juegan; D ve 2 fantasmas; A ve la tabla
    await a.evaluate(PLAY,[0,4000])
    await a.evaluate('()=>{SS.save.name="Leandro"}');await a.click('#dare');await a.wait_for_timeout(1500)
    sid=await a.evaluate('()=>Object.entries(SS.save.salas).sort((x,y)=>y[1].at-x[1].at)[0][0]')
    url=await a.evaluate('(id)=>location.origin+location.pathname+"#r="+id',sid)
    async def juega(uid,nombre,sc):
      cx,px=await phone(b,uid,errs);await px.goto('about:blank');await px.goto(url);await px.wait_for_timeout(1200)
      tab=await px.evaluate('()=>[document.getElementById("retoT").innerText,document.getElementById("retoTab").hidden?"":document.getElementById("retoTab").innerText.replace(/\\n/g," ")]')
      await px.fill('#retoName',nombre);await px.click('#retoGo');await px.wait_for_timeout(700)
      gh=await px.evaluate('()=>SS.ghosts.map(g=>g.n)')
      if len(gh)>1: await px.wait_for_timeout(3500);await px.screenshot(path=SP+'m_fantasmas.png')
      await px.evaluate('(sc)=>{SS.notes.forEach(n=>{n.st=1;n.off=0.02});SS.cnt.p=SS.notes.length;SS.score=sc;SS.finish(true)}',sc);await px.wait_for_timeout(2000)
      fin=await px.evaluate('()=>document.getElementById("resVs").innerText.replace(/\\n/g," ")')
      dare=await px.inner_text('#dare');await cx.close();return tab,gh,fin,dare
    c1=await juega('anonC','Sofi',3000);c2=await juega('anonD','Deisy',7000)
    await a.evaluate('async()=>{SS.toMenu();await SS.checkResults(true)}');await a.wait_for_timeout(500)
    av=await a.evaluate('()=>[SS.save.newRes,document.getElementById("histB").innerText.replace(/\\n/g," ")]')
    await a.evaluate('async()=>{await SS.openHist("duels")}');await a.wait_for_timeout(400)
    du=await a.evaluate('()=>[...document.querySelectorAll("#histList .part")].map(e=>e.innerText.replace(/\\n/g," "))[0]')
    await a.evaluate('(id)=>SS.openSala(id)',sid);await a.wait_for_timeout(800)
    sa=await a.evaluate('()=>[document.getElementById("saSub").innerText,document.getElementById("saList").innerText.replace(/\\n/g," "),!document.getElementById("saRace").hidden]')
    await a.screenshot(path=SP+'m_sala.png')
    print('sala: enlace',url.split('#')[1],len(url),'letras · Sofi ve',c1[0],'fantasmas',c1[1],'termina',c1[2],'botón',c1[3])
    print('      Deisy ve',c2[0],'fantasmas',c2[1],'termina',c2[2])
    print('      A: aviso',av,'· duelos',du,'· sala',sa)
    print(errs);await b.close()
if __name__=="__main__": asyncio.run(main())
