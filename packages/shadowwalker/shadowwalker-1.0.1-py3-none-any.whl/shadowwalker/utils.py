from omnitools import IS_WIN32, def_template
from subprocess import run, PIPE
import threadwrapper
import shadowwalker
import threading
import requests
import time
import json
import os


def ping(host):
    output = run("chcp 65001 && ping -{} 1{} {}".format(
        "n" if IS_WIN32 else "c",
        " -w 500" if IS_WIN32 else " -W 1",
        host
    ), shell=True, stdout=PIPE, stderr=PIPE, close_fds=not IS_WIN32)
    if IS_WIN32:
        try:
            # print(output.stdout.decode())
            # print(output.stdout.decode().splitlines()[3].split("ms")[0].split("=")[-1])
            return float(output.stdout.decode().splitlines()[3].split("ms")[0].split("=")[-1])
        except:
            return 999
    else:
        try:
            return float(output.stdout.decode().splitlines()[-1].split(" ")[-2].split("/")[0])
        except:
            return 999


def benchmark(_10MB_file=None):
    _sw = shadowwalker.ShadowWalker()
    proxies = _sw.proxies
    sws = [None]*len(proxies)
    sws[0] = _sw
    bench = {}
    if os.path.isfile("bench.json"):
        bench = json.loads(open("bench.json", "rb").read().decode())
    tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**3))
    for i, proxy in enumerate(proxies):
        def job(i, proxy):
            try:
                if not sws[i]:
                    for __ in range(10):
                        if sws[i-1]:
                            if sws[i-1].clash_port > 65000:
                                sws[i-1].clash_port = 7890
                            sws[i] = sws[i-1].clone()
                        else:
                            time.sleep(2)
                sw = sws[i]
                host = "{}:{}".format(proxy["server"], proxy["port"])
                if host in bench:
                    return
                p = threading.Thread(target=lambda: sw.start(proxy=proxy))
                p.daemon = True
                p.start()
                start = time.time()
                print(i + 1, len(sws))
                state = 0
                max_time = 10

                def job2():
                    nonlocal state
                    link = _10MB_file
                    r = requests.get(link, proxies={"all": sw.proxy}, timeout=max_time)
                    if len(r.content) == 10 * 1024 * 1024:
                        state = 1

                time.sleep(2)
                p2 = threading.Thread(target=job2)
                p2.daemon = True
                p2.start()
                d = 10
                for j in range(0, max_time*d):
                    time.sleep(1/d)
                    if state:
                        break
                bench[host] = [state, time.time() - start]
                print(i + 1, len(sws), *bench[host])
                open("bench.json", "wb").write(json.dumps(dict(sorted(bench.items(), key=lambda x: x[1][1]))).encode())
                sw.stop()
            except:
                import traceback
                traceback.print_exc()
        tw.add(job=def_template(job, i, proxy))
    tw.wait()


def benchmark_mega():
    _sw = shadowwalker.ShadowWalker()
    proxies = _sw.proxies
    sws = [None]*len(proxies)
    sws[0] = _sw
    bench = {}
    if os.path.isfile("bench_mega.json"):
        bench = json.loads(open("bench_mega.json", "rb").read().decode())
    tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**3))
    for i, proxy in enumerate(proxies):
        def job(i, proxy):
            try:
                if not sws[i]:
                    for __ in range(10):
                        if sws[i-1]:
                            if sws[i-1].clash_port > 65000:
                                sws[i-1].clash_port = 7890
                            sws[i] = sws[i-1].clone()
                        else:
                            time.sleep(2)
                sw = sws[i]
                host = "{}:{}".format(proxy["server"], proxy["port"])
                if host in bench:
                    return
                p = threading.Thread(target=lambda: sw.start(proxy=proxy))
                p.daemon = True
                p.start()
                start = time.time()
                print(i + 1, len(sws))
                state = 0
                max_time = 20

                def job2():
                    nonlocal state
                    import megadownloader
                    md = megadownloader.MegaDownloader(proxies=[sw.proxy], db_i=i)
                    link = md.client.get_file_link("https://mega.nz/file/L8diRATC#Juh2xd4AduwyPBv9TW5UTLtrimRisNHEa0xYkWszfuQ")
                    md.stop()
                    os.remove("db_{}.db".format(i))
                    r = requests.get(link, proxies={"all": sw.proxy}, timeout=max_time)
                    if len(r.content) == 10 * 1024 * 1024:
                        state = 1

                time.sleep(2)
                p2 = threading.Thread(target=job2)
                p2.daemon = True
                p2.start()
                d = 10
                for j in range(0, max_time*d):
                    time.sleep(1/d)
                    if state:
                        break
                bench[host] = [state, time.time() - start]
                print(i + 1, len(sws), *bench[host])
                open("bench_mega.json", "wb").write(json.dumps(dict(sorted(bench.items(), key=lambda x: x[1][1]))).encode())
                sw.stop()
            except:
                import traceback
                traceback.print_exc()
        tw.add(job=def_template(job, i, proxy))
    tw.wait()


def benchmark_pixeldrain():
    _sw = shadowwalker.ShadowWalker()
    proxies = _sw.proxies
    sws = [None]*len(proxies)
    sws[0] = _sw
    bench = {}
    if os.path.isfile("bench_pixeldrain.json"):
        bench = json.loads(open("bench_pixeldrain.json", "rb").read().decode())
    tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**3))
    for i, proxy in enumerate(proxies):
        def job(i, proxy):
            try:
                if not sws[i]:
                    for __ in range(10):
                        if sws[i-1]:
                            if sws[i-1].clash_port > 65000:
                                sws[i-1].clash_port = 7890
                            sws[i] = sws[i-1].clone()
                        else:
                            time.sleep(2)
                sw = sws[i]
                host = "{}:{}".format(proxy["server"], proxy["port"])
                if host in bench:
                    return
                p = threading.Thread(target=lambda: sw.start(proxy=proxy))
                p.daemon = True
                p.start()
                start = time.time()
                print(i + 1, len(sws))
                state = 0
                max_time = 20

                def job2():
                    nonlocal state
                    import pixeldraindownloader
                    pd = pixeldraindownloader.PixeldrainDownloader(proxies=[sw.proxy], db_i=i)
                    pd.client.view_file("https://pixeldrain.com/u/2Z49VFxt", {"all": sw.proxy})
                    link = pd.client.get_download_link("https://pixeldrain.com/u/2Z49VFxt")
                    pd.stop()
                    os.remove("db_{}.db".format(i))
                    r = pd.client.s.get(link, proxies={"all": sw.proxy}, timeout=max_time)
                    if len(r.content) == 10 * 1024 * 1024:
                        state = 1

                time.sleep(2)
                p2 = threading.Thread(target=job2)
                p2.daemon = True
                p2.start()
                d = 10
                for j in range(0, max_time*d):
                    time.sleep(1/d)
                    if state:
                        break
                bench[host] = [state, time.time() - start]
                print(i + 1, len(sws), *bench[host])
                open("bench_pixeldrain.json", "wb").write(json.dumps(dict(sorted(bench.items(), key=lambda x: x[1][1]))).encode())
                sw.stop()
            except:
                import traceback
                traceback.print_exc()
        tw.add(job=def_template(job, i, proxy))
    tw.wait()


def gse_availability():
    _sw = shadowwalker.ShadowWalker()
    proxies = _sw.proxies
    sws = [None]*len(proxies)
    sws[0] = _sw
    gse = {}
    if os.path.isfile("gse.json"):
        gse = json.loads(open("gse.json", "rb").read().decode())
    for i, proxy in enumerate(proxies):
        if not sws[i]:
            for __ in range(10):
                if sws[i-1]:
                    if sws[i-1].clash_port > 65000:
                        sws[i-1].clash_port = 7890
                    sws[i] = sws[i-1].clone()
                else:
                    time.sleep(2)
        sw = sws[i]
        host = "{}:{}".format(proxy["server"], proxy["port"])
        if host in gse:
            return
        p = threading.Thread(target=lambda: sw.start(proxy=proxy))
        p.daemon = True
        p.start()
        print(i + 1, len(proxies))
        state = 0

        def job():
            nonlocal state
            r = requests.get("https://google.com/search?q=foxe6", proxies={"all": sw.proxy}, timeout=2)
            if b"foxe6.kozow.com" in r.content:
                state = 1

        p2 = threading.Thread(target=job)
        p2.daemon = True
        p2.start()
        for j in range(0, 2*20):
            time.sleep(2/20)
            if state:
                break
        if state:
            gse.append(host)
        print(i + 1, len(proxies), state)
        open("gse.json", "wb").write(json.dumps(gse).encode())
        sw.stop()

