import json
import requests as req

from nmap_scanner import NmapScanner
from device import DeviceDecoder

NVESERVER_ADDR = "127.0.0.1:5000"

class Console:
    def __init__(self):
        pass

    def _split_cmds(self, s):
        s_stripped = s.strip()
        if s_stripped == "":
            return {"cmd": "", "args": []}

        s_split = s.split(maxsplit=1)
        if len(s_split) == 1:
            return {"cmd": s_split[0], "args": []}
        
        cmd, args = s_split[0], s_split[1]
        argv = []

        quote = False
        temp = ""
        for ch in args:
            if ch == "\"":
                if quote:
                    argv.append(temp)
                    temp = ""
                    quote = False
                else:
                    quote = True
            elif ch == " ":
                if quote:
                    temp += ch
                else:
                    argv.append(temp)
                    temp = ""
            else:
                temp += ch
        if quote:
            raise ValueError("Quote not closed from \"%s" % temp)
        else:
            if temp != "":
                argv.append(temp)
        
        return {"cmd": cmd, "args": argv}

    def run(self):
        while True:
            cmd, argv = [x for x in self._split_cmds(input("NVE> ")).values()]
            if cmd == "exit":
                self.shutdown()
                return
            elif cmd == "device":
                self.get_devices(argv)
            elif cmd == "vuln":
                self.get_vulns(argv[0])
            else:
                print("Invalid Command")

    def shutdown(self):
        resp = req.get(NVESERVER_ADDR + "/shutdown")

    def get_devices(self, argv):
        if argv[0] == "all":
            return self._get_all_devices()
        else:
            return self._get_device(argv[0])
    
    def _get_all_devices(self):
        resp = req.get(NVESERVER_ADDR + "/device/all")
        print("length: ", len(resp.json()))
        return resp.json(cls = DeviceDecoder)

    def _get_device(self, ip):
        param = {"discovery_ip": ip}
        resp = req.get(NVESERVER_ADDR + "/device", params=param)
        print("resp: ", resp.status_code)
        return resp.json(cls = DeviceDecoder)

    def get_vulns(self, ip):
        param = {"discovery_ip": ip}
        resp = req.get(NVESERVER_ADDR + "/vuln", params=param)
        print("length: ", len(resp.json()))
        return resp.json()

if __name__ == "__main__":
    c = Console()
    c.run()