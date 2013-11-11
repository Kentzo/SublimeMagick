import sublime, sublime_plugin
from subprocess import Popen, PIPE

class SublimeMagick(sublime_plugin.EventListener):
    settings = sublime.load_settings('SublimeMagick.sublime-settings')

    def on_activated(self, view):
        file_name = view.file_name()
        if file_name and len(file_name):
            infos = self.identify(file_name)
            if len(infos):
                sublime.status_message(infos[0])

    def identify(self, file_name):
        identify_path = self.settings.get('sublimemagick_identify_path', "env identify")
        format = self.settings.get('sublimemagick_format', "%w x %h")
        infos = self.run_shell('{0} -format "{1}\n" {2}'.format(identify_path, format, file_name))
        return [info.strip() for info in infos]

    @staticmethod
    def run_shell(cmd):
        return Popen(cmd, shell=True, stdout=PIPE).stdout.read().decode("utf-8").splitlines()