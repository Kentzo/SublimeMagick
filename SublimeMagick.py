import sublime
import sublime_plugin
from subprocess import Popen, PIPE


class SublimeMagick(sublime_plugin.EventListener):
    settings = sublime.load_settings(__name__ + '.sublime-settings')

    def on_activated(self, view):
        file_name = view.file_name()
        if file_name and len(file_name):
            format = self.settings.get('sublimemagick_format', "%w x %h")
            infos = self.identify(file_name, format)
            if len(infos):
                sublime.status_message(infos[0])

    def identify(self, file_name, format):
        infos = self.run_shell('identify -format "{0}\n" {1}'.format(format, file_name))
        return [info.strip() for info in infos]

    @staticmethod
    def run_shell(cmd):
        return Popen(cmd, shell=True, stdout=PIPE).stdout.read().splitlines()
