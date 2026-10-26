import asyncio
from playwright.async_api import async_playwright
import os; SP=os.path.dirname(os.path.abspath(__file__))+'/'
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    pg=await b.new_page(viewport={'width':380,'height':780});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type in('error','warning') and errs.append(m.text))
    await pg.goto('http://localhost:8766/#prueba');await pg.wait_for_timeout(500)
    await pg.screenshot(path=SP+'m_menu.png')
    await pg.click('#cfgB');await pg.wait_for_timeout(200);await pg.screenshot(path=SP+'m_cfg.png')
    await pg.wait_for_timeout(1300)
    print('pantalla',await pg.evaluate('()=>[SS.HZ.hz,document.getElementById("hzLbl").innerText]'))
    await pg.click('#smoothSeg button[data-s="0"]');print('60 cuadros',await pg.evaluate('()=>[SS.save.set.smooth,document.getElementById("hzLbl").innerText]'))
    await pg.click('#smoothSeg button[data-s="1"]')
    await pg.click('#fpsT');await pg.wait_for_timeout(1200)
    f1=await pg.evaluate('()=>[SS.save.set.fps,!document.getElementById("fpsBox").hidden,document.getElementById("fpsBox").textContent]')
    await pg.screenshot(path=SP+'m_cfg.png')
    await pg.click('#fpsT');print('contador',f1,'apagado',await pg.evaluate('()=>document.getElementById("fpsBox").hidden'))
    # reloj suave: audio que avanza a saltos (como en Android) y pantalla de 120 Hz
    print('reloj suave',await pg.evaluate('''()=>{const out=[];
      for(const [step,late] of [[.02,0],[.04,0],[.1,0],[.04,.2]]){
        const sm=SS.makeSmooth(),fr=1/120;let quietRaw=0,quietSm=0,worst=0,prevR=null,prevS=null,errEnd=0;
        for(let i=0;i<600;i++){const p=10+i*fr,real=Math.max(0,p-10-late),raw=Math.floor(real/step)*step,v=sm(raw,p,true);
          if(i>120&&prevR!=null){if(raw===prevR)quietRaw++;if(v-prevS<fr*.25)quietSm++;worst=Math.max(worst,Math.abs((v-prevS)-fr))}
          prevR=raw;prevS=v;errEnd=v-real}
        out.push(`saltos ${step*1000} ms${late?' (arranque tardío)':''}: cuadros quietos ${quietRaw} -> ${quietSm}, peor desvío ${(worst*1000).toFixed(1)} ms, error final ${(errEnd*1000).toFixed(1)} ms`)}
      return out}'''))
    # calibrador: toques simulados 130 ms después de cada golpe -> debería dar 130
    await pg.click('#calB');await pg.click('#calPad');await pg.wait_for_timeout(100)
    await pg.evaluate('()=>{window.cb=setInterval(()=>{const c=SS.cal;if(!c)return;const t=SS.now();for(let i=0;i<c.clicks.length;i++){if(!c.hit[i]&&!c["s"+i]&&t>=c.clicks[i]+0.13){c["s"+i]=1;SS.calTap();break}}},2)}')
    await pg.wait_for_timeout(11500);await pg.screenshot(path=SP+'m_cal.png')
    print('calibrador',await pg.evaluate('()=>[SS.calVal,document.getElementById("calRes").innerText]'))
    await pg.evaluate('()=>clearInterval(cb)');await pg.click('#calSave')
    print('ajuste guardado',await pg.evaluate('()=>SS.save.set.lat'))
    await pg.evaluate('()=>{SS.save.set.lat=0}')
    await pg.click('#cfgOk')
    await pg.click('#mineB');await pg.wait_for_timeout(200)
    # audio
    await pg.set_input_files('#fileIn',SP+'test.wav');await pg.wait_for_timeout(2500)
    r=await pg.evaluate('()=>{const a=SS.lastFile.an;return [a.bpm,a.onsets.map(o=>o.t.toFixed(2)).join(","),SS.state,SS.notes.length]}')
    truth=[float(x) for x in open(SP+'truth.txt').read().split(',')]
    det=[float(x) for x in r[1].split(',')]
    hit=sum(1 for t in truth if any(abs(t-d)<0.035 for d in det)); extra=sum(1 for d in det if not any(abs(t-d)<0.035 for t in truth))
    print('audio bpm',r[0],'real hits',hit,'/',len(truth),'extra',extra,'state',r[2],'notes',r[3])
    await pg.evaluate('''()=>{window.bot=setInterval(()=>{const t=SS.now();for(const n of SS.notes){if(!n.st&&!n.sk&&Math.abs(n.t-t)<0.02){n.sk=1;SS.tap();break}}},5)}''')
    await pg.wait_for_timeout(6000);await pg.screenshot(path=SP+'m_audio.png')
    await pg.evaluate('()=>clearInterval(bot)')
    await pg.click('#pauseB');await pg.click('#quit');await pg.wait_for_timeout(200)
    await pg.click('#mineB');await pg.set_input_files('#fileIn',SP+'test.mid');await pg.wait_for_timeout(800)
    print('midi',await pg.evaluate('()=>[SS.lastFile.data.bpm,SS.lastFile.data.ev.length,SS.lastFile.data.cand.length,SS.lastFile.data.len.toFixed(1),SS.state,SS.notes.length,SS.notes.slice(0,4).map(n=>(n.t-SS.notes[0].t).toFixed(2)).join()]'))
    await pg.wait_for_timeout(4000);await pg.screenshot(path=SP+'m_midi.png')
    await pg.click('#pauseB');await pg.click('#quit');await pg.click('#mineB')
    await pg.click('#newSong');await pg.click('#compEx');await pg.wait_for_timeout(200);await pg.screenshot(path=SP+'m_comp.png')
    await pg.click('#compPlay');await pg.wait_for_timeout(1500);await pg.click('#compPlay')
    await pg.click('#compGo');await pg.wait_for_timeout(500)
    print('comp',await pg.evaluate('()=>[SS.state,SS.notes.length,SS.save.songs.length]'))
    await pg.click('#pauseB');await pg.click('#quit');await pg.click('#mineB');await pg.wait_for_timeout(200);await pg.screenshot(path=SP+'m_mine.png')
    await pg.set_viewport_size({'width':320,'height':568});await pg.click('#mineBack');await pg.wait_for_timeout(200);await pg.screenshot(path=SP+'s_menu.png')
    await pg.click('#mineB');await pg.click('#newSong');await pg.wait_for_timeout(200);await pg.screenshot(path=SP+'s_comp.png')
    # pausa y cuenta 3-2-1 al ritmo
    await pg.set_viewport_size({'width':380,'height':780});await pg.click('#compBack');await pg.click('#mineBack')
    await pg.click('.st[data-i="0"]')
    await pg.evaluate('()=>{window.bot=setInterval(()=>{const t=SS.now();for(const n of SS.notes){if(!n.st&&!n.sk&&Math.abs(n.t-t)<0.02){n.sk=1;SS.tap();break}}},4)}')
    await pg.wait_for_timeout(7000);m0=await pg.evaluate('()=>SS.cnt.m')
    await pg.click('#pauseB');await pg.wait_for_timeout(1200)
    await pg.screenshot(path=SP+'m_pausa.png')
    a=await pg.evaluate('()=>[SS.paused,SS.AC.state,SS.now()]')
    await pg.click('#resume');await pg.wait_for_timeout(500)
    c=await pg.evaluate('()=>{const c=SS.counting;return c?[(c.end-SS.now())/c.b,SS.paused]:null}')
    await pg.screenshot(path=SP+'m_cuenta.png')
    await pg.wait_for_timeout(7000)
    print('pausa',a[:2],'cuenta (golpes que faltan)',c and round(c[0],2),'fallos antes/después',m0,await pg.evaluate('()=>SS.cnt.m'),'aciertos',await pg.evaluate('()=>SS.cnt.p+SS.cnt.b'))
    await pg.evaluate('()=>clearInterval(bot)');await pg.click('#pauseB');await pg.click('#quit')
    # pausa con música de archivo: sigue desde donde iba
    await pg.click('#mineB');await pg.set_input_files('#fileIn',SP+'test.wav');await pg.wait_for_timeout(5000)
    await pg.click('#pauseB');await pg.wait_for_timeout(300);await pg.click('#resume');await pg.wait_for_timeout(300)
    print('archivo',await pg.evaluate('()=>{const e=SS.ev.slice(SS.evI).find(x=>x.k==="buf");return e?["sigue desde",e.off.toFixed(2)]:"sin buf (ya programado)"}'))
    await pg.click('#pauseB');await pg.click('#quit')
    # Dina Run: personajes comprados allá y frutillas que pasan para allá
    pg2=await b.new_page(viewport={'width':360,'height':640});pg2.on('pageerror',lambda e:errs.append(str(e)))
    await pg2.add_init_script("if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('sofiRunner.v1',JSON.stringify({total:1000,spent:400,owned:['sofi','deisy'],char:'deisy',outfit:'default',best:777}))}")
    await pg2.goto('http://localhost:8766/#prueba');await pg2.wait_for_timeout(500)
    r=[await pg2.evaluate('()=>SS.charId()'),await pg2.inner_text('#wallet')]
    await pg2.screenshot(path=SP+'r_menu.png')
    await pg2.click('#chNext')
    r.append(await pg2.evaluate('()=>[SS.charId(),document.getElementById("heroImg").classList.contains("lock"),document.getElementById("chName").innerText]'))
    await pg2.screenshot(path=SP+'r_lock.png')
    await pg2.click('#chPrev')
    await pg2.click('.st[data-i="0"]')
    await pg2.evaluate('()=>{window.bot=setInterval(()=>{const t=SS.now();for(const n of SS.notes){if(!n.st&&!n.sk&&Math.abs(n.t-t)<0.02){n.sk=1;SS.tap();break}}},5)}')
    await pg2.wait_for_timeout(20000);await pg2.screenshot(path=SP+'r_juego.png')
    await pg2.evaluate('()=>{clearInterval(bot);SS.finish(true)}');await pg2.wait_for_timeout(900)
    d=await pg2.evaluate('()=>[JSON.parse(localStorage.getItem("sofiRunner.v1")),document.getElementById("resRun").innerText,document.getElementById("resImg").src.split("/").pop()]')
    await pg2.screenshot(path=SP+'r_fin.png')
    print('dina run',r,'total',d[0]['total'],'best intacto',d[0]['best']==777,d[1],d[2])
    print(errs);await b.close()
asyncio.run(main())
