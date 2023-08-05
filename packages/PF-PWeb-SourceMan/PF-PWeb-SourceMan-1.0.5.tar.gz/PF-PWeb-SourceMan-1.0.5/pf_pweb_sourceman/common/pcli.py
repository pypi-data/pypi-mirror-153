import subprocess


class PCLI:

    def run(self, command, home, env=None):
        response = subprocess.run(command, shell=True, cwd=home, env=env)
        return response


pcli = PCLI()
