import subprocess

class VagrantManager:
    def __init__(self, vagrant_dir="."):
        self.vagrant_dir = vagrant_dir

    def run_command(self, command):
        try:
            subprocess.run(
                command,
                cwd=self.vagrant_dir,
                check=True,
                text=True
            )
            return "Command executed successfully."
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

    def up(self):
        return self.run_command(["vagrant", "up"])

    def halt(self):
        return self.run_command(["vagrant", "halt"])

    def reload(self):
        return self.run_command(["vagrant", "reload"])

    def destroy(self, force=False):
        command = ["vagrant", "destroy"]
        if force:
            command.append("-f")
        return self.run_command(command)

    def status(self):
        return self.run_command(["vagrant", "status"])

    def ssh(self, command=None):
        if command:
            return self.run_command(["vagrant", "ssh", "-c", command])
        else:
            return self.run_command(["vagrant", "ssh"])
          
    