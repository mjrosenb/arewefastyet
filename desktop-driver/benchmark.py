import subprocess
import socket
import os
import time
import json

class Benchmark:
    def __init__(self, name, page):
        self.name = name
        self.page = "localhost:8000/"+page

    def run(self, engine, submit):
        for modeInfo in engine.modes:
            if os.path.exists("results"):
                os.unlink("results")

            engine.run(self.page)
            while not os.path.exists("results"):
                time.sleep(10)
            engine.kill()

            fp = open("results", "r")
            results = json.loads(fp.read())
            fp.close()

            results = self.processResults(results)
            submit.AddTests(results, self.name, modeInfo["name"])

    def processResults(self, results):
        return results

class Octane(Benchmark):
    def __init__(self):
        Benchmark.__init__(self, "octane", "desktop-driver/octane.html")

    def processResults(self, results):
        ret = []
        for key in results: 
            if key == "total":
                ret.append({'name': "__total__", 'time': results[key]})
            else:
                ret.append({'name': key, 'time': results[key]})
        return ret

class SunSpider(Benchmark):
    def __init__(self):
        Benchmark.__init__(self, "ss", "desktop-driver/ss.html")

class Kraken(Benchmark):
    def __init__(self):
        Benchmark.__init__(self, "kraken", "desktop-driver/kraken.html")

Benchmarks = [Octane(), SunSpider(), Kraken()]

# Test if server is running and start server if needed.
s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = s.connect_ex(("localhost", 8000))
s.close()
if result > 0:
    subprocess.Popen(["python", "server.py"])
