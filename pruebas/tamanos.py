import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();errs=[]
    for w,h in [(320,568),(360,640),(390,844),(768,1024),(1280,720)]:
      pg=await b.new_page(viewport={'width':w,'height':h});pg.on('pageerror',lambda e:errs.append(str(e)))
      await pg.goto('http://localhost:8766/');await pg.wait_for_timeout(300)
      for scr,act in [('menu',None),('mine','#mineB'),('comp','#newSong'),('cfg',None),('cal','#calB')]:
        if act: await pg.click(act);await pg.wait_for_timeout(100)
        if scr=='cfg': await pg.evaluate("()=>{document.getElementById('compBack').click();document.getElementById('mineBack').click();document.getElementById('cfgB').click()}")
        r=await pg.evaluate(f"""()=>{{const s=document.getElementById('{scr}');return [s.scrollHeight>s.clientHeight+1,document.documentElement.scrollWidth>innerWidth]}}""")
        if any(r): print(w,h,scr,'desliza/ancho',r)
      if (w,h)==(320,568): await pg.screenshot(path='tamanos.png')
    print('ok',errs);await b.close()
asyncio.run(main())
