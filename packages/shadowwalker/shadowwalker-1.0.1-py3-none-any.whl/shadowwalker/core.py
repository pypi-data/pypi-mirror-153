from omnitools import def_template, IS_WIN32, abs_dir
from subprocess import Popen, PIPE
from .utils import ping
import threadwrapper
import threading
import requests
import shutil
import random
import yaml
import stat
import time
import json
import os


pkg_data_dir = os.path.join(abs_dir(__file__), "pkg_data")
# content has to be clash proxies yaml format
SOURCE = "https://proxies.bihai.cf/clash/proxies?type=ss"


class ShadowWalker:
    clash = None
    clash_port = 7890
    terminate = False
    blacklist = [
        # "38.114.114.",
    ]
    multiple = False

    @property
    def proxy(self):
        return "127.0.0.1:{}".format(self.clash_port)

    def __init__(
            self,
            clash_bin=os.path.join(pkg_data_dir, "clash.{}".format("exe" if IS_WIN32 else "bin")),
            exclude_country=["CN"],
            bench_file=os.path.join(pkg_data_dir, "bench.json"),
            gse_file=os.path.join(pkg_data_dir, "gse.json"),
            proxies=None
    ):
        self.clash_bin = clash_bin
        if not IS_WIN32:
            t = os.stat(self.clash_bin)
            os.chmod(self.clash_bin, t.st_mode | stat.S_IEXEC)
        self.exclude_country = exclude_country
        self.bench_file = bench_file
        self.gse_file = gse_file
        self.fast_proxy = []
        self.gse_proxy = []
        self.proxies = proxies
        if not self.proxies:
            self.update_proxies()

    def clone(self):
        self.multiple = True
        sw = ShadowWalker(
            proxies=self.proxies
        )
        sw.multiple = True
        sw.clash = None
        sw.clash_bin = self.clash_bin
        sw.exclude_country = self.exclude_country
        sw.bench_file = self.bench_file
        sw.gse_file = self.gse_file
        sw.clash_port = self.clash_port+10
        sw.fast_proxy = self.fast_proxy
        sw.gse_proxy = self.gse_proxy
        return sw

    def update_proxies(self):
        self.proxies = []
        for i in range(0, 10):
            try:
                print("\r", "fetching proxies, try {}/10".format(i+1), end="", flush=True)
                if os.path.isfile("proxies_cache.yaml") and os.path.getmtime("proxies_cache.yaml")+60*60*24 > time.time():
                    c = open("proxies_cache.yaml", "rb").read()
                else:
                    c = requests.get(SOURCE, timeout=3).content
                    open("proxies_cache.yaml", "wb").write(c)
                self.proxies = yaml.safe_load(c.decode())["proxies"]
                break
            except:
                if os.path.isfile("proxies_cache.yaml"):
                    os.remove("proxies_cache.yaml")
        if not self.proxies:
            raise Exception("empty proxies")
        print("\r", end="", flush=True)
        self.proxies = [_ for _ in self.proxies if not any(_["server"].startswith(ip) for ip in self.blacklist)]
        self.test_latency(self.exclude_country)

    def start(self, quiet: bool = False, proxy: dict = None):
        if not self.proxies and not proxy:
            raise ValueError("empty proxies")
        if not proxy:
            if len(self.fast_proxy) > 1:
                proxies = self.fast_proxy
            else:
                proxies = self.proxies
            proxy = random.SystemRandom().choice(proxies)
            proxy = random.SystemRandom().choice(proxies)
        id = "{}_{}".format(proxy["server"], proxy["port"])
        config_fp = os.path.join("config", "{}_{}".format(self.clash_port, id), "config_ss.yaml")
        os.makedirs(os.path.dirname(config_fp), exist_ok=True)
        data = ["cache.db", "Country.mmdb"]
        for _ in data:
            shutil.copyfile(os.path.join(pkg_data_dir, _), os.path.join(os.path.dirname(config_fp), _))
        open(config_fp, "wb").write(('''\
port: {}
allow-lan: true
mode: rule
proxies:
  - name: "PROXY"
    type: ss
    server: "{}"
    port: {}
    cipher: {}
    password: "{}"
rules:
  - MATCH,PROXY
'''.format(
            self.clash_port,
            proxy["server"],
            proxy["port"],
            proxy["cipher"],
            proxy["password"],
        )).encode())
        if not quiet:
            self.clash = Popen([self.clash_bin, "-f", config_fp, "-d", os.path.dirname(config_fp)], close_fds=not IS_WIN32)
        else:
            self.clash = Popen([self.clash_bin, "-f", config_fp, "-d", os.path.dirname(config_fp)], stdout=PIPE, stderr=PIPE, close_fds=not IS_WIN32)
        pid = self.clash.pid
        if self.multiple:
            print("\rstarted clash", self.clash_port, id, "pid", pid, end="")
        else:
            print("started clash", self.clash_port, id, "pid", pid)
        while not self.terminate:
            time.sleep(1)
        self.clash.terminate()
        time.sleep(1)
        shutil.rmtree(os.path.dirname(config_fp))
        self.terminate = False

    def start_fast_proxy(self, *args, **kwargs):
        return self.start(*args, **kwargs)

    def start_gse_proxy(self, quiet: bool = False):
        if not self.gse_proxy:
            raise ValueError("empty proxies")
        proxies = self.gse_proxy
        proxy = random.SystemRandom().choice(proxies)
        proxy = random.SystemRandom().choice(proxies)
        return self.start(quiet=quiet, proxy=proxy)

    def stop(self):
        if self.clash:
            if self.multiple:
                print("\rclash terminating", self.clash.pid, end="")
            else:
                print("clash terminating", self.clash.pid)
            self.terminate = True
            while self.terminate:
                time.sleep(1)
            if self.multiple:
                print("\rclash terminated", self.clash.pid, end="")
            else:
                print("clash terminated", self.clash.pid)
            self.clash = None

    def test_latency(self, exclude_country):
        print("clash testing latency, please wait")
        tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**4))
        self.proxies = [_ for _ in self.proxies if "country" in _ and _["country"][-2:] not in exclude_country]
        ping_cache = {}
        if os.path.isfile("ping_cache.json") and os.path.getmtime("ping_cache.json")+60*60*24 > time.time():
            ping_cache = json.loads(open("ping_cache.json", "rb").read().decode())
        for i, proxy in enumerate(self.proxies):
            def job(i, proxy):
                print("\r", i+1, len(self.proxies), "pinging", proxy["server"], end="", flush=True)
                if proxy["server"] in ping_cache:
                    proxy["ping"] = ping_cache[proxy["server"]]
                else:
                    pings = [999]
                    for i in range(0, 5):
                        p = ping(proxy["server"])
                        pings.append(p)
                        if p < 999:
                            break
                    proxy["ping"] = min(pings)
                    ping_cache[proxy["server"]] = proxy["ping"]
                print("\r", i+1, len(self.proxies), "pinging", proxy["server"], proxy["ping"], end="", flush=True)
            tw.add(job=def_template(job, i, proxy))
        tw.wait()
        open("ping_cache.json", "wb").write(json.dumps(ping_cache).encode())
        self.proxies = [_ for _ in self.proxies if _["ping"] <= 171]
        self.proxies = sorted(self.proxies, key=lambda x: x["ping"])
        i = 2.6-7.5
        try:
            bench_file = json.loads(open(self.bench_file, "rb").read().decode())
        except:
            bench_file = {}
        if bench_file:
            while not self.fast_proxy:
                i += 7.5
                fast_proxy = [_[0] for _ in bench_file.items() if _[1][0] and _[1][1] < i]
                self.fast_proxy = [_ for _ in self.proxies if "{}:{}".format(_["server"], _["port"]) in fast_proxy]
        else:
            self.fast_proxy = []
        try:
            gse_file = json.loads(open(self.gse_file, "rb").read().decode())
        except:
            gse_file = {}
        self.gse_proxy = [_ for _ in self.proxies if "{}:{}".format(_["server"], _["port"]) in gse_file]
        print("\r", end="", flush=True)
        # print("\r", self.proxies)




