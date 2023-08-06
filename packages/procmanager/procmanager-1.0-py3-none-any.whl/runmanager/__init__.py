#!/bin/env python
import os
import sys
import time
import json
import fcntl
import subprocess

KILL_SIGNALS = (2, 15, 3, 9)
POLL_INTERVAL = 0.4


class ProcDB:
    CONF_ROOT = os.environ.get("APPS_STATE", "~/.config/runningapps")

    def __init__(self):
        DB_DIR = self.getDir()
        if not os.path.isdir(DB_DIR):
            os.mkdir(DB_DIR)

        self.dbFile = os.path.join(DB_DIR, "status.json")
        self.apps = {}

        if os.path.exists(self.dbFile):
            with open(self.dbFile) as f:
                self.apps.update(json.load(f))

    def isAlive(self, name):
        return name in self.apps and isProcAlive(self.apps[name])

    def save(self):
        with open(self.dbFile, "w") as f:
            json.dump(self.apps, f)

    @classmethod
    def getDir(kls, *suffix):
        return os.path.join(os.path.expanduser(kls.CONF_ROOT), *suffix)


def isProcAlive(pid):
    return os.path.exists("/proc/%s" % pid)


def killIfAlive(pid, sig, delay=1):
    for n in range(int(delay / POLL_INTERVAL)):
        time.sleep(POLL_INTERVAL)
        if not isProcAlive(pid):
            break
    else:
        if isProcAlive(pid):
            os.kill(pid, sig)


def writeIfAny(inp, outp):
    data = inp.readlines()
    if data:
        outp.writelines(data)


def main():
    args = list(sys.argv[1:])
    label = ""

    if "-n" in args:
        idx = args.index("-n")
        label = args[idx + 1]
        del args[idx]
        del args[idx]

    if not args:
        print("""%s (list|watch|start|stop|clean) [-n name] [...]""" % sys.argv[0])
        sys.exit(0)

    action = args[0]
    db = ProcDB()

    if action[0] == "l":  # list / ls
        for app in db.apps:
            print(" + %s (%s)" % (app, db.apps[app] if db.isAlive(app) else "dead"))
    elif action[0] == "w":  # watch
        app = label or args[1]
        std_log = open(db.getDir(app + ".stdout"))
        err_log = open(db.getDir(app + ".stderr"))
        while True:
            writeIfAny(std_log, sys.stdout)
            writeIfAny(err_log, sys.stderr)
            time.sleep(POLL_INTERVAL)
    elif action[0] == "c":  # clean / clear
        for app in list(db.apps):
            if not db.isAlive(app):
                print(" - %s" % app)
                del db.apps[app]
            else:
                print(" + %s" % app)
        db.save()
    elif action == "start":
        if len(args[1]) == 0:
            print("No program specified.")
        else:
            app = label or args[1]
            if db.isAlive(app):
                print("Already running.")
            else:
                if app in db.apps:
                    print("Restarting...")
                if os.fork() == 0:
                    os.setsid()
                    proc = subprocess.Popen(
                        args[1:],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    db.apps[app] = proc.pid
                    db.save()
                    for fd in (proc.stdout.fileno(), proc.stderr.fileno()):
                        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                    out_log = open(db.getDir(app + ".stdout"), "ab+")
                    err_log = open(db.getDir(app + ".stderr"), "ab+")
                    while True:
                        writeIfAny(proc.stdout, out_log)
                        writeIfAny(proc.stderr, err_log)

                        if proc.poll() != None:
                            break
                        else:
                            time.sleep(POLL_INTERVAL)
                    out_log.write(b"Exit code: %d\n" % proc.returncode)
                    out_log.close()
                    err_log.close()
    elif action == "stop":
        app = label or args[1]
        if app not in db.apps:
            print("Not running.")
        else:
            try:
                pid = db.apps[app]
                for n in KILL_SIGNALS:
                    killIfAlive(pid, n, 2)
            except ProcessLookupError:
                print("Process already dead.")
            del db.apps[app]
            db.save()
            for filename in (db.getDir(app + ".stdout"), db.getDir(app + ".stderr")):
                shortname = "%s " % filename.rsplit(os.path.sep, 1)[-1].strip()
                print(shortname.upper().center(80, "#"))
                print(open(filename).read())
                os.unlink(filename)
    else:
        print("Unknown action:", action)


if __name__ == "__main__":
    main()
