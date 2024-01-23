from webview import Webview
if __name__=='__main__':
     

    if 1:
        html ='''<button id="increment">Tap me</button>
    <div>You tapped <span id="count">0</span> time(s).</div>
    <button id="compute">Compute</button>
    <div>Result of computation: <span id="compute-result">0</span></div>
    <script>
    const [incrementElement, countElement, computeElement, computeResultElement] =
        document.querySelectorAll("#increment, #count, #compute, #compute-result");
    document.addEventListener("DOMContentLoaded", () => {
        incrementElement.addEventListener("click", () => {
        window.increment().then(result => {
            countElement.textContent = result.count;
        });
        });
        computeElement.addEventListener("click", () => {
        computeElement.disabled = true;
        window.compute(6, 7).then(result => {
            computeResultElement.textContent = result;
            computeElement.disabled = false;
        });
        });
    });
    </script>'''
        wv=Webview()
        wv.set_title('basic')
        wv.set_size(500,500)
        count=0
        def increment(seq,req):
            global count
            count+=10
            return "{\"count\": " + str(count) + "}"
        import threading,time,json
        def compute(seq,req):
            def _(seq,req):
                print(seq,req)
                time.sleep(1)
                _js=json.loads(req)
                wv.resolve(seq,0,str(_js[0]+_js[1]))
            threading.Thread(target=_,args=(seq,req,)).start()
        wv.bind('increment',(increment))
        wv.bind('compute',(compute))
        wv.set_html(html)  
        def haha():
            print("?")
        wv.dispatch(haha)
        wv.run()